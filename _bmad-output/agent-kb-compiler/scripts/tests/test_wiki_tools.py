"""Tests for wiki-tools.py — wiki links, check-links, uncompiled, inventory."""

import sys
import tempfile
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location(
    "wiki_tools",
    Path(__file__).parent.parent / "wiki-tools.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

find_wiki_links = mod.find_wiki_links
parse_frontmatter = mod.parse_frontmatter
cmd_check_links = mod.cmd_check_links
cmd_uncompiled = mod.cmd_uncompiled
cmd_inventory = mod.cmd_inventory


def _make_vault(tmp, files=None):
    vault = Path(tmp)
    for d in ["raw/articles", "wiki/summaries", "wiki/concepts", "wiki/connections"]:
        (vault / d).mkdir(parents=True, exist_ok=True)
    if files:
        for rel_path, content in files.items():
            p = vault / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    return vault


class TestFindWikiLinks:
    def test_simple_link(self):
        assert find_wiki_links("See [[Machine Learning]]") == ["Machine Learning"]

    def test_aliased_link(self):
        assert find_wiki_links("See [[ML|Machine Learning]]") == ["ML"]

    def test_multiple_links(self):
        result = find_wiki_links("[[A]] and [[B]] relate to [[C]]")
        assert result == ["A", "B", "C"]

    def test_no_links(self):
        assert find_wiki_links("No links here") == []


class TestCmdCheckLinks:
    def test_no_wiki_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            result = cmd_check_links(vault)
            assert "error" in result

    def test_finds_broken_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/summaries/s1.md": "---\ntitle: S1\n---\nSee [[NonExistent]]",
            })
            result = cmd_check_links(vault)
            assert len(result["broken_links"]) == 1
            assert result["broken_links"][0]["target"] == "NonExistent"

    def test_valid_links_not_broken(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/ml.md": "---\ntitle: ML\n---\nMachine Learning",
                "wiki/summaries/s1.md": "---\ntitle: S1\n---\nSee [[wiki/concepts/ml]]",
            })
            result = cmd_check_links(vault)
            assert result["broken_links"] == []

    def test_finds_orphaned_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/orphan.md": "---\ntitle: Orphan\n---\nAlone",
                "wiki/concepts/linked.md": "---\ntitle: Linked\n---\nSee [[orphan]]",
            })
            result = cmd_check_links(vault)
            orphaned = result["orphaned_files"]
            # "linked.md" is orphaned (no one links TO it), "orphan.md" is linked
            assert any("linked.md" in o for o in orphaned)


class TestCmdUncompiled:
    def test_lists_uncompiled(self):
        raw_fm = "---\ntitle: Test\nstatus: raw\ndate_ingested: 2026-01-01\n---\n"
        compiled_fm = "---\ntitle: Done\nstatus: compiled\ndate_ingested: 2026-01-01\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/pending.md": raw_fm,
                "raw/articles/done.md": compiled_fm,
            })
            result = cmd_uncompiled(vault)
            assert result["total_sources"] == 2
            assert result["uncompiled_count"] == 1
            assert result["sources"][0]["title"] == "Test"

    def test_empty_raw(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            result = cmd_uncompiled(vault)
            assert result["total_sources"] == 0


class TestCmdInventory:
    def test_extracts_concepts(self):
        concept_fm = "---\ntitle: Neural Networks\nstatus: draft\nsources: [s1, s2]\ntags: [ai, dl]\n---\n"
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/neural-networks.md": concept_fm,
            })
            result = cmd_inventory(vault)
            assert result["total"] == 1
            assert result["concepts"][0]["name"] == "Neural Networks"
            assert result["concepts"][0]["sources"] == 2

    def test_no_concepts_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            result = cmd_inventory(vault)
            assert result["total"] == 0

    def test_status_grouping(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "wiki/concepts/a.md": "---\ntitle: A\nstatus: draft\nsources: []\n---\n",
                "wiki/concepts/b.md": "---\ntitle: B\nstatus: mature\nsources: []\n---\n",
                "wiki/concepts/c.md": "---\ntitle: C\nstatus: draft\nsources: []\n---\n",
            })
            result = cmd_inventory(vault)
            assert result["by_status"]["draft"] == 2
            assert result["by_status"]["mature"] == 1
