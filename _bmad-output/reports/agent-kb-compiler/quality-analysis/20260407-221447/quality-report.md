# BMad Quality Report · Cartographer (agent-kb-compiler)

🗺️ **Cartographer** — Knowledge Base Wiki Compiler

> A master synthesizer who sees the forest in the trees. Thinks in connections — every new source is an opportunity to strengthen the web of understanding.

**Agent Type:** Memory Agent (Bootloader) | **Capabilities:** 4 built-in | **Evolvable:** Yes

---

## Grade: Good

No critical issues. Strong identity, lean architecture, zero waste patterns. The compilation pipeline (sources → summaries → concepts → connections → maintenance) is well-designed. Primary gaps: headless infrastructure and missing query capability.

---

## Capability Dashboard

| Code | Capability | Status | Notes |
|------|-----------|--------|-------|
| [CS] | Compile Sources | ✅ Good | Full outcome structure, Memory Integration + After Session |
| [MC] | Manage Concepts | ✅ Good | Rich operation set (create, update, promote, merge, split) |
| [MW] | Maintain Wiki | ⚠️ Needs attention | Link checking and index rebuild are scriptable |
| [WC] | Write Connections | ✅ Good | Excellent connection taxonomy (convergence, contradiction, evolution, pattern, comparison) |

---

## Themes

### 1. Headless Mode Declared But Non-Functional (High)

**Observations:** 3 scanners | **Impact:** `--headless` silently fails

PULSE-template.md missing. Every headless invocation hits a dead end.

**Fix:** Create `assets/PULSE-template.md` with default wake behavior: scan source index for uncompiled sources, compile the oldest N, update wiki index.

### 2. Missing Search/Query Capability (Medium)

**Observations:** 2 scanners | **Impact:** Agent builds a wiki it can't help query

The Cartographer compiles knowledge but offers no way to search or query it. This is a natural extension.

**Fix:** Consider adding a `[QW] Query Wiki` capability or defer to a dedicated Q&A agent.

### 3. First Breath Needs Progression Gates (Medium)

**Observations:** 2 findings | **Impact:** 98-line discovery flow with no completion signals

No explicit transitions between discovery phases or voice-absorption mechanic.

**Fix:** Add lightweight progression markers and voice-mirroring guidance.

### 4. capability-authoring.md Needs Memory Lifecycle Hooks (Medium)

**Observations:** 2 findings | **Impact:** Inconsistent capability file structure

Missing Memory Integration and After Session sections that all other capabilities have.

**Fix:** Add both sections.

### 5. Script Opportunities for Deterministic Operations (Medium)

**Observations:** 3 findings | **Impact:** Token waste at scale

- `check-wiki-links.py` — broken link detection costs 5,000-30,000+ tokens at scale; script does it in 0
- `concept-inventory.py` — frontmatter extraction from all concept files
- `list-uncompiled.py` — source index parsing for uncompiled entries

**Fix:** Create these scripts in `scripts/`.

---

## Standalone Findings

- **Medium:** No parallelization path for batch compilations of 5+ sources in `compile-sources.md`
- **Medium:** Init script lacks argparse, JSON output, and unit tests
- **Low:** No "What's Next" rebirth hook (on normal activation, suggest what to compile next)

---

## Strengths

- Lean bootloader with evocative identity seed
- Standout CREED: "Synthesis over aggregation", "Connections are the product", "Let structure emerge"
- All 4 core capabilities have Memory Integration + After Session sections
- Rich connection taxonomy in `write-connections.md` (5 types with formats)
- Two-tier memory architecture with 200-line cap
- Concept article lifecycle (stub → draft → mature) is well-designed
- Zero waste patterns across all files
- Evolvable init script

---

## Sanctum Architecture: Excellent

All 6 templates present, well-seeded with domain-specific content. CREED standing orders are domain-adapted (Connection Hunting, Surprise and Delight, Self-Improvement). BOND has wiki-specific sections. Only gap: PULSE-template absent.
