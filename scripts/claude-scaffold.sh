#!/usr/bin/env bash
# claude-scaffold.sh — bootstrap a project from ~/.claude/templates/
#
# Usage: run from inside a project root (must be a git repo).
#   ~/.claude/scripts/claude-scaffold.sh [package_name]
#
# Won't overwrite existing files. Safe to re-run.

set -euo pipefail

TEMPLATES="$HOME/.claude/templates"
PKG_NAME="${1:-}"

if [ ! -d "$TEMPLATES" ]; then
    echo "ERROR: $TEMPLATES not found." >&2
    exit 1
fi

if [ ! -d ".git" ]; then
    echo "ERROR: not a git repo. Run 'git init' first." >&2
    exit 1
fi

# Default package name from directory if not given
if [ -z "$PKG_NAME" ]; then
    PKG_NAME=$(basename "$PWD" | tr '-' '_' | tr '[:upper:]' '[:lower:]')
fi

echo "==> scaffolding into $(pwd) (package: $PKG_NAME)"

copy_if_missing() {
    local src="$1"
    local dst="$2"
    if [ -e "$dst" ]; then
        echo "    skip   $dst (exists)"
    else
        mkdir -p "$(dirname "$dst")"
        cp "$src" "$dst"
        echo "    create $dst"
    fi
}

# Top-level files
copy_if_missing "$TEMPLATES/CLAUDE.md"           "CLAUDE.md"
copy_if_missing "$TEMPLATES/.gitignore"          ".gitignore"
copy_if_missing "$TEMPLATES/.env.example"        ".env.example"
copy_if_missing "$TEMPLATES/pyproject.toml"      "pyproject.toml"

# docs
copy_if_missing "$TEMPLATES/docs/HANDBOOK.md"    "docs/HANDBOOK.md"

# CI
copy_if_missing "$TEMPLATES/.github/workflows/ci.yml" ".github/workflows/ci.yml"

# Source layout
mkdir -p "src/$PKG_NAME/core" "src/$PKG_NAME/data" "tests/fixtures"
[ -f "src/$PKG_NAME/__init__.py" ]      || echo '__version__ = "0.1.0"' > "src/$PKG_NAME/__init__.py"
[ -f "src/$PKG_NAME/core/__init__.py" ] || : > "src/$PKG_NAME/core/__init__.py"
[ -f "src/$PKG_NAME/data/__init__.py" ] || : > "src/$PKG_NAME/data/__init__.py"
[ -f "tests/__init__.py" ]              || : > "tests/__init__.py"
[ -f "tests/conftest.py" ]              || : > "tests/conftest.py"

# Replace project_name placeholder in pyproject.toml (only on first scaffold)
if [ -f "pyproject.toml" ] && grep -q '"project_name"' pyproject.toml; then
    if [ "$(uname)" = "Darwin" ]; then
        sed -i '' "s/project_name/$PKG_NAME/g" pyproject.toml
    else
        sed -i "s/project_name/$PKG_NAME/g" pyproject.toml
    fi
    echo "    update pyproject.toml (project_name -> $PKG_NAME)"
fi

echo ""
echo "Done. Next steps:"
echo "  1. uv venv && uv sync --all-extras"
echo "  2. write src/$PKG_NAME/config.py and logger.py (templates in docs/HANDBOOK.md)"
echo "  3. write docs/ALGORITHM.md"
echo "  4. git add . && git commit -m 'chore: initial commit from team template'"
