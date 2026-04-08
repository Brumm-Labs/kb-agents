# Use Cases

Practical scenarios for using KB Agents.

## I Want to Ingest a Web Article

1. Save the article to `raw/articles/` (use Obsidian Web Clipper or download manually)
2. Activate the Ingest Agent — it finds the file automatically via `[AD]`
3. The agent normalizes the content, adds frontmatter (title, author, tags, source URL), and updates the source index

**Or directly via URL:**

```
"Ingest https://example.com/great-article"
```

The agent fetches, normalizes, and catalogs it.

## I Want to Ingest a Research Paper

1. Put the PDF into `raw/papers/`
2. Activate the Ingest Agent
3. The agent extracts metadata, creates a Markdown summary with frontmatter, and indexes it

**Tip:** For large batches (e.g., a conference proceedings folder):

```
"Batch-ingest everything in raw/papers/neurips2025/"
```

## I Want to Compile My Sources Into a Wiki

1. Activate the Compiler Agent
2. Say: "Compile the new sources"
3. The agent finds all uncompiled sources, creates summaries in `wiki/summaries/`, identifies concepts, and weaves `[[wiki-links]]` between them
4. Open Obsidian to see the graph grow

**After initial compilation:**

```
"Create concept articles for the most referenced topics"
"Write connections between related concepts"
```

## I Want to Read and Browse My Knowledge Base

Open the vault in Obsidian:
- `wiki/_index.md` — master index with all concepts and summaries
- `wiki/concepts/` — browse concept articles
- Use Obsidian's **graph view** to see how everything connects
- Click any `[[wiki-link]]` to navigate between articles

## I Want to Research a Topic From My Wiki

Activate the Compiler Agent and use `[QW]`:

```
"What do my sources say about Scaling Laws?"
"Compare the approaches to attention mechanisms across my papers"
"Summarize everything I have on reinforcement learning"
```

The agent searches your wiki and raw sources, then synthesizes an answer with links back to the original sources.

**Save the result:**

```
"Write this as a report to outputs/scaling-laws-summary.md"
```

## I Want to Check Wiki Quality

Activate the Linter Agent:

```
"Health Check"
```

The agent runs structural checks (broken links, orphans, missing frontmatter, stale content) and provides an overall health assessment with prioritized issues.

**Then fix them:**

```
"Fix the issues from the health check"
```

## I Want to Find Gaps in My Research

Activate the Linter Agent:

```
"What articles could improve the wiki?"
```

The agent analyzes tag frequency, source cross-references, and concept coverage to suggest:
- New concept articles for recurring themes
- Connection articles for related topics
- Promotions for stubs with enough sources

## I Want to Manage Multiple Knowledge Bases

Each KB is a separate Obsidian vault with its own agents and memory. Run `kb-init.sh` once per KB:

```bash
./kb-init.sh ~/vaults/ai-safety "AI Safety"
./kb-init.sh ~/vaults/ml-papers "ML Papers"
./kb-init.sh ~/vaults/philosophy "Philosophy"
```

Each vault has independent agents with their own Sanctum (memory). Switch between them by `cd`-ing into the vault directory and running `claude`.

See [Best Practices](best-practices.md#multiple-vaults) for tips on managing multiple KBs.
