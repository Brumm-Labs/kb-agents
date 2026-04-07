# BMad Quality Report · Inspector (agent-kb-linter)

🔍 **Inspector** — Knowledge Base Wiki Linter

> A sharp-eyed quality auditor who cares about knowledge integrity without being pedantic. Pragmatic, clear in reporting, focused on issues that actually matter.

**Agent Type:** Memory Agent (Bootloader) | **Capabilities:** 4 built-in | **Evolvable:** Yes

---

## Grade: Good

No critical issues. Excellent CREED template with real domain-adapted values. Clean bootloader, zero path violations. Primary gaps: headless infrastructure, missing scripts for deterministic operations, and no progression signals.

---

## Capability Dashboard

| Code | Capability | Status | Notes |
|------|-----------|--------|-------|
| [HC] | Health Check | ⚠️ Needs attention | Deterministic checks should be scripts; high token savings |
| [FX] | Fix Issues | ✅ Good | Excellent three-tier taxonomy (auto-fix, needs confirmation, needs decision) |
| [SA] | Suggest Articles | ⚠️ Needs attention | No draft-offer follow-through |
| [CC] | Consistency Check | ✅ Good | Thorough check categories |

---

## Themes

### 1. Capability Completion Gap (High)

**Observations:** 9 findings across 3 scanners | **Impact:** No task-end signals

Zero progression/completion signals across all capability files. The agent has no explicit "done" criteria.

**Fix:** Add "Done When" sections and natural next-step transitions to HC, FX, SA, CC.

### 2. Headless Mode Non-Functional (High)

**Observations:** 3 scanners | **Impact:** `--headless` silently fails

PULSE-template.md missing. The Inspector is a natural candidate for scheduled health checks.

**Fix:** Create `assets/PULSE-template.md` with default wake behavior: run health check, fix safe issues, write report to `outputs/`.

### 3. High-Value Script Opportunity (High)

**Observations:** 1 major finding | **Impact:** 800-1,500 tokens/invocation savings

A `prepass-wiki-health.py` script could handle all deterministic health check operations: broken link detection, orphan scanning, frontmatter validation, file counting. Estimated 66,000-141,000 tokens/year savings.

**Fix:** Create `scripts/prepass-wiki-health.py` that outputs JSON; Health Check capability then focuses on interpreting results.

### 4. Script Infrastructure Immaturity (High)

**Observations:** 4 findings | **Impact:** Init script not production-ready

No test directory, no unit tests, no argparse, no JSON output on `init-sanctum.py`.

**Fix:** Add argparse, JSON output, create `scripts/tests/test-init-sanctum.py`.

### 5. Capability Scope Gaps (Medium)

**Observations:** 3 findings | **Impact:** Missing complementary capabilities

- No search/query capability for the wiki
- No awareness of the ingest/compilation pipeline (can't tell if wiki issues stem from bad raw data)
- `suggest-articles.md` has no follow-through (suggests articles but doesn't offer to draft them)

**Fix:** Consider adding a query capability; add pipeline-awareness notes to Health Check; add "draft stub?" offer to Suggest Articles.

---

## Standalone Findings

- **Medium:** `{vault}` placeholder in CREED template not substituted by init script (design ambiguity — vault path is session-specific, not birth-time)
- **Medium:** Config headers missing across capability files
- **Low:** Frontmatter description missing "Use when..." trigger phrase

---

## Strengths

- CREED template excellence: "Signal over noise", "Always include the fix", "Trends over snapshots", "Respect the draft"
- Standing orders are domain-perfect (False-Positive Learning, Surprise and Delight, Self-Improvement)
- `fix-issues.md` three-tier taxonomy (auto-fix / needs confirmation / needs decision) is elegant
- Anti-patterns are concrete and actionable ("Don't cry wolf", "Don't be pedantic about style when content accuracy is the issue")
- Zero waste patterns, zero path violations
- Lean correct bootloader
- Evolvable capabilities enabled

---

## Sanctum Architecture: Excellent

All 6 templates present, well-seeded. CREED is the standout: real core values with rationale, real domain-adapted standing orders, concrete anti-patterns. BOND has quality-specific sections. Only gap: PULSE-template absent.
