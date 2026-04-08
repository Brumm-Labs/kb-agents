---
name: memory-guidance
description: Memory philosophy and practices for Cartographer
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every conversation begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened.

## What to Remember

- Concept inventory — names, statuses, source counts
- Category structure decisions and rationale
- Wiki conventions (link format, article depth, naming)
- Interesting connections spotted but not yet written
- Patterns across compilation sessions
- What writing style the owner prefers for articles

## What NOT to Remember

- Full article content — that's in `wiki/`
- Source contents — that's in `raw/`
- Transient compilation details
- Things derivable from the wiki index

## Two-Tier Memory: Session Logs → Curated Memory

### Session Logs (raw, append-only)
After each session, append to `sessions/YYYY-MM-DD.md`:

```markdown
## Session — {time or context}

**What happened:** {1-2 sentence summary}

**Compiled:** {count} sources, {count} concepts created/updated

**Connections spotted:** {list}

**Observations:** {patterns, preferences, style notes}

**Follow-up:** {stubs to flesh out, connections to write, index to reorganize}
```

### MEMORY.md (curated, distilled)
Long-term memory loaded every session. Keep it tight: concept inventory, category structure, wiki conventions, connection candidates.

## Where to Write

- **`sessions/YYYY-MM-DD.md`** — raw session notes
- **MEMORY.md** — curated (concept inventory, conventions, connection candidates)
- **BOND.md** — owner preferences (article style, depth, organization)
- **PERSONA.md** — your evolution

**Every time you create a new organic file or folder, update INDEX.md.**

## Token Discipline

Keep MEMORY.md under 200 lines. The concept inventory will be the biggest section — use compact format (table or comma-separated with status flags).
