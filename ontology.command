#!/usr/bin/env bash
# ontology.command — regenerate the agent ontology and open the interactive map.
#
# Double-click this file in Finder. No terminal, no arguments.
# Falls back to opening the existing page if the generator cannot run.

set -uo pipefail

# Finder launches with an arbitrary cwd; resolve our own directory first.
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
REPO_DIR="$PWD"
PAGE="$REPO_DIR/agents/ontology.html"

echo "==> agent ontology"
echo "    repo: $REPO_DIR"
echo ""

regenerated=0
if command -v uv >/dev/null 2>&1; then
    echo "==> regenerating from agents/ontology.yaml"
    if uv run --no-project --with pyyaml python scripts/render_ontology.py \
       && uv run --no-project --with pyyaml python scripts/render_ontology_html.py; then
        regenerated=1
    else
        echo "    generator failed — opening the existing page instead" >&2
    fi
elif python3 -c "import yaml" >/dev/null 2>&1; then
    echo "==> regenerating (system python3 + PyYAML)"
    if python3 scripts/render_ontology.py && python3 scripts/render_ontology_html.py; then
        regenerated=1
    else
        echo "    generator failed — opening the existing page instead" >&2
    fi
else
    echo "    uv not installed and PyYAML unavailable — skipping regeneration."
    echo "    Install uv from https://docs.astral.sh/uv/ to refresh the page."
fi

if [ ! -f "$PAGE" ]; then
    echo ""
    echo "ERROR: $PAGE does not exist and could not be generated." >&2
    echo "Install uv, then run: uv run --no-project --with pyyaml python scripts/render_ontology_html.py" >&2
    echo ""
    read -r -p "Press Return to close."
    exit 1
fi

[ "$regenerated" -eq 1 ] && echo "    up to date"
echo ""
echo "==> opening $PAGE"
open "$PAGE"
