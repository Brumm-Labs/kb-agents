# Pulse

## Default Wake Behavior

When invoked with `--headless` and no specific task:

1. **Memory curation first** — review recent session logs, distill into MEMORY.md, prune stale entries
2. **Compile pending sources** — check source index for `status: raw` or `status: summarized`, compile the oldest N (default: 5)
3. **Concept maintenance** — promote stubs with 3+ sources to drafts, update existing concept articles with new source material
4. **Wiki index update** — rebuild `wiki/_index.md` with any new entries
5. **Report** — write a brief summary to `sessions/YYYY-MM-DD.md`

## Named Tasks

| Task | Trigger | Action |
|------|---------|--------|
| `compile` | `-H:compile` | Compile all pending raw sources |
| `concepts` | `-H:concepts` | Promote stubs, update existing concepts |
| `index` | `-H:index` | Rebuild wiki master index |
| `curate` | `-H:curate` | Memory curation only — session logs → MEMORY.md |

## Frequency

Default: once daily, after ingest agent runs. Respect owner preferences from BOND.md.

## Quiet Hours

None set. Owner configures during First Breath or later sessions.
