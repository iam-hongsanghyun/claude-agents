#!/usr/bin/env bash
# sync-to-local.sh — push templates from this repo to ~/.claude/templates/
#
# Run after pulling updates from GitHub:
#   git pull && ./scripts/sync-to-local.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.claude/templates"
SCRIPTS_DEST="$HOME/.claude/scripts"
AGENTS_DEST="$HOME/.claude/agents"

echo "==> syncing $REPO_DIR -> $DEST and $AGENTS_DEST"
mkdir -p "$DEST/docs" "$DEST/.github/workflows" "$SCRIPTS_DEST" "$AGENTS_DEST"

# --- templates ---
cp "$REPO_DIR/CLAUDE.md"                          "$DEST/CLAUDE.md"
cp "$REPO_DIR/docs/HANDBOOK.md"                   "$DEST/docs/HANDBOOK.md"
cp "$REPO_DIR/pyproject.toml"                     "$DEST/pyproject.toml"
cp "$REPO_DIR/.env.example"                       "$DEST/.env.example"
cp "$REPO_DIR/.gitignore"                         "$DEST/.gitignore"
cp "$REPO_DIR/.github/workflows/ci.yml"           "$DEST/.github/workflows/ci.yml"

# --- scripts ---
cp "$REPO_DIR/scripts/claude-scaffold.sh"         "$SCRIPTS_DEST/claude-scaffold.sh"
chmod +x "$SCRIPTS_DEST/claude-scaffold.sh"

# --- subagents (user-level: available in every Claude Code session) ---
# Only copies our 5 named agents — won't touch other agents you have.
for agent in planner-and-qc-lead developer math-reviewer auditor data-scientist; do
    if [ -f "$REPO_DIR/agents/$agent.md" ]; then
        cp "$REPO_DIR/agents/$agent.md" "$AGENTS_DEST/$agent.md"
    fi
done

echo "    templates  -> $DEST/"
echo "    scaffold   -> $SCRIPTS_DEST/claude-scaffold.sh"
echo "    agents     -> $AGENTS_DEST/{planner-and-qc-lead,developer,math-reviewer,auditor,data-scientist}.md"
echo ""
echo "Done."
