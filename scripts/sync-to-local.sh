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
# Only copies our named agents — won't touch other agents you have at ~/.claude/agents/.
AGENTS=(
    # Tier 1: Workflow orchestration
    planner-and-qc-lead
    # Tier 2: Code — writing & review
    developer
    frontend-developer
    tester
    reviewer
    math-reviewer
    auditor
    refactor-architect
    debugger
    # Tier 3: Code — domain specialists
    data-scientist
    optimization-modeller
    gis-analyst
    data-collector
    visualizer
    doc-writer
    # Tier 4: Research & analysis (no code)
    energy-finance-team
    investment-asset-team
    writing-support-team
)
for agent in "${AGENTS[@]}"; do
    if [ -f "$REPO_DIR/agents/$agent.md" ]; then
        cp "$REPO_DIR/agents/$agent.md" "$AGENTS_DEST/$agent.md"
    fi
done

echo "    templates  -> $DEST/"
echo "    scaffold   -> $SCRIPTS_DEST/claude-scaffold.sh"
echo "    agents     -> $AGENTS_DEST/ (${#AGENTS[@]} agents)"
echo ""
echo "Done."
