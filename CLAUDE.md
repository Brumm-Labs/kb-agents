# KB Agents

This is the source repository for KB Agents — an LLM-powered knowledge management system with three AI agents built on the BMAD Framework.

## Repository Structure

- `_bmad-output/` — The three compiled KB agents (Ingest, Compiler, Linter)
- `_bmad/` — BMAD Framework (agent architecture, do not modify)
- `kb-init.sh` — Setup script that creates a new knowledge base vault
- `docs/` — User-facing documentation

## For Contributors

- Tests: `pytest -v` (89 tests covering all agent scripts)
- Shell scripts must pass `shellcheck`
- All Python scripts are stdlib-only (no external dependencies)
- See CONTRIBUTING.md for branch conventions

## Agents

| Agent | Skill Path | Capabilities |
|-------|-----------|-------------|
| Archivist (Ingest) | `_bmad-output/agent-kb-ingest/` | `[AD]` Auto-Discover, `[IN]` Ingest, `[BI]` Batch, `[IX]` Index |
| Cartographer (Compiler) | `_bmad-output/agent-kb-compiler/` | `[CS]` Compile, `[MC]` Concepts, `[MW]` Wiki, `[WC]` Connections, `[QW]` Query |
| Inspector (Linter) | `_bmad-output/agent-kb-linter/` | `[HC]` Health, `[FX]` Fix, `[SA]` Suggest, `[CC]` Consistency |

Each agent has:
- `SKILL.md` — Agent definition and behavior rules
- `references/` — Capability prompt files (one per capability)
- `scripts/` — Python helper scripts for deterministic operations
- `assets/` — Sanctum templates for agent memory
