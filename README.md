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
| [`agents/`](./agents/) | 5 user-level subagents auto-installed to `~/.claude/agents/` (see below). |
| [`scripts/claude-scaffold.sh`](./scripts/claude-scaffold.sh) | Bootstrap a new project from these templates. |
| [`scripts/sync-to-local.sh`](./scripts/sync-to-local.sh) | Pull updates from this repo into `~/.claude/{templates,agents}/`. |
| [`settings.json.example`](./settings.json.example) | Claude Code SessionStart hook to auto-create `CLAUDE.md` in new git repos. |

---

## Subagents (user-level — available in every Claude Code session)

After running `scripts/install.sh` or `scripts/sync-to-local.sh`, all 12 agents are installed to `~/.claude/agents/` and available in every project — no per-project setup needed.

### Core team (always-applicable workflow agents)

| Agent | When to use |
|---|---|
| [`planner-and-qc-lead`](./agents/planner-and-qc-lead.md) | At the start of any non-trivial task. Plans, decomposes, produces a tailored QC checklist, routes work to other subagents. Does not write code. |
| [`developer`](./agents/developer.md) | Implementation, refactoring, documenting code. Follows CLAUDE.md: type hints, Google docstrings with `Algorithm:` (LaTeX + ASCII), `uv`/`ruff`/`mypy`/`pytest`, no hardcoded values, `pint` units, reproducible seeds. |
| [`math-reviewer`](./agents/math-reviewer.md) | Whenever math/numerics change. Cross-checks code vs docstring `Algorithm:`, `ALGORITHM.md`, references. Validates stability, sign conventions, indexing, tolerances, edge cases. Read-only. |
| [`auditor`](./agents/auditor.md) | End-to-end pre-merge review. No hardcoded values, externalized config, `pint` units at boundaries, doc/code alignment, project layout, tooling clean. Read-only. |
| [`data-scientist`](./agents/data-scientist.md) | EDA + ML + experiment analysis. **Specifically**: input/output data alignment (schemas, units, dtypes, time zones) + file-format best practice (parquet > CSV for numerical data, etc.). |

### Domain specialists (use as needed)

| Agent | When to use |
|---|---|
| [`visualizer`](./agents/visualizer.md) | Charts, maps, dashboards. matplotlib / seaborn / plotly / folium / pydeck. Catches legend-off-canvas, log-scale-zeros, twin-axis, color-blind-unsafe palettes; produces publication-ready figures. |
| [`optimization-modeller`](./agents/optimization-modeller.md) | LP / MILP / NLP. PyPSA, linopy, pyomo, cvxpy. Formulation correctness, infeasibility debugging, solver tuning, duality interpretation. Distinct from `energy-finance-team` (research, not code). |
| [`gis-analyst`](./agents/gis-analyst.md) | Geospatial work — geopandas, shapely, rasterio, xarray. Catches CRS bugs (#1 source of GIS errors), spatial-join pitfalls, raster/vector mismatches, choropleth binning issues. |
| [`data-collector`](./agents/data-collector.md) | Web scraping, API ingestion (OpenDART, Yahoo Finance, news APIs, KOSIS, government open data). Polite scraping, retries, schema validation (pydantic/pandera), idempotent storage. |
| [`debugger`](./agents/debugger.md) | Diagnosing bugs — crashes, wrong outputs, flaky tests. Reproduce → isolate → fix. Bisecting, hypothesis-driven log inspection, root-cause analysis (not symptom patching). |
| [`refactor-architect`](./agents/refactor-architect.md) | Restructure existing code without changing behavior. Extract to utils, deduplicate, reduce coupling, remove dead code, simplify over-abstractions. Tests stay green at every step. |
| [`doc-writer`](./agents/doc-writer.md) | Code-facing docs: README, CLI manuals, tutorials, troubleshooting. **Not** for research reports (use `writing-support-team`) or docstrings (use `developer`). Diátaxis-aware. |

### Recommended flow

```
planner-and-qc-lead   →   developer / domain specialist
                      →   math-reviewer       (if math changed)
                      →   data-scientist      (if data I/O changed)
                      →   visualizer          (if any chart involved)
                      →   auditor             (before merge)
```

When the bug is the problem, route differently:

```
debugger (reproduce, isolate)   →   developer (apply fix)   →   auditor
```

When the goal is restructuring (no behavior change):

```
refactor-architect (plan + execute)   →   auditor (verify no regression)
```

### Invoking from Claude Code

```
> Use the planner-and-qc-lead subagent to plan adding radiative forcing.
> Use the optimization-modeller subagent on simplePyPSA_KR/network.py.
> Use the gis-analyst subagent on the spatial join in gisanalysis/process.py.
> Use the visualizer subagent to fix the legend in pypsa_gui/charts.py.
> Use the math-reviewer subagent on src/ebm/core/forcing.py.
> Use the auditor subagent on this branch before I merge.
```

### Coexistence with your existing research / writing agents

These code-facing agents are designed to **complement**, not replace, your existing `energy-finance-team`, `investment-asset-team`, and `writing-support-team` agents:

| Task | Agent |
|---|---|
| Research / market analysis / reports | `energy-finance-team`, `investment-asset-team` |
| Formal reports, memos, presentations | `writing-support-team` |
| Build / debug / refactor / optimize **code** | the agents in this pack |
| Code-facing docs (README, CLI manual, tutorial) | `doc-writer` (this pack) |

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
