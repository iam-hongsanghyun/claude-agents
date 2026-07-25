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
| [`agents/`](./agents/) | 21 user-level subagents auto-installed to `~/.claude/agents/` (see below). |
| [`scripts/claude-scaffold.sh`](./scripts/claude-scaffold.sh) | Bootstrap a new project from these templates. |
| [`scripts/sync-to-local.sh`](./scripts/sync-to-local.sh) | Pull updates from this repo into `~/.claude/{templates,agents}/`. |
| [`settings.json.example`](./settings.json.example) | Claude Code SessionStart hook to auto-create `CLAUDE.md` in new git repos. |

---

## Subagents (user-level — available in every Claude Code session)

After running `scripts/install.sh` or `scripts/sync-to-local.sh`, all 21 agents are installed to `~/.claude/agents/` and available in every project — no per-project setup needed.

See [`agents/README.md`](./agents/README.md) for the full role reference and disambiguation guide.

### Tier 0 — Engagement governance

For work bound by a **contract, proposal, or funding agreement**. All artefacts live under `claude-docs/` in the project.

| Agent | When to use |
|---|---|
| [`research-director`](./agents/research-director.md) | Own the research design and its governance. Contract/proposal is the truth source → `charter.md` → phases (purpose, objectives, deliverables) → stages (the actual activities, many-to-many to phases) → process (general + one per stage: how, when to stop, when to repeat, data handling, referencing, methodology) → toolbox → one live `tracker.md` → team roster, writing new agents only for real capability gaps. Five passes: Inception, Design, Conformance, Tracking, Team. |
| [`consultant`](./agents/consultant.md) | The only customer-facing role. Engagement (inception, progress meetings, data requests, review rounds, change control, delay notice) and plain-language translation the client can present without you. Never sends anything; never accepts scope. |
| [`report-manager`](./agents/report-manager.md) | Governance pass (tracker freshness, figure gating, unserved objectives, traceability, process conformance, directory hygiene, gate integrity, claimed-vs-actual) → self-contained HTML progress and team dashboards under `claude-docs/dashboard/`. Reads the documents, never edits them. |

### Tier 1 — Workflow orchestration

| Agent | When to use |
|---|---|
| [`planner-and-qc-lead`](./agents/planner-and-qc-lead.md) | Start of any non-trivial task. Plans, decomposes, produces QC checklist, routes to other agents. Does not write code or research. |

### Tier 2 — Code: writing & review

| Agent | When to use |
|---|---|
| [`developer`](./agents/developer.md) | Implement features, refactor, write inline docstrings. Enforces CLAUDE.md: type hints, `Algorithm:` (LaTeX + ASCII), `uv`/`ruff`/`mypy`/`pytest`, `pint`, reproducible seeds. **Not** React/TS UI (→ `frontend-developer`). |
| [`frontend-developer`](./agents/frontend-developer.md) | React + TypeScript + Vite browser clients: React Flow canvases, Leaflet / d3-geo maps, data grids, SVG charts, resizable rails. Honors existing layout/design contract, reuses CSS, keeps the backend↔frontend type contract exact, no icons/emojis. |
| [`tester`](./agents/tester.md) | Mechanical build gate after any change, before review — type-check (`tsc`/`mypy`), compile, lint on a plain `ruff check .`, emoji/icon scan, tests. Pass/fail only, no judgment. |
| [`reviewer`](./agents/reviewer.md) | Judgment review of a diff against the one task asked: APPROVE/REJECT on scope creep, duplication, hardcoded domain data, broken contract, icons/emojis. Assumes `tester` ran first. |
| [`math-reviewer`](./agents/math-reviewer.md) | Whenever math/numerics change. Cross-checks code vs `Algorithm:` docstring vs `ALGORITHM.md`. Stability, sign conventions, indexing, tolerances, edge cases. **Read-only.** |
| [`auditor`](./agents/auditor.md) | Pre-merge: no hardcoded values, config externalized, `pint` at boundaries, doc/code alignment, tooling clean. **Read-only.** |
| [`refactor-architect`](./agents/refactor-architect.md) | Restructure code without changing behavior. Extract, deduplicate, reduce coupling, remove dead code. Tests stay green. |
| [`debugger`](./agents/debugger.md) | Bugs — crashes, wrong outputs, flaky tests. Reproduce → isolate → fix (root cause, not symptom). |

### Tier 3 — Code: domain specialists

| Agent | When to use |
|---|---|
| [`data-scientist`](./agents/data-scientist.md) | EDA, ML, experiment analysis **in code**. Schema/dtype/unit alignment; file-format best practice (parquet > CSV). |
| [`optimization-modeller`](./agents/optimization-modeller.md) | LP/MILP/NLP code: PyPSA, linopy, pyomo, cvxpy. Formulation, infeasibility debugging, solver tuning. **Not** energy market research (→ `energy-finance-team`). |
| [`gis-analyst`](./agents/gis-analyst.md) | Geospatial code: geopandas, shapely, rasterio, xarray. CRS audits, spatial-join pitfalls, raster/vector mismatches. |
| [`data-collector`](./agents/data-collector.md) | Build ingestion pipelines in code (OpenDART, Yahoo Finance, KOSIS, news APIs). Polite scraping, schema validation (pydantic/pandera), idempotent storage. **Not** ad-hoc research (→ research teams). |
| [`visualizer`](./agents/visualizer.md) | Charts, maps, dashboards in code: matplotlib, seaborn, plotly, folium, pydeck. Publication-ready figures. |
| [`doc-writer`](./agents/doc-writer.md) | **Code-facing docs only**: README, CLI manuals, tutorials, troubleshooting, ARCHITECTURE.md. **Not** research reports/memos (→ `writing-support-team`). |

### Tier 4 — Research & analysis (no code)

| Agent | When to use |
|---|---|
| [`energy-finance-team`](./agents/energy-finance-team.md) | Energy markets, ESG, climate finance, energy policy research → structured report. Uses web search, Yahoo Finance, DART. |
| [`investment-asset-team`](./agents/investment-asset-team.md) | Portfolio, equity, bond/credit, risk analysis → structured investment report. Uses Yahoo Finance, DART, web research. |
| [`writing-support-team`](./agents/writing-support-team.md) | Research reports, white papers, policy briefs, memos, presentations. **Not** code-facing docs (→ `doc-writer`). |

> Tier 4 teams are structured by **function, not named personas**, and share an analytical-integrity discipline: understand before you build the deliverable; correlation not causation ("areas to explore," never "X caused Y"); dollars alongside percentages; explicit coverage/sample/unit caveats; provenance and change-logs; state AI use; gate figures `[verified]` vs `[compute]`.

### Quick disambiguation

| Task | Agent |
|---|---|
| Set up or govern a contracted research engagement | `research-director` |
| Draft anything the customer will read | `consultant` |
| Build the progress / team dashboard | `report-manager` |
| Research / find information about energy, ESG, climate | `energy-finance-team` |
| Research / find information about stocks, portfolio, bonds | `investment-asset-team` |
| Write a report, memo, or presentation | `writing-support-team` |
| Write README / CLI docs / tutorial | `doc-writer` |
| Implement Python code | `developer` |
| Build a data-ingestion pipeline in code | `data-collector` |
| Analyse data in code (EDA, ML) | `data-scientist` |
| Write optimization model code | `optimization-modeller` |
| Write a chart in code | `visualizer` |

### Recommended flows

```
# Contracted / funded research engagement
research-director (Inception → charter, confirm with user)
                  →  research-director (Design: phases, stages, process, toolbox)
                  →  research-director (Team: roster, new agents for real gaps)
                  →  consultant        (inception pack, data + decision requests)
per stage:  stage owners  →  review chain  →  research-director (Tracking)
                                           →  report-manager   (governance + dashboards)
at each gate: research-director (Conformance)  →  report-manager  →  consultant

# Feature development
planner-and-qc-lead  →  developer / frontend-developer
                     →  math-reviewer     (if math changed)
                     →  data-scientist    (if data I/O changed)
                     →  visualizer        (if charts involved)
                     →  tester            (mechanical gate)
                     →  reviewer          (judgment gate, before commit)
                     →  auditor           (before merge)

# Bug fix
debugger  →  developer / frontend-developer  →  tester  →  reviewer  →  auditor

# Refactor
refactor-architect  →  auditor

# Research → report
energy-finance-team  or  investment-asset-team  →  writing-support-team

# Data pipeline
data-collector  →  data-scientist  →  developer
```

### Invoking from Claude Code

```
> Use the research-director subagent to read the contract and proposal and build the charter.
> Use the research-director subagent to run a tracking pass.
> Use the report-manager subagent to rebuild the progress and team dashboards.
> Use the consultant subagent to draft the inception agenda and the data request list.
> Use the planner-and-qc-lead subagent to plan adding radiative forcing.
> Use the developer subagent to implement it in src/ebm/core/forcing.py.
> Use the math-reviewer subagent on src/ebm/core/forcing.py.
> Use the optimization-modeller subagent on simplePyPSA_KR/network.py.
> Use the gis-analyst subagent on the spatial join in gisanalysis/process.py.
> Use the visualizer subagent to fix the legend in pypsa_gui/charts.py.
> Use the frontend-developer subagent to add a resizable properties rail in frontend/pathwise.
> Use the tester subagent on the changed files, then the reviewer subagent on the diff.
> Use the auditor subagent on this branch before I merge.
> Use the energy-finance-team subagent to research Korean offshore wind policy.
> Use the investment-asset-team subagent to analyze KEPCO's debt profile.
> Use the writing-support-team subagent to draft a policy brief on carbon markets.
> Use the data-collector subagent to build a DART filing ingestion pipeline.
> Use the doc-writer subagent to write the CLI manual for scripts/run_model.py.
```

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
