"""Tests for scan-new-sources.py — index parsing, raw scanning, frontmatter check."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# The module uses dashes in filename, import via importlib
import importlib.util

spec = importlib.util.spec_from_file_location(
    "scan_new_sources",
    Path(__file__).parent.parent / "scan-new-sources.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

get_indexed_paths = mod.get_indexed_paths
scan_raw_directory = mod.scan_raw_directory
_has_frontmatter = mod._has_frontmatter


def _make_vault(tmp, files=None, index_content=None):
    """Create a minimal vault structure in a temp dir."""
    vault = Path(tmp)
    (vault / "raw" / "articles").mkdir(parents=True)
    (vault / "raw" / "papers").mkdir(parents=True)
    (vault / "raw" / "images").mkdir(parents=True)
    if index_content is not None:
        (vault / "raw" / "_source-index.md").write_text(index_content)
    if files:
        for rel_path, content in files.items():
            p = vault / rel_path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    return vault


class TestGetIndexedPaths:
    def test_missing_index_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            assert get_indexed_paths(vault) == set()

    def test_empty_index_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, index_content="# Source Index\n")
            assert get_indexed_paths(vault) == set()

    def test_parses_paths_from_index(self):
        index = (
            "# Source Index\n\n"
            "| Title | Type | Tags | Status | Date | Path |\n"
            "|-------|------|------|--------|------|------|\n"
            "| Test | article | ai | raw | 2026-01-01 | `raw/articles/test.md` |\n"
            "| Paper | paper | ml | raw | 2026-01-02 | `raw/papers/paper.md` |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, index_content=index)
            result = get_indexed_paths(vault)
            assert result == {"raw/articles/test.md", "raw/papers/paper.md"}


class TestScanRawDirectory:
    def test_empty_raw_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp)
            assert scan_raw_directory(vault) == []

    def test_finds_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/test.md": "# Test\nSome content",
            })
            result = scan_raw_directory(vault)
            assert len(result) == 1
            assert result[0]["path"] == "raw/articles/test.md"
            assert result[0]["type"] == "document"

    def test_finds_image_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/images/photo.png": "fake-png-data",
            })
            result = scan_raw_directory(vault)
            assert len(result) == 1
            assert result[0]["type"] == "image"

    def test_skips_hidden_and_underscore_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/visible.md": "content",
                "raw/articles/.hidden.md": "hidden",
            })
            # _source-index.md is created by _make_vault but should be skipped
            result = scan_raw_directory(vault)
            assert len(result) == 1
            assert result[0]["name"] == "visible.md"

    def test_skips_unsupported_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/notes.md": "content",
                "raw/articles/data.csv": "a,b,c",
                "raw/articles/script.py": "print('hi')",
            })
            result = scan_raw_directory(vault)
            assert len(result) == 1

    def test_detects_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = _make_vault(tmp, files={
                "raw/articles/with-fm.md": "---\ntitle: Test\n---\nContent",
                "raw/articles/no-fm.md": "# Just a heading\nContent",
            })
            result = scan_raw_directory(vault)
            by_name = {r["name"]: r for r in result}
            assert by_name["with-fm.md"]["has_frontmatter"] is True
            assert by_name["no-fm.md"]["has_frontmatter"] is False

    def test_no_raw_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            assert scan_raw_directory(vault) == []


class TestHasFrontmatter:
    def test_with_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("---\ntitle: Hello\n---\nBody")
            assert _has_frontmatter(p) is True

    def test_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("# Just a heading")
            assert _has_frontmatter(p) is False

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("")
            assert _has_frontmatter(p) is False
