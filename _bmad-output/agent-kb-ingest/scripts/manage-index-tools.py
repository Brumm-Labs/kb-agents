#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Deterministic index management tools for the KB Ingest Agent.

Handles operations that don't require LLM judgment: rebuild index from
frontmatter, find orphaned files, and compute statistics.

Usage:
    python3 manage-index-tools.py <vault-path> <command> [--json]

Commands:
    rebuild   — Rebuild source index from raw/ frontmatter
    orphans   — Find files in raw/ not in index, or index entries without files
    stats     — Show counts by type, tag frequency, status distribution
"""

import argparse
import json
import re
from pathlib import Path


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    meta = {}
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return meta

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return meta

    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            value = value.strip().strip("'\"")
            # Handle YAML lists
            if value.startswith("[") and value.endswith("]"):
                items = [i.strip().strip("'\"") for i in value[1:-1].split(",")]
                meta[key.strip()] = [i for i in items if i]
            elif value:
                meta[key.strip()] = value
    return meta


def find_raw_files(vault_path: Path) -> list[Path]:
    """Find all markdown files in raw/ subdirectories."""
    raw_dir = vault_path / "raw"
    if not raw_dir.exists():
        return []
    files = []
    for md_file in sorted(raw_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue
        files.append(md_file)
    return files


def cmd_rebuild(vault_path: Path) -> dict:
    """Rebuild source index from frontmatter."""
    files = find_raw_files(vault_path)
    entries = []
    errors = []

    for f in files:
        meta = parse_frontmatter(f)
        rel_path = f.relative_to(vault_path)
        if not meta.get("title"):
            errors.append({"file": str(rel_path), "issue": "missing title in frontmatter"})
            continue
        entries.append({
            "title": meta.get("title", f.stem),
            "type": meta.get("source_type", "unknown"),
            "tags": meta.get("tags", []),
            "status": meta.get("status", "raw"),
            "date_ingested": meta.get("date_ingested", "unknown"),
            "path": str(rel_path),
        })

    # Generate index content
    lines = [
        "# Source Index",
        "",
        f"_Auto-generated. {len(entries)} sources indexed._",
        "",
        "| Title | Type | Tags | Status | Date Ingested | Path |",
        "|-------|------|------|--------|---------------|------|",
    ]
    for e in entries:
        tags = ", ".join(e["tags"]) if isinstance(e["tags"], list) else e["tags"]
        lines.append(f"| {e['title']} | {e['type']} | {tags} | {e['status']} | {e['date_ingested']} | `{e['path']}` |")

    index_path = vault_path / "raw" / "_source-index.md"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "command": "rebuild",
        "entries": len(entries),
        "errors": errors,
        "index_path": str(index_path),
    }


def cmd_orphans(vault_path: Path) -> dict:
    """Find orphaned files and missing index entries."""
    raw_files = {str(f.relative_to(vault_path)) for f in find_raw_files(vault_path)}

    # Parse existing index
    index_path = vault_path / "raw" / "_source-index.md"
    indexed_paths = set()
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8").split("\n"):
            if line.startswith("|") and "`raw/" in line:
                # Extract path from table row
                parts = [p.strip() for p in line.split("|")]
                for part in parts:
                    if part.startswith("`raw/") and part.endswith("`"):
                        indexed_paths.add(part.strip("`"))

    not_in_index = sorted(raw_files - indexed_paths)
    missing_files = sorted(indexed_paths - raw_files)

    return {
        "command": "orphans",
        "files_not_in_index": not_in_index,
        "index_entries_without_files": missing_files,
        "total_raw_files": len(raw_files),
        "total_index_entries": len(indexed_paths),
    }


def cmd_stats(vault_path: Path) -> dict:
    """Compute statistics from frontmatter."""
    files = find_raw_files(vault_path)
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    tag_freq: dict[str, int] = {}

    for f in files:
        meta = parse_frontmatter(f)
        stype = meta.get("source_type", "unknown")
        by_type[stype] = by_type.get(stype, 0) + 1
        status = meta.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        tags = meta.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                tag_freq[tag] = tag_freq.get(tag, 0) + 1

    # Sort tags by frequency
    top_tags = sorted(tag_freq.items(), key=lambda x: -x[1])[:20]

    return {
        "command": "stats",
        "total_sources": len(files),
        "by_type": dict(sorted(by_type.items())),
        "by_status": dict(sorted(by_status.items())),
        "top_tags": [{"tag": t, "count": c} for t, c in top_tags],
        "unique_tags": len(tag_freq),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic index management tools for KB Ingest Agent"
    )
    parser.add_argument("vault_path", help="Path to the knowledge base vault")
    parser.add_argument("command", choices=["rebuild", "orphans", "stats"],
                        help="Operation to perform")
    parser.add_argument("--json", action="store_true",
                        help="Output structured JSON (default: human-readable)")
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(json.dumps({"error": f"Vault not found: {vault_path}"}))
        raise SystemExit(1)

    commands = {
        "rebuild": cmd_rebuild,
        "orphans": cmd_orphans,
        "stats": cmd_stats,
    }

    result = commands[args.command](vault_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
