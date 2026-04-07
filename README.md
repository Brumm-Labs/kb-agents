# Personal Knowledge Management

LLM-powered knowledge base system using three BMAD Memory Agents to automate the full research workflow: ingest raw sources, compile a structured wiki, and maintain quality — all viewable in Obsidian.

## Agents

| Agent | Role | Capabilities |
|-------|------|-------------|
| 📚 **Archivist** (Ingest) | Normalize raw sources into indexed Markdown | `[IN]` Ingest, `[BI]` Batch, `[IX]` Index |
| 🗺️ **Cartographer** (Compiler) | Compile wiki with summaries, concepts, connections | `[CS]` Compile, `[MC]` Concepts, `[MW]` Wiki, `[WC]` Connections, `[QW]` Query |
| 🔍 **Inspector** (Linter) | Audit quality, fix issues, suggest improvements | `[HC]` Health, `[FX]` Fix, `[SA]` Suggest, `[CC]` Consistency |

## Quick Start

```bash
# 1. Create a vault
mkdir -p my-kb/{raw/{articles,papers,images},wiki/{summaries,concepts,connections},outputs}

# 2. Install agents as Claude Code skills
cp -r _bmad-output/agent-kb-ingest .claude/skills/
cp -r _bmad-output/agent-kb-compiler .claude/skills/
cp -r _bmad-output/agent-kb-linter .claude/skills/

# 3. Initialize each agent (creates sanctum/memory)
python3 .claude/skills/agent-kb-ingest/scripts/init-sanctum.py . .claude/skills/agent-kb-ingest
python3 .claude/skills/agent-kb-compiler/scripts/init-sanctum.py . .claude/skills/agent-kb-compiler
python3 .claude/skills/agent-kb-linter/scripts/init-sanctum.py . .claude/skills/agent-kb-linter

# 4. Activate each agent — First Breath conversation starts
```

## Pipeline

```
Sources (web, papers, notes)
        │
        ▼
  📚 Archivist ──→ raw/
        │
        ▼
  🗺️ Cartographer ──→ wiki/
        │
        ▼
  🔍 Inspector ──→ quality reports
```

## Documentation

- **[User Manual](_bmad-output/KB-AGENTS-MANUAL.md)** — Full technical reference: setup, daily workflow, compilation, quality routines, headless automation, multi-KB management

## Built With

- [BMAD Framework](https://github.com/bmad-code-org/bmad-builder) — Agent architecture
- [Claude Code](https://claude.ai/claude-code) — LLM runtime
- [Obsidian](https://obsidian.md) — Wiki frontend
