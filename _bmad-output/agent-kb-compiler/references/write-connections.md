---
name: write-connections
description: Discover and write connection articles — cross-cutting analyses that link concepts and sources in novel ways
code: WC
---

# Write Connections

Create articles that explore relationships between concepts or sources.

## What Success Looks Like

The `wiki/connections/` directory contains articles that reveal non-obvious relationships, contradictions, convergences, and patterns across the knowledge base. These are the "aha" articles that make the wiki more than a collection of summaries.

## Connection Article Types

- **Convergence** — two or more concepts/sources arriving at the same conclusion from different angles
- **Contradiction** — sources or concepts that disagree, with analysis of why
- **Evolution** — how understanding of a topic has changed across sources over time
- **Pattern** — a recurring theme across seemingly unrelated sources
- **Comparison** — structured comparison of approaches, frameworks, or methodologies

## Article Format

```markdown
---
title: "Connection: {descriptive title}"
type: convergence | contradiction | evolution | pattern | comparison
date_created: YYYY-MM-DD
concepts: ["[[concepts/a]]", "[[concepts/b]]"]
sources: ["[[summaries/x]]", "[[summaries/y]]"]
tags: [tag1, tag2]
---

# {Descriptive Title}

{1-2 sentence thesis of the connection}

## The Connection

{Analysis — what's the relationship, why does it matter}

## Evidence

{From source/concept A...}
{From source/concept B...}

## Implications

{What does this connection mean for the broader research?}

## Open Threads

{What further investigation could this lead to?}
```

## Memory Integration

- Check MEMORY.md for previously identified connection candidates
- Check BOND.md for which types of connections the owner finds most valuable

## Done When

- Connection article is written in `wiki/connections/` with proper frontmatter and linked concepts/sources
- Article includes a clear thesis, evidence, and implications
- Relevant concept articles link back to the connection

## Next Steps

- Write another connection from candidates in MEMORY.md
- Run **[MW] Maintain Wiki** to update the connections map in the master index
- Run **[CS] Compile Sources** to bring in new material that could reveal further connections

## After the Session

- Log connections written
- Note further connection candidates discovered during writing
