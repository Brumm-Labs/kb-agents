# Workflow

How to use the KB agents day-to-day, from ingesting sources to maintaining quality.

## Daily: Ingest New Sources

The most common workflow is dropping files and letting the Ingest agent handle them.

### 1. Drop Files

Put your sources into `raw/`:
- Articles → `raw/articles/`
- Papers → `raw/papers/`
- Images/diagrams → `raw/images/`

**Tip:** Use the [Obsidian Web Clipper](https://obsidian.md/clipper) to save articles directly into `raw/articles/`.

### 2. Auto-Discover `[AD]`

Start the Ingest Agent. It scans `raw/` automatically and finds everything new:

```
You: (activate Ingest Agent)
Agent: "Found 3 new files in raw/. Processing them now."
```

Each file gets YAML frontmatter with title, author, tags, and status.

### 3. Manual Ingest `[IN]`

For specific sources:
- **URL:** "Ingest https://example.com/article"
- **Paste:** Paste text directly into the chat
- **Image:** "Ingest `raw/images/diagram.png`" (creates a description file)

### 4. Batch Import `[BI]`

For a whole folder at once:

```
"Batch-ingest everything in raw/articles/new/"
```

## Daily: Compile Wiki

After ingesting, the Compiler agent turns raw sources into structured knowledge.

### Compile Sources `[CS]`

```
You: "Compile the new sources"
```

The agent:
1. Finds all sources with `status: raw` or `summarized`
2. Creates summaries in `wiki/summaries/` with `[[wiki-links]]` to concepts
3. Updates the source status to `compiled`
4. Updates `wiki/_index.md`

### Manage Concepts `[MC]`

| Command | What happens |
|---------|-------------|
| "Create a concept article about Transformers" | New article in `wiki/concepts/` |
| "Update the article on Attention Mechanisms" | Enriched with new sources |
| "Promote all stubs with 3+ sources" | Stub → draft lifecycle |
| "Concept inventory" | Overview of all concepts with status |

Concepts follow a lifecycle: `stub` → `draft` → `mature`

### Write Connections `[WC]`

"Write a connection between Transformers and CNNs"

Connection types:
- **Convergence** — different approaches, same conclusion
- **Contradiction** — sources disagree
- **Evolution** — how understanding changed over time
- **Pattern** — recurring theme across unrelated sources
- **Comparison** — structured comparison of approaches

### Query Your Wiki `[QW]`

"What do my sources say about Scaling Laws?"

Output formats:
- **Inline** (default) — answer in chat with `[[wiki-links]]`
- **Markdown** — save to `outputs/`
- **Table** — structured comparison

## Weekly: Quality Check

### Health Check `[HC]`

Start the Linter agent:

```
"Health Check"
```

It runs a pre-pass script for deterministic checks (broken links, orphans, frontmatter issues), then adds LLM-based analysis on top.

### Fix Issues `[FX]`

"Fix the issues from the health check"

Three levels:
- **Auto-fix** — missing backlinks, index updates (no confirmation needed)
- **Confirmation** — removing broken links, deleting orphans (asks first)
- **Owner decision** — resolving contradictions, choosing categories (shows options)

### Suggest New Articles `[SA]`

"What could improve the wiki?"

The agent finds gaps: tags appearing in 3+ sources without a concept article, contradictions worth documenting, stubs ready for promotion.

## Monthly: Deep Maintenance

### Consistency Check `[CC]`

"Deep consistency check"

Checks for:
- Factual contradictions between articles
- Inconsistent terminology
- Claims without source attribution
- Frontmatter schema violations

### Index Rebuild `[IX]`

"Index rebuild" — regenerates `raw/_source-index.md` from frontmatter. Useful after manual edits.

### Wiki Maintenance `[MW]`

| Command | What happens |
|---------|-------------|
| "Check links" | Find broken `[[wiki-links]]` and orphans |
| "Uncompiled sources" | List sources not yet compiled |
| "Rebuild index" | Regenerate `wiki/_index.md` |

## Routine Summary

| Frequency | What | Agent | Time |
|-----------|------|-------|------|
| Daily | Ingest new sources | Ingest `[AD]` | 2-5 min |
| Daily | Compile sources | Compiler `[CS]` | 10-20 min |
| Weekly | Health check + fix | Linter `[HC]` `[FX]` | 10 min |
| Weekly | Manage concepts | Compiler `[MC]` `[WC]` | 15-20 min |
| Weekly | Suggest articles | Linter `[SA]` | 5 min |
| Monthly | Deep consistency check | Linter `[CC]` | 15-20 min |
| Monthly | Index rebuild + wiki maintenance | Ingest `[IX]`, Compiler `[MW]` | 10 min |
