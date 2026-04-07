---
name: query-wiki
description: Answer questions against the knowledge base — research across wiki articles, synthesize findings, and produce structured outputs
code: QW
---

# Query Wiki

Answer complex questions by researching across the wiki.

## What Success Looks Like

The owner asks a question and receives a well-sourced answer that draws on multiple wiki articles, concept pages, and connection documents. The answer is richer than any single article because it synthesizes across the knowledge web.

## Approach

1. Parse the question to identify relevant concepts, tags, and topics
2. Scan the wiki index and concept inventory (from MEMORY.md) for relevant articles
3. Read the most relevant articles (summaries, concepts, connections)
4. Synthesize an answer that cites sources with `[[wiki-links]]`
5. Present the answer in the owner's preferred format

## Output Formats

The owner may request different output formats:
- **Inline answer** — direct response in the conversation
- **Markdown file** — written to `outputs/` for viewing in Obsidian
- **Slide deck** — Marp-format slides written to `outputs/`
- **Comparison table** — structured comparison of concepts or sources

Default to inline answer unless the owner specifies otherwise.

## Memory Integration

- Check MEMORY.md for the concept inventory to quickly identify relevant articles
- Check BOND.md for preferred answer depth and format
- Reference previous queries in session logs to build on past research

## Done When

- Question answered with citations to wiki sources
- Output delivered in the requested format
- Any gaps in wiki coverage noted for potential new articles

## Next Steps

- File the output into the wiki if it adds value (as a connection or concept article)
- Run **[SA] Suggest Articles** (via Linter) for gaps discovered during research
- Ask another question to deepen understanding

## After the Session

- Log the query and key findings in the session log
- Note any wiki gaps discovered — concepts without articles, missing connections
- If the answer revealed new relationships, flag them as connection candidates
