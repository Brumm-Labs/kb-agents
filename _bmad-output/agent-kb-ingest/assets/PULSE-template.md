# Pulse

## Default Wake Behavior

When invoked with `--headless` and no specific task:

1. **Memory curation first** — review recent session logs, distill into MEMORY.md, prune stale entries
2. **Scan for new sources** — check `{vault}/raw/` for files not in the source index
3. **Auto-ingest** — process any new files found using the Ingest Source capability with established conventions from BOND.md
4. **Index maintenance** — run orphan check, update stats in source index
5. **Report** — write a brief summary to `sessions/YYYY-MM-DD.md`

## Named Tasks

| Task | Trigger | Action |
|------|---------|--------|
| `ingest` | `-H:ingest` | Scan and ingest all new sources in `raw/` |
| `reindex` | `-H:reindex` | Rebuild source index from frontmatter |
| `curate` | `-H:curate` | Memory curation only — session logs → MEMORY.md |

## Frequency

Default: once daily. Respect owner preferences from BOND.md.

## Quiet Hours

None set. Owner configures during First Breath or later sessions.
