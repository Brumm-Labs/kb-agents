# Structure & Capabilities Analysis — agent-kb-compiler

## Assessment

The agent-kb-compiler (Cartographer) is a well-formed memory agent bootloader. All four required bootloader sections are present, the Three Laws and Sacred Truth are verbatim and complete, and the SKILL.md is lean at 39 lines (content lines: 18). The only structural concern from the pre-pass is a missing "Use when..." trigger clause in the frontmatter description, and that all 7 capability/reference files lack config headers and progression conditions — both expected patterns for memory agents but worth noting.

## Sections Found

Memory agent bootloader structure confirmed (`is_memory_agent: true`). Standard bootloader sections present:

| Section | Present | Line |
|---------|---------|------|
| The Three Laws | Yes | 10 |
| The Sacred Truth | Yes | 20 |
| On Activation | Yes | 24 |
| Session Close | Yes | 36 |

No Overview, Identity, Communication Style, or Principles sections — correct by bootloader design. These live in sanctum templates (`assets/`).

## Capabilities Inventory

Capabilities are routed via `assets/CAPABILITIES-template.md`, not SKILL.md directly. All four built-in capabilities reference files that exist in `references/`:

| Code | Capability | File | Exists | Has Memory Integration | Has After Session | Has Success Section |
|------|------------|------|--------|------------------------|-------------------|---------------------|
| CS | Compile Sources | references/compile-sources.md | Yes | Yes | Yes | Yes |
| MC | Manage Concepts | references/manage-concepts.md | Yes | Yes | Yes | Yes |
| MW | Maintain Wiki | references/maintain-wiki.md | Yes | Yes | Yes | Yes |
| WC | Write Connections | references/write-connections.md | Yes | Yes | Yes | Yes |

Supporting references (not capabilities per se):

| File | Purpose | Notes |
|------|---------|-------|
| references/first-breath.md | Onboarding | Has config header with `{communication_language}` |
| references/memory-guidance.md | Memory discipline | No config header (acceptable for guidance files) |
| references/capability-authoring.md | Capability creation guide | No code/menu-code, no memory integration — by design |

## Pre-Pass Findings (Preserved)

**Total issues: 14 — 7 high, 7 medium, 0 critical**

| File | Line | Severity | Category | Issue |
|------|------|----------|----------|-------|
| SKILL.md | 1 | medium | frontmatter | Description missing "Use when..." trigger phrase |
| capability-authoring.md | 1 | medium | config-header | No config header with language variables found |
| capability-authoring.md | 42 | high | progression | No progression condition keywords found |
| compile-sources.md | 1 | medium | config-header | No config header with language variables found |
| compile-sources.md | 67 | high | progression | No progression condition keywords found |
| first-breath.md | 98 | high | progression | No progression condition keywords found |
| maintain-wiki.md | 1 | medium | config-header | No config header with language variables found |
| maintain-wiki.md | 63 | high | progression | No progression condition keywords found |
| manage-concepts.md | 1 | medium | config-header | No config header with language variables found |
| manage-concepts.md | 80 | high | progression | No progression condition keywords found |
| memory-guidance.md | 1 | medium | config-header | No config header with language variables found |
| memory-guidance.md | 62 | high | progression | No progression condition keywords found |
| write-connections.md | 1 | medium | config-header | No config header with language variables found |
| write-connections.md | 66 | high | progression | No progression condition keywords found |

**Note on config headers:** Memory agents receive language configuration from BOND.md in their sanctum, not from `{communication_language}` config headers. Missing config headers in `references/` files are low severity for memory agents. The one exception — `first-breath.md` — correctly has a config header since it runs before a sanctum exists.

**Note on progression conditions:** The pre-pass flags all 7 files. For memory agent capability references, progression keywords are less critical since these files are loaded on-demand per capability trigger rather than chained sequentially. Not false positives, but context matters.

## Key Findings

**[Medium] SKILL.md:1 — Missing "Use when..." trigger clause**
The frontmatter description is specific and well-written but lacks the standard "Use when: 'compile knowledge base', 'add to wiki'..." trigger clause. For a memory agent, this is less critical than for stateless agents (users typically activate the agent, not the skill), but adding it improves discoverability.
Fix: Append "Use when: 'compile wiki', 'process research sources', 'build knowledge base'" to the description.

**[Medium] capability-authoring.md — Missing menu-code, no memory integration**
This file guides the agent through co-creating capabilities with the owner. It has no `code:` field (intentional — it's not a user-triggered capability), no Memory Integration section (worth adding — the agent should note new capabilities in CAPABILITIES.md during creation), and no After Session section.
Fix: Add a brief Memory Integration note: "After creating a capability, update CAPABILITIES.md and INDEX.md."

**[Low] All references/*.md — Missing `menu-code` frontmatter field**
All 7 reference files report `missing_fields: ["menu-code"]`. For memory agents, capability codes are managed in CAPABILITIES.md rather than per-file frontmatter. The `compile-sources.md`, `maintain-wiki.md`, `manage-concepts.md`, and `write-connections.md` files have `code:` fields — this is sufficient.
Fix: No action required. The pre-pass is applying a stateless agent schema to memory agent references.

## Memory & Headless Status

**Memory:** Fully configured. Sanctum location defined (`{project-root}/_bmad/memory/agent-kb-compiler/`). Three-path activation routing in On Activation covers: First Breath, headless, and standard rebirth. Session Close is present and directs to memory-guidance.md.

**Headless:** Declared and routed. On Activation line 2 handles `--headless` via PULSE.md. However, no `PULSE-template.md` exists in `assets/` (confirmed absent in sanctum-architecture-prepass.json, marked optional). If the headless mode is intended for production use, PULSE-template.md should be created.

## Strengths

- Bootloader is lean and correct — 18 content lines, exactly the right sections
- Three Laws and Sacred Truth are verbatim and philosophically consistent with the agent's purpose
- Identity seed ("A master synthesizer who sees the forest in the trees...") is evocative and specific
- All four core capabilities have files that exist, are well-structured, and include Memory Integration and After Session sections
- Memory paths are consistent across all files — no path conflicts detected
- `first-breath.md` correctly has the one config header needed (language)
- Activation sequence is logically ordered: First Breath → headless → rebirth
