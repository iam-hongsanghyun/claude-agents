# claude-md

Personal Claude Code template & convention pack for **scientific modelling** projects (data science, energy, finance, economic modelling).

This repo is the source of truth. Local working copy at `~/.claude/templates/` is synced from here.

---

## What's in here

| Path | Purpose |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Slim Claude-context file (~3KB). Auto-loaded by Claude Code in any project. |
| [`docs/HANDBOOK.md`](./docs/HANDBOOK.md) | Full team handbook (humans). Tooling rationale, templates, examples. |
| [`pyproject.toml`](./pyproject.toml) | Modern Python config: `uv` + `ruff` + `mypy` + `pytest`. |
| [`.env.example`](./.env.example) | Environment variable template (incl. `RANDOM_SEED`). |
| [`.gitignore`](./.gitignore) | Python + scientific-stack ignores (`data/`, `mlruns/`, `*.parquet`, etc.). |
| [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) | uv-based CI (Python 3.11 + 3.12). |
| [`scripts/claude-scaffold.sh`](./scripts/claude-scaffold.sh) | Bootstrap a new project from these templates. |
| [`scripts/sync-to-local.sh`](./scripts/sync-to-local.sh) | Pull updates from this repo into `~/.claude/templates/`. |
| [`settings.json.example`](./settings.json.example) | Claude Code SessionStart hook to auto-create `CLAUDE.md` in new git repos. |

---

## How it's wired up locally

1. **Templates** live at `~/.claude/templates/` (synced from this repo)
2. **Scaffold script** at `~/.claude/scripts/claude-scaffold.sh`
3. **SessionStart hook** in `~/.claude/settings.json` auto-creates `CLAUDE.md` when Claude Code starts in a git repo:

   ```bash
   [ -d .git ] && [ ! -f CLAUDE.md ] && cp ~/.claude/templates/CLAUDE.md CLAUDE.md
   ```

   Guards:
   - Only fires in **git repos** (won't pollute random dirs like `~/`, `/tmp`)
   - Only creates if `CLAUDE.md` is **missing** (won't overwrite project-specific edits)

---

## Usage

### Brand-new project (full scaffolding)

```bash
mkdir my-project && cd my-project
git init
~/.claude/scripts/claude-scaffold.sh my_pkg
uv venv && uv sync --all-extras
```

This creates the full src layout, renames `project_name` → `my_pkg` in `pyproject.toml`, and seeds `tests/`, `docs/`, `.env.example`, CI, gitignore.

### Existing project (just CLAUDE.md)

When you start `claude` in an existing git repo, the hook drops `CLAUDE.md` in automatically. Or manually:

```bash
cp ~/.claude/templates/CLAUDE.md .
```

### Customizing per-project

`CLAUDE.md` is a starting point. Edit it freely per-project — the hook won't overwrite an existing file.

---

## Bootstrapping on a new machine

```bash
git clone https://github.com/iam-hongsanghyun/claude-md.git ~/github/claude-md
~/github/claude-md/scripts/install.sh   # syncs to ~/.claude/templates/, installs hook
```

(See `scripts/install.sh`.)

---

## Conventions captured

- **Python 3.11+** with mandatory type hints (mypy strict)
- **`ruff`** for lint + format (replaces flake8 + black + isort)
- **`uv`** for package management (replaces pip + venv + pip-tools)
- **`pyproject.toml`** as single source of truth (no `setup.py`, no `requirements.txt`)
- **Reproducibility**: `numpy.random.default_rng(seed)`, lockfile committed
- **Units**: `pint` for physical quantities at module boundaries
- **Math**: single-letter variables allowed in `core/` when they mirror equations; `Algorithm:` section in docstrings with LaTeX + ASCII fallback
- **Numerical correctness**: regression tests against analytical solutions over arbitrary line-coverage targets
- **Git**: feature branch → PR → CI green → squash-merge → delete branch; conventional commits

See [`docs/HANDBOOK.md`](./docs/HANDBOOK.md) for the full rationale and ready-to-copy code (`config.py`, `logger.py`, docstring template, PR template, etc.).

---

## License

MIT — use, fork, modify freely.
