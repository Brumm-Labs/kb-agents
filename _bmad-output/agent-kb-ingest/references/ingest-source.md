---
name: ingest-source
description: Ingest a new source document into the knowledge base — normalize, extract metadata, add frontmatter, and register in the index
code: IN
---

# Ingest Source

Take a new piece of raw material and prepare it for the knowledge base.

## What Success Looks Like

The source ends up in the correct `raw/` subdirectory as a clean Markdown file with complete YAML frontmatter. The master source index knows about it. Duplicates have been flagged. The owner doesn't have to touch the file afterward.

## Input Modes

The owner may provide sources in several ways:
- A file path to an already-downloaded `.md`, `.pdf`, `.html`, or `.txt` file
- A URL to fetch and convert
- Pasted content directly in the conversation
- A batch of files in a directory to process

Detect the mode and adapt. For URLs, fetch and convert to Markdown. For PDFs, extract text content. For images, describe them and create a reference entry.

## Frontmatter Schema

Every ingested source gets this frontmatter:

```yaml
---
title: "Source title"
author: "Author name(s)"
date_published: YYYY-MM-DD  # or "unknown"
date_ingested: YYYY-MM-DD
source_url: "https://..."  # or "local"
source_type: article | paper | repo | dataset | note | image | video
tags: [tag1, tag2, tag3]
summary: "1-2 sentence summary"
status: raw  # raw → summarized → compiled
related: []  # wiki links to related sources, filled by compiler
---
```

## Memory Integration

- Check BOND.md for preferred tagging conventions and category names
- Check MEMORY.md for established tags — reuse existing tags before inventing new ones
- Reference the source index at `{vault}/raw/_source-index.md` for duplicate detection

## Duplicate Detection

Before ingesting, scan the source index for:
- Same URL
- Very similar title (fuzzy match)
- Same author + similar date + similar topic

If a potential duplicate is found, flag it to the owner with both entries side by side. Don't silently overwrite.

## File Placement

- Articles → `raw/articles/`
- Papers → `raw/papers/`
- Images → `raw/images/` (with a companion `.md` description file)
- Other → `raw/` root or ask the owner

## Connection Spotting

While ingesting, actively scan for connections to existing material:
- Does this source contradict something already in the wiki?
- Does it converge with sources from a different domain?
- Does it introduce a concept not yet covered?

Flag interesting connections in the frontmatter `related: []` field and mention them to the owner. These are gifts for the Wiki Compiler.

## Done When

- Source file is in the correct `raw/` subdirectory with complete YAML frontmatter
- Source is registered in `raw/_source-index.md` with status `raw`
- Duplicate check is clean (or duplicates flagged and resolved with owner)

## Next Steps

- Ingest another source or run **[BI] Batch Ingest** for multiple files
- Hand off to the Wiki Compiler to create summaries from new sources
- Review the canonical tag list in MEMORY.md for consistency

## After the Session

- Log ingested sources in the session log (count, titles, any issues)
- Note any new tags created — these inform future tagging consistency
- Flag sources that seem related to existing wiki concepts
