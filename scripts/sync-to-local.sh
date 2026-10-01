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
# Project-scoped agents under agents/project/ are deliberately NOT synced: they belong to a
# single engagement, not every session. See agents/project/README.md.
AGENTS=(
    # Governance
    research-director consultant report-manager log-reporter result-reporter
    # Orchestration
    planner-and-qc-lead
    # Code and gates
    developer web-developer debugger tester reviewer math-reviewer provenance-auditor
    # Modelling
    data-scientist econometrician optimization-modeller system-dynamics-modeller
    computational-economist renewable-resource-scientist climate-risk-modeller gis-analyst
    # Data, output, platform
    data-collector visualizer doc-writer
    mcp-server-engineer agent-app-engineer plugin-framework-architect app-distribution-engineer
    # Research (no code)
    data-scout energy-finance-team investment-asset-team esg-disclosure-analyst
    policy-analyst transport-emissions-reviewer writing-support-team
)
# Agents removed from the pack; deleted from ~/.claude/agents so stale copies stop routing.
RETIRED=(
    auditor refactor-architect frontend-developer web-app-engineer
    kr-power-data-scout ir-disclosure-analyst source-reconciliation-analyst
)
for agent in "${RETIRED[@]}"; do
    rm -f "$AGENTS_DEST/$agent.md"
done
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
