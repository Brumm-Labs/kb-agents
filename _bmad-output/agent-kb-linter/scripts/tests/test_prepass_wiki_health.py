"""Tests for prepass-wiki-health.py — broken links, orphans, frontmatter, staleness, health score."""

import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location(
    "prepass_wiki_health",
    Path(__file__).parent.parent / "prepass-wiki-health.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_frontmatter = mod.parse_frontmatter
find_wiki_links = mod.find_wiki_links
check_broken_links = mod.check_broken_links
check_orphaned_files = mod.check_orphaned_files
check_frontmatter = mod.check_frontmatter
check_source_index_sync = mod.check_source_index_sync
check_staleness = mod.check_staleness
count_files = mod.count_files


def _make_vault(tmp, files=None):
    vault = Path(tmp)
    for d in ["raw/articles", "wiki/summaries", "wiki/concepts", "wiki/connections"]:
        (vault / d).mkdir(parents=True, exist_ok=True)
    # Always create a source index
    (vault / "raw" / "_source-index.md").write_text("# Source Index\n")
    if files:
        for rel_path, content in files.items():
            p = vault / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    return vault


class TestCheckBrokenLinks:
    def test_no_wiki_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            assert check_broken_links(vault) == []

    def test_finds_broken_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/summaries/s1.md": "See [[DoesNotExist]]",
            })
            result = check_broken_links(vault)
            assert len(result) == 1
            assert result[0]["target"] == "DoesNotExist"
            assert result[0]["severity"] == "critical"

    def test_valid_link_by_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/ml.md": "# ML",
                "wiki/summaries/s1.md": "See [[ml]]",
            })
            assert check_broken_links(vault) == []


class TestCheckOrphanedFiles:
    def test_no_wiki(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert check_orphaned_files(Path(tmp)) == []

    def test_finds_orphan(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/alone.md": "# Alone\nNo one links here",
            })
            result = check_orphaned_files(vault)
            assert any("alone.md" in r for r in result)

    def test_linked_file_not_orphan(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/target.md": "# Target",
                "wiki/summaries/linker.md": "See [[target]]",
            })
            result = check_orphaned_files(vault)
            assert not any("target.md" in r for r in result)

    def test_skips_underscore_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/_index.md": "# Index",
            })
            result = check_orphaned_files(vault)
            assert result == []


class TestCheckFrontmatter:
    def test_complete_source_no_issues(self):
        fm = "---\ntitle: T\nsource_type: article\ntags: [a]\nstatus: raw\ndate_ingested: 2026-01-01\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"raw/articles/ok.md": fm})
            assert check_frontmatter(vault) == []

    def test_missing_source_fields(self):
        fm = "---\ntitle: T\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"raw/articles/bad.md": fm})
            issues = check_frontmatter(vault)
            assert len(issues) == 1
            assert "source_type" in issues[0]["missing_fields"]

    def test_missing_concept_fields(self):
        fm = "---\ntitle: C\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"wiki/concepts/bad.md": fm})
            issues = check_frontmatter(vault)
            assert len(issues) == 1
            assert "sources" in issues[0]["missing_fields"]

    def test_missing_summary_fields(self):
        fm = "---\ntitle: S\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"wiki/summaries/bad.md": fm})
            issues = check_frontmatter(vault)
            assert len(issues) == 1
            assert "source_ref" in issues[0]["missing_fields"]


class TestCheckSourceIndexSync:
    def test_synced(self):
        index = "| T | a | t | raw | 2026-01-01 | `raw/articles/a.md` |\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": "---\ntitle: A\n---\n",
            })
            (vault / "raw" / "_source-index.md").write_text(index)
            result = check_source_index_sync(vault)
            assert result["files_not_in_index"] == []
            assert result["index_entries_without_files"] == []

    def test_file_not_in_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/new.md": "---\ntitle: New\n---\n",
            })
            result = check_source_index_sync(vault)
            assert "raw/articles/new.md" in result["files_not_in_index"]

    def test_index_entry_without_file(self):
        index = "| Gone | a | t | raw | 2026-01-01 | `raw/articles/gone.md` |\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            (vault / "raw" / "_source-index.md").write_text(index)
            result = check_source_index_sync(vault)
            assert "raw/articles/gone.md" in result["index_entries_without_files"]


class TestCheckStaleness:
    def test_stale_content(self):
        old_date = (date.today() - timedelta(days=60)).isoformat()
        fm = f"---\ntitle: Old\ndate_updated: {old_date}\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"wiki/concepts/old.md": fm})
            result = check_staleness(vault, days=30)
            assert len(result) == 1
            assert result[0]["days_ago"] >= 60

    def test_fresh_content(self):
        today = date.today().isoformat()
        fm = f"---\ntitle: Fresh\ndate_updated: {today}\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={"wiki/concepts/fresh.md": fm})
            result = check_staleness(vault, days=30)
            assert result == []

    def test_no_date_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/nodate.md": "---\ntitle: No Date\n---\n",
            })
            result = check_staleness(vault, days=30)
            assert result == []


class TestCountFiles:
    def test_counts_all_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/a.md": "a",
                "raw/articles/b.md": "b",
                "wiki/summaries/s.md": "s",
                "wiki/concepts/c.md": "c",
                "wiki/connections/x.md": "x",
            })
            result = count_files(vault)
            assert result["by_directory"]["raw"] == 2
            assert result["by_directory"]["summaries"] == 1
            assert result["by_directory"]["concepts"] == 1
            assert result["by_directory"]["connections"] == 1

    def test_empty_vault(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            result = count_files(vault)
            assert result["by_directory"]["raw"] == 0
