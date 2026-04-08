---
name: fix-issues
description: Fix identified wiki issues — repair broken links, add missing backlinks, update stale frontmatter, fill gaps
code: FX
---

# Fix Issues

Repair issues identified by the health check or spotted during browsing.

## What Success Looks Like

Identified issues are resolved cleanly. Broken links point to real files. Missing backlinks are added bidirectionally. Stale frontmatter is updated. The owner is informed of every change made.

## Fix Categories

### Auto-fixable (proceed without asking)
- Add missing backlinks (if the forward link exists and target file exists)
- Update `date_updated` frontmatter on modified articles
- Add missing files to `_index.md`
- Fix obvious typos in `[[wiki-links]]` (close matches)

### Needs confirmation
- Remove broken links to non-existent files
- Merge near-duplicate concept articles
- Promote stub concepts to draft
- Delete orphaned files

### Needs owner decision
- Resolve contradictions between sources
- Choose between competing categorizations
- Decide if a gap should be filled or is intentional

## Memory Integration

- Check MEMORY.md for fix patterns — recurring issues might indicate a structural problem
- Check BOND.md for owner's auto-fix preferences (how much autonomy do they want?)

## Done When

- All targeted fixes applied and verified
- Owner informed of every change made, grouped by category
- Owner-decision items flagged separately for review

## Next Steps

- Re-run **[HC] Health Check** to verify fixes and update baseline
- Run **[SA] Suggest Articles** for improvement opportunities
- Review MEMORY.md for recurring issue patterns that suggest structural changes

## After the Session

- Log all fixes applied (count by category)
- Note recurring issues that suggest structural improvements
- Update MEMORY.md if new auto-fix patterns were established
