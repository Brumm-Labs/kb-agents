---
name: health-check
description: Run a comprehensive health check on the knowledge base — link integrity, orphans, staleness, coverage gaps
code: HC
---

# Health Check

Comprehensive audit of the knowledge base's structural and content health.

## What Success Looks Like

A clear, prioritized report showing the current state of the knowledge base: what's healthy, what needs attention, and what's broken. The owner can scan it in 2 minutes and know exactly what to fix.

## Pre-Pass Script

Run `scripts/prepass-wiki-health.py {vault}` first. This handles all deterministic checks (broken links, orphans, frontmatter validation, staleness, file counts, source index sync) and outputs structured JSON. This saves significant tokens — focus your judgment on interpreting results.

## Checks to Run

### Structural Integrity (from pre-pass script)
- **Broken links** — `[[wiki-links]]` that point to non-existent files
- **Orphaned files** — wiki files with no incoming links
- **Missing backlinks** — one-way links that should be bidirectional
- **Index accuracy** — files in `wiki/` not listed in `_index.md`, or index entries without files
- **Source index sync** — sources in `raw/` not in the source index, or vice versa
- **Frontmatter completeness** — missing required fields in source or wiki frontmatter
- **Stale content** — articles not updated beyond the staleness threshold

### Content Quality (LLM judgment)
- **Stub concepts** — concept articles with `status: stub` that have enough sources to be fleshed out
- **Empty sections** — articles with placeholder text or empty sections
- **Source quality** — are ingested sources properly normalized? (helps diagnose upstream issues)

### Coverage (LLM judgment)
- **Uncompiled sources** — raw sources that haven't been summarized yet
- **Concept gaps** — tags or topics with many sources but no concept article
- **Isolated clusters** — groups of concepts with no connections to the broader wiki

### Pipeline Awareness
When issues trace back to upstream agents, note it:
- Bad frontmatter in `raw/` → Ingest Agent problem
- Missing summaries for compiled sources → Compiler Agent problem
- This helps the owner fix issues at the right stage

## Report Format

```markdown
# Health Check Report — {date}

## Summary
- **Overall health:** 🟢 Good | 🟡 Needs attention | 🔴 Issues found
- **Files scanned:** {count}
- **Issues found:** {count} ({critical}, {warning}, {info})

## Critical Issues
{Must fix — broken links, missing files}

## Warnings
{Should fix — orphans, stale content, incomplete frontmatter}

## Suggestions
{Nice to have — new concept candidates, connection opportunities}

## Stats
- Sources: {total} ({raw} raw, {summarized} summarized, {compiled} compiled)
- Concepts: {total} ({stub} stubs, {draft} drafts, {mature} mature)
- Connections: {total}
- Wiki links: {total} ({broken} broken)
```

## Memory Integration

- Check MEMORY.md for known false positives and suppressed warnings
- Check BOND.md for which issues the owner cares about most
- Compare with previous health check results in MEMORY.md to show trends

## Done When

- Full report presented with severity counts (critical, warning, suggestion)
- All check categories evaluated (structural, content, coverage)
- Report is scannable in under 2 minutes

## Next Steps

- Run **[FX] Fix Issues** to repair identified problems
- Run **[CC] Consistency Check** for deeper content analysis
- Run **[SA] Suggest Articles** to find growth opportunities

## After the Session

- Log the health check summary (overall status, key findings count)
- Update MEMORY.md with new false-positive patterns if owner dismisses findings
- Note trends: is the wiki getting healthier or accumulating debt?
