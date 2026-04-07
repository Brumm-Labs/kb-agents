# Structure & Capabilities Analysis — agent-kb-linter

**Scanner:** StructureBot v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent (bootloader)

---

## Assessment

Inspector (agent-kb-linter) is a structurally sound memory agent with a lean, correct bootloader. All four required bootloader sections are present, the sanctum template set is complete, and the init script aligns correctly with its declared parameters. The primary structural gaps are a missing "Use when" trigger phrase in the frontmatter description, and the absence of config headers and progression conditions across most capability files in `references/` — both are addressable without rearchitecting anything.

---

## Memory Agent Status

`metadata.is_memory_agent: true` — bootloader expectations applied throughout. Standard stateless agent section checks (Overview, Identity, Communication Style, Principles) are intentionally not flagged.

---

## Sections Found (SKILL.md Bootloader)

| Section | Present | Notes |
|---------|---------|-------|
| Identity seed (free-flowing) | Yes | Line 6–8, "A sharp-eyed quality auditor..." |
| The Three Laws | Yes | Line 10–16 |
| The Sacred Truth | Yes | Line 20–22 |
| On Activation | Yes | Line 24–34 |
| Session Close | Yes | Line 36–38 |

All required bootloader sections are present. No invalid sections (On Exit, Exiting) detected.

---

## Capabilities Inventory

Capability routing lives in `assets/CAPABILITIES-template.md` (correct for memory agents).

| Code | Name | Source File | Has name | Has code | Has description | Memory Integration | After Session | Success Section |
|------|------|------------|----------|----------|-----------------|-------------------|---------------|-----------------|
| HC | Health Check | `references/health-check.md` | Yes | Yes | Yes | Yes | Yes | Yes |
| FX | Fix Issues | `references/fix-issues.md` | Yes | Yes | Yes | Yes | Yes | Yes |
| SA | Suggest Articles | `references/suggest-articles.md` | Yes | Yes | Yes | Yes | Yes | Yes |
| CC | Consistency Check | `references/consistency-check.md` | Yes | Yes | Yes | Yes | Yes | Yes |
| — | Capability Authoring | `references/capability-authoring.md` | Yes | No | Yes | No | No | No |
| — | Memory Guidance | `references/memory-guidance.md` | Yes | No | Yes | No | No | No |
| — | First Breath | `references/first-breath.md` | Yes | No | Yes | N/A | N/A | N/A |

All four operational capability files exist and resolve correctly. `capability-authoring.md` and `memory-guidance.md` are support references, not direct capabilities — their missing `code`, `menu-code`, memory integration, and after-session sections are not structural errors for their role.

---

## Pre-Pass Findings (Preserved Verbatim)

**Total issues: 14 (7 high, 7 medium)**

| Severity | File | Line | Category | Issue |
|----------|------|------|----------|-------|
| Medium | SKILL.md | 1 | frontmatter | Description missing "Use when..." trigger phrase |
| Medium | capability-authoring.md | 1 | config-header | No config header with language variables found |
| High | capability-authoring.md | 35 | progression | No progression condition keywords found |
| Medium | consistency-check.md | 1 | config-header | No config header with language variables found |
| High | consistency-check.md | 55 | progression | No progression condition keywords found |
| High | first-breath.md | 85 | progression | No progression condition keywords found |
| Medium | fix-issues.md | 1 | config-header | No config header with language variables found |
| High | fix-issues.md | 44 | progression | No progression condition keywords found |
| Medium | health-check.md | 1 | config-header | No config header with language variables found |
| High | health-check.md | 72 | progression | No progression condition keywords found |
| Medium | memory-guidance.md | 1 | config-header | No config header with language variables found |
| High | memory-guidance.md | 62 | progression | No progression condition keywords found |
| Medium | suggest-articles.md | 1 | config-header | No config header with language variables found |
| High | suggest-articles.md | 48 | progression | No progression condition keywords found |

---

## Key Findings (Judgment-Based)

### [Medium] Missing "Use when" trigger phrase in frontmatter
**File:** `SKILL.md`, line 1  
The `description` field reads: "Knowledge Base Wiki Linter — audits wiki health, finds inconsistencies, broken links, missing content, and suggests improvements. Memory agent that learns quality priorities and false-positive patterns."  
This is descriptive but lacks a "Use when..." clause or quoted trigger phrases. Without it, agent selection logic has less signal for when to activate this agent vs. a general search or note-taking agent.  
**Fix:** Append "Use when the user says 'run health check', 'check the wiki', 'inspect my knowledge base', or 'lint my notes'."

### [Medium] Config headers absent on 6 of 7 capability files
**Files:** All `references/*.md` except `first-breath.md`  
Memory agents get language from BOND.md at rebirth — per the scanner spec, missing config headers in `./references/` files are not high severity for memory agents. However, adding a `{communication_language}` reference in at least the main operational capabilities (health-check, consistency-check, fix-issues, suggest-articles) would provide explicit language context if capabilities are ever loaded standalone.  
**Fix:** Low priority — add a one-line language note to the operational capabilities if needed.

### [High] Progression conditions absent across all capability files
**Files:** All 7 references files (lines: 35, 55, 85, 44, 72, 62, 48)  
No progression condition keywords are detected in any capability. For operational capabilities (HC, FX, SA, CC) that involve multi-step workflows, absence of progression conditions means the agent has no formal logic for when to transition between phases. For support files (first-breath, memory-guidance, capability-authoring), this is less critical.  
**Fix (operational):** Add a progression anchor to health-check.md, consistency-check.md, fix-issues.md, and suggest-articles.md — e.g., "When the analysis is complete and the report is drafted, present findings and await owner response before applying any fixes."

### [Low] `capability-authoring.md` missing `menu-code` frontmatter field
**File:** `references/capability-authoring.md`, line 1  
All operational capabilities have `code` field for menu routing, but `capability-authoring.md` (a support reference) lacks a `menu-code`. Given its role as a meta-capability invoked conversationally rather than by code, this is minor.  
**Fix:** Optional — add `code: CA` if the owner wants to invoke it by menu code.

---

## Strengths

- **Clean bootloader:** At 39 lines (18 content lines per sanctum prepass), SKILL.md is lean and correctly minimal. Identity seed is vivid and behavior-priming.
- **Three Laws and Sacred Truth:** Both present verbatim. Foundational continuity intact.
- **Complete sanctum template set:** All 6 standard templates exist (INDEX, PERSONA, CREED, BOND, MEMORY, CAPABILITIES). No missing templates.
- **Path standards:** Zero path standard violations across all 14 files scanned.
- **Init script alignment:** `SKILL_NAME` matches, `TEMPLATE_FILES` matches actual assets. `skill_name_match: true`, `template_files_match: true`.
- **Operational capabilities well-formed:** health-check, fix-issues, suggest-articles, consistency-check all have name, code, description, memory integration, after-session, and success sections.
- **Activation routing correct:** Three-path On Activation (First Breath / Headless / Rebirth) is logically ordered and complete.
- **Mission specificity:** The mission in SKILL.md ("Keep the knowledge base honest...") is domain-specific and meaningful.

---

## Memory & Headless Status

- **Memory:** Fully configured. Sanctum path `memory/agent-kb-linter/` declared. Session Close instructs loading `memory-guidance.md` and writing session logs. Memory paths consistent across files.
- **Headless:** Declared in On Activation (`--headless` → Quiet Rebirth → load PULSE.md). PULSE-template.md does not exist (marked optional in prepass). If headless/autonomous mode is intended, the PULSE template needs to be created.
