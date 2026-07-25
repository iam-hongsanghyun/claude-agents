# Agents — Role Reference

All 26 agents are installed to `~/.claude/agents/` and available globally in every Claude Code session.

---

## Quick-pick: given task X, call agent Y

| Task | Agent |
|---|---|
| Set up / govern a contracted or funded research engagement | `research-director` |
| Talk to the customer; turn output into plain language | `consultant` |
| Progress dashboards; check the process is being followed | `report-manager` |
| Plan a non-trivial task; produce a QC checklist | `planner-and-qc-lead` |
| Implement a feature / write or refactor Python code | `developer` |
| React + TypeScript + Vite UI (canvas, maps, grids, charts) | `frontend-developer` |
| Mechanical build gate before review (tsc, mypy, lint, emoji scan) | `tester` |
| Judgment review of a diff: scope, duplication, contract | `reviewer` |
| Verify math in code vs docstrings vs ALGORITHM.md | `math-reviewer` |
| Pre-merge audit: hardcoded values, pint, tooling, layout | `auditor` |
| Audit data provenance, manifests, licence, reproducibility | `provenance-auditor` |
| Two sources disagree — decide, and record the rule | `source-reconciliation-analyst` |
| Design / debug an MCP server tool surface | `mcp-server-engineer` |
| Double-clickable launchers for non-technical users | `app-distribution-engineer` |
| Find a Korean dataset; establish what a Korean metric measures | `kr-power-data-scout` |
| Restructure code without changing behavior | `refactor-architect` |
| Diagnose and fix a bug / crash / wrong output | `debugger` |
| EDA, ML prototyping, schema alignment in code | `data-scientist` |
| LP/MILP/NLP optimization code (PyPSA, linopy, pyomo) | `optimization-modeller` |
| Geospatial code: CRS, spatial joins, raster/vector | `gis-analyst` |
| Build a data-ingestion pipeline in code | `data-collector` |
| Charts, maps, dashboards in code | `visualizer` |
| README, CLI manual, tutorial, troubleshooting guide | `doc-writer` |
| Energy market / ESG / climate / policy research → report | `energy-finance-team` |
| Portfolio, equity, bond, risk analysis → report | `investment-asset-team` |
| Research report, memo, white paper, presentation | `writing-support-team` |

---

## Tier 0 — Engagement Governance

For work that is bound by a **contract, proposal, or funding agreement** rather than by a backlog. Tier 0 answers *what is the research, who is on it, is it on track, and what does the client see* — Tiers 1–4 answer *how is the work done*.

The three roles are deliberately separated, because in practice one person doing all three quietly drops the least urgent: designing the process, checking the process is followed, and facing the client are different jobs with different failure modes.

All Tier 0 artefacts live under **`claude-docs/`** in the project — never scattered across the repo root. See `research-director` for the directory contract and the hygiene rules that keep it from becoming a markdown dump.

### `research-director`
Owns the research design and its governance. Reads the **contract/proposal as the single truth source**, then derives:
- **`charter.md`** — purpose, deliverables (with acceptance conditions), obligations, exclusions, each with a traceable id;
- **phases** — purpose, testable objectives, deliverables, entry/exit criteria;
- **stages** — the actual research activities, linked **many-to-many** to phases;
- **process** — one general process document plus one per stage: how to do it, when to stop, when to repeat, how to handle data (never hardcode), how and where to reference, and the methodology that governs;
- **toolbox** — data catalogue / register / assumptions, method files, reference sets;
- **`tracker.md`** — the single live tracking document that judges whether current activity is actually meeting each phase's objectives;
- **`team/roster.md`** — which agents the project needs, and new agent definitions where a stage genuinely has no competent owner.

Runs five named passes: Inception → Design → Conformance (re-read the contract; catch a method that answers an easier question) → Tracking → Team. Does not compute figures, does not write code, does not talk to the client.
- **Not for**: planning a single coding task → `planner-and-qc-lead`; client communication → `consultant`; dashboards → `report-manager`; the internal lead *function* inside `energy-finance-team` is unrelated to this agent

### `consultant`
The only customer-facing role. Runs the engagement — inception, progress meetings, data and decision requests, review rounds, change control, early warning of delay — and translates technical output into language the client can read, present, and defend without you in the room. Two hard boundaries: **never sends anything** (drafts only; the user sends), and **never accepts scope** (any request outside `charter.md` becomes a change request routed to `research-director`). Keeps an append-only engagement register of every commitment, request and decision.
- **Not for**: designing phases/stages → `research-director`; full formal reports and decks → `writing-support-team`; domain analysis → the Tier 4 research teams

### `report-manager`
Governs whether the designed process is actually being run, and makes the state visible. Runs an eight-check governance pass (tracker freshness, figure gating, unserved objectives, deliverable traceability, process conformance, directory hygiene, gate integrity, claimed-vs-actual) — then generates `claude-docs/dashboard/`: a **progress dashboard** and a **team dashboard** as self-contained HTML that opens by double-click, offline, with no CDN and no build step. Reads the documents, never edits them: if the tracker is wrong it reports it rather than fixing it. Also writes the internal progress note that `consultant` translates.
- **Not for**: designing the process → `research-director`; client-facing writing → `consultant`; figures inside a deliverable → `visualizer`

---

## Tier 1 — Workflow Orchestration

### `planner-and-qc-lead`
Plans any non-trivial task: decomposes into steps, identifies risks, produces a tailored QC checklist, routes work to the right agents. **Does not write code or research.**

---

## Tier 2 — Code: Writing & Review

### `developer`
Implements features, refactors, documents inline (docstrings). Enforces CLAUDE.md: type hints, `Algorithm:` docstring sections (LaTeX + ASCII), `uv`/`ruff`/`mypy`/`pytest`, no hardcoded values, `pint` units, reproducible seeds. Finishes the task completely, generalises over special-casing, reuses over duplicating, and verifies in the running app.
- **Not for**: React/TS UI → `frontend-developer`; research reports → `writing-support-team`; code-facing docs → `doc-writer`

### `frontend-developer`
React + TypeScript + Vite browser clients for scientific-modelling GUIs: React Flow canvases, Leaflet / d3-geo maps, Glide/TanStack data grids, hand-rolled SVG charts, resizable rails, plugin hosts. Honors the project's existing layout/interaction contract and design system, reuses CSS (no duplication, `:root` variables), keeps the backend↔frontend type contract exact, verifies in the running app, and never adds icons/emojis.
- **Not for**: Python model code → `developer`; matplotlib/plotly figures → `visualizer`

### `tester`
Mechanical build gate — no judgment. Type-check (`tsc`/`mypy`), compile, lint on a **plain** `ruff check .`, emoji/icon scan, tests. Pass/fail report. Runs *before* `reviewer` so the reviewer focuses on intent.
- **Not for**: design/scope judgment → `reviewer`

### `reviewer`
APPROVE/REJECT a diff against the one task asked for. Rejects on icons/emojis, scope creep, duplication of existing functionality, hardcoded domain data, and broken backend↔frontend contract. Read-only judgment; assumes `tester` passed first.
- **Not for**: mechanical checks → `tester`; deep math correctness → `math-reviewer`

### `math-reviewer`
Verifies that code matches the equations in `Algorithm:` docstring sections and `docs/ALGORITHM.md`. Checks discretization stability, sign conventions, indexing, tolerances, edge cases. **Read-only.**
- **Not for**: fixing code → `developer`

### `auditor`
End-to-end pre-merge review: no hardcoded values, config externalized, `pint` at boundaries, doc/code alignment, project layout, tooling clean. **Read-only.**
- **Not for**: fixing code → `developer`

### `provenance-auditor`
Audits **data** provenance and republication licence, where `auditor` audits code rules. Every figure traces to a data-register row or a numbered assumption; every raw drop has a manifest that re-hashes; raw data has not been edited; the one-way raw → interim → processed flow holds; every fact-bearing record carries its source; every source's licence permits the intended republication (including 공공누리 / KOGL type for Korean public data); every published figure regenerates from a clean checkout. Counts rather than samples, and reports blocker / major / minor with row-level precision. **Read-only by design** — an audit that repairs its own findings cannot be trusted twice.
- **Not for**: code conventions and hardcoded values → `auditor`; equations → `math-reviewer`; whether the process is being followed → `report-manager`

### `refactor-architect`
Restructures code without changing behavior: extract functions/modules, deduplicate, reduce coupling, remove dead code. Tests stay green at every step.
- **Not for**: new features → `developer`

### `debugger`
Reproduces bugs, isolates root cause (not symptoms), proposes minimal fix. Bisects, inspects logs, traces hypotheses. Writes a failing test before fixing.
- **Not for**: new features → `developer`

---

## Tier 3 — Code: Domain Specialists

### `data-scientist`
EDA, statistical analysis, ML prototyping, experiment analysis **in code**. Verifies input/output data alignment (schemas, dtypes, units, time zones) and enforces file-format best practice (parquet > CSV for numerical data).
- **Not for**: internet research → `energy-finance-team` / `investment-asset-team`; charts → `visualizer`

### `optimization-modeller`
LP / MILP / NLP model code using PyPSA, linopy, pyomo, cvxpy. Formulation correctness, infeasibility debugging, solver tuning, duality interpretation.
- **Not for**: energy market research → `energy-finance-team`

### `gis-analyst`
Geospatial **code**: geopandas, shapely, rasterio, xarray. CRS audits (the #1 source of GIS errors), spatial-join pitfalls, raster/vector mismatches, choropleth binning.
- **Not for**: general charts for reports → `visualizer` or `writing-support-team`

### `data-collector`
Builds **reusable, tested Python pipelines** for web scraping and API ingestion (OpenDART, Yahoo Finance, KOSIS, news APIs, government open data). Polite scraping, retry/backoff, pydantic/pandera schema validation, idempotent storage.
- **Not for**: one-off research lookups → `energy-finance-team` / `investment-asset-team`; analysing already-collected data → `data-scientist`

### `source-reconciliation-analyst`
For when two or more sources disagree about the same quantity and the build must pick a value. One rule: **never silently pick** — no `coalesce` across sources, no averaging the difference away, no "the newer one". Proves the join first (row and key counts, unmatched both directions), classifies the disagreement (missing / conflicting / unit / granularity / vintage / naming / definitional), quantifies the distribution rather than the count, presents representative cases for a decision, then **records the decision as a reusable rule** with an id so the next rebuild does not re-ask. Preserves the rejected value in a parallel column, implements the rule declaratively in config, and gates it with a tolerance test.
- **Not for**: acquiring the sources → `data-collector` / `kr-power-data-scout`; analysing the merged result → `data-scientist`

### `mcp-server-engineer`
The MCP server tool surface — often the *primary* interface to these projects, and sometimes one of several surfaces (MCP / CLI / HTTP) that must not drift. Owns tool granularity (a tool answers a question someone asks, never one tool per table), input schemas with descriptions and vocab-sourced enums, errors an LLM can recover from, **output token budgeting** with explicit truncation reporting, stdio correctness (stdout belongs to the protocol — a stray `print()` kills the client), client registration with an absolute interpreter path, and a parity test across surfaces.
- **Not for**: generic Python → `developer`; browser UI → `frontend-developer`; the pipeline behind a tool → `data-collector`

### `app-distribution-engineer`
The ten seconds between a double-click and a working app, for users who never open a terminal. `.command` / `.bat` / `.ps1` launchers, interpreter and venv bootstrap, first-run `.env` seeding that *names* what is missing instead of throwing, port selection and occupancy reporting, Gatekeeper and quarantine, readiness before opening the browser, log files, and one actionable sentence on every failure path. Keeps per-OS variants from drifting by sharing one launch implementation behind thin wrappers, and verifies with an empty-environment simulation rather than a developer shell.
- **Not for**: application code → `developer` / `frontend-developer`; MCP client registration → `mcp-server-engineer`; README prose → `doc-writer`

### `visualizer`
Produces charts, maps, and dashboards **in code**: matplotlib, seaborn, plotly, folium, pydeck. Catches legend-off-canvas, log-scale zeros, twin-axis confusion, color-blind-unsafe palettes. Publication-ready figures.
- **Not for**: report narrative around a chart → `writing-support-team`

### `doc-writer`
**Code-facing documentation only**: README, CLI manuals, tutorials with runnable examples, troubleshooting guides, architecture overviews, contributor guides, CHANGELOG entries. Diátaxis-aware (tutorial / how-to / reference / explanation).
- **Not for**: research reports, memos, presentations → `writing-support-team`; inline docstrings → `developer`; energy/investment content → domain research teams

---

## Tier 4 — Research & Analysis (no code)

Tier 4 teams are structured by **function, not named personas**, and enforce a shared analytical-integrity discipline: understand before you build the deliverable; correlation not causation ("areas to explore," never "X caused Y"); absolute magnitudes (dollars) alongside percentages; explicit coverage/sample/unit caveats; provenance and change-logs; state AI use; and gate every figure `[verified]` vs `[compute]`.

### `energy-finance-team`
Functional research team (PLANiT Institute) — Research Director plus Energy Markets, Financial Markets, and Policy & Regulatory functions — delivering structured reports on energy markets, ESG, climate finance, and energy policy. Uses web search, Yahoo Finance, and DART.
- **Not for**: optimization model code → `optimization-modeller`; data pipelines → `data-collector`; investment portfolio analysis → `investment-asset-team`

### `investment-asset-team`
Functional investment-analysis team — Investment Lead plus Portfolio, Equity, Fixed-Income, and Risk functions — covering allocation, valuation, credit, and risk. Outputs structured, non-directive investment reports using Yahoo Finance, DART, and web research.
- **Not for**: energy/policy research → `energy-finance-team`; model code or data pipelines → `developer` / `data-collector`

### `kr-power-data-scout`
Finds Korean datasets and — the part that saves the project — establishes **what a Korean metric actually measures** before anyone builds on it: 설비용량 vs 발전용량, 발전기현황 vs 설비현황, 발전단 vs 송전단, SMP vs 정산단가, 잠정 vs 확정, 회계연도 vs 역년, 호기 granularity. Covers KPX/EPSIS, KEPCO statistics, 전기본 and the transmission plan, KOSIS, data.go.kr, OpenDART, KEEI, KMA, GIR/K-ETS, and the legal sources. Searches sibling repositories *before* the web, classifies access honestly (api / credential / browser / human / unavailable) **and at what data level**, and settles the 공공누리 (KOGL) licence at discovery rather than at publication. Returns a sourced dossier per dataset; never code.
- **Not for**: building the fetcher → `data-collector`; analysing the acquired data → `data-scientist`; policy or market commentary → `energy-finance-team`

### `writing-support-team`
Functional writing team — Lead Editor plus Research Writer, Technical Writer, Copy Editor, and a **Bilingual Editor (KO/EN)** — for research reports, white papers, policy briefs, business memos, executive summaries, presentations, and methodology descriptions for non-code audiences. Bilingual deliverables are parallel work with a maintained terminology glossary, never a translation pass at the end.
- **Not for**: code-facing docs (README, CLI, tutorials) → `doc-writer`; domain energy/investment analysis → those teams

---

## Recommended workflows

### Contracted / funded research engagement
```
research-director  (Inception: contract+proposal -> claude-docs/charter.md)
                   -> confirm charter with the user
research-director  (Design: phases, stages, process, toolbox)
research-director  (Team: roster; write new agents only for real gaps)
consultant         (inception pack, data + decision requests)

  per stage:  stage owner agents  ->  review chain  ->  research-director (Tracking)
                                                     ->  report-manager  (governance + dashboards)

at every gate:     research-director (Conformance: re-read the contract)
                   report-manager (governance pass)  ->  consultant (client-facing translation)
```
Tracking is a pass, not a daemon. It is mandatory at every stage entry, exit, backward move and phase gate; for a standing cadence, schedule it:
```
/loop 30m Use the research-director subagent to run a tracking pass, then the report-manager subagent to rebuild the dashboards
```

### Feature development
```
planner-and-qc-lead  →  developer / frontend-developer
                     →  math-reviewer      (if math changed)
                     →  optimization-modeller (if LP/MILP changed)
                     →  data-scientist     (if data I/O changed)
                     →  visualizer         (if charts involved)
                     →  tester             (mechanical gate)
                     →  reviewer           (judgment gate, before commit)
                     →  auditor            (before merge)
```

### Bug fix
```
debugger  →  developer / frontend-developer  →  tester  →  reviewer  →  auditor
```

### Refactor
```
refactor-architect  →  auditor
```

### Research → report
```
energy-finance-team  or  investment-asset-team
→  writing-support-team   (if formal document needed)
```

### Data pipeline
```
data-collector  →  data-scientist  →  developer  (integrate into codebase)
```

### New Korean dataset
```
kr-power-data-scout  (dossier: what it measures, level, access, licence)
  →  data-collector             (build the fetcher)
  →  source-reconciliation-analyst  (if it overlaps a source we already hold)
  →  provenance-auditor         (manifest, licence, register row)
```

### MCP surface
```
mcp-server-engineer  →  tester  →  reviewer
  (+ app-distribution-engineer if it ships with an install script)
```

### Before publishing a dataset or deliverable
```
provenance-auditor  →  auditor  →  (contract work) research-director Conformance pass
```

---

## Invoking from Claude Code

```
> Use the research-director subagent to read the contract and proposal and build the charter.
> Use the research-director subagent to run a tracking pass.
> Use the report-manager subagent to rebuild the progress and team dashboards.
> Use the consultant subagent to draft the inception agenda and the data request list.
> Use the planner-and-qc-lead subagent to plan adding radiative forcing.
> Use the developer subagent to implement the energy balance model in src/ebm/core/forcing.py.
> Use the math-reviewer subagent on src/ebm/core/forcing.py.
> Use the auditor subagent on this branch before I merge.
> Use the energy-finance-team subagent to research Korean offshore wind policy.
> Use the investment-asset-team subagent to analyze KEPCO's debt profile.
> Use the writing-support-team subagent to draft a policy brief on carbon markets.
> Use the optimization-modeller subagent on simplePyPSA_KR/network.py.
> Use the gis-analyst subagent on the spatial join in gisanalysis/process.py.
> Use the visualizer subagent to fix the legend in pypsa_gui/charts.py.
> Use the frontend-developer subagent to add a resizable properties rail in frontend/pathwise.
> Use the tester subagent on the changed files, then the reviewer subagent on the diff.
> Use the data-collector subagent to build a DART filing ingestion pipeline.
> Use the doc-writer subagent to write the CLI manual for scripts/run_model.py.
```
