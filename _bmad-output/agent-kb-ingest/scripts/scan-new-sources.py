#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Scan for new source files not yet in the source index.

Checks raw/ for any files that aren't tracked in _source-index.md.
Returns a JSON list of new files with basic metadata (path, extension, size).

Usage:
    python3 scan-new-sources.py <vault-path> [--json]
"""

import argparse
import json
import re
from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".txt", ".html", ".pdf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def get_indexed_paths(vault_path: Path) -> set[str]:
    """Parse source index for already-tracked paths."""
    index_path = vault_path / "raw" / "_source-index.md"
    indexed = set()
    if not index_path.exists():
        return indexed
    for line in index_path.read_text(encoding="utf-8").split("\n"):
        match = re.search(r"`(raw/[^`]+)`", line)
        if match:
            indexed.add(match.group(1))
    return indexed


def scan_raw_directory(vault_path: Path) -> list[dict]:
    """Find all processable files in raw/."""
    raw_dir = vault_path / "raw"
    if not raw_dir.exists():
        return []

    files = []
    for f in sorted(raw_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.name.startswith("_") or f.name.startswith("."):
            continue
        ext = f.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS and ext not in IMAGE_EXTENSIONS:
            continue

        rel = str(f.relative_to(vault_path))
        file_type = "image" if ext in IMAGE_EXTENSIONS else "document"
        files.append({
            "path": rel,
            "name": f.name,
            "extension": ext,
            "size_bytes": f.stat().st_size,
            "type": file_type,
            "has_frontmatter": _has_frontmatter(f) if ext == ".md" else False,
        })
    return files


def _has_frontmatter(path: Path) -> bool:
    """Check if a markdown file already has YAML frontmatter."""
    try:
        content = path.read_text(encoding="utf-8")
        return content.startswith("---\n")
    except (UnicodeDecodeError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Scan for new source files not yet in the source index"
    )
    parser.add_argument("vault_path", help="Path to the knowledge base vault")
    parser.add_argument("--json", action="store_true", help="Output structured JSON")
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(json.dumps({"error": f"Vault not found: {vault_path}"}))
        raise SystemExit(1)

    indexed = get_indexed_paths(vault_path)
    all_files = scan_raw_directory(vault_path)

    new_files = [f for f in all_files if f["path"] not in indexed]
    already_indexed = [f for f in all_files if f["path"] in indexed]

    # Separate new files by whether they have frontmatter
    needs_ingest = [f for f in new_files if not f["has_frontmatter"]]
    has_frontmatter = [f for f in new_files if f["has_frontmatter"]]

    result = {
        "vault": str(vault_path),
        "total_files_in_raw": len(all_files),
        "already_indexed": len(already_indexed),
        "new_files": len(new_files),
        "needs_ingest": len(needs_ingest),
        "has_frontmatter_but_not_indexed": len(has_frontmatter),
        "files": new_files,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
