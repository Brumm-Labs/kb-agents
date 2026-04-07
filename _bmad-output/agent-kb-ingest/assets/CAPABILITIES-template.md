# Capabilities

## Built-in

| Code | Name | Description | Source |
|------|------|-------------|--------|
| [IN] | Ingest Source | Take a single source and normalize it with frontmatter and metadata | `references/ingest-source.md` |
| [BI] | Batch Ingest | Process multiple sources at once from a directory or file list | `references/batch-ingest.md` |
| [IX] | Manage Index | Search, maintain, and report on the source index | `references/manage-index.md` |

## Learned

_Capabilities added by the owner over time. Prompts live in `capabilities/`._

| Code | Name | Description | Source | Added |
|------|------|-------------|--------|-------|

## How to Add a Capability

Tell me "I want you to be able to do X" and we'll create it together.
I'll write the prompt, save it to `capabilities/`, and register it here.
Next session, I'll know how. Load `references/capability-authoring.md` for the full creation framework.

## Tools

Prefer crafting your own tools over depending on external ones. A script you wrote and saved is more reliable than an external API. Use the file system creatively.

### User-Provided Tools

_MCP servers, APIs, or services the owner has made available. Document them here._
