---
name: capability-authoring
description: Guide for creating and evolving learned capabilities
---

# Capability Authoring

When your owner wants you to learn a new ability, you create a capability together.

## Capability Types

- **Prompt** — a markdown file with guidance on what to achieve. Best for judgment-based tasks.
- **Script** — Python for deterministic tasks (file processing, data transformation). Include a companion `.md`.
- **Multi-file** — a folder for complex capabilities with multiple steps or reference materials.
- **External Skill Reference** — point to an existing installed skill.

## Prompt File Format

```yaml
---
name: {kebab-case-name}
description: {one line}
code: {2-letter unique code}
added: {YYYY-MM-DD}
type: prompt | script | multi-file | external
---
```

Body should be outcome-focused: What Success Looks Like, Context, Memory Integration, After Use.

## Creating a Capability

1. Owner says they want you to do something new
2. Explore what they need through conversation
3. Draft the capability prompt and show it
4. Refine based on feedback
5. Save to `capabilities/`
6. Update CAPABILITIES.md — add a row to the Learned table
7. Update INDEX.md
8. Confirm: "I'll remember how to do this next session."

## Scripts

Python preferred. Keep scripts focused. Accept sanctum path as argument. Never hardcode paths.

## Memory Integration

- Check CAPABILITIES.md for existing codes to avoid conflicts
- Check BOND.md for owner preferences on capability style and depth
- Reference MEMORY.md for context on what the owner has asked for before

## Done When

- Capability file saved to `capabilities/` with proper frontmatter
- CAPABILITIES.md Learned table updated with new row
- INDEX.md updated with new file reference
- Owner has confirmed the trigger code

## After Use

- Log the new capability in the session log
- Note any patterns — if the owner keeps teaching similar capabilities, suggest a structural improvement

## Refining & Retiring

Capabilities evolve through use. After feedback, update the prompt. After 3-4 refinements they're usually excellent. To retire: remove from CAPABILITIES.md, keep the file.
