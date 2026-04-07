#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Deterministic wiki tools for the KB Compiler Agent.

Handles operations that don't require LLM judgment: check wiki links,
list uncompiled sources, and extract concept inventory.

Usage:
    python3 wiki-tools.py <vault-path> <command> [--json]

Commands:
    check-links   — Find broken [[wiki-links]] and orphaned files
    uncompiled    — List sources not yet compiled (status != compiled)
    inventory     — Extract concept inventory from frontmatter
"""

import argparse
import json
import re
from pathlib import Path


def find_wiki_links(content: str) -> list[str]:
    """Extract all [[wiki-links]] from markdown content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


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
            if value.startswith("[") and value.endswith("]"):
                items = [i.strip().strip("'\"") for i in value[1:-1].split(",")]
                meta[key.strip()] = [i for i in items if i]
            elif value:
                meta[key.strip()] = value
    return meta


def cmd_check_links(vault_path: Path) -> dict:
    """Find broken wiki-links and orphaned files."""
    wiki_dir = vault_path / "wiki"
    if not wiki_dir.exists():
        return {"command": "check-links", "error": "wiki/ directory not found"}

    # Collect all wiki files
    all_files: set[str] = set()
    for md in wiki_dir.rglob("*.md"):
        rel = md.relative_to(vault_path)
        all_files.add(str(rel))
        # Also add without extension for [[link]] matching
        all_files.add(str(rel.with_suffix("")))

    # Also include raw/ files for cross-references
    raw_dir = vault_path / "raw"
    if raw_dir.exists():
        for md in raw_dir.rglob("*.md"):
            rel = md.relative_to(vault_path)
            all_files.add(str(rel))
            all_files.add(str(rel.with_suffix("")))

    broken_links = []
    link_counts: dict[str, int] = {}

    for md in wiki_dir.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="replace")
        links = find_wiki_links(content)
        source = str(md.relative_to(vault_path))

        for link in links:
            link_counts[link] = link_counts.get(link, 0) + 1
            # Check if target exists
            if link not in all_files and f"{link}.md" not in all_files:
                # Try relative to wiki/
                wiki_link = f"wiki/{link}"
                if wiki_link not in all_files and f"{wiki_link}.md" not in all_files:
                    broken_links.append({"source": source, "target": link})

    # Find orphaned files (no incoming links)
    linked_targets = set()
    for md in wiki_dir.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="replace")
        for link in find_wiki_links(content):
            linked_targets.add(link)
            linked_targets.add(f"{link}.md")

    orphaned = []
    for md in wiki_dir.rglob("*.md"):
        rel = str(md.relative_to(vault_path))
        rel_no_ext = str(md.relative_to(vault_path).with_suffix(""))
        name = md.stem
        if md.name.startswith("_"):
            continue
        if rel not in linked_targets and rel_no_ext not in linked_targets and name not in linked_targets:
            orphaned.append(rel)

    return {
        "command": "check-links",
        "total_wiki_files": len([f for f in all_files if f.startswith("wiki/") and f.endswith(".md")]),
        "broken_links": broken_links,
        "orphaned_files": sorted(orphaned),
        "total_links": sum(link_counts.values()),
    }


def cmd_uncompiled(vault_path: Path) -> dict:
    """List sources not yet compiled."""
    index_path = vault_path / "raw" / "_source-index.md"
    raw_dir = vault_path / "raw"

    uncompiled = []
    total = 0

    if raw_dir.exists():
        for md in sorted(raw_dir.rglob("*.md")):
            if md.name.startswith("_"):
                continue
            total += 1
            meta = parse_frontmatter(md)
            status = meta.get("status", "raw")
            if status != "compiled":
                uncompiled.append({
                    "path": str(md.relative_to(vault_path)),
                    "title": meta.get("title", md.stem),
                    "status": status,
                    "date_ingested": meta.get("date_ingested", "unknown"),
                })

    return {
        "command": "uncompiled",
        "total_sources": total,
        "uncompiled_count": len(uncompiled),
        "sources": uncompiled,
    }


def cmd_inventory(vault_path: Path) -> dict:
    """Extract concept inventory from frontmatter."""
    concepts_dir = vault_path / "wiki" / "concepts"
    if not concepts_dir.exists():
        return {"command": "inventory", "concepts": [], "total": 0}

    concepts = []
    for md in sorted(concepts_dir.rglob("*.md")):
        meta = parse_frontmatter(md)
        sources = meta.get("sources", [])
        source_count = len(sources) if isinstance(sources, list) else 0
        concepts.append({
            "name": meta.get("title", md.stem),
            "status": meta.get("status", "unknown"),
            "sources": source_count,
            "path": str(md.relative_to(vault_path)),
            "tags": meta.get("tags", []),
        })

    return {
        "command": "inventory",
        "total": len(concepts),
        "by_status": {
            s: len([c for c in concepts if c["status"] == s])
            for s in set(c["status"] for c in concepts)
        },
        "concepts": concepts,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic wiki tools for KB Compiler Agent"
    )
    parser.add_argument("vault_path", help="Path to the knowledge base vault")
    parser.add_argument("command", choices=["check-links", "uncompiled", "inventory"],
                        help="Operation to perform")
    parser.add_argument("--json", action="store_true",
                        help="Output structured JSON")
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(json.dumps({"error": f"Vault not found: {vault_path}"}))
        raise SystemExit(1)

    commands = {
        "check-links": cmd_check_links,
        "uncompiled": cmd_uncompiled,
        "inventory": cmd_inventory,
    }

    result = commands[args.command](vault_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
