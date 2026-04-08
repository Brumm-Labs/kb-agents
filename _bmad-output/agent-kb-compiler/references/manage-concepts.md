---
name: manage-concepts
description: Create, update, and maintain concept articles — the backbone of the wiki's knowledge structure
code: MC
---

# Manage Concepts

Create and maintain concept articles that synthesize knowledge across multiple sources.

## What Success Looks Like

The `wiki/concepts/` directory contains well-written articles for every significant concept in the knowledge base. Each concept article synthesizes what multiple sources say about the topic, links back to those sources, and connects to related concepts. The concept inventory in MEMORY.md stays current.

## Concept Article Format

```markdown
---
title: "Concept Name"
aliases: ["Alternative Name", "Abbreviation"]
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
tags: [tag1, tag2]
sources: ["[[summaries/source-a]]", "[[summaries/source-b]]"]
related: ["[[concepts/related-concept]]"]
status: stub | draft | mature
---

# Concept Name

{1-2 sentence definition}

## Overview

{2-4 paragraphs synthesizing what the sources say about this concept}

## Key Aspects

### {Aspect 1}
{detail with source references}

### {Aspect 2}
{detail with source references}

## Connections

- [[related-concept-1]]: {how they relate}
- [[related-concept-2]]: {how they relate}

## Sources

- [[summaries/source-a]] — {what this source contributes}
- [[summaries/source-b]] — {what this source contributes}

## Open Questions

- {things not yet well-covered by available sources}
```

## Operations

- **Create** — new concept article from identified concept mentions
- **Update** — enrich existing concept with new source material
- **Promote** — move a stub to draft or mature based on coverage
- **Merge** — combine two concept articles that overlap significantly
- **Split** — break a too-broad concept into sub-concepts
- **Inventory** — list all concepts with their status and source count

## Memory Integration

- Maintain concept inventory in MEMORY.md (name, status, source count)
- Check BOND.md for preferred article depth and structure
- Check MEMORY.md for merge/split decisions already made

## Done When

- All requested concept operations (create, update, promote, merge, split) are complete
- Concept inventory in MEMORY.md reflects current state
- Every concept article has bidirectional links to sources and related concepts

## Next Steps

- Run **[CS] Compile Sources** to process pending raw sources that may enrich concepts
- Run **[WC] Write Connections** to articulate cross-cutting relationships
- Run **[MW] Maintain Wiki** to check coverage gaps and verify links

## After the Session

- Log new concepts created and existing ones updated
- Note concepts that need more sources (stubs)
- Flag potential merges or splits for next session
