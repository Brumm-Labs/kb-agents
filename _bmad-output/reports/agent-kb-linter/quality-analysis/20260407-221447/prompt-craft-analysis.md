# Prompt Craft Analysis — agent-kb-linter

**Scanner:** PromptCraftBot v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent (bootloader)

---

## Assessment

Inspector is a memory agent with a correctly lean bootloader (~39 lines, 670 tokens) and seven tight reference files totaling ~4,107 tokens across all prompts. Zero waste patterns, back-references, or wall-of-text blocks were detected by the pre-pass. The craft is clean, outcome-focused, and largely free of the common anti-patterns. The main concern is the complete absence of progression conditions across all seven files and the near-absence of config headers — both are addressable. The agent's persona voice is consistent, actionable, and well-suited to its analytical role.

**Skill type:** Domain expert / audit companion. Should lean toward outcome + domain context (which it does).

---

## Prompt Health Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Total prompts scanned | 7 | In `references/` |
| Prompts with config header | 1 (first-breath.md only) | Per memory agent spec, not high severity |
| Prompts with progression conditions | 0 | Actionable gap — see Key Findings |
| Waste patterns detected | 0 | Clean |
| Back-references detected | 0 | Self-contained |
| Wall-of-text blocks | 0 | Well structured |
| Total token estimate | 4,107 | Lean and appropriate |

---

## SKILL.md Craft

The bootloader is intentionally minimal — this is correct architecture, not over-optimization.

- **Identity seed (lines 6–8):** "A sharp-eyed quality auditor who cares about knowledge integrity. You systematically examine the wiki for inconsistencies, broken links, orphaned content, missing backlinks, and gaps in coverage. You're not nitpicky for its own sake — you focus on issues that actually affect the usefulness of the knowledge base. You deliver findings clearly, prioritize what matters, and suggest actionable fixes."

  This is an excellent identity seed. It's evocative, behavior-priming, and operationally specific. It establishes the "pragmatic, not pedantic" stance in a single paragraph — a key behavioral differentiator that will shape how the agent handles borderline findings.

- **No Overview section:** Correct by design. No flag.
- **Mission:** Domain-specific and earned. "Keep the knowledge base honest. Find the broken links before they mislead, the inconsistencies before they confuse, and the gaps before they become blind spots." Strong mission framing.
- **On Activation:** Three-path routing is clean and complete. Config loading instruction is present.
- **Section count:** 4 sections, 18 content lines. Within correct bootloader bounds.

---

## Per-Capability Craft

### `references/health-check.md` (72 lines, 661 tokens) — STRONG

Outcome-focused throughout. "A clear, prioritized report showing the current state... The owner can scan it in 2 minutes and know exactly what to fix" — this is a quality bar, not a procedure. Check categories are domain-appropriate (structural integrity, content quality, coverage). The inline report format template is load-bearing — it specifies the exact output contract, which is valuable for a capability that produces a structured artifact. Memory Integration and After the Session sections are present and specific. Voice matches the bootloader's pragmatic-auditor persona.

**No significant craft issues.** The inline report format block is 21 fenced lines — borderline for extraction to a reference file, but given it's the canonical output template, keeping it inline is defensible.

### `references/consistency-check.md` (55 lines, 503 tokens) — STRONG

Clear outcome ("genuine inconsistencies — places where the wiki contradicts itself"). Check categories are well-defined and domain-specific (factual, terminology, attribution, structural). Report format guidance is appropriately brief — severity tiers, not a full template. Memory Integration references BOND.md for terminology preferences, which is a nice contextual hook. After the Session section is specific. Persona voice consistent.

### `references/fix-issues.md` (44 lines, 366 tokens) — STRONG

The three-tier fix taxonomy (auto-fixable / needs confirmation / needs owner decision) is the strongest craft element in the capability set. This directly operationalizes the "not pedantic" principle from the identity seed — it gives the agent a decision framework rather than requiring it to ask every time. Memory Integration correctly directs to BOND.md for auto-fix preferences. After the Session is minimal but sufficient.

### `references/suggest-articles.md` (48 lines, 501 tokens) — STRONG

Four suggestion types (New Concept, New Connection, Coverage Improvements, Gap Analysis) are distinct and well-differentiated. The gap analysis section referencing BOND.md for research priorities is a good memory integration touch. After the Session correctly tracks accepted/dismissed suggestions — feeding future false-positive avoidance. Voice consistent.

### `references/first-breath.md` (85 lines, 717 tokens) — GOOD

Configuration-style First Breath. Discovery questions are domain-specific and well-organized across four territory areas (knowledge base, quality priorities, workflow, tolerance). Save As You Go and Urgency Detection present. The sanctum file destinations table is a strong closing element — it makes the First Breath feel purposeful rather than just a conversation. The "Wrapping Up the Birthday" section follows standard ceremony well.

**Minor gap:** No explicit pacing guidance ("we'll explore these over time" or "ask one area at a time"). Risk: First Breath becomes an interrogation. Low severity given the configuration-style approach already implies structure.

### `references/capability-authoring.md` (35 lines, 224 tokens) — ADEQUATE

A lean meta-capability guide. Serves its purpose as a reference for creating new capabilities. The four capability types (Prompt, Script, Multi-file, External Skill Reference) are the right taxonomy. The four-step creation flow is correct at this level of abstraction.

**Note:** This is a support reference, not an operational capability. Absence of Memory Integration and After the Session sections is appropriate — this capability isn't repeated regularly enough to generate session-log-worthy insights.

### `references/memory-guidance.md` (62 lines, 465 tokens) — STRONG

Well-crafted memory philosophy. The "What to Remember / What NOT to Remember" contrast is explicit and useful — it prevents MEMORY.md from bloating with per-session scan results. The two-tier memory architecture (session logs → curated MEMORY.md) is clearly explained with a concrete session log template. Token Discipline section (keep under 200 lines) is a good operational constraint.

---

## Key Findings

### [High] Zero progression conditions across all 7 capability files

**Files:** All `references/*.md` (health-check.md:72, consistency-check.md:55, fix-issues.md:44, suggest-articles.md:48, first-breath.md:85, capability-authoring.md:35, memory-guidance.md:62)

Operational capabilities (HC, FX, SA, CC) all describe what to do but none define when they're done or how to transition. For fix-issues.md especially, where the agent distinguishes auto-fixable from needs-confirmation items, there's no explicit point where the capability concludes — no "when all items are resolved or deferred, summarize changes and return to standby."

**Why it matters:** Without a completion signal, capabilities can drift — the agent may keep offering to do more work after the task is finished, or terminate abruptly without a final summary.

**Fix:** Add a brief "Done When" or "Completing" section to each operational capability. Example for health-check.md: "When the report is presented and any immediate questions answered, ask: 'Anything you'd like me to dig into further, or shall we move to fixes?'"

### [Medium] No config headers on 6 of 7 files

**Files:** All `references/*.md` except `first-breath.md`

Per the memory agent spec, this is not high severity (agent gets language from BOND.md at rebirth). However, first-breath.md correctly includes `{communication_language}` — the other operational capabilities should follow suit for the case where a capability is loaded fresh without full rebirth context.

**Fix:** Add `**Language:** Use {communication_language} for all responses.` near the top of health-check.md, consistency-check.md, fix-issues.md, and suggest-articles.md.

### [Low] health-check.md inline report template could move to a reference

**File:** `references/health-check.md`, lines 37–59 (21 lines, fenced block)

The inline markdown template is load-bearing but sizeable. If the report format evolves, it requires editing the capability prompt rather than a separate reference file. At current size (661 tokens) this is not a problem, but worth noting for maintenance.

**Fix:** Optional — extract to `references/health-check-report-format.md` and reference it from health-check.md.

---

## Strengths

- **Zero detected waste patterns** — no defensive padding, meta-explanation, or conversational filler anywhere in the prompt set. Every token earns its place.
- **Identity seed quality** — one of the better bootloader seeds reviewed. "Not nitpicky for its own sake" is behavioral guidance, not just description.
- **fix-issues.md three-tier taxonomy** — genuinely load-bearing intelligence placement. The auto-fixable / needs-confirmation / needs-decision split prevents over-asking.
- **Mission specificity** — "Find the broken links before they mislead, the inconsistencies before they confuse, and the gaps before they become blind spots" — this is an evocative, specific mission that shapes judgment calls.
- **Memory integration consistency** — HC, FX, SA, CC all correctly reference both MEMORY.md (false positives) and BOND.md (owner preferences). This is the right pattern.
- **Self-containment** — no back-references to "as described above" or "see overview." All capability files work independently.
