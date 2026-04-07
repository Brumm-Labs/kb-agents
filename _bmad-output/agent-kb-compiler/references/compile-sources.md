---
name: compile-sources
description: Process new or updated raw sources into wiki summaries — read source, create summary, link to concepts, update index
code: CS
---

# Compile Sources

Take raw sources that haven't been compiled yet and integrate them into the wiki.

## What Success Looks Like

Every uncompiled source in `raw/` gets a corresponding summary in `wiki/summaries/`, linked to relevant concept articles, and marked as `compiled` in the source index. The master wiki index is updated. Obsidian `[[wiki-links]]` connect everything.

## Approach

1. Read the source index (`raw/_source-index.md`) to find sources with `status: raw` or `status: summarized`
2. For each source, read the full content from `raw/`
3. Create or update a summary in `wiki/summaries/` with:
   - YAML frontmatter (title, source_ref, date_compiled, concepts, tags)
   - A concise summary of the key ideas
   - Obsidian `[[wiki-links]]` to relevant concept articles
   - A "Source" backlink to the raw file
4. Identify concepts mentioned — check if concept articles exist, flag new ones
5. Update the source's status to `compiled` in the source index
6. Update `wiki/_index.md` with the new summary entry

## Summary Format

```markdown
---
title: "Summary: {source title}"
source_ref: "[[raw/{path}]]"
date_compiled: YYYY-MM-DD
concepts: ["[[concept-name]]", "[[concept-name]]"]
tags: [inherited from source]
---

# {Source Title}

**Source:** [[raw/{path}]] | **Author:** {author} | **Date:** {date}

{2-4 paragraph summary of key ideas}

## Key Takeaways

- {takeaway 1}
- {takeaway 2}

## Connections

- Related to [[concept-name]]: {how it relates}
- Complements [[summary-other-source]]: {connection}
```

## Memory Integration

- Check BOND.md for preferred summary depth and style
- Check MEMORY.md for the concept inventory — reuse existing concepts before creating new ones
- Reference `wiki/_index.md` to understand existing wiki structure

## Done When

- Every targeted source has a corresponding summary in `wiki/summaries/` with frontmatter and `[[wiki-links]]`
- Source index shows `status: compiled` for all processed sources
- `wiki/_index.md` includes entries for all new summaries

## Next Steps

- Run **[MC] Manage Concepts** to create or update concept articles for newly identified concepts
- Run **[WC] Write Connections** to explore relationships between compiled sources
- Run **[MW] Maintain Wiki** to verify index completeness and link integrity

## After the Session

- Log compiled sources (count, titles)
- Note new concepts identified but not yet articled
- Note interesting connections discovered between sources
