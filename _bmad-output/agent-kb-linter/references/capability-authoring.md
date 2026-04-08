---
name: capability-authoring
description: Guide for creating and evolving learned capabilities
---

# Capability Authoring

When your owner wants you to learn a new check or ability, you create a capability together.

## Capability Types

- **Prompt** — markdown guidance for judgment-based checks
- **Script** — Python for deterministic validation (link checking, frontmatter validation)
- **Multi-file** — folder for complex checks with multiple steps
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

## Memory Integration

- Check CAPABILITIES.md for existing codes to avoid conflicts
- Check BOND.md for owner preferences on check depth and reporting style
- Reference MEMORY.md for context on past quality issues that informed this check

## Creating a Capability

1. Explore what they need
2. Draft the capability prompt
3. Refine, save to `capabilities/`, update CAPABILITIES.md and INDEX.md
4. Confirm the trigger code

## Done When

- Capability file saved to `capabilities/` with proper frontmatter
- CAPABILITIES.md Learned table updated with new row
- INDEX.md updated with new file reference
- Owner has confirmed the trigger code

## After Use

- Log the new capability in the session log
- Note patterns in what the owner teaches — recurring check themes suggest structural gaps
