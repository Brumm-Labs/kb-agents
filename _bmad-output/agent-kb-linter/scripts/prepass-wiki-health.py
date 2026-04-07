#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Deterministic wiki health pre-pass for the KB Linter Agent.

Performs all structural checks that don't require LLM judgment:
broken links, orphans, frontmatter validation, file counting, staleness.

The LLM Health Check capability then interprets these results and
adds judgment-based analysis (content quality, coverage gaps).

Usage:
    python3 prepass-wiki-health.py <vault-path> [--json]
"""

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path

REQUIRED_SOURCE_FIELDS = {"title", "source_type", "tags", "status", "date_ingested"}
REQUIRED_CONCEPT_FIELDS = {"title", "status", "sources"}
REQUIRED_SUMMARY_FIELDS = {"title", "source_ref", "date_compiled"}


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


def find_wiki_links(content: str) -> list[str]:
    """Extract all [[wiki-links]] from markdown content."""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)


def check_broken_links(vault_path: Path) -> list[dict]:
    """Find broken [[wiki-links]]."""
    all_files: set[str] = set()
    for d in ["wiki", "raw"]:
        dir_path = vault_path / d
        if dir_path.exists():
            for md in dir_path.rglob("*.md"):
                rel = md.relative_to(vault_path)
                all_files.add(str(rel))
                all_files.add(str(rel.with_suffix("")))
                all_files.add(md.stem)

    broken = []
    wiki_dir = vault_path / "wiki"
    if not wiki_dir.exists():
        return broken

    for md in wiki_dir.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="replace")
        for link in find_wiki_links(content):
            if link not in all_files and f"{link}.md" not in all_files:
                wiki_link = f"wiki/{link}"
                if wiki_link not in all_files and f"{wiki_link}.md" not in all_files:
                    broken.append({
                        "source": str(md.relative_to(vault_path)),
                        "target": link,
                        "severity": "critical",
                    })
    return broken


def check_orphaned_files(vault_path: Path) -> list[str]:
    """Find wiki files with no incoming links."""
    wiki_dir = vault_path / "wiki"
    if not wiki_dir.exists():
        return []

    linked = set()
    for md in wiki_dir.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="replace")
        for link in find_wiki_links(content):
            linked.add(link)
            linked.add(f"{link}.md")

    orphaned = []
    for md in wiki_dir.rglob("*.md"):
        if md.name.startswith("_"):
            continue
        rel = str(md.relative_to(vault_path))
        name = md.stem
        if name not in linked and rel not in linked:
            orphaned.append(rel)
    return sorted(orphaned)


def check_frontmatter(vault_path: Path) -> list[dict]:
    """Check frontmatter completeness."""
    issues = []

    checks = [
        ("raw", "*.md", REQUIRED_SOURCE_FIELDS, "source"),
        ("wiki/concepts", "*.md", REQUIRED_CONCEPT_FIELDS, "concept"),
        ("wiki/summaries", "*.md", REQUIRED_SUMMARY_FIELDS, "summary"),
    ]

    for subdir, pattern, required, file_type in checks:
        dir_path = vault_path / subdir
        if not dir_path.exists():
            continue
        for md in dir_path.rglob(pattern):
            if md.name.startswith("_"):
                continue
            meta = parse_frontmatter(md)
            missing = required - set(meta.keys())
            if missing:
                issues.append({
                    "file": str(md.relative_to(vault_path)),
                    "type": file_type,
                    "missing_fields": sorted(missing),
                    "severity": "warning",
                })
    return issues


def check_source_index_sync(vault_path: Path) -> dict:
    """Check if source index matches actual files."""
    raw_dir = vault_path / "raw"
    index_path = raw_dir / "_source-index.md"

    raw_files = set()
    if raw_dir.exists():
        for md in raw_dir.rglob("*.md"):
            if not md.name.startswith("_"):
                raw_files.add(str(md.relative_to(vault_path)))

    indexed_paths = set()
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8").split("\n"):
            if "`raw/" in line:
                match = re.search(r"`(raw/[^`]+)`", line)
                if match:
                    indexed_paths.add(match.group(1))

    return {
        "files_not_in_index": sorted(raw_files - indexed_paths),
        "index_entries_without_files": sorted(indexed_paths - raw_files),
        "total_files": len(raw_files),
        "total_indexed": len(indexed_paths),
    }


def check_staleness(vault_path: Path, days: int = 30) -> list[dict]:
    """Find articles not updated recently despite newer related sources."""
    stale = []
    today = date.today()
    wiki_dir = vault_path / "wiki"
    if not wiki_dir.exists():
        return stale

    for md in wiki_dir.rglob("*.md"):
        if md.name.startswith("_"):
            continue
        meta = parse_frontmatter(md)
        date_updated = meta.get("date_updated") or meta.get("date_compiled") or meta.get("date_created")
        if date_updated:
            try:
                updated = datetime.strptime(date_updated, "%Y-%m-%d").date()
                age = (today - updated).days
                if age > days:
                    stale.append({
                        "file": str(md.relative_to(vault_path)),
                        "last_updated": date_updated,
                        "days_ago": age,
                        "severity": "info",
                    })
            except ValueError:
                pass
    return sorted(stale, key=lambda x: -x["days_ago"])


def count_files(vault_path: Path) -> dict:
    """Count files by directory and status."""
    counts = {"raw": 0, "summaries": 0, "concepts": 0, "connections": 0}
    status_counts = {"raw": 0, "summarized": 0, "compiled": 0}

    for subdir, key in [("raw", "raw"), ("wiki/summaries", "summaries"),
                        ("wiki/concepts", "concepts"), ("wiki/connections", "connections")]:
        dir_path = vault_path / subdir
        if dir_path.exists():
            for md in dir_path.rglob("*.md"):
                if not md.name.startswith("_"):
                    counts[key] += 1

    raw_dir = vault_path / "raw"
    if raw_dir.exists():
        for md in raw_dir.rglob("*.md"):
            if md.name.startswith("_"):
                continue
            meta = parse_frontmatter(md)
            status = meta.get("status", "raw")
            status_counts[status] = status_counts.get(status, 0) + 1

    return {"by_directory": counts, "by_status": status_counts}


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic wiki health pre-pass for KB Linter Agent"
    )
    parser.add_argument("vault_path", help="Path to the knowledge base vault")
    parser.add_argument("--json", action="store_true", help="Output structured JSON")
    parser.add_argument("--stale-days", type=int, default=30,
                        help="Days before content is considered stale (default: 30)")
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(json.dumps({"error": f"Vault not found: {vault_path}"}))
        raise SystemExit(1)

    broken_links = check_broken_links(vault_path)
    orphaned = check_orphaned_files(vault_path)
    frontmatter_issues = check_frontmatter(vault_path)
    index_sync = check_source_index_sync(vault_path)
    stale = check_staleness(vault_path, args.stale_days)
    file_counts = count_files(vault_path)

    critical = len(broken_links)
    warnings = len(orphaned) + len(frontmatter_issues) + len(index_sync["files_not_in_index"]) + len(index_sync["index_entries_without_files"])
    info = len(stale)

    result = {
        "vault": str(vault_path),
        "date": date.today().isoformat(),
        "summary": {
            "overall": "critical" if critical > 0 else "warning" if warnings > 0 else "healthy",
            "critical": critical,
            "warnings": warnings,
            "info": info,
        },
        "file_counts": file_counts,
        "broken_links": broken_links,
        "orphaned_files": orphaned,
        "frontmatter_issues": frontmatter_issues,
        "source_index_sync": index_sync,
        "stale_content": stale[:20],
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
