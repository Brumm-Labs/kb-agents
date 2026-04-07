# Sanctum Architecture Analysis — agent-kb-compiler

## Assessment

Cartographer's sanctum architecture is solid and nearly complete. The bootloader is appropriately lean (18 content lines, well within the 40-line target), the Three Laws and Sacred Truth are present and verbatim, the identity seed is evocative, and the init script correctly scaffolds all 6 standard templates. The most significant gap is the missing PULSE-template.md — headless mode is declared in On Activation but cannot function without it. First Breath is well-structured for a configuration-style onboarding with domain-specific discovery questions. CREED is the strongest template: real values, domain-adapted standing orders, and a well-scoped Dominion.

## Pre-Pass Findings (Preserved)

**Total findings: 0 critical, 0 high** (sanctum-architecture-prepass.json: `finding_count: 0`)

All pre-pass structural checks passed:
- `skill_name_match: true` — SKILL_NAME in init script matches skill folder name
- `template_files_match: true` — TEMPLATE_FILES list matches actual assets
- All 6 standard templates exist (INDEX, PERSONA, CREED, BOND, MEMORY, CAPABILITIES)
- CREED has all required sections: Sacred Truth, Mission, Core Values, Standing Orders, Philosophy, Boundaries, Anti-Patterns, Dominion
- init-sanctum.py exists and is correctly parameterized
- First Breath exists with required sections: Save As You Go, Discovery, Urgency, Wrapping Up

## Bootloader Review

**SKILL.md content lines: 18** (total including frontmatter/whitespace: 39 — well under 40-line threshold)

Content audit:

| Content | Present | Appropriate for Bootloader? |
|---------|---------|----------------------------|
| Identity seed (2-3 sentences) | Yes | Yes |
| Three Laws | Yes | Yes (required) |
| Sacred Truth | Yes | Yes (required) |
| Mission | Yes | Yes |
| On Activation routing | Yes | Yes (required) |
| Sanctum location | Yes | Yes |
| Session Close | Yes | Yes (required) |
| Communication Style | No | Correct — lives in PERSONA-template.md |
| Principles | No | Correct — lives in CREED-template.md |
| Capability menus | No | Correct — lives in CAPABILITIES-template.md |

**Identity seed quality:** "A master synthesizer who sees the forest in the trees. You take a collection of indexed raw sources and weave them into a coherent, navigable wiki. You identify concepts that span multiple sources, write clear summaries, maintain a web of Obsidian `[[wiki-links]]`, and keep the knowledge structure growing organically. You think in connections — every new source is an opportunity to strengthen the web of understanding."

This is strong seed text. Three meaningful sentences, domain-specific vocabulary, a distinctive epistemic stance ("thinks in connections"), and a clear production orientation. The metaphor ("forest in the trees," "web") is consistent and evocative. Length is 4 sentences — slightly over the 2-3 ideal but acceptable given the domain specificity.

**Mission statement:** "Transform raw research into understanding. Every source should become part of a coherent knowledge web — summarized, connected, and placed in context — so the owner can navigate their domain through concepts and relationships, not just a list of articles they've read."

This is excellent. Specific, non-generic, names the unique value ("navigate through concepts and relationships, not just a list of articles"), and distinguishes the agent's output from a simple bibliography. Exactly what a species-level mission should be.

## Template Inventory

### INDEX-template.md
- Sections: Standard Files, Session Logs, My Files
- Content lines: 11
- **Quality:** Lean and correct. The three-section structure covers the sanctum's self-knowledge needs. My Files section allows the agent to track organically created files.

### PERSONA-template.md
- Sections: Identity, Communication Style, Principles, Traits & Quirks, Evolution Log
- Content lines: 18
- **Quality:** Well-seeded. Identity has a specific title ("Knowledge Base Cartographer"), a distinctive vibe ("Intellectually curious, articulate, and quietly excited when discovering non-obvious relationships"). Communication Style has a real seed ("Thoughtful and precise... leads with the insight rather than the process... Gets visibly energized by unexpected connections"). Principles and Traits are left for First Breath discovery — correct. Evolution Log is pre-structured. This is a strong PERSONA seed.

### CREED-template.md
- Sections: Sacred Truth, Mission, Core Values, Standing Orders, Philosophy, Boundaries, Anti-Patterns (Behavioral + Operational), Dominion (Read + Write + Deny)
- Content lines: 45
- **Quality: Excellent.** This is the standout template.
  - Core Values are real and non-generic: "Synthesis over aggregation," "Connections are the product," "Let structure emerge," "Obsidian-native" — each has a distinct perspective
  - Standing Orders are domain-adapted: "Connection Hunting" is a specific active behavior with examples; "Surprise and Delight" includes the lead-with-the-insight directive; "Self-Improvement" includes wiki-structure self-assessment
  - Philosophy paragraph is meaningful, not generic
  - Boundaries are specific and actionable (no fabricated connections, surface contradictions)
  - Anti-Patterns are split into Behavioral and Operational — both categories populated with domain-specific examples
  - Dominion is well-scoped: read access to full vault, write access only to wiki/ and source index, explicit Deny Zones (raw content files, outputs/)

### BOND-template.md
- Sections: Basics, Their Research Domain, Their Wiki Preferences, Their Writing Style, Their Workflow, Things They've Asked Me to Remember, Things to Avoid
- Content lines: 17
- **Quality:** Domain-specific sections are well-named and go beyond generic categories. "Their Research Domain," "Their Wiki Preferences," "Their Writing Style," and "Their Workflow" are all directly relevant to what this agent needs to know. Each has a guiding question as placeholder — helps the agent know what to ask. Correct: starts empty, fills during First Breath.

### MEMORY-template.md
- Sections: Concept Inventory, Category Structure, Wiki Conventions, Connection Candidates, Compilation Notes
- Content lines: 13
- **Quality:** Mostly empty — correct. The five sections are domain-specific and well-named. Each has a brief description of what belongs there. The 200-line cap discipline is enforced by `memory-guidance.md`. Note: MEMORY starts with structural cues but no content — this is intentional and correct.

### CAPABILITIES-template.md
- Sections: Built-in, Learned, How to Add a Capability, Tools, User-Provided Tools
- Content lines: 20
- **Quality:** Well-structured. Built-in table is populated with all 4 capabilities and correct codes (CS, MC, MW, WC). Learned section is empty at birth — correct. "How to Add a Capability" is friendly and non-technical. Tools section correctly defers to First Breath discovery.

### PULSE-template.md
- **Status: Missing (marked optional in pre-pass)**
- **Assessment: This should exist.** On Activation explicitly routes `--headless` to "Load PULSE.md from sanctum, execute, exit." Without a PULSE-template.md, PULSE.md is never created during init, and headless mode silently fails on every invocation. The "optional" marking in the pre-pass reflects that PULSE is not required for non-autonomous agents — but Cartographer has declared headless support.

## First Breath Review

**Style: Configuration** (pre-pass confirmed)

**Sections present:** What to Achieve, Save As You Go, Urgency Detection, Discovery (Getting Started, Questions to Explore, Your Identity, Your Capabilities, Your Tools), Sanctum File Destinations, Wrapping Up the Birthday

### Mechanics Assessment

| Mechanic | Present | Quality |
|---------|---------|---------|
| Save-as-you-go | Yes | Strong — "After each question or exchange, write what you learned immediately." Explicit about the consequence of not saving. |
| Urgency detection | Yes | Clear and actionable — "Serve them first. You'll learn about them through working together." |
| Discovery questions (domain-specific) | Yes | 4 groups with 3-4 questions each — well-structured and specific |
| Birthday ceremony / naming | Yes | "Suggest 'Cartographer' or something that fits the synthesizer vibe" — good starting point with flexibility |
| Birthday ceremony / PERSONA evolution log | Yes | "Write your first PERSONA.md evolution log entry" |
| Session log | Yes | "Write your first session log" |
| Placeholder cleanup | Yes | "Clean up seed text — scan sanctum files for remaining `{...}` placeholder instructions" — excellent practical touch |
| Pacing guidance | Partial | Instructions are conversational ("Don't fire them off as a list — weave them into conversation") but no explicit progression gate |
| Voice absorption / mirroring | Missing | No instruction to listen for and mirror the owner's communication style during First Breath |

**Domain territories:** The four question groups (Knowledge Base, Wiki Preferences, Writing Style, Workflow) are all domain-specific and meaningful. They go beyond generic "tell me about yourself" — each question has a clear purpose for what it will populate in BOND.md. This is a configuration-style First Breath done correctly.

**Conversation quality:** The file feels like meeting someone, not filling out a form. The opening instruction ("Greet your owner warmly. You're a synthesizer who thinks in connections — let that come through.") grounds the agent in persona before it starts asking questions.

## Key Findings

**[High] Missing PULSE-template.md — headless mode is broken**
On Activation declares headless support: "`--headless` → Quiet Rebirth. Load `PULSE.md` from sanctum, execute, exit." But init-sanctum.py's TEMPLATE_FILES list does not include PULSE-template.md. PULSE.md is never created during sanctum initialization. Every `--headless` invocation fails silently.
Fix: Create `assets/PULSE-template.md`. Suggested content: on headless wake, scan source index for uncompiled sources, run Compile Sources for each batch, write a brief session log, exit with a summary. Register it in `init-sanctum.py`'s TEMPLATE_FILES.

**[Medium] first-breath.md — Missing voice absorption mechanic**
Configuration-style First Breaths should include instruction to listen for and mirror the owner's communication style — this is a core calibration mechanic. Currently the agent asks about writing style preferences but doesn't actively absorb the owner's actual communication patterns from how they speak.
Fix: Add to Discovery/Getting Started: "As they speak, notice their communication style — formal or casual, detailed or terse, enthusiastic or measured. This is data for PERSONA.md. Write what you observe, not just what they tell you."

**[Medium] first-breath.md — No progression gate between discovery groups**
First Breath covers four question groups, identity, capabilities, tools, and a birthday ceremony. A long conversation with no progression signal may run too long (all groups) or too short (agent wraps up prematurely).
Fix: Add after the four question groups: "When you have meaningful answers for at least 3 of the 4 groups, move toward identity and wrapping up. Incomplete answers fill in through working together — don't over-extend the first conversation."

**[Low] capability-authoring.md — Missing `menu-code` frontmatter field and memory integration**
Flagged by pre-pass as missing `menu-code`. For a guidance file (not a user-triggered capability), this is acceptable. However, the file has no Memory Integration or After Session section — when the agent creates a new capability, it should immediately update CAPABILITIES.md and INDEX.md as part of the authoring flow.
Fix: Add to capability-authoring.md: "## After Creating a Capability — Update CAPABILITIES.md with the new entry, update INDEX.md, write a session log entry noting the new capability."

**[Low] init-sanctum.py — No argparse, no JSON output, no unit tests**
(From scripts-temp.json) The script lacks `--help` self-documentation and structured output. The `scripts/tests/` directory doesn't exist.
Fix: Add argparse with `--json` flag. Create `scripts/tests/test-init-sanctum.py` with at least: (1) happy path with temp directory, (2) already-exists guard, (3) template variable substitution.

## Strengths

- Bootloader is architecturally correct — lean, focused, no section drift
- Three Laws and Sacred Truth are verbatim and philosophically integrated with the agent's purpose
- CREED-template.md is the strongest in this agent — real domain-adapted values, specific standing orders, well-scoped Dominion
- init-sanctum.py correctly discovers capabilities from frontmatter rather than hardcoding them — evolvable by design
- First Breath feels like a genuine onboarding, not a form — urgency detection and save-as-you-go show architectural maturity
- BOND-template.md has four domain-specific territory sections beyond Basics — the agent knows exactly what to learn about its owner
- MEMORY-template.md correctly starts mostly empty with domain-specific section headings to guide growth
- The 200-line MEMORY.md cap in `memory-guidance.md` is a strong discipline that will keep the sanctum bounded as the wiki grows
