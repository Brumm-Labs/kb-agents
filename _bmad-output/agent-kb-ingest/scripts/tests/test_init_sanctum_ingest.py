"""Tests for init-sanctum.py (ingest agent) — config parsing, sanctum creation, template substitution."""

import sys
import tempfile
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location(
    "init_sanctum",
    Path(__file__).parent.parent / "init-sanctum.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

parse_yaml_config = mod.parse_yaml_config
parse_frontmatter = mod.parse_frontmatter
copy_references = mod.copy_references
copy_scripts = mod.copy_scripts
discover_capabilities = mod.discover_capabilities
generate_capabilities_md = mod.generate_capabilities_md
substitute_vars = mod.substitute_vars
SKILL_ONLY_FILES = mod.SKILL_ONLY_FILES


class TestParseYamlConfig:
    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "config.yaml"
            p.write_text('name: "My KB"\ncreated: 2026-01-01\n')
            result = parse_yaml_config(p)
            assert result["name"] == "My KB"
            assert result["created"] == "2026-01-01"

    def test_missing_file(self):
        assert parse_yaml_config(Path("/nonexistent/config.yaml")) == {}

    def test_comments_and_empty_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "config.yaml"
            p.write_text("# Comment\n\nkey: value\n# Another comment\n")
            result = parse_yaml_config(p)
            assert result == {"key": "value"}


class TestParseFrontmatter:
    def test_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("---\nname: Test\ncode: TC\ndescription: A test\n---\nBody")
            meta = parse_frontmatter(p)
            assert meta["name"] == "Test"
            assert meta["code"] == "TC"

    def test_no_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.md"
            p.write_text("# No frontmatter")
            assert parse_frontmatter(p) == {}


class TestCopyReferences:
    def test_copies_files_skipping_skill_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            dst = Path(tmp) / "dst"
            src.mkdir()
            (src / "ingest-source.md").write_text("content")
            (src / "auto-discover.md").write_text("content")
            (src / "first-breath.md").write_text("skill only")
            (src / "memory-guidance.md").write_text("skill only")
            copied = copy_references(src, dst)
            assert "ingest-source.md" in copied
            assert "auto-discover.md" in copied
            assert "first-breath.md" not in copied
            assert "memory-guidance.md" not in copied
            assert (dst / "ingest-source.md").exists()

    def test_creates_dest_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            dst = Path(tmp) / "nested" / "dst"
            src.mkdir()
            (src / "file.md").write_text("content")
            copy_references(src, dst)
            assert dst.exists()


class TestCopyScripts:
    def test_copies_scripts_skipping_init(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            dst = Path(tmp) / "dst"
            src.mkdir()
            (src / "scan-new-sources.py").write_text("code")
            (src / "init-sanctum.py").write_text("skip me")
            copied = copy_scripts(src, dst)
            assert "scan-new-sources.py" in copied
            assert "init-sanctum.py" not in copied

    def test_nonexistent_source(self):
        assert copy_scripts(Path("/nonexistent"), Path("/dst")) == []


class TestDiscoverCapabilities:
    def test_discovers_from_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            refs = Path(tmp) / "refs"
            refs.mkdir()
            (refs / "ingest-source.md").write_text(
                "---\nname: Ingest Source\ncode: IN\ndescription: Manual ingest\n---\nBody"
            )
            (refs / "auto-discover.md").write_text(
                "---\nname: Auto-Discover\ncode: AD\ndescription: Scan raw/\n---\nBody"
            )
            # Skill-only file should be skipped
            (refs / "first-breath.md").write_text(
                "---\nname: First Breath\ncode: FB\n---\nBody"
            )
            caps = discover_capabilities(refs, "./references")
            codes = [c["code"] for c in caps]
            assert "IN" in codes
            assert "AD" in codes
            assert "FB" not in codes

    def test_skips_files_without_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            refs = Path(tmp) / "refs"
            refs.mkdir()
            (refs / "no-code.md").write_text("---\nname: No Code\n---\nBody")
            assert discover_capabilities(refs, "./references") == []


class TestGenerateCapabilitiesMd:
    def test_generates_table(self):
        caps = [{"name": "Test", "description": "A test", "code": "TC", "source": "./references/test.md"}]
        content = generate_capabilities_md(caps, evolvable=True)
        assert "| [TC] |" in content
        assert "## Learned" in content

    def test_not_evolvable(self):
        content = generate_capabilities_md([], evolvable=False)
        assert "## Learned" not in content


class TestSubstituteVars:
    def test_replaces_placeholders(self):
        template = "Hello {user_name}, born on {birth_date}."
        result = substitute_vars(template, {"user_name": "Alice", "birth_date": "2026-01-01"})
        assert result == "Hello Alice, born on 2026-01-01."

    def test_no_placeholders(self):
        assert substitute_vars("No vars", {}) == "No vars"

    def test_missing_var_left_as_is(self):
        assert substitute_vars("{unknown}", {"other": "val"}) == "{unknown}"
