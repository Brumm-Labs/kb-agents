# Personal Knowledge Management

LLM-powered knowledge base system using three BMAD Memory Agents to automate the full research workflow: ingest raw sources, compile a structured wiki, and maintain quality — all viewable in Obsidian.

## Agents

| Agent | Role | Capabilities |
|-------|------|-------------|
| 📚 **Archivist** (Ingest) | Normalize raw sources into indexed Markdown | `[AD]` Auto-Discover, `[IN]` Ingest, `[BI]` Batch, `[IX]` Index |
| 🗺️ **Cartographer** (Compiler) | Compile wiki with summaries, concepts, connections | `[CS]` Compile, `[MC]` Concepts, `[MW]` Wiki, `[WC]` Connections, `[QW]` Query |
| 🔍 **Inspector** (Linter) | Audit quality, fix issues, suggest improvements | `[HC]` Health, `[FX]` Fix, `[SA]` Suggest, `[CC]` Consistency |

## Quick Start

```bash
# One command sets up everything:
./kb-init.sh ~/vaults/my-research "My Research"

# Then:
cd ~/vaults/my-research
claude   # agents are ready, First Breath starts on first activation
```

Drop files into `raw/` and the Ingest Agent finds them automatically — no need to specify file paths.

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
