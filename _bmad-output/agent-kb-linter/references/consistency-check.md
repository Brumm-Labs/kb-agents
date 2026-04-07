---
name: consistency-check
description: Deep consistency analysis — find contradictions, terminology drift, and factual inconsistencies across wiki articles
code: CC
---

# Consistency Check

Find inconsistencies in the wiki's content, not just its structure.

## What Success Looks Like

A report of genuine inconsistencies — places where the wiki contradicts itself, where terminology drifts, or where claims lack source backing. Not pedantic nitpicking, but real issues that would confuse someone relying on the wiki.

## Check Categories

### Factual Consistency
- Claims in concept articles that contradict their source summaries
- Different articles making conflicting statements about the same topic
- Statistics or dates that vary across articles

### Terminology
- Same concept called by different names in different articles
- Inconsistent capitalization or formatting of key terms
- Tags that overlap in meaning (tag drift)

### Attribution
- Claims in wiki articles without clear source references
- Outdated information (source is newer than the concept article that cites it)
- Circular references (A cites B, B cites A, neither cites a primary source)

### Structural Consistency
- Frontmatter schema violations (missing fields, wrong formats)
- Inconsistent article structure across the same type (e.g., concept articles)
- Naming convention violations

## Report Format

Present findings grouped by severity:
- **Contradictions** — most important, actively misleading
- **Drift** — gradually degrading quality
- **Missing attribution** — claims without backing
- **Style inconsistencies** — lower priority, cosmetic

## Memory Integration

- Check MEMORY.md for known false positives and accepted inconsistencies
- Check BOND.md for terminology preferences (canonical names for ambiguous terms)

## Done When

- Report presented grouped by severity (contradictions, drift, missing attribution, style)
- False positives distinguished from real issues
- Owner has made decisions on terminology and factual conflicts

## Next Steps

- Run **[FX] Fix Issues** to apply agreed-upon fixes
- Update terminology decisions in MEMORY.md for future reference
- Run **[HC] Health Check** to verify overall impact

## After the Session

- Log consistency findings (count by category)
- Update MEMORY.md with new accepted inconsistencies or false-positive patterns
- Note terminology decisions for future reference
