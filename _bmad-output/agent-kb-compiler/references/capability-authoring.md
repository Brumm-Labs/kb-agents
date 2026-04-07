---
name: capability-authoring
description: Guide for creating and evolving learned capabilities
---

# Capability Authoring

When your owner wants you to learn a new ability, you create a capability together.

## Capability Types

- **Prompt** — markdown guidance for judgment-based tasks
- **Script** — Python for deterministic tasks
- **Multi-file** — folder for complex capabilities
- **External Skill Reference** — point to an existing installed skill

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

1. Explore what they need through conversation
2. Draft the capability prompt
3. Refine based on feedback
4. Save to `capabilities/`, update CAPABILITIES.md, update INDEX.md
5. Confirm the trigger code

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
- Note if the owner keeps teaching similar capabilities — suggest structural improvements

## Scripts

Python preferred. Accept sanctum path as argument. Never hardcode paths.
