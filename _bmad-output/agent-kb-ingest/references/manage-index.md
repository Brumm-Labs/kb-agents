---
name: manage-index
description: View, search, and maintain the source index — find sources, check status, update metadata
code: IX
---

# Manage Source Index

Maintain and query the master source index.

## What Success Looks Like

The source index at `{vault}/raw/_source-index.md` is accurate, up-to-date, and useful for both the owner and the compiler agent. The owner can quickly find sources, check status, and see what's been ingested.

## The Source Index

The source index is a Markdown table that tracks all ingested sources:

```markdown
| Title | Type | Tags | Status | Date Ingested | Path |
|-------|------|------|--------|---------------|------|
```

## Operations

- **Search** — find sources by title, tag, type, date range, or status
- **Status update** — mark sources as `summarized` or `compiled` (typically done by the compiler agent, but can be done manually)
- **Rebuild** — run `scripts/manage-index-tools.py {vault} rebuild` to regenerate the index from frontmatter
- **Stats** — run `scripts/manage-index-tools.py {vault} stats` for counts by type, tag frequency, status distribution
- **Orphan check** — run `scripts/manage-index-tools.py {vault} orphans` to find mismatches between files and index

For Rebuild, Stats, and Orphan check: use the script for the deterministic scan, then interpret and present the results to the owner.

## Memory Integration

- Use MEMORY.md for context about which sources are most important to the owner
- Check BOND.md for preferred sort order or grouping in the index

## Done When

- Requested operation is complete with results displayed to the owner
- Index matches the actual files on disk (no orphans, no missing entries)
- Any inconsistencies found have been resolved or flagged

## Next Steps

- Run a different index operation (search, stats, rebuild)
- Ingest new sources with **[IN] Ingest Source**
- Hand off to the Wiki Compiler if uncompiled sources were found

## After the Session

- Log any index maintenance performed
- Note any orphaned files or inconsistencies found
