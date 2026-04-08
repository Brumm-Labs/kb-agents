# Pulse

## Default Wake Behavior

When invoked with `--headless` and no specific task:

1. **Memory curation first** — review recent session logs, distill into MEMORY.md, prune stale entries
2. **Run health check** — structural integrity, broken links, orphans, frontmatter completeness
3. **Auto-fix safe issues** — add missing backlinks, update index, fix frontmatter dates (only auto-fixable tier from Fix Issues capability)
4. **Compare with baseline** — check trends against last health check in MEMORY.md
5. **Report** — write health check results to `sessions/YYYY-MM-DD.md`, update quality baselines in MEMORY.md

## Named Tasks

| Task | Trigger | Action |
|------|---------|--------|
| `health` | `-H:health` | Full health check + auto-fix |
| `consistency` | `-H:consistency` | Deep consistency analysis only |
| `suggest` | `-H:suggest` | Generate article suggestions |
| `curate` | `-H:curate` | Memory curation only — session logs → MEMORY.md |

## Frequency

Default: weekly. Respect owner preferences from BOND.md.

## Quiet Hours

None set. Owner configures during First Breath or later sessions.
