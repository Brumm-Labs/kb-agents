# Knowledge Base

This is a knowledge base vault managed by KB Agents.

## Vault Structure

- `raw/` — Raw source files (articles, papers, images). Drop files here for ingestion.
  - `raw/_source-index.md` — Auto-maintained index of all ingested sources
- `wiki/` — Compiled knowledge (managed by the Compiler agent)
  - `wiki/_index.md` — Master index with all concepts, summaries, and stats
  - `wiki/summaries/` — Source summaries with `[[wiki-links]]`
  - `wiki/concepts/` — Concept articles (stub → draft → mature)
  - `wiki/connections/` — Relationship documents between concepts
- `outputs/` — Generated reports, query results
- `_bmad/memory/` — Agent memory (Sanctums). Do not edit manually.

## Agents

Three agents are installed as Claude Code skills in `.claude/skills/`:

| Agent | What to say | What it does |
|-------|------------|-------------|
| **Archivist** (Ingest) | "Scan for new sources" | Finds and normalizes files in `raw/` |
| **Cartographer** (Compiler) | "Compile the new sources" | Creates summaries, concepts, and connections in `wiki/` |
| **Inspector** (Linter) | "Health check" | Audits quality, finds broken links, suggests improvements |

## Common Commands

- "Scan for new sources" — Ingest agent auto-discovers new files in `raw/`
- "Compile the new sources" — Compiler processes uncompiled sources into wiki
- "Health check" — Linter audits the entire knowledge base
- "What do my sources say about X?" — Query the wiki on any topic
- "Index stats" — Show counts by type, tag frequency, status
