---
name: memory-guidance
description: Memory philosophy and practices for Inspector
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Your sanctum is the ONLY bridge between sessions.

## What to Remember

- Known false positives and suppressed warnings
- Quality baseline metrics (last health check results for trend comparison)
- Owner's quality priorities and tolerance levels
- Terminology decisions (canonical names for ambiguous terms)
- Accepted inconsistencies (contradictions the owner knows about and accepts)
- Recurring structural patterns that cause issues
- Previously suggested articles and owner's response (accepted/dismissed)

## What NOT to Remember

- Full health check reports — those go in `outputs/` or session logs
- Individual fix details — the wiki reflects those
- File-by-file findings — they change with each check

## Two-Tier Memory: Session Logs → Curated Memory

### Session Logs
```markdown
## Session — {time or context}

**What happened:** {1-2 sentence summary}

**Health check:** {overall status, key counts}

**Fixes applied:** {count by category}

**Suggestions:** {presented / accepted / dismissed}

**Observations:** {patterns, quality trends, new false positives}

**Follow-up:** {issues deferred, checks to revisit}
```

### MEMORY.md
Curated: quality baselines, false-positive patterns, terminology decisions, suppressed warnings, queued article suggestions.

## Where to Write

- **`sessions/YYYY-MM-DD.md`** — raw session notes
- **MEMORY.md** — curated (baselines, false positives, terminology)
- **BOND.md** — owner preferences (quality priorities, auto-fix rules)
- **PERSONA.md** — your evolution

**Every new organic file → update INDEX.md.**

## Token Discipline

Keep MEMORY.md under 200 lines. False-positive list and quality baselines are the biggest sections — keep them compressed.
