---
name: batch-ingest
description: Process multiple source files at once — scan a directory, normalize all files, and update the source index
code: BI
---

# Batch Ingest

Process multiple sources in one go.

## What Success Looks Like

All files in the given directory (or file list) are ingested with consistent frontmatter, placed in the correct `raw/` subdirectories, and registered in the source index. A summary report shows what was processed, what was skipped (duplicates), and what needs attention.

## Approach

1. Scan the input directory or file list
2. For each file, determine source type from extension and content
3. Apply the same normalization as single ingest (frontmatter, clean Markdown)
4. Check for duplicates against the existing source index
5. Place files in correct subdirectories
6. Update the source index with all new entries
7. Present a summary to the owner

## Memory Integration

- Use MEMORY.md for established tag vocabulary — batch ingests are where tag drift happens most
- Check BOND.md for any batch-specific preferences (e.g., auto-tag by directory name)

## Done When

- All files in the batch are processed with consistent frontmatter and placed in correct subdirectories
- Source index is updated with all new entries
- Summary report shown to owner: X ingested, Y skipped (duplicates), Z need review

## Next Steps

- Review skipped/flagged items and resolve duplicates
- Hand off new sources to the Wiki Compiler for summarization
- Run **[IX] Manage Index** to verify index integrity

## After the Session

- Log the batch summary: X ingested, Y skipped, Z need review
- Note any new patterns in the source material that might inform categorization
