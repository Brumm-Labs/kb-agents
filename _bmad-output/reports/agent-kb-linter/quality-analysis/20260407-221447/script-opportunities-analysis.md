# Script Opportunity Analysis — agent-kb-linter

**Scanner:** ScriptHunter v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent

---

## Existing Scripts Inventory

| Script | Type | Purpose | Has argparse | Has JSON output | Has tests |
|--------|------|---------|--------------|-----------------|-----------|
| `scripts/init-sanctum.py` | Python | First Breath sanctum scaffolding | No | No | No |

One script exists. It is functional and well-structured (correct use of pathlib, template substitution, capability discovery via frontmatter parsing). The scan-scripts linter flagged three medium issues and one high issue, documented below.

`scripts/tests/` directory does not exist.

---

## Assessment

Inspector's intelligence placement is good overall — the LLM handles judgment (severity assessment, terminology analysis, content contradiction detection) and the init script handles deterministic scaffolding (file copying, template substitution, directory creation). However, the capability prompts instruct the LLM to perform several operations that are structurally deterministic: link extraction, index cross-reference checking, frontmatter field validation, and file enumeration. These are excellent pre-pass script candidates that would reduce token cost on every health-check invocation.

The highest-value opportunity is a pre-pass scanner for wiki structural checks — equivalent to what the BMad prepass scripts do for agents. A `prepass-wiki-health.py` that extracts broken links, orphaned files, frontmatter violations, and index mismatches as JSON before the LLM sees the raw wiki would dramatically reduce the token cost of health checks.

---

## Scripts Linter Findings (Preserved Verbatim)

| Severity | File | Issue | Action |
|----------|------|-------|--------|
| High | `scripts/tests/` | scripts/tests/ directory does not exist — no unit tests | Create scripts/tests/ with test files for each script |
| Medium | `scripts/init-sanctum.py` | No argparse found — script lacks --help self-documentation | Add argparse with description and argument help text |
| Medium | `scripts/init-sanctum.py` | No json.dumps found — output may not be structured JSON | Use json.dumps for structured output parseable by workflows |
| Medium | `scripts/init-sanctum.py` | No unit test found for init-sanctum.py | Create scripts/tests/test-init-sanctum.py with test cases |

---

## Key Findings — Script Opportunities in Prompt Files

### [High] health-check.md: Broken link extraction is fully deterministic
**File:** `references/health-check.md`, lines 17–22 (Structural Integrity section)  
**What the LLM currently does:** Scans wiki files for `[[wiki-links]]`, checks if target files exist, identifies broken links, orphaned files, missing backlinks, index accuracy, and source index sync.  
**What a script would do:**
```python
# prepass-wiki-health.py
# - Glob all .md files in wiki/
# - Extract [[wiki-links]] with regex
# - Cross-reference against file index
# - Check _index.md for missing/extra entries
# - Check raw/_source-index.md vs raw/ directory
# - Output JSON: {broken_links: [...], orphans: [...], missing_backlinks: [...], index_mismatches: [...]}
```
**Estimated token savings:** 800–1,500 tokens per health check invocation (scanning 50–200 files for structural issues).  
**LLM Tax:** Heavy (500+ tokens)  
**Pre-pass potential:** High — feeds health-check.md directly, reducing LLM to interpreting structured results, not extracting them.

### [High] health-check.md: Frontmatter completeness check is schema validation
**File:** `references/health-check.md`, line 28 ("Frontmatter completeness — missing required fields")  
**What the LLM currently does:** Reads each wiki file's frontmatter, compares against expected fields.  
**What a script would do:**
```python
# Extend prepass-wiki-health.py:
# - Parse YAML frontmatter from each .md file
# - Compare against required field schema (from config or hardcoded)
# - Output list of files with missing/invalid fields
```
**Estimated token savings:** 200–600 tokens per health check (depends on wiki size).  
**LLM Tax:** Heavy (scales with wiki size)  
**Reuse:** Could be a standalone `scan-frontmatter.py` usable by consistency-check too.

### [High] consistency-check.md: Tag/terminology extraction is regex work
**File:** `references/consistency-check.md`, lines 22–25 (Terminology section)  
**What the LLM currently does:** Reads all wiki files, extracts tags, identifies overlapping/duplicate tags and terminology drift.  
**What a script would do:**
```python
# prepass-terminology.py
# - Parse frontmatter tags from all wiki files
# - Build tag frequency map
# - Detect near-duplicate tags (difflib.SequenceMatcher)
# - Extract key terms from headings (regex)
# - Output: {tags: {tag: count}, near_duplicates: [...], heading_terms: [...]}
```
**Estimated token savings:** 500–1,000 tokens per consistency-check invocation.  
**LLM Tax:** Heavy  
**Pre-pass potential:** High — gives the LLM a compact tag inventory instead of raw file contents.

### [Medium] health-check.md: File statistics are pure counting
**File:** `references/health-check.md`, lines 54–58 (Stats section of report template)  
**What the LLM currently does:** Counts sources (raw/summarized/compiled), concepts (stub/draft/mature), connections, wiki links.  
**What a script would do:**
```python
# Extend prepass-wiki-health.py:
# - Count files by status field in frontmatter
# - Count wiki-link references across all files
# - Output: {sources: {raw: N, summarized: N, compiled: N}, concepts: {stub: N, ...}, total_links: N}
```
**Estimated token savings:** 200–400 tokens per invocation.  
**LLM Tax:** Moderate  

### [Medium] consistency-check.md: Naming convention violations are regex
**File:** `references/consistency-check.md`, line 35 ("Naming convention violations")  
**What the LLM currently does:** Reads file names, checks against naming conventions.  
**What a script would do:** `pathlib.glob("wiki/**/*.md")` + regex pattern check against naming rules. Output: list of violating files.  
**Estimated token savings:** 100–200 tokens.  
**LLM Tax:** Moderate  

### [Low] suggest-articles.md: Tag frequency for concept gap detection
**File:** `references/suggest-articles.md`, lines 17–20 (New Concept Articles)  
**What the LLM currently does:** Finds tags appearing in 3+ sources but without a concept article.  
**What a script would do:** Tag frequency from prepass-terminology.py already covers this. Cross-reference against existing concept files. Output: `{tag_gaps: [{tag: "X", source_count: N, has_concept: false}]}`.  
**Estimated token savings:** 100–300 tokens.  
**LLM Tax:** Light to Moderate  
**Note:** This is the same pre-pass output as the terminology script — zero additional work if prepass-terminology.py exists.

---

## Scripts Linter Finding Analysis

### [High] No unit tests (scripts/tests/ missing)
The init-sanctum.py script handles critical First Breath scaffolding. Key operations that should be tested:
- `parse_yaml_config()` — handles malformed YAML gracefully?
- `parse_frontmatter()` — handles files without frontmatter?
- `substitute_vars()` — handles missing variables (no `{key}` in template)?
- `generate_capabilities_md()` — correct markdown table output?
- Main flow — existing sanctum detected correctly?

**Create:** `scripts/tests/test-init-sanctum.py` with at least 5 test cases using Python `unittest` or `pytest`.

### [Medium] No argparse — init-sanctum.py lacks --help
Current usage output (line 9–11) is a docstring, not an argparse interface. When invoked by the LLM, the LLM must inline the usage instructions rather than running `python3 init-sanctum.py --help`.  
**Fix:** Replace positional argument parsing with argparse:
```python
import argparse
parser = argparse.ArgumentParser(description="First Breath — Deterministic sanctum scaffolding for agent-kb-linter")
parser.add_argument("project_root", help="Project root directory (contains _bmad/)")
parser.add_argument("skill_path", help="Path to agent-kb-linter skill directory")
args = parser.parse_args()
```
**Token savings:** ~50 tokens per LLM invocation (no need to inline usage docs).

### [Medium] No json.dumps — output is human-readable only
init-sanctum.py prints human-readable status messages. In a headless or automated invocation, structured JSON output would be parseable.  
**Fix:** Add `--json` flag. When set, output `{"status": "created|exists|error", "sanctum_path": "...", "files_created": [...]}` and suppress print statements.

---

## Aggregate Savings

| Script Opportunity | Per-Invocation Savings | Frequency Estimate | Annual Token Impact |
|-------------------|----------------------|-------------------|---------------------|
| prepass-wiki-health.py (links + orphans + index) | 800–1,500 tokens | Weekly health check | 40,000–78,000 tokens/year |
| Frontmatter schema validation | 200–600 tokens | Weekly health check | 10,000–31,000 tokens/year |
| prepass-terminology.py | 500–1,000 tokens | Monthly consistency check | 6,000–12,000 tokens/year |
| File statistics counting | 200–400 tokens | Weekly health check | 10,000–20,000 tokens/year |
| **Total** | **1,700–3,500 tokens** | — | **~66,000–141,000 tokens/year** |

**Highest-priority script to build:** `prepass-wiki-health.py` — covers the most expensive LLM operations, feeds the most-used capability (HC), and has clear standalone lint value (could be run in CI independently of the LLM).
