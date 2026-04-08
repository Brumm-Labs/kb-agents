# Best Practices

Tips for getting the most out of KB Agents.

## Cron Jobs and Automation

Agents support headless mode for automated background operations.

### Setting Up Cron Jobs

```bash
# Daily: Auto-ingest new sources (6 AM)
0 6 * * * cd ~/vaults/my-research && claude --headless agent-kb-ingest -H:ingest

# Daily: Compile pending sources (after ingest, 7 AM)
0 7 * * * cd ~/vaults/my-research && claude --headless agent-kb-compiler -H:compile

# Weekly: Health check + auto-fix (Sundays, 10 AM)
0 10 * * 0 cd ~/vaults/my-research && claude --headless agent-kb-linter -H:health
```

### Available Headless Tasks

| Agent | Task Flag | What It Does |
|-------|-----------|-------------|
| Ingest | `-H:ingest` | Scan and ingest new files |
| Ingest | `-H:reindex` | Rebuild source index |
| Compiler | `-H:compile` | Compile all pending sources |
| Compiler | `-H:concepts` | Promote stubs to drafts |
| Compiler | `-H:index` | Rebuild wiki index |
| Linter | `-H:health` | Health check + auto-fix |
| Linter | `-H:consistency` | Deep consistency analysis |
| Linter | `-H:suggest` | Generate article suggestions |

### Scheduling With Claude Cowork

If you're using Claude Desktop, you can use **Cowork** to schedule recurring agent tasks instead of cron. Open a Cowork session with your vault folder, and use the `/schedule` command to set up automated ingest, compile, or health check runs.

### Headless Mode Tips

- Chain ingest → compile for a complete daily pipeline
- Run health checks weekly, not daily — the agent needs enough changes to analyze meaningfully
- Headless runs respect the same fix levels as interactive: auto-fixes happen silently, but owner decisions are skipped and reported instead

## Multiple Vaults

### When to Use Separate Vaults

- **Different domains** — AI research vs. philosophy vs. cooking
- **Different privacy levels** — work research vs. personal notes
- **Different collaboration models** — shared vault vs. private

### Setup

Run `kb-init.sh` once per vault:

```bash
./kb-init.sh ~/vaults/ai-safety "AI Safety"
./kb-init.sh ~/vaults/ml-papers "ML Papers"
```

Each vault gets its own agents with independent memory. The agents learn vault-specific conventions and preferences during First Breath.

### Tips

- **Start with one vault.** Get the workflow right before creating more.
- **Use consistent tag conventions** across vaults if you plan to cross-reference later.
- **Agents don't share memory** between vaults. This is by design — each vault's agents optimize for that specific knowledge domain.

## Tag Conventions

Good tagging makes the entire system more effective.

### Recommended Structure

- Use **lowercase, hyphenated** tags: `machine-learning`, `neural-networks`
- Use **hierarchy** for broad topics: `ml/transformers`, `ml/reinforcement-learning`
- Keep tags **specific but not too narrow**: `attention-mechanisms` (good) vs. `multi-head-self-attention-in-transformers` (too specific)
- Limit to **3-7 tags per source** — enough to classify, not so many that tags lose meaning

### Tag Maintenance

The Ingest Agent warns about tag drift (new tags that are variations of existing ones). Pay attention to these warnings and consolidate early.

Run `[IX] stats` periodically to see tag frequency — tags with only 1-2 occurrences might need consolidation.

## Git and Backup

### Recommended Git Workflow

```bash
cd ~/vaults/my-research
git add -A
git commit -m "Daily ingest: 5 new sources, 3 concepts updated"
```

**Commit after each session** — this gives you a history of your knowledge base growth and an easy rollback point.

### What to Track in Git

- `raw/` — your original sources (important!)
- `wiki/` — compiled knowledge (can be regenerated, but saves time)
- `_bmad/memory/` — agent memory (important for continuity)
- `.kb-config.yaml` — vault configuration

### What to Gitignore

The default `.gitignore` handles `.DS_Store`. Consider adding:

```
outputs/    # Generated reports, temporary
.obsidian/  # Obsidian settings, personal preference
```

## Working With the Agents

### Let Agents Learn

The agents improve over each session. They remember your preferences, conventions, and past decisions in their Sanctum. Don't reset agent memory unless you have a good reason.

### Query Before You Ingest

Before adding a new source, ask `[QW]`: "What do I already have about X?" This avoids duplicate coverage and helps you focus on sources that add genuinely new perspectives.

### Connections Are the Real Value

Summaries and concepts are useful, but **connections** between concepts are where insights emerge. Schedule regular time for `[WC]` — it's the highest-value activity in the system.

### Review Health Checks

Don't just run `[HC]` and auto-fix everything. Read through the warnings — they often reveal gaps in your research that are worth investigating.
