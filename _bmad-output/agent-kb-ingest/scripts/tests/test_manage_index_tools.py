"""Tests for manage-index-tools.py — frontmatter parsing, rebuild, orphans, stats."""

import sys
import tempfile
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location(
    "manage_index_tools",
    Path(__file__).parent.parent / "manage-index-tools.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_frontmatter = mod.parse_frontmatter
find_raw_files = mod.find_raw_files
cmd_rebuild = mod.cmd_rebuild
cmd_orphans = mod.cmd_orphans
cmd_stats = mod.cmd_stats

SOURCE_FM = """\
---
title: "Test Article"
source_type: article
tags: [ai, ml]
status: raw
date_ingested: "2026-01-15"
---
# Content here
"""


def _make_vault(tmp, files=None, index_content=None):
    vault = Path(tmp)
    (vault / "raw" / "articles").mkdir(parents=True)
    if index_content is not None:
        (vault / "raw" / "_source-index.md").write_text(index_content)
    if files:
        for rel_path, content in files.items():
            p = vault / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    return vault


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text(SOURCE_FM)
            meta = parse_frontmatter(p)
            assert meta["title"] == "Test Article"
            assert meta["source_type"] == "article"
            assert meta["status"] == "raw"

    def test_list_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text(SOURCE_FM)
            meta = parse_frontmatter(p)
            assert isinstance(meta["tags"], list)
            assert "ai" in meta["tags"]
            assert "ml" in meta["tags"]

    def test_no_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("# Just content")
            assert parse_frontmatter(p) == {}

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("")
            assert parse_frontmatter(p) == {}


class TestFindRawFiles:
    def test_finds_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": "content",
                "raw/articles/b.md": "content",
            })
            result = find_raw_files(vault)
            assert len(result) == 2

    def test_skips_underscore_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": "content",
            })
            # _source-index.md is always created
            result = find_raw_files(vault)
            names = [f.name for f in result]
            assert "_source-index.md" not in names
            assert "a.md" in names

    def test_empty_raw(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            assert find_raw_files(vault) == []


class TestCmdRebuild:
    def test_rebuilds_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/test.md": SOURCE_FM,
            })
            result = cmd_rebuild(vault)
            assert result["entries"] == 1
            assert result["errors"] == []
            index = (vault / "raw" / "_source-index.md").read_text()
            assert "Test Article" in index
            assert "`raw/articles/test.md`" in index

    def test_skips_missing_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/no-title.md": "---\nstatus: raw\n---\ncontent",
            })
            result = cmd_rebuild(vault)
            assert result["entries"] == 0
            assert len(result["errors"]) == 1


class TestCmdOrphans:
    def test_finds_files_not_in_index(self):
        index = (
            "| Title | Type | Tags | Status | Date | Path |\n"
            "|-------|------|------|--------|------|------|\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/orphan.md": SOURCE_FM,
            }, index_content=index)
            result = cmd_orphans(vault)
            assert "raw/articles/orphan.md" in result["files_not_in_index"]

    def test_finds_missing_files(self):
        index = (
            "| Title | Type | Tags | Status | Date | Path |\n"
            "|-------|------|------|--------|------|------|\n"
            "| Gone | article | ai | raw | 2026-01-01 | `raw/articles/gone.md` |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, index_content=index)
            result = cmd_orphans(vault)
            assert "raw/articles/gone.md" in result["index_entries_without_files"]

    def test_synced_vault(self):
        index = (
            "| Title | Type | Tags | Status | Date | Path |\n"
            "|-------|------|------|--------|------|------|\n"
            "| Test | article | ai | raw | 2026-01-01 | `raw/articles/test.md` |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/test.md": SOURCE_FM,
            }, index_content=index)
            result = cmd_orphans(vault)
            assert result["files_not_in_index"] == []
            assert result["index_entries_without_files"] == []


class TestCmdStats:
    def test_counts_by_type_and_status(self):
        fm2 = "---\ntitle: Paper\nsource_type: paper\ntags: [ml]\nstatus: summarized\ndate_ingested: 2026-01-01\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": SOURCE_FM,
                "raw/papers/b.md": fm2,
            })
            result = cmd_stats(vault)
            assert result["total_sources"] == 2
            assert result["by_type"]["article"] == 1
            assert result["by_type"]["paper"] == 1
            assert result["by_status"]["raw"] == 1
            assert result["by_status"]["summarized"] == 1

    def test_tag_frequency(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": SOURCE_FM,
            })
            result = cmd_stats(vault)
            tags = {t["tag"]: t["count"] for t in result["top_tags"]}
            assert tags["ai"] == 1
            assert tags["ml"] == 1
