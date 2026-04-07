---
name: maintain-wiki
description: Maintain wiki structure — update the master index, manage backlinks, ensure structural integrity
code: MW
---

# Maintain Wiki

Keep the wiki structurally sound and navigable.

## What Success Looks Like

The master index at `wiki/_index.md` is complete and current. All `[[wiki-links]]` resolve to real files. Backlinks are bidirectional. The wiki hierarchy makes sense and is easy to navigate in Obsidian.

## The Master Index

`wiki/_index.md` is the entry point to the knowledge base:

```markdown
# {Knowledge Base Name}

_Last updated: YYYY-MM-DD | {X} concepts | {Y} summaries | {Z} sources_

## Concepts

### {Category 1}
- [[concepts/concept-a]] — {one-line description}
- [[concepts/concept-b]] — {one-line description}

### {Category 2}
- ...

## Recent Additions

- YYYY-MM-DD: [[summaries/new-source]] — {title}
- ...

## Connections Map

_Key relationships between concepts._

- [[concept-a]] ↔ [[concept-b]]: {relationship}
- ...
```

## Operations

- **Check links** — run `scripts/wiki-tools.py {vault} check-links` to find broken links and orphans, then interpret results
- **List uncompiled** — run `scripts/wiki-tools.py {vault} uncompiled` to find sources needing compilation
- **Concept inventory** — run `scripts/wiki-tools.py {vault} inventory` to get current concept status
- **Rebuild index** — scan all wiki files and regenerate `_index.md`
- **Update backlinks** — ensure every link has a reciprocal reference
- **Reorganize** — restructure categories in the index based on how concepts cluster

For Check links, List uncompiled, and Concept inventory: use the script for the deterministic scan, then interpret and present results to the owner.

## Memory Integration

- Check BOND.md for preferred index organization (flat vs. categorized)
- Check MEMORY.md for category structure decisions

## Done When

- Master index (`wiki/_index.md`) is complete, current, and accurate
- All `[[wiki-links]]` resolve to real files with no broken links or orphans
- Backlinks are bidirectional and category structure is coherent

## Next Steps

- Run **[CS] Compile Sources** to process pending raw sources
- Run **[WC] Write Connections** to fill gaps in the connections map
- Hand off to the Wiki Linter for a full health check

## After the Session

- Log maintenance performed
- Note any structural issues found and fixed
