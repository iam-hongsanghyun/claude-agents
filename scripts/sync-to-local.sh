#!/usr/bin/env bash
# sync-to-local.sh — push templates from this repo to ~/.claude/templates/
#
# Run after pulling updates from GitHub:
#   git pull && ./scripts/sync-to-local.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.claude/templates"
SCRIPTS_DEST="$HOME/.claude/scripts"

echo "==> syncing $REPO_DIR -> $DEST"
mkdir -p "$DEST/docs" "$DEST/.github/workflows" "$SCRIPTS_DEST"

cp "$REPO_DIR/CLAUDE.md"                          "$DEST/CLAUDE.md"
cp "$REPO_DIR/docs/HANDBOOK.md"                   "$DEST/docs/HANDBOOK.md"
cp "$REPO_DIR/pyproject.toml"                     "$DEST/pyproject.toml"
cp "$REPO_DIR/.env.example"                       "$DEST/.env.example"
cp "$REPO_DIR/.gitignore"                         "$DEST/.gitignore"
cp "$REPO_DIR/.github/workflows/ci.yml"           "$DEST/.github/workflows/ci.yml"

cp "$REPO_DIR/scripts/claude-scaffold.sh"         "$SCRIPTS_DEST/claude-scaffold.sh"
chmod +x "$SCRIPTS_DEST/claude-scaffold.sh"

echo "    CLAUDE.md           -> $DEST/CLAUDE.md"
echo "    docs/HANDBOOK.md    -> $DEST/docs/HANDBOOK.md"
echo "    pyproject.toml      -> $DEST/pyproject.toml"
echo "    .env.example        -> $DEST/.env.example"
echo "    .gitignore          -> $DEST/.gitignore"
echo "    .github/workflows/  -> $DEST/.github/workflows/ci.yml"
echo "    scripts/scaffold    -> $SCRIPTS_DEST/claude-scaffold.sh"
echo ""
echo "Done."
