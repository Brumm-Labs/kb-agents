# Pulse

## Default Wake Behavior

When invoked with `--headless` and no specific task:

1. **Memory curation first** — review recent session logs, distill into MEMORY.md, prune stale entries
2. **Auto-Discover** — run `scripts/scan-new-sources.py {vault}` to find untracked files
3. **Auto-ingest** — process all new files found using established conventions from BOND.md and MEMORY.md
4. **Index maintenance** — run `scripts/manage-index-tools.py {vault} orphans` to check consistency
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
