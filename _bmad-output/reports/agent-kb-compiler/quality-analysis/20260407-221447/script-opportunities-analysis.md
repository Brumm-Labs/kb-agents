# Script Opportunities Analysis — agent-kb-compiler

## Existing Scripts Inventory

| Script | Type | Purpose | argparse | JSON output | Tests |
|--------|------|---------|----------|-------------|-------|
| `scripts/init-sanctum.py` | Python | Deterministic sanctum scaffolding | No | No | No (`scripts/tests/` missing) |

The `init-sanctum.py` script is well-designed for its purpose: it reads config, copies templates, substitutes variables, generates CAPABILITIES.md from capability frontmatter, and creates the sanctum directory structure. It is a good model for the additional scripts identified below.

**Scripts lint findings (from scripts-temp.json):**
- Medium: No argparse — script lacks `--help` self-documentation
- Medium: No `json.dumps` — output may not be structured JSON
- Medium: No unit test for `init-sanctum.py`
- High: `scripts/tests/` directory does not exist

## Assessment

The agent's prompts are notably clean of deterministic operations. The capability authors have correctly used LLM judgment for the things that require judgment (synthesis, concept identification, connection discovery) and kept the prompts outcome-focused. However, three meaningful script opportunities exist: link validation (currently not done, but needed), source index management (partially manual), and wiki metrics (surfaced by LLM when a script could pre-extract). The most impactful addition would be a link checker — this is a classic deterministic operation that prompts currently can't handle at all.

## Key Findings

**[High] maintain-wiki.md — "Check links" is LLM-described but needs a script**

The "Check links" operation in `maintain-wiki.md` lists: "find broken `[[wiki-links]]` and orphaned files." Currently there is no mechanism for this — if the LLM were to attempt it, it would need to:
1. Read every file in `wiki/` (concepts, summaries, connections)
2. Extract all `[[wiki-link]]` references with regex
3. Check each against a file system listing
4. Report broken links

This is 100% deterministic and reading 50+ wiki files would cost 10,000-30,000+ tokens with high error rate on large wikis. A Python script does it in milliseconds.

**Script:** `scripts/check-wiki-links.py <vault-path>`
```python
# Uses pathlib to glob wiki/ for all .md files
# Regex: r'\[\[([^\]|]+)' to extract link targets
# For each link: check if target file exists in wiki/
# Output: JSON with broken_links, orphaned_files, stats
```

**LLM Tax:** Heavy (500+ tokens per "Check links" invocation on any non-trivial wiki). With a script: 0 tokens.

**Pre-pass potential:** Yes — output JSON feeds `maintain-wiki.md` directly. The prompt's "Check links" operation becomes: "Run `scripts/check-wiki-links.py` and use the JSON output to report and fix broken links."

**Standalone value:** Yes — useful as a lint check independent of quality analysis. Could be scheduled.

---

**[Medium] compile-sources.md:17 — Source index parsing is deterministic**

Step 1 of Compile Sources: "Read the source index (`raw/_source-index.md`) to find sources with `status: raw` or `status: summarized`."

The LLM is being asked to parse a markdown file and filter by a status field — a deterministic extraction operation. For small source indexes (10 items), this is negligible. For larger ones (50+ sources), the LLM reads the full index, does pattern matching, and returns a list. A script extracts this in one pass.

**Script:** `scripts/list-uncompiled.py <vault-path>`
```python
# Reads raw/_source-index.md
# Regex or markdown parser to extract source entries with status: raw|summarized
# Output: JSON list of {path, title, status, date_added}
# Feeds compile-sources.md as "here are the sources to compile today"
```

**LLM Tax:** Moderate (~100-300 tokens depending on index size). Grows with index size — will become Heavy for mature knowledge bases.

**Pre-pass potential:** Yes — the JSON list replaces step 1 of the Compile Sources workflow, giving the LLM a clean list rather than raw markdown to parse.

---

**[Medium] manage-concepts.md — "Inventory" operation scans and counts concept files**

The Inventory operation ("list all concepts with their status and source count") requires the LLM to read all files in `wiki/concepts/`, extract frontmatter status and source list lengths, and compile a summary. For a mature knowledge base with 50+ concepts, this is a significant token cost.

**Script:** `scripts/concept-inventory.py <vault-path>`
```python
# Globs wiki/concepts/*.md
# Parses YAML frontmatter from each file (pyyaml or regex)
# Extracts: title, status, len(sources), len(related), date_updated
# Output: JSON list + summary stats (stub_count, draft_count, mature_count)
```

**LLM Tax:** Moderate per invocation (~200-500 tokens for 20-30 concepts, Heavy for 50+). Grows unbounded with wiki size.

**Pre-pass potential:** Yes — feeds `manage-concepts.md` Inventory operation. Also useful as a standalone wiki health report.

---

**[Medium] maintain-wiki.md — "Stats" operation counts files and tracks staleness**

The Stats operation ("counts, coverage metrics, staleness indicators") currently has no mechanism at all — the LLM would need to list directories and count files. This is pure filesystem enumeration.

**Script:** `scripts/wiki-stats.py <vault-path>`
```python
# Counts: summaries, concepts (by status), connections (by type)
# Identifies: concepts not updated in 30+ days (staleness)
# Checks: concepts with 0 sources (stubs with no content)
# Output: JSON stats object
```

**LLM Tax:** Moderate if attempted by LLM (~150-300 tokens). With a script: 0 tokens. Could be part of `concept-inventory.py`.

---

**[Low] compile-sources.md — YAML frontmatter generation is templated but manual**

The Summary Format section provides an exact YAML frontmatter template. The LLM fills it in per source. The `date_compiled` field is today's date (deterministic), `source_ref` is a path (deterministic), and `concepts`/`tags` require judgment. The deterministic fields could be pre-filled by a script.

This is low priority because the template is small and the judgment fields (concepts, tags) dominate the work. The date field is trivial for the LLM to fill correctly.

**LLM Tax:** Light (<50 tokens for deterministic fields). Not worth a dedicated script.

---

**[Low] init-sanctum.py — Add argparse and JSON output (from scripts-temp.json)**

The existing `init-sanctum.py` lacks `--help` self-documentation and structured JSON output. Current output is human-readable print statements. Adding argparse with documented arguments and a `--json` flag for structured output would:
- Allow prompts invoking the script to use `--help` instead of inlining the interface
- Enable downstream parsing of what was created

**Fix:**
```python
import argparse, json
parser = argparse.ArgumentParser(description="Scaffold sanctum for agent-kb-compiler")
parser.add_argument("project_root", help="Path to project root")
parser.add_argument("skill_path", help="Path to skill directory")
parser.add_argument("--json", action="store_true", help="Output JSON result")
```

## Aggregate Savings

| Script | LLM Tax Level | Est. Tokens Saved per Invocation | Priority |
|--------|--------------|----------------------------------|----------|
| check-wiki-links.py | Heavy | 5,000-30,000+ (scales with wiki size) | High |
| list-uncompiled.py | Moderate | 100-300 (scales with source count) | Medium |
| concept-inventory.py | Moderate→Heavy | 200-3,000+ (scales with concept count) | Medium |
| wiki-stats.py | Moderate | 150-300 | Medium |
| init-sanctum.py argparse/JSON | Light | 50-100 (self-documentation) | Low |

**Total estimated savings:** Primarily driven by `check-wiki-links.py` — this is the standout opportunity. As the wiki grows, the savings from `concept-inventory.py` and `list-uncompiled.py` will compound. All three should be built before the wiki reaches 50+ articles, when LLM-based scanning becomes genuinely costly.

**Reuse potential:** `check-wiki-links.py` and `wiki-stats.py` are useful across any Obsidian-wiki-based agent. They could be generalized as shared BMad utilities.
