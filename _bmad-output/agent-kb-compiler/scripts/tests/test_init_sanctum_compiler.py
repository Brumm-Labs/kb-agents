"""Tests for init-sanctum.py (compiler agent) — config parsing, sanctum creation, template substitution."""

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
            p.write_text('name: "My KB"\n')
            assert parse_yaml_config(p)["name"] == "My KB"

    def test_missing_file(self):
        assert parse_yaml_config(Path("/nonexistent")) == {}


class TestCopyReferences:
    def test_copies_and_skips_skill_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            dst = Path(tmp) / "dst"
            src.mkdir()
            (src / "compile-sources.md").write_text("content")
            (src / "first-breath.md").write_text("skill only")
            copied = copy_references(src, dst)
            assert "compile-sources.md" in copied
            assert "first-breath.md" not in copied


class TestCopyScripts:
    def test_skips_init_sanctum(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            dst = Path(tmp) / "dst"
            src.mkdir()
            (src / "wiki-tools.py").write_text("code")
            (src / "init-sanctum.py").write_text("skip")
            copied = copy_scripts(src, dst)
            assert "wiki-tools.py" in copied
            assert "init-sanctum.py" not in copied


class TestDiscoverCapabilities:
    def test_discovers_capabilities(self):
        with tempfile.TemporaryDirectory() as tmp:
            refs = Path(tmp) / "refs"
            refs.mkdir()
            (refs / "compile-sources.md").write_text(
                "---\nname: Compile Sources\ncode: CS\ndescription: Process sources\n---\n"
            )
            caps = discover_capabilities(refs, "./references")
            assert len(caps) == 1
            assert caps[0]["code"] == "CS"


class TestGenerateCapabilitiesMd:
    def test_generates_table(self):
        caps = [{"name": "T", "description": "D", "code": "TC", "source": "s"}]
        content = generate_capabilities_md(caps, evolvable=True)
        assert "| [TC] |" in content


class TestSubstituteVars:
    def test_replaces(self):
        assert substitute_vars("{x} world", {"x": "hello"}) == "hello world"
