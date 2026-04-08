# Agent Cohesion Analysis — agent-kb-linter

**Scanner:** CohesionBot v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent

---

## Assessment

Inspector is a coherent, purposeful agent whose persona, capabilities, and domain all fit together naturally. The "sharp-eyed quality auditor who's not nitpicky for its own sake" identity is directly expressed in every capability — especially in fix-issues.md's three-tier taxonomy (auto-fix / confirm / decide) which operationalizes the pragmatic-not-pedantic stance. The capability set covers the core wiki maintenance lifecycle well. A few meaningful gaps exist, primarily around source ingestion/compilation and search/query capabilities that a quality-focused KB agent might reasonably have.

---

## Cohesion Dimensions

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona-capability alignment | Strong | Every capability reflects the analytical, pragmatic auditor identity |
| Identity consistency across files | Strong | Bootloader seed, CREED values, PERSONA template all reinforce the same character |
| Capability completeness | Moderate | Core audit loop is complete; content creation and search absent |
| Redundancy | Strong | No overlapping capabilities; each serves a distinct purpose |
| External skill integration | Moderate | capability-authoring.md mentions "External Skill Reference" type but no integrations defined |
| Capability granularity | Strong | Four capabilities at the right level — not too atomic, not too broad |
| User journey coherence | Moderate | Full audit loop works; no entry point for proactive browsing or search |

---

## Per-Capability Cohesion

### [HC] Health Check — Strong fit
A quality auditor's primary tool. This is the most natural capability for the persona — systematic, comprehensive, report-focused. The coverage check categories (structural integrity, content quality, coverage) match exactly what "keeping a knowledge base honest" requires. The "2-minute scan" success criterion matches the pragmatic persona.

### [FX] Fix Issues — Strong fit
Directly enables the auditor to do more than report — it acts. The three-tier taxonomy is especially coherent with the persona: auto-fix the obvious, confirm the consequential, escalate the ambiguous. A quality auditor who can only report but not fix would feel incomplete.

### [SA] Suggest Articles — Good fit, slight persona stretch
Suggest Articles is forward-looking rather than reactive, which is a mild stretch from the "find what's broken" framing of the bootloader. However, the CREED's "Surprise and Delight" standing order explicitly calls for noticing positive patterns and opportunities — so this capability is justified. The gap analysis sub-type (referencing BOND.md for owner interests) makes it feel earned rather than bolted on.

### [CC] Consistency Check — Strong fit
Deep consistency analysis is what separates a true knowledge quality tool from a superficial link checker. This capability reflects the "inspect what the wiki says, not just how it's connected" dimension of quality. Factual consistency and attribution checking are sophisticated checks that fit an agent with genuine domain expertise.

### capability-authoring — Meta-capability, coherent
Teaching the agent new tricks is a natural extension of the memory agent pattern. The four capability types (prompt/script/multi-file/external) are well-scoped. This capability makes Inspector feel like a living tool rather than a fixed utility.

### memory-guidance — Infrastructure, not a user-facing capability
Correctly scoped as a support reference. Its inclusion makes the agent's memory discipline explicit and auditable. Coherent.

### first-breath — Strong configuration experience
Domain-specific discovery questions across four territories (KB characteristics, quality priorities, workflow, tolerance). The vault path and maturity questions are particularly important — they calibrate the agent's sensitivity before the first health check. Birthday ceremony present.

---

## Key Findings

### [Medium] No search or query capability
Inspector can audit the wiki, fix issues, and suggest new articles — but it cannot answer the question "what does my wiki say about X?" A knowledge base inspector who can't query the knowledge base is missing an obvious companion capability.

**Suggestion:** Add a `[QR] Quick Reference` or `[SR] Search` capability — "Find what the wiki says about a topic, surface related articles, and note coverage quality." This would make Inspector useful in everyday browsing, not just dedicated audit sessions.

### [Medium] No source ingestion / compilation workflow
The health-check looks for "uncompiled sources" (raw sources not summarized), but Inspector has no capability to actually compile them. A user who sees "23 uncompiled sources" in a health check report must switch agents or do it manually.

**Suggestion:** Add a `[CI] Compile/Ingest` capability — "Summarize a raw source into the wiki format and link it to relevant concepts." This would close the audit-to-action loop for the most common type of KB debt.

### [Low] Suggest Articles doesn't offer to draft the suggested articles
The suggest-articles capability identifies article opportunities but stops at the list. A natural follow-on is "want me to draft the skeleton for this article?" — creating a two-step flow (suggest → draft) that keeps the owner in Inspector for longer.

**Suggestion:** Add a brief section to suggest-articles.md: "After presenting suggestions, offer to draft a skeleton for any accepted suggestion before closing the session."

### [Suggestion] Trend dashboard as a reporting capability
Inspector accumulates health check results in MEMORY.md for trend comparison. A dedicated `[TD] Trend Dashboard` capability that visualizes quality trends over time ("the wiki had 47 issues in January, 23 in February, 12 today") would surface the value of the memory system and make quality progress visible.

### [Suggestion] Bulk frontmatter audit
The health-check includes frontmatter completeness checks, but a dedicated `[FM] Frontmatter Audit` capability with configurable schemas (e.g., "all source files must have: author, date, tags, status") would give power users fine-grained control over what "correct" frontmatter looks like — and could be driven by a script pre-pass rather than pure LLM scanning.

---

## Strengths

- **Tight audit loop:** HC → FX → SA → CC covers the complete quality management lifecycle without redundancy.
- **Pragmatic persona fully expressed:** Every capability reflects the "not nitpicky for its own sake" stance. No capability feels like it was added to pad the feature list.
- **Memory as competitive advantage:** The false-positive learning loop (MEMORY.md + BOND.md) is what distinguishes Inspector from a one-shot linter — and every capability correctly feeds into it.
- **Graduated autonomy:** The auto-fix / confirm / decide taxonomy in fix-issues.md is a genuinely coherent design choice. It respects owner autonomy while enabling real action.

---

## Creative Suggestions

1. **"Inspector Mode" for new articles:** When the owner is writing a new article, Inspector could be invoked mid-draft to check it against existing content for contradictions, orphan status, and missing backlinks — before the article is finalized.

2. **Wiki health certificate:** After a clean health check, Inspector issues a "Knowledge Base Certified" summary with a date stamp — something the owner can use to signal to themselves that the KB is trustworthy as of a specific moment.

3. **Contradiction tracker:** A living list in MEMORY.md of known contradictions the owner has accepted (vs. ones they plan to resolve). This turns inconsistency from a shame metric into an explicit backlog — more honest and more actionable.
