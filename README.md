# KB Agents

LLM-powered knowledge management with three AI agents for [Claude Code](https://claude.ai/claude-code) and [Obsidian](https://obsidian.md). Ingest raw sources, compile a structured wiki, and maintain quality — automatically.

![Tests](https://github.com/brumm-labs/kb-agents/actions/workflows/tests.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/brumm-labs/kb-agents)

## What Is This?

KB Agents is a system of three AI agents that automate the full research workflow. You drop sources (articles, papers, notes, images) into a folder, and the agents take it from there: they normalize and catalog your sources, compile them into an interconnected wiki with cross-referenced concepts, and audit everything for quality.

Each agent has persistent memory ("Sanctum") — it remembers your preferences, learns new capabilities, and picks up where it left off across sessions. The result is a structured knowledge base you can browse in Obsidian like a personal Wikipedia.

The agents are built on the [BMAD Framework](https://github.com/bmad-code-org/bmad-builder), which provides the agent architecture, memory system, and capability model that makes all of this possible.

## Pipeline

```
Sources (web, papers, notes, images)
        |
        v
  Archivist  -->  raw/
        |
        v
  Cartographer  -->  wiki/
        |
        v
  Inspector  -->  quality reports
```

## Agents

| Agent | Role | Capabilities |
|-------|------|-------------|
| **Archivist** (Ingest) | Normalize raw sources into indexed Markdown | `[AD]` Auto-Discover, `[IN]` Ingest, `[BI]` Batch, `[IX]` Index |
| **Cartographer** (Compiler) | Compile wiki with summaries, concepts, connections | `[CS]` Compile, `[MC]` Concepts, `[MW]` Wiki, `[WC]` Connections, `[QW]` Query |
| **Inspector** (Linter) | Audit quality, fix issues, suggest improvements | `[HC]` Health, `[FX]` Fix, `[SA]` Suggest, `[CC]` Consistency |

## Quick Start

### Prerequisites

- [Claude Code](https://claude.ai/claude-code) or [Claude Desktop](https://claude.ai/download)
- Python 3.10+
- [Obsidian](https://obsidian.md) (recommended, for viewing your wiki)

> **Hint:** Not sure if you have the prerequisites? Just ask Claude to install the dependencies for you.

### Setup

Tell Claude:

```
Clone https://github.com/brumm-labs/kb-agents,
then run ./kb-init.sh ~/vaults/my-research "My Research"
```

`~/vaults/my-research` is the path where your knowledge base will be created — change it to wherever you want. `"My Research"` is the display name for your KB.

Or do it manually:

```bash
git clone https://github.com/brumm-labs/kb-agents.git
cd kb-agents
./kb-init.sh ~/vaults/my-research "My Research"
```

Then start working with your agents:

**Claude Code CLI:**

```bash
cd ~/vaults/my-research
claude
```

**Claude Desktop (Cowork):**

1. Open Claude Desktop and start a new Cowork session
2. Add your vault folder (`~/vaults/my-research`) as the working directory
3. Start interacting with the agents

On first activation, each agent starts a **First Breath** conversation to learn your preferences. After that, open the folder as an Obsidian vault, drop files into `raw/`, and say "scan for new sources" — the agents take it from there.

## Documentation

- **[Setup Guide](docs/setup.md)** — Prerequisites, detailed installation, First Breath, troubleshooting
- **[Workflow](docs/workflow.md)** — Daily routines, weekly reviews, automation
- **[Use Cases](docs/use-cases.md)** — Ingesting, compiling, querying, researching
- **[Best Practices](docs/best-practices.md)** — Cron jobs, multiple vaults, tag conventions

## Built With

This project is built on the [BMAD Framework](https://github.com/bmad-code-org/bmad-builder) — the agent architecture, persistent memory system, and capability model that powers the KB agents. BMAD provides the foundation that makes agent memory, capability discovery, and First Breath possible.

- [Claude Code](https://claude.ai/claude-code) — LLM runtime
- [Obsidian](https://obsidian.md) — Wiki frontend

## License

[MIT](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

Built with 🤖 by [Brumm Labs](https://github.com/brumm-labs)
