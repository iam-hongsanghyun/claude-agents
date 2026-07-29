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
| [`agents/`](./agents/) | 36 user-level subagents auto-installed to `~/.claude/agents/` (see below). |
| [`scripts/claude-scaffold.sh`](./scripts/claude-scaffold.sh) | Bootstrap a new project from these templates. |
| [`scripts/sync-to-local.sh`](./scripts/sync-to-local.sh) | Pull updates from this repo into `~/.claude/{templates,agents}/`. |
| [`agents/ontology.yaml`](./agents/ontology.yaml) | The agent ontology — tiers, nodes, typed edges, workflows. Source of truth for agent relationships. |
| [`agents/ontology.html`](./agents/ontology.html) | Interactive ontology map (generated, self-contained, offline). Open via [`ontology.command`](./ontology.command). |
| [`agents/project/`](./agents/project/README.md) | Registry of project-authored agents — mirrored for visibility, **not** installed globally. |
| [`settings.json.example`](./settings.json.example) | Claude Code SessionStart hook to auto-create `CLAUDE.md` in new git repos. |

---

## Subagents (user-level — available in every Claude Code session)

After running `scripts/install.sh` or `scripts/sync-to-local.sh`, all 36 agents are installed to `~/.claude/agents/` and available in every project — no per-project setup needed.

See [`agents/README.md`](./agents/README.md) for the full role reference and disambiguation guide.

- Relationships between agents (tiers, hand-offs, gates, routing boundaries) live in the machine-readable [`agents/ontology.yaml`](./agents/ontology.yaml), rendered to [`agents/ONTOLOGY.md`](./agents/ONTOLOGY.md) and to an interactive map, [`agents/ontology.html`](./agents/ontology.html) — self-contained and offline, with every agent's full role and routing boundaries. **Double-click [`ontology.command`](./ontology.command)** to regenerate both and open the map.
- Project-authored agents (created inside a single engagement by `research-director`, **not** installed globally) are registered in [`agents/project/README.md`](./agents/project/README.md).

### Tier 0 — Engagement governance

For work bound by a **contract, proposal, or funding agreement**. All artefacts live under `claude-docs/` in the project.

| Agent | When to use |
|---|---|
| [`research-director`](./agents/research-director.md) | Own the research design and its governance. Contract/proposal is the truth source → `charter.md` → phases (purpose, objectives, deliverables) → stages (the actual activities, many-to-many to phases) → process (general + one per stage: how, when to stop, when to repeat, data handling, referencing, methodology) → toolbox → one live `tracker.md` → team roster, writing new agents only for real capability gaps. Six passes: Inception, Design, Conformance, Tracking, Team, **Refresh**. Refresh is the re-run pass: after any data or logic update it fingerprints every stage's declared inputs, re-runs only the stages that actually changed **plus their transitive downstream closure** (the chain reaction), skips the rest only where a fingerprint proves them unchanged, re-arms the verification gates on anything re-run, and iterates to a fixpoint — then writes a project `<project>-refresh` **skill** so the next re-run is one invocation. **Interim reporting** is not a pass but a step-by-step responsibility it *defines and gates* rather than writes: two families per unit under `claude-docs/reports/` — a **log report** (`log-reporter`: what was done, what failed) and a **result report** (`result-reporter`: the analysis as a journal article, with a conference-presentation deck and figures). It never fills a results table, marks a number `[verified]`, or writes HTML. |
| [`consultant`](./agents/consultant.md) | The only customer-facing role. Engagement (inception, progress meetings, data requests, review rounds, change control, delay notice) and plain-language translation the client can present without you. Never sends anything; never accepts scope. |
| [`log-reporter`](./agents/log-reporter.md) | The **log report** per unit — what was done and what failed: commands, environment, seeds, input/output fingerprints, dead ends and abandoned approaches, deviations, timing, the one reproduction command, and the handoff. *A log with no failures recorded is a log nobody kept.* |
| [`result-reporter`](./agents/result-reporter.md) | The **result report** per unit — the analysis as a journal article: why it was conducted, data-handling result (rows in/out, drops, join match rates), descriptive statistics, methods, and results carried by figures with every number gated and ranged. Its `.html` is a **conference presentation**, not the article reflowed. This family travels to the client. |
| [`report-manager`](./agents/report-manager.md) | Governance pass (tracker freshness, figure gating, unserved objectives, traceability, process conformance, directory hygiene, gate integrity, claimed-vs-actual) → self-contained HTML progress and team dashboards under `claude-docs/dashboard/`. Reads the documents, never edits them. |

### Tier 1 — Workflow orchestration

| Agent | When to use |
|---|---|
| [`planner-and-qc-lead`](./agents/planner-and-qc-lead.md) | Start of any non-trivial task. Plans, decomposes, produces QC checklist, routes to other agents. Does not write code or research. |

### Tier 2 — Code: writing & review

| Agent | When to use |
|---|---|
| [`developer`](./agents/developer.md) | Implement features, refactor, write inline docstrings. Enforces CLAUDE.md: type hints, `Algorithm:` (LaTeX + ASCII), `uv`/`ruff`/`mypy`/`pytest`, `pint`, reproducible seeds. **Not** React/TS UI (→ `frontend-developer`). |
| [`frontend-developer`](./agents/frontend-developer.md) | The **rich** React + TypeScript + Vite browser client: React Flow canvases, Leaflet / d3-geo maps, data grids, SVG charts, resizable rails. Honors existing layout/design contract, reuses CSS, keeps the backend↔frontend type contract exact, no icons/emojis. **Not** no-build vanilla-JS/d3 web apps & thin backends (→ `web-app-engineer`). |
| [`web-app-engineer`](./agents/web-app-engineer.md) | No-build, framework-less web apps end to end: vanilla-JS + d3 (topojson/world-atlas) or KaTeX single-file frontends, a thin FastAPI/uvicorn or stdlib `http.server` JSON backend serving the SPA (SQLite or Supabase/Postgres), static/Vercel/Netlify deploy. Owns the backend↔frontend JSON contract for these apps; the portfolio's dominant web idiom. **Not** rich React+TS+Vite GUIs (→ `frontend-developer`), scientific Python core (→ `developer`), MCP surface (→ `mcp-server-engineer`), desktop launchers (→ `app-distribution-engineer`). |
| [`tester`](./agents/tester.md) | Mechanical build gate after any change, before review — type-check (`tsc`/`mypy`), compile, lint on a plain `ruff check .`, emoji/icon scan, tests. Pass/fail only, no judgment. |
| [`reviewer`](./agents/reviewer.md) | Judgment review of a diff against the one task asked: APPROVE/REJECT on scope creep, duplication, hardcoded domain data, broken contract, icons/emojis. Assumes `tester` ran first. |
| [`math-reviewer`](./agents/math-reviewer.md) | Whenever math/numerics change. Cross-checks code vs `Algorithm:` docstring vs `ALGORITHM.md`. Stability, sign conventions, indexing, tolerances, edge cases. **Read-only.** |
| [`auditor`](./agents/auditor.md) | Pre-merge: no hardcoded values, config externalized, `pint` at boundaries, doc/code alignment, tooling clean. **Read-only.** |
| [`provenance-auditor`](./agents/provenance-auditor.md) | Pre-publication **data** audit: every figure traces to a register row or numbered assumption, manifests re-hash, raw unedited, source attribution present, licence permits republication (incl. 공공누리/KOGL), clean-checkout reproducibility. **Read-only.** |
| [`refactor-architect`](./agents/refactor-architect.md) | Restructure code without changing behavior. Extract, deduplicate, reduce coupling, remove dead code. Tests stay green. |
| [`debugger`](./agents/debugger.md) | Bugs — crashes, wrong outputs, flaky tests. Reproduce → isolate → fix (root cause, not symptom). |

### Tier 3 — Code: domain specialists

| Agent | When to use |
|---|---|
| [`data-scientist`](./agents/data-scientist.md) | EDA, ML, experiment analysis **in code**. Schema/dtype/unit alignment; file-format best practice (parquet > CSV). **Not** a coefficient reported as an effect (→ `econometrician`). |
| [`econometrician`](./agents/econometrician.md) | Reduced-form causal inference in code: difference-in-differences (staggered-adoption-robust — Callaway–Sant'Anna / Sun–Abraham, not raw TWFE), event studies and pre-trend evidence, panel fixed effects, IV and RD, pass-through and elasticities, plus the inference layer (clustering level, few-cluster corrections, multiple-hypothesis adjustment). Owns the **estimand**: which comparison the estimator makes, which assumption licenses reading it as an effect, and what would break it. The pack's one licensed exception to "associations, not causes" — and it carries the assumption with every claim. **Not** structural equilibria (→ `computational-economist`), simulation calibration (→ `system-dynamics-modeller`), EDA/ML (→ `data-scientist`). |
| [`optimization-modeller`](./agents/optimization-modeller.md) | LP/MILP/NLP code: PyPSA, linopy, pyomo, cvxpy. Formulation, infeasibility debugging, solver tuning; PyPSA network construction, power flow (`n.pf()`) and calibration. **Not** stock-and-flow feedback (→ `system-dynamics-modeller`), market-clearing/game-theoretic equilibria (→ `computational-economist`), energy market research (→ `energy-finance-team`). |
| [`system-dynamics-modeller`](./agents/system-dynamics-modeller.md) | Stock-and-flow simulation with feedback: integration schemes and dt/stiffness, loop-dominance analysis, Vensim `.mdl` semantics (SMOOTH/DELAY/TREND), unit-strict rates, Monte-Carlo sweeps, calibration. Integrates coupled ODEs of accumulating stocks — not an optimizer. **Not** LP/MILP/NLP (→ `optimization-modeller`), equilibria (→ `computational-economist`). |
| [`computational-economist`](./agents/computational-economist.md) | Equilibrium & mechanism modelling: partial/general-equilibrium market clearing (tâtonnement, mixed-complementarity), Nash-Cournot/Stackelberg games, Hotelling dynamics, carbon-market design (MSR, CBAM, output-based allocation, collars), welfare/incidence. Equilibrium is a fixed point, not a single optimum. **Not** a single LP/MILP/NLP program (→ `optimization-modeller`), feedback simulation (→ `system-dynamics-modeller`), market/policy research (→ `energy-finance-team`). |
| [`gis-analyst`](./agents/gis-analyst.md) | Geospatial code: geopandas, shapely, rasterio, xarray. CRS audits, spatial-join pitfalls, raster/vector mismatches. |
| [`renewable-resource-scientist`](./agents/renewable-resource-scientist.md) | Wind/solar resource from reanalysis and observations: ERA5/atlite cutouts, hub-height shear extrapolation, air-density-corrected power curves, quantile-mapping bias correction vs masts/buoys, capacity-factor series, zone→node aggregation, representative-year & complementarity, solar via pvlib. **Not** CRS/geo mechanics (pair with `gis-analyst`), the dispatch that consumes the profiles (→ `optimization-modeller`), dataset/metric meaning (→ `data-collector` / `kr-power-data-scout`). |
| [`climate-risk-modeller`](./agents/climate-risk-modeller.md) | Physical & transition climate-risk in code: CLIMADA hazard × exposure × vulnerability → impact, expected annual impact, return-period loss curves, Monte-Carlo uncertainty, adaptation cost-benefit; NGFS transition-risk carbon-cost passthrough. Owns the heavy GPL CLIMADA/GDAL stack as an isolated conda subprocess behind a JSON contract. **Not** CRS/raster mechanics (pair with `gis-analyst`), no-code climate research (→ `energy-finance-team`), the map UI (→ `web-app-engineer`). |
| [`data-collector`](./agents/data-collector.md) | Build ingestion pipelines in code (OpenDART, Yahoo Finance, KOSIS, news APIs). Polite scraping, schema validation (pydantic/pandera), idempotent storage. **Not** ad-hoc research (→ research teams). |
| [`source-reconciliation-analyst`](./agents/source-reconciliation-analyst.md) | Two sources disagree about the same quantity. Prove the join, classify and quantify the disagreement, get the decision, **record it as a reusable rule** with an id, preserve the losing value in a parallel column, gate on a tolerance. Never silently picks. |
| [`mcp-server-engineer`](./agents/mcp-server-engineer.md) | MCP server tool surface: tool granularity, schemas with vocab-sourced enums, recoverable errors, output token budgeting with explicit truncation, stdio correctness, client registration, MCP/CLI/HTTP parity. |
| [`plugin-framework-architect`](./agents/plugin-framework-architect.md) | The host↔plugin contract: the SDK surface a plugin may depend on, entry-point discovery with two-phase load and failure isolation, contract-version negotiation and the semver bump policy, isolation guards checked in both directions, composing a selected plugin set into a shippable product and detecting conflicts, keeping a lean install lean, and strangler extraction of in-tree code into its own distribution while proving the default build stays byte-identical. **Not** the MCP tool surface (→ `mcp-server-engineer`), code inside one plugin (→ `developer`), restructure within a single package (→ `refactor-architect`), the panel-host UI (→ `frontend-developer`). |
| [`agent-app-engineer`](./agents/agent-app-engineer.md) | Applications that consume LLMs/agents at runtime: Claude Agent SDK orchestration and session lifecycle, a provider abstraction over the Claude API / `claude -p` CLI / local (Ollama), autonomy sliders with token & wall-clock budgets, PreToolUse approval gates and prompt-injection guards, worktree/venv/sandbox isolation, RAG and structured extraction, and an agent evaluation harness. The layer above the MCP tool surface. **Not** the MCP tool surface (→ `mcp-server-engineer`), the chat UI (→ `frontend-developer` / `web-app-engineer`), generic Python (→ `developer`). |
| [`app-distribution-engineer`](./agents/app-distribution-engineer.md) | Double-clickable `.command` / `.bat` / `.ps1` launchers for non-technical users: cwd and interpreter resolution, venv bootstrap, first-run `.env`, ports, Gatekeeper, actionable failure messages, per-OS parity. **Not** cloud/static web deploy — Vercel/Netlify (→ `web-app-engineer`). |
| [`visualizer`](./agents/visualizer.md) | Charts, maps, dashboards in code: matplotlib, seaborn, plotly, folium, pydeck. Publication-ready figures. Also builds the **research report pages** commissioned by `research-director` — `reports/build.py`, every unit `.html`, and the `index.html` over the set: self-contained, offline, deterministic, generated from the report's `.md` and data file. |
| [`doc-writer`](./agents/doc-writer.md) | **Code-facing docs only**: README, CLI manuals, tutorials, troubleshooting, ARCHITECTURE.md. **Not** research reports/memos (→ `writing-support-team`). |

### Tier 4 — Research & analysis (no code)

| Agent | When to use |
|---|---|
| [`energy-finance-team`](./agents/energy-finance-team.md) | Energy markets, ESG, climate finance, energy policy research → structured report. Uses web search, Yahoo Finance, DART. |
| [`investment-asset-team`](./agents/investment-asset-team.md) | Portfolio, equity, bond/credit, risk analysis → structured investment report. Uses Yahoo Finance, DART, web research. |
| [`kr-power-data-scout`](./agents/kr-power-data-scout.md) | Find a Korean dataset and establish **what the metric actually measures** (설비용량 vs 발전용량, 발전단 vs 송전단, SMP vs 정산단가, 잠정 vs 확정). KPX/EPSIS, KEPCO, 전기본, KOSIS, data.go.kr, OpenDART, KEEI, KMA, GIR. Returns a dossier with level, access class, and KOGL licence — never code. |
| [`writing-support-team`](./agents/writing-support-team.md) | Research reports, white papers, policy briefs, memos, presentations, and **parallel KO/EN deliverables** with a maintained terminology glossary. **Not** code-facing docs (→ `doc-writer`). |

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
| No-build vanilla-JS/d3 web app + thin backend + Vercel deploy | `web-app-engineer` |
| Build a data-ingestion pipeline in code | `data-collector` |
| Find a Korean dataset / check what a Korean metric means | `kr-power-data-scout` |
| Two sources disagree about the same number | `source-reconciliation-analyst` |
| Build or debug an MCP server | `mcp-server-engineer` |
| Build an app that embeds an LLM / Claude Agent SDK (RAG, guardrails, eval) | `agent-app-engineer` |
| Make it launch by double-click for a non-technical user | `app-distribution-engineer` |
| Check every figure traces to a source before publishing | `provenance-auditor` |
| Analyse data in code (EDA, ML) | `data-scientist` |
| Estimate an effect — DiD, event study, panel FE, IV, RD, pass-through | `econometrician` |
| Design or defend a plugin contract; extract a module into its own package | `plugin-framework-architect` |
| Write optimization model code | `optimization-modeller` |
| Stock-and-flow / feedback simulation (Vensim-style), SFC/E-SFC accounting | `system-dynamics-modeller` |
| Equilibrium / carbon-market / game-theoretic economics | `computational-economist` |
| Wind/solar resource, capacity factors from reanalysis | `renewable-resource-scientist` |
| Physical climate risk (CLIMADA) / NGFS transition risk | `climate-risk-modeller` |
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
planner-and-qc-lead  →  developer / frontend-developer / web-app-engineer
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

# New Korean dataset
kr-power-data-scout  →  data-collector  →  source-reconciliation-analyst  →  provenance-auditor

# Energy model
kr-power-data-scout  →  data-collector  →  renewable-resource-scientist  →  optimization-modeller  →  math-reviewer  →  visualizer

# Causal estimation (an effect, not an association)
econometrician (estimand + design, stated first)  →  econometrician (timing table → estimator)
                                                  →  econometrician (pre-trends & placebos BEFORE the headline)
                                                  →  visualizer      (event-study figure with CIs)
                                                  →  result-reporter  (as a range, assumption attached)

# Plugin contract change
plugin-framework-architect (classify additive/breaking → semver)  →  guard that fails on re-crossing
                                                                  →  anchor + parity: default build must not move
                                                                  →  tester (everything / lean / empty)  →  reviewer

# MCP surface
mcp-server-engineer  →  tester  →  reviewer   (+ app-distribution-engineer if it ships an installer or a .mcpb bundle)

# LLM / agent application
agent-app-engineer  →  mcp-server-engineer  →  web-app-engineer  →  tester  →  reviewer

# Before publishing a dataset or deliverable
provenance-auditor  →  auditor
```

The complete relationship graph and every workflow are in [`agents/ONTOLOGY.md`](./agents/ONTOLOGY.md).

### Invoking from Claude Code

```
> Use the research-director subagent to read the contract and proposal and build the charter.
> Use the research-director subagent to run a tracking pass.
> Use the report-manager subagent to rebuild the progress and team dashboards.
> Use the consultant subagent to draft the inception agenda and the data request list.
> Use the planner-and-qc-lead subagent to plan adding radiative forcing.
> Use the developer subagent to implement it in src/ebm/core/forcing.py.
> Use the math-reviewer subagent on src/ebm/core/forcing.py.
> Use the optimization-modeller subagent on gist2217/code/pypsa_model.py.
> Use the system-dynamics-modeller subagent on the stock-flow engine in systemdynamics.
> Use the computational-economist subagent on the K-ETS partial-equilibrium clearing in partial-equilibrium.
> Use the gis-analyst subagent on the spatial join in gisanalysis/process.py.
> Use the renewable-resource-scientist subagent on the ERA5 hub-height extrapolation for offshore wind.
> Use the climate-risk-modeller subagent on the CLIMADA impact pipeline in climaterisk.
> Use the visualizer subagent to fix the legend in a Ragnarok results chart in project_bifrost.
> Use the frontend-developer subagent to add a resizable properties rail in the pathwise frontend workspace.
> Use the web-app-engineer subagent to build the d3 dashboard and its FastAPI backend for landscape.
> Use the tester subagent on the changed files, then the reviewer subagent on the diff.
> Use the auditor subagent on this branch before I merge.
> Use the energy-finance-team subagent to research Korean offshore wind policy.
> Use the investment-asset-team subagent to analyze KEPCO's debt profile.
> Use the writing-support-team subagent to draft a policy brief on carbon markets.
> Use the kr-power-data-scout subagent to establish what KPX 발전기현황 actually measures.
> Use the source-reconciliation-analyst subagent on the fleet-vs-topology capacity conflict.
> Use the mcp-server-engineer subagent to review the landscape MCP tool surface.
> Use the agent-app-engineer subagent to add the Claude Agent SDK copilot loop in project_bifrost.
> Use the app-distribution-engineer subagent to make run.command work on a clean Mac.
> Use the provenance-auditor subagent before we publish the open data bundle.
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
git clone https://github.com/iam-hongsanghyun/claude-agents.git ~/github/claude-md
~/github/claude-md/scripts/install.sh   # syncs to ~/.claude/templates/, installs hook
```

The remote is **`claude-agents`**; the working copy stays at `~/github/claude-md` because project
`CLAUDE.md` files reference `~/github/claude-md/docs/HANDBOOK.md` by that path.

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
