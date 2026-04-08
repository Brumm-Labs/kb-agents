#!/bin/bash
# KB Init — Creates a new Knowledge Base vault with all agents ready to use.
#
# Usage:
#   ./kb-init.sh <target-directory> [kb-name]
#
# Example:
#   ./kb-init.sh ~/vaults/ai-safety "AI Safety Research"
#   ./kb-init.sh ~/iCloud/my-research
#
# After running:
#   cd <target-directory>
#   claude   # agents are ready, start with First Breath

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AGENTS_DIR="$SCRIPT_DIR/_bmad-output"

# --- Pre-flight checks ---

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required but not found on PATH."
    echo "Install Python 3.10+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
    echo "ERROR: Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi

if [ ! -d "$AGENTS_DIR" ]; then
    echo "ERROR: Agent directory not found at $AGENTS_DIR"
    echo "Make sure you're running this from the kb-agents repository root."
    exit 1
fi

# --- Args ---

if [ $# -lt 1 ]; then
    echo "Usage: ./kb-init.sh <target-directory> [kb-name]"
    echo ""
    echo "Creates a new Knowledge Base vault with all agents installed."
    echo "After setup, cd into the directory and run 'claude' to start."
    exit 1
fi

TARGET="$(cd "$(dirname "$1")" 2>/dev/null && pwd)/$(basename "$1")" || TARGET="$1"
KB_NAME="${2:-$(basename "$TARGET")}"

echo "=== KB Init ==="
echo "Target:  $TARGET"
echo "Name:    $KB_NAME"
echo ""

# --- Vault structure ---

echo "Creating vault structure..."
mkdir -p "$TARGET"/{raw/{articles,papers,images},wiki/{summaries,concepts,connections},outputs}

# Source index
if [ ! -f "$TARGET/raw/_source-index.md" ]; then
    cat > "$TARGET/raw/_source-index.md" << 'INDEXEOF'
# Source Index

_Auto-maintained by the Ingest Agent._

| Title | Type | Tags | Status | Date Ingested | Path |
|-------|------|------|--------|---------------|------|
INDEXEOF
fi

# Wiki master index
if [ ! -f "$TARGET/wiki/_index.md" ]; then
    cat > "$TARGET/wiki/_index.md" << WIKIEOF
# $KB_NAME

_Last updated: $(date +%Y-%m-%d) | 0 concepts | 0 summaries | 0 sources_

## Concepts

_No concepts yet. Run the Compiler agent to create them from ingested sources._

## Recent Additions

_No additions yet._
WIKIEOF
fi

# KB config
if [ ! -f "$TARGET/.kb-config.yaml" ]; then
    cat > "$TARGET/.kb-config.yaml" << CONFEOF
name: "$KB_NAME"
created: $(date +%Y-%m-%d)
vault_path: "$TARGET"
CONFEOF
fi

echo "  Vault structure created."

# --- BMAD config ---

echo "Copying BMAD configuration..."
mkdir -p "$TARGET/_bmad"

# Copy core config if it exists in source
if [ -d "$SCRIPT_DIR/_bmad/_config" ]; then
    cp -r "$SCRIPT_DIR/_bmad/_config" "$TARGET/_bmad/"
fi
if [ -f "$SCRIPT_DIR/_bmad/core/config.yaml" ]; then
    mkdir -p "$TARGET/_bmad/core"
    cp "$SCRIPT_DIR/_bmad/core/config.yaml" "$TARGET/_bmad/core/"
fi

echo "  BMAD config copied."

# --- Install agents as Claude Code skills ---

echo "Installing agents..."
mkdir -p "$TARGET/.claude/skills"

for AGENT in agent-kb-ingest agent-kb-compiler agent-kb-linter; do
    if [ -d "$AGENTS_DIR/$AGENT" ]; then
        cp -r "$AGENTS_DIR/$AGENT" "$TARGET/.claude/skills/"
        echo "  Installed $AGENT"
    else
        echo "  WARNING: $AGENTS_DIR/$AGENT not found, skipping"
    fi
done

# Copy Claude settings if they exist
if [ -f "$SCRIPT_DIR/.claude/settings.json" ]; then
    cp "$SCRIPT_DIR/.claude/settings.json" "$TARGET/.claude/"
fi

echo "  Agents installed."

# --- Init sanctums ---

echo "Initializing agent sanctums..."

for AGENT in agent-kb-ingest agent-kb-compiler agent-kb-linter; do
    SKILL_PATH="$TARGET/.claude/skills/$AGENT"
    INIT_SCRIPT="$SKILL_PATH/scripts/init-sanctum.py"
    if [ -f "$INIT_SCRIPT" ]; then
        python3 "$INIT_SCRIPT" "$TARGET" "$SKILL_PATH" 2>&1 | sed 's/^/  /'
        echo ""
    else
        echo "  WARNING: $INIT_SCRIPT not found, skipping"
    fi
done

# --- Git init (optional) ---

if [ ! -d "$TARGET/.git" ]; then
    echo "Initializing git repository..."
    (cd "$TARGET" && git init -q && echo ".DS_Store" > .gitignore)
    echo "  Git initialized."
fi

# --- Done ---

echo ""
echo "=== Done ==="
echo ""
echo "Your Knowledge Base '$KB_NAME' is ready at:"
echo "  $TARGET"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET"
echo "  2. Open the folder as an Obsidian vault"
echo "  3. Run 'claude' to start — each agent will greet you on first activation"
echo ""
echo "Drop sources into raw/articles/ or raw/papers/, then ask the Ingest Agent"
echo "to process them. Or just say 'scan for new sources' — it finds them automatically."
