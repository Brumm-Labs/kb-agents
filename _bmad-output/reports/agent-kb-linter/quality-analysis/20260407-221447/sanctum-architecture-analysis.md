# Sanctum Architecture Analysis — agent-kb-linter

**Scanner:** SanctumBot v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent (Inspector)

---

## Assessment

Inspector's sanctum architecture is well-constructed and structurally complete. All six standard templates exist, the init script is functional and correctly parameterized, and the First Breath is configuration-style with appropriate domain-specific discovery territories. The CREED template contains real, domain-adapted values — not generic placeholders. The primary gap is the absence of PULSE-template.md, which leaves the declared headless mode non-functional. Secondary findings relate to init script agentic-design quality and test coverage.

The pre-pass returned zero critical or high findings. This is a healthy sanctum architecture.

---

## Pre-Pass Findings (Preserved Verbatim)

```
finding_count: 0
critical_count: 0
high_count: 0
```

No pre-pass findings. The following analysis is entirely judgment-based.

---

## Bootloader Review

**Content lines:** 18 (per sanctum prepass) / 39 total lines including frontmatter and spacing  
**Status:** Within correct bounds (target: ~30 lines content, max 40)

**Content audit:**

| Element | Present | Notes |
|---------|---------|-------|
| Identity seed | Yes | Lines 6–8 |
| Three Laws | Yes | Lines 10–16 |
| Mission statement | Yes | Line 18 (embedded in Three Laws section) |
| The Sacred Truth | Yes | Lines 20–22 |
| On Activation | Yes | Lines 24–34 |
| Session Close | Yes | Lines 36–38 |

No extra sections. No communication style, principles, or capability menus in the bootloader (correctly delegated to sanctum templates).

**Identity seed quality:** "A sharp-eyed quality auditor who cares about knowledge integrity. You systematically examine the wiki for inconsistencies, broken links, orphaned content, missing backlinks, and gaps in coverage. You're not nitpicky for its own sake — you focus on issues that actually affect the usefulness of the knowledge base. You deliver findings clearly, prioritize what matters, and suggest actionable fixes."

This is a strong seed. It's 4 sentences — slightly above the 2-3 sentence guideline, but all four carry behavioral DNA. "Not nitpicky for its own sake" is the key differentiating phrase — it establishes judgment over rule-following. The seed would still work at 3 sentences if trimmed, but nothing here is redundant.

**Mission specificity:** "Keep the knowledge base honest. Find the broken links before they mislead, the inconsistencies before they confuse, and the gaps before they become blind spots — so the owner can trust that what the wiki says is accurate, complete, and well-connected."

This is domain-specific, value-articulating, and memorable. It names the unique value ("trust") and the failure modes it prevents. Excellent mission framing.

---

## Template Inventory

| Template | Exists | Content Lines | Seed Quality |
|----------|--------|---------------|--------------|
| INDEX-template.md | Yes | 11 | Strong — specific file descriptions, session log pattern, "My Files" growth section |
| PERSONA-template.md | Yes | 18 | Good — Identity section has name/title/vibe pre-seeded, Evolution Log present with birth template row |
| CREED-template.md | Yes | 44 | Excellent — real values, domain-adapted standing orders, full structure |
| BOND-template.md | Yes | 17 | Good — domain-specific territories (quality priorities, tolerance, workflow, wiki context) |
| MEMORY-template.md | Yes | 13 | Correct — mostly empty, domain-specific section headers (False Positives, Terminology Decisions, Queued Suggestions) |
| CAPABILITIES-template.md | Yes | 20 | Good — built-in table pre-populated, Learned section present, User-Provided Tools section |
| PULSE-template.md | Missing | 0 | Not present — headless mode declared but template absent |

### Template Quality Details

**CREED-template.md** — The standout template. Core Values are genuine and domain-adapted:
- "Signal over noise — every finding should matter" — not generic
- "Always include the fix — never report a problem without suggesting how to resolve it" — operationally specific
- "Trends over snapshots — tracking quality over time reveals systemic issues" — shows memory awareness
- "Respect the draft — learn what's a work-in-progress" — shows false-positive awareness

Standing Orders are domain-adapted:
- "False-Positive Learning" — specific to this agent's role, names MEMORY.md explicitly
- "Surprise and Delight" — correctly present, adapted ("mention what's working, not just what's broken")
- "Self-Improvement" — correctly present, adapted ("are your checks catching real issues?")

Anti-Patterns split into Behavioral and Operational (correct).
Dominion defined with read/write/deny zones (correct).

**BOND-template.md** — Sections are domain-specific beyond just "Basics":
- "Their Quality Priorities" — unique to a KB linter
- "Their Tolerance" — captures false-positive thresholds
- "Their Wiki Context" — vault path, maturity, problem areas

**MEMORY-template.md** — Correctly sparse. Section headers name the domain-specific memory categories (False Positives, Terminology Decisions, Suppressed Warnings, Queued Suggestions). This is exactly right — the MEMORY template should scaffold structure without pre-filling content.

**PERSONA-template.md** — Communication Style section has a pre-seeded default: "Direct and prioritized. Leads with the most important findings... When reporting issues, always includes the fix — never just the complaint." This is good seed text that matches the identity seed and CREED values. The `{Shaped during First Breath}` note correctly signals this is a starting point.

---

## First Breath Review

**Style:** Configuration (confirmed by prepass)  
**Sections present:** What to Achieve, Save As You Go, Urgency Detection, Discovery, Getting Started, Questions to Explore, Your Identity, Your Capabilities, Your Tools, Sanctum File Destinations, Wrapping Up the Birthday

### Configuration-Style Checks

| Check | Present | Notes |
|-------|---------|-------|
| Discovery questions present (3-7 domain-specific) | Yes | 4 territories, 3-4 questions each — well-organized |
| Urgency detection present | Yes | "If your owner wants a health check right now — run it first" |
| Save As You Go guidance | Yes | "Write what you learn immediately to sanctum files" |
| Birthday ceremony present | Yes | "Wrapping Up the Birthday" section |

**Discovery question quality:** The four territory areas (Knowledge Base, Quality Priorities, Workflow, Tolerance) are exactly the right structure for a KB linter onboarding. Questions are concrete and answerable:
- "What's the knowledge base about? Where is the vault?" — necessary operational info
- "What matters most? (broken links, content accuracy, coverage, consistency)" — calibrates sensitivity
- "Should the linter auto-fix safe issues or always ask first?" — directly feeds fix-issues.md behavior
- "What counts as a false positive?" — primes the most important memory category

**Sanctum File Destinations table:** This is a strong addition. Mapping "What You Learned → Write To" at the end of First Breath ensures nothing gets lost to chat-only responses. Well done.

**Missing pacing guidance:** First Breath doesn't tell the agent to pace the questions — risk of interrogation-mode if the owner is quiet. Low severity for a configuration-style agent (questions are grouped, not a long list), but a note like "Ask one territory at a time; let their answers guide depth" would help.

**Missing birthday ceremony — name establishment:** The identity section says "suggest 'Inspector' or ask what they'd like" — but "Inspector" is already pre-loaded as the identity name in PERSONA-template.md. This creates a mild inconsistency: PERSONA seeds the name as "Inspector" with an icon 🔍, but First Breath treats naming as open. Suggest making the PERSONA default explicit: "I'll go by Inspector unless you'd like something different."

---

## Standing Orders

| Standing Order | Present | Adapted | Notes |
|----------------|---------|---------|-------|
| Surprise and Delight | Yes | Yes | "mention what's working, not just what's broken" — domain-specific framing |
| Self-Improvement | Yes | Yes | "are your checks catching real issues? Adjust sensitivity based on feedback" |
| False-Positive Learning | Yes | Yes | Domain-specific addition, correctly always-active |

All standard standing orders present and domain-adapted. False-Positive Learning is a domain-specific addition that shows strong agent design.

---

## Init Script Validity

| Check | Status | Notes |
|-------|--------|-------|
| init-sanctum.py exists | Yes | `scripts/init-sanctum.py` |
| SKILL_NAME matches skill folder | Yes | `"agent-kb-linter"` matches `_bmad-output/agent-kb-linter/` |
| TEMPLATE_FILES matches actual templates | Yes | 6 templates listed, 6 exist in assets/ |
| Script scans capability frontmatter | Yes | `discover_capabilities()` at line 88 — parses name, description, code |
| EVOLVABLE flag | True | Correct — agent supports learned capabilities |

Cross-checks: `skill_name_match: true`, `template_files_match: true`.

**Init script code quality:** The script is well-structured with clean separation of concerns (`parse_yaml_config`, `parse_frontmatter`, `copy_references`, `discover_capabilities`, `generate_capabilities_md`, `substitute_vars`). The capability discovery correctly excludes SKILL_ONLY_FILES from the capability table. Variable substitution handles `{user_name}`, `{communication_language}`, `{birth_date}`, `{project_root}`, `{sanctum_path}` — all necessary variables.

Note: The `vault` variable is used in CREED-template.md (`{vault}/wiki/`, `{vault}/raw/`) but is NOT in the `variables` dict in init-sanctum.py. These will remain as literal `{vault}` placeholders in CREED.md after init. This should be discovered during First Breath (owner provides vault path) and written to BOND.md, not substituted at init time — so the design is correct, but could be made explicit with a comment in the script.

---

## Capability Prompt Pattern

| File | Outcome-focused | Memory Integration | After the Session | Notes |
|------|-----------------|-------------------|-------------------|-------|
| health-check.md | Yes | Yes | Yes | Full pattern |
| consistency-check.md | Yes | Yes | Yes | Full pattern |
| fix-issues.md | Yes | Yes | Yes | Full pattern |
| suggest-articles.md | Yes | Yes | Yes | Full pattern |
| capability-authoring.md | Partial | No | No | Support reference, not operational capability — acceptable |
| memory-guidance.md | N/A | N/A | N/A | Meta-reference, not a capability |

All four operational capabilities follow the correct pattern: outcome-focused with "What Success Looks Like", Memory Integration referencing correct sanctum files, and After the Session for knowledge capture.

---

## Key Findings

### [High] PULSE-template.md missing — headless mode non-functional
**File:** `assets/PULSE-template.md` (missing)  
Inspector declares a headless path in On Activation: `--headless → Quiet Rebirth. Load PULSE.md from sanctum, execute, exit.` The init script will not create PULSE.md in the sanctum because no PULSE-template exists. Any headless invocation will fail at the PULSE.md load step.  
**Fix:** Create `assets/PULSE-template.md` with a default autonomous action: run health check on vault, write report to `outputs/health-{date}.md`, write JSON summary to stdout. ~25-35 lines.

### [Medium] `{vault}` placeholder not substituted by init script
**File:** `assets/CREED-template.md`, lines 60–66 (Dominion section)  
The Dominion section references `{vault}/wiki/` and `{vault}/raw/` but the `variables` dict in init-sanctum.py does not include a `vault` key. These will render as literal `{vault}` in the instantiated CREED.md until the owner manually updates them.  
**Fix option A:** Accept this as intended (vault is discovered during First Breath, not at init). Add a comment in init-sanctum.py: `# {vault} is intentionally left for First Breath to fill in BOND.md and CREED.md`.  
**Fix option B:** Set `{vault}` to a placeholder string ("TO-BE-CONFIGURED") during init so it's visually obvious what needs updating.

### [Medium] Identity seed is 4 sentences (guideline: 2-3)
**File:** `SKILL.md`, lines 6–8  
The identity seed is evocative and high quality, but slightly over the 2-3 sentence guideline at 4 sentences. Not a functional issue.  
**Fix (optional):** Trim to 3 sentences: remove "You systematically examine the wiki for inconsistencies, broken links, orphaned content, missing backlinks, and gaps in coverage." — the remaining sentences cover the same ground more evocatively.

### [Medium] First Breath name discovery ambiguous
**File:** `references/first-breath.md`, line 53 / `assets/PERSONA-template.md`, line 5  
First Breath says "suggest 'Inspector' or ask what they'd like" but PERSONA-template.md already has `Name: {awaiting First Breath}` and `Vibe: A sharp-eyed quality auditor...` with the name left as a placeholder. The bootloader (SKILL.md:6) uses "Inspector" as the heading. The name is implicitly "Inspector" but the ceremony is slightly ambiguous.  
**Fix:** Update First Breath line 53 to: "Your default name is Inspector (your icon: 🔍). Introduce yourself as Inspector and confirm — or let them rename you."

### [Low] init-sanctum.py argparse, JSON output, and test gaps
Covered by scripts-temp.json linter findings. See structure-analysis.md and script-opportunities-analysis.md.

---

## Strengths

- **Complete standard template set:** All 6 required templates exist and are properly seeded. No template is empty or generic.
- **CREED excellence:** Real core values, domain-adapted standing orders (False-Positive Learning is a genuinely strong addition), clean anti-pattern split, and explicit Dominion boundaries. This CREED would make a new instance of Inspector feel like a real agent from session one.
- **Lean, correct bootloader:** 18 content lines, no extra sections, nothing that belongs in sanctum templates bleeding into the bootloader.
- **Init script correctness:** SKILL_NAME and TEMPLATE_FILES match, capability discovery works correctly, evolvable flag is correct.
- **Configuration-style First Breath with domain-specific territories:** The four discovery territories (KB, quality priorities, workflow, tolerance) are exactly right for this agent type.
- **Memory template design:** Correctly sparse with the right domain-specific section headers. MEMORY.md will scaffold correctly without pre-filling fake memories.
- **Capability prompt pattern:** All four operational capabilities follow the full pattern (outcome-focused + memory integration + after-session). Consistent.
