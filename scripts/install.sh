#!/usr/bin/env bash
# install.sh — first-time setup on a new machine
#
# Run after cloning the repo:
#   git clone https://github.com/iam-hongsanghyun/claude-md.git ~/github/claude-md
#   ~/github/claude-md/scripts/install.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Installing claude-md templates"

# 1. Sync templates to ~/.claude/templates/
"$REPO_DIR/scripts/sync-to-local.sh"

# 2. Install SessionStart hook into ~/.claude/settings.json
SETTINGS="$HOME/.claude/settings.json"
HOOK_CMD='[ -d .git ] && [ ! -f CLAUDE.md ] && cp ~/.claude/templates/CLAUDE.md CLAUDE.md 2>/dev/null; true'

if [ ! -f "$SETTINGS" ]; then
    echo "==> creating $SETTINGS"
    mkdir -p "$(dirname "$SETTINGS")"
    cp "$REPO_DIR/settings.json.example" "$SETTINGS"
    echo "    written from settings.json.example"
elif command -v jq >/dev/null 2>&1 && jq -e '.hooks.SessionStart' "$SETTINGS" >/dev/null 2>&1; then
    if jq -e --arg cmd "$HOOK_CMD" '.hooks.SessionStart[].hooks[] | select(.command == $cmd)' "$SETTINGS" >/dev/null 2>&1; then
        echo "==> hook already installed in $SETTINGS"
    else
        echo "==> SessionStart hooks exist; merge manually from settings.json.example"
        echo "    (refusing to clobber existing hooks)"
    fi
else
    echo "==> $SETTINGS exists but has no SessionStart hooks — merge manually"
    echo "    See settings.json.example for the snippet to add"
fi

echo ""
echo "Done. Restart Claude Code so the hook watcher picks up changes."
