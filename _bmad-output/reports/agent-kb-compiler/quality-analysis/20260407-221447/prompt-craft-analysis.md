# Prompt Craft Analysis — agent-kb-compiler

## Assessment

**Agent type:** Memory agent bootloader (Cartographer — Knowledge Base Wiki Compiler)

The bootloader SKILL.md is intentionally lean at 39 lines / ~687 tokens — correct architecture, not under-optimization. The identity seed is evocative and sets a distinctive persona. Capability prompts in `references/` are well-crafted: outcome-focused, appropriately structured with "What Success Looks Like" sections, and consistently include Memory Integration and After Session hooks. No waste patterns, back-references, or wall-of-text blocks detected across all 8 files (~4,470 tokens total). The craft is solid throughout.

## Prompt Health Summary

| Metric | Count | Notes |
|--------|-------|-------|
| Total prompts scanned | 7 | In `references/` |
| With config header | 1 | `first-breath.md` only — correct for memory agent |
| With progression conditions | 0 | None flagged — see notes below |
| Waste patterns | 0 | Clean across all files |
| Back-references | 0 | All prompts self-contained |
| Suggestive loading | 0 | All references are mandatory |
| Wall-of-text blocks | 0 | Good structure throughout |
| Total token estimate | ~4,470 | Lean for 8 files |

**On progression conditions:** The pre-pass flags 7 files for missing progression keywords. For memory agent capability references, this is expected — these are loaded on-demand per capability, not chained sequentially. The concern would be in `first-breath.md` (98 lines), which runs as a long interactive conversation without explicit progression gates. This is a real craft observation — see Key Findings.

## SKILL.md Craft

The bootloader identity seed: *"A master synthesizer who sees the forest in the trees. You take a collection of indexed raw sources and weave them into a coherent, navigable wiki. You identify concepts that span multiple sources, write clear summaries, maintain a web of Obsidian `[[wiki-links]]`, and keep the knowledge structure growing organically. You think in connections — every new source is an opportunity to strengthen the web of understanding."*

This is strong seed text. It is specific to the domain, uses vivid language ("weave," "web," "forest in the trees"), and gives the agent a clear epistemic stance ("thinks in connections"). The three-sentence structure is appropriate. No formal Overview, Identity, Communication Style, or Principles sections — correct for bootloader architecture.

Mission statement in On Activation is clear and domain-specific. The three-path activation routing (First Breath → headless → rebirth) is correctly ordered and self-explanatory.

## Per-Capability Craft

### compile-sources.md (67 lines, ~528 tokens, code: CS)

**Verdict: Well-crafted.** Outcome-focused with a clear "What Success Looks Like" section. The Approach section gives numbered steps, which is appropriate here — this is a workflow capability where ordering matters (read index → read source → write summary → update index). The Summary Format is a template block, which is load-bearing domain knowledge (the agent needs to know the exact YAML frontmatter fields). Memory Integration and After Session are brief and appropriate.

One observation: the Approach section lists 6 numbered steps inline. This works for this capability's scope, but if the compilation workflow grows more complex (e.g., handling different source types differently), this should be extracted.

### manage-concepts.md (80 lines, ~562 tokens, code: MC)

**Verdict: Well-crafted.** The Concept Article Format is a full template block — appropriate load-bearing domain knowledge (YAML fields, section structure). The Operations section is a clean list of named operations (Create, Update, Promote, Merge, Split, Inventory) with one-line descriptions — excellent capability granularity. Memory Integration and After Session are present and specific.

The concept article template makes up ~40 lines of the 80 — this is not waste, it is the agent's production format specification.

### maintain-wiki.md (63 lines, ~399 tokens, code: MW)

**Verdict: Well-crafted.** The Master Index section provides the exact template structure the agent needs to produce — this is correct intelligence placement. Operations are clearly named. Memory Integration and After Session are tight.

Minor observation: the `{Category 1}` and `{Category 2}` placeholders in the master index template (lines 26-31) are template artifacts that will appear in the agent's working memory. These are intentional (the actual categories emerge during First Breath), but they could confuse the agent when it runs "Maintain Wiki" before categories have been named. Consider adding a note: "Replace `{Category 1}` etc. with actual category names from BOND.md."

### write-connections.md (66 lines, ~476 tokens, code: WC)

**Verdict: Well-crafted.** The Connection Article Types taxonomy (Convergence, Contradiction, Evolution, Pattern, Comparison) is excellent domain knowledge — it gives the agent a framework for classification that goes beyond generic summarization. The article format template is appropriately specific. Memory Integration points to MEMORY.md for connection candidates (correct — this is where the agent pre-stages ideas).

### first-breath.md (98 lines, ~1,069 tokens)

**Verdict: Good but could be more resilient.** The file has the right sections and the right tone — warm, conversational, with clear urgency detection and a "Save As You Go" discipline. The Questions to Explore section is well-organized into four thematic groups (Knowledge Base, Wiki Preferences, Writing Style, Workflow).

Craft concern: the file is 98 lines with no internal progression guidance. A First Breath conversation that covers all four question groups plus identity, capabilities, tools, and birthday ceremony could easily span 30-50 user turns. The agent has no internal signal for when to transition from discovery to wrapping up. The "Wrapping Up the Birthday" section exists but is only reachable if the agent gets there — there's no "if you've covered 3 of 4 areas, you can proceed" condition.

### memory-guidance.md (62 lines, ~485 tokens)

**Verdict: Correct architecture, appropriate scope.** This is a discipline reference loaded at session close, not a user-facing capability. It correctly explains what to remember, what not to, the two-tier session log → MEMORY.md flow, and a token discipline ceiling (200 lines for MEMORY.md). This is load-bearing operational knowledge, not waste.

Minor observation: the file has a template artifact — `## Session — {time or context}` appears as a section header inside the session log format example (line 34). This is inside a prose explanation block, so it shouldn't confuse the agent, but it looks like a section header from the pre-pass. Low risk.

### capability-authoring.md (42 lines, ~264 tokens)

**Verdict: Appropriate lean reference.** This guides the agent through co-creating new capabilities with the owner. It's intentionally instructional (how to create a capability) rather than outcome-focused. The Prompt File Format section gives the exact YAML frontmatter needed — this is domain knowledge, not over-specification. The script note ("Python preferred. Accept sanctum path as argument. Never hardcode paths.") is a principle, not a procedure.

Voice assessment: slightly more instructional/technical than the agent's warm synthesizer persona. Acceptable for a meta-capability that the agent and owner use together.

## Key Findings

**[Medium] first-breath.md — No progression conditions for a long interactive flow**
The file is 98 lines covering a multi-stage discovery conversation with no internal completion signals. The agent may compress discovery questions, rush to wrap up, or over-extend the conversation without knowing when it has "enough."
Fix: Add a soft gate after the four question groups: "Once you have a sense of their domain, preferences, style, and workflow — even if incomplete — move toward identity and wrapping up. Incomplete answers now get completed through working together."

**[Medium] maintain-wiki.md:26-31 — Template placeholder artifacts in working index format**
The `{Category 1}` and `{Category 2}` in the master index template are correct for initial setup but are never replaced — the actual categories emerge from BOND.md. This could confuse the agent when regenerating the index.
Fix: Add an inline note: "Replace placeholder category names with actual categories from BOND.md."

**[Low] capability-authoring.md — Voice slightly clinical for Cartographer's persona**
The file reads more like a technical spec than something the Cartographer would naturally say. The synthesizer persona is warm and intellectually curious — this file is terse and procedural.
Fix: Soften the opening. Instead of "When your owner wants you to learn a new ability, you create a capability together," try something like "Learning new abilities is collaborative — you and your owner design them together. Here's how."

**[Note] config headers absent from capability references — correct for memory agents**
The pre-pass flags 6 of 7 files for missing config headers. Memory agents receive language from BOND.md during rebirth. Only `first-breath.md` needs a config header (it runs before a sanctum exists), and it has one. No action needed.

## Strengths

- Zero waste patterns across all 8 files — no defensive padding, no meta-explanation, no filler
- Capability prompts are outcome-focused, not procedural — "What Success Looks Like" is the primary frame
- Memory Integration sections are specific and actionable (check BOND.md for style, check MEMORY.md for concept inventory)
- Article format templates are load-bearing domain knowledge, not over-specification
- `memory-guidance.md` is a lean, precise discipline reference — exactly what it needs to be
- The identity seed is the strongest element in the entire agent — specific, evocative, and domain-grounded
