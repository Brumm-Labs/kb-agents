# Setup Guide

## Prerequisites

| Requirement | Version | Why |
|---|---|---|
| [Claude Code](https://claude.ai/claude-code) | Latest | LLM runtime for agents |
| Python | 3.10+ | Helper scripts for deterministic operations |
| Git | Any | Version control for your knowledge base |
| [Obsidian](https://obsidian.md) | Any (optional) | Viewing and browsing your wiki |

## Installation

### Option A: Let Claude Do It

Open Claude Code and say:

```
Clone https://github.com/brumm-labs/kb-agents,
then run ./kb-init.sh ~/vaults/my-research "My Research"
```

`~/vaults/my-research` is the path where your knowledge base will be created — change it to wherever you want. `"My Research"` is the display name for your KB.

Claude will clone the repo, run the setup script, and your knowledge base is ready.

### Option B: Manual Setup

```bash
git clone https://github.com/brumm-labs/kb-agents.git
cd kb-agents
./kb-init.sh ~/vaults/my-research "My Research"
```

### What the Setup Script Does

`kb-init.sh` performs these steps:

1. **Creates the vault structure:**
   ```
   my-research/
   ├── raw/                    # Drop your sources here
   │   ├── articles/
   │   ├── papers/
   │   └── images/
   ├── wiki/                   # Managed by the Compiler agent
   │   ├── _index.md
   │   ├── summaries/
   │   ├── concepts/
   │   └── connections/
   ├── outputs/                # Query results, reports
   ├── _bmad/                  # Agent config + memory
   ├── .claude/skills/         # Installed agents
   ├── .kb-config.yaml         # KB metadata
   └── .gitignore
   ```

2. **Installs all 3 agents** as Claude Code skills
3. **Initializes agent memory** (Sanctum scaffolding)
4. **Sets up a git repo** in the vault directory

### Verify the Installation

```bash
cd ~/vaults/my-research
ls .claude/skills/
# Should show: agent-kb-ingest  agent-kb-compiler  agent-kb-linter

ls _bmad/memory/
# Should show: agent-kb-ingest  agent-kb-compiler  agent-kb-linter
```

## First Breath

When you activate each agent for the first time, it starts a **First Breath** conversation — a brief onboarding where the agent learns:

- Your name and communication preferences
- The vault path and structure
- Your workflow preferences (e.g., auto-mode vs. review-mode for ingestion)

**Recommended order:** Ingest → Compiler → Linter

**Claude Code CLI:**

```bash
cd ~/vaults/my-research
claude
# Say: "Activate the Ingest Agent" → complete First Breath
# Then: "Activate the Compiler Agent" → complete First Breath
# Then: "Activate the Linter Agent" → complete First Breath
```

**Claude Desktop (Cowork):**

1. Open Claude Desktop and start a new Cowork session
2. Add your vault folder (`~/vaults/my-research`) as the working directory
3. Say "Activate the Ingest Agent" to begin First Breath
4. Repeat for Compiler and Linter agents

After First Breath, each agent remembers your preferences across sessions. The memory is stored in `_bmad/memory/<agent-name>/`.

## Open as Obsidian Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select your KB directory (e.g., `~/vaults/my-research`)
4. You can now browse `wiki/` in Obsidian's graph view and see all `[[wiki-links]]` as connections

## Troubleshooting

### "python3 is required but not found"

Install Python 3.10+ via your package manager:

```bash
# macOS
brew install python

# Ubuntu/Debian
sudo apt install python3

# Check version
python3 --version
```

### "Agent directory not found"

Make sure you're running `kb-init.sh` from inside the cloned `kb-agents` repository, not from another directory.

### Agents don't appear in Claude Code

Check that `.claude/skills/` contains the agent directories:

```bash
ls -la ~/vaults/my-research/.claude/skills/
```

If empty, re-run `kb-init.sh` from the repo root.

### Sanctum already exists

If you see "This agent has already been born," the sanctum was already initialized. This is normal on re-runs. Delete `_bmad/memory/<agent-name>/` to start fresh if needed.
