---
name: auto-discover
description: Automatically scan for new files in raw/ that aren't indexed yet — process them all without manual file-by-file input
code: AD
---

# Auto-Discover

Scan the vault for new sources and process them automatically.

## What Success Looks Like

The owner drops files into `raw/` (or its subdirectories) and says "scan for new sources" — or just activates the agent without a specific task. All untracked files are found, ingested with proper frontmatter, and registered in the index. Zero manual file paths needed.

## Approach

1. Run `scripts/scan-new-sources.py {vault}` to get a JSON list of untracked files
2. Present the findings to the owner: "{N} new files found in raw/"
3. For each new file:
   - If it already has frontmatter but isn't indexed → register it in the index
   - If it needs full ingest → apply the Ingest Source `[IN]` capability (normalize, add frontmatter, register)
4. After processing all files, show a summary

## Auto-Mode vs. Review Mode

Check BOND.md for the owner's preference:

- **Auto-mode** (default after trust is established): Process all new files without asking for each one. Show a summary at the end.
- **Review mode**: Show the list of new files first, let the owner select which to process, skip, or handle differently.

If BOND.md doesn't have a preference yet, ask on first use and remember the choice.

## Default Activation Behavior

When the agent is activated and the owner hasn't given a specific task, **auto-discover is the default**. Greet the owner, then immediately scan for new sources:

"Hey Björn! Let me check for new sources... Found 3 new files in raw/. Processing them now."

This makes the agent useful from the first message without requiring explicit commands.

## Memory Integration

- Check BOND.md for auto-mode vs. review-mode preference
- Check MEMORY.md for canonical tags — apply consistent tagging to batch discoveries
- Check the source index to avoid re-processing already-indexed files

## Done When

- All new files are processed (ingested or registered)
- Source index is up to date
- Summary shown to owner with counts and any issues

## Next Steps

- Hand off to the Wiki Compiler to create summaries from new sources
- Run `[IX]` Manage Index for a full health check
- Drop more files and scan again later

## After the Session

- Log the auto-discover results (count found, count processed, any issues)
- Note any new file patterns (e.g., "owner started dropping PDFs, might need PDF extraction tool")
- Update tag list in MEMORY.md if new tags were created
