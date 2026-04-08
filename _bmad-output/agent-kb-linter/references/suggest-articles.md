---
name: suggest-articles
description: Analyze the wiki for new article opportunities — concept candidates, connection ideas, and coverage improvements
code: SA
---

# Suggest Articles

Proactively find opportunities to grow and improve the wiki.

## What Success Looks Like

A curated list of article suggestions, each with a clear rationale. Not a dump of everything that could exist — a focused set of articles that would genuinely improve the knowledge base, ranked by impact.

## Suggestion Types

### New Concept Articles
- Tags that appear in 3+ sources but have no concept article
- Topics frequently mentioned across sources but never explicitly defined
- Sub-concepts that deserve their own article (splitting an overly broad concept)

### New Connection Articles
- Sources that contradict each other on the same topic
- Concepts from different domains that converge on similar conclusions
- Temporal patterns — how understanding of a topic evolved across sources
- Surprising overlaps between seemingly unrelated areas

### Coverage Improvements
- Concept articles that are stubs but have enough sources to be fleshed out
- Summaries that are too brief given the richness of the source material
- Areas where a visual (diagram, comparison table) would add clarity

### Gap Analysis
- Topics the owner seems interested in (from tags and BOND.md) but with thin coverage
- Questions raised in connection articles that lack answers in the wiki
- External references in sources that could be ingested to strengthen coverage

## Memory Integration

- Check MEMORY.md for previously suggested articles (avoid repeating dismissed suggestions)
- Check BOND.md for the owner's research priorities — weight suggestions toward their interests
- Cross-reference with the concept inventory for gap detection

## Draft Offer

For accepted suggestions, offer to create a starter stub:
- For concept articles: create a stub with frontmatter, empty sections, and source references
- For connection articles: create a starter with the thesis and linked concepts
- Save stubs to `wiki/concepts/` or `wiki/connections/` so the Compiler can flesh them out

## Done When

- Ranked suggestions presented with clear rationale for each
- Owner has responded to each suggestion (accepted, deferred, dismissed)
- Accepted suggestions have starter stubs (if owner wants them) or are ready for Compiler handoff

## Next Steps

- Hand off accepted suggestions to the Wiki Compiler for drafting
- Run **[HC] Health Check** to assess overall wiki health
- Update MEMORY.md queued-suggestions list with accepted items

## After the Session

- Log suggestions presented and owner's response (accepted, deferred, dismissed)
- Update MEMORY.md: add accepted suggestions to a "queued articles" list, mark dismissed topics
