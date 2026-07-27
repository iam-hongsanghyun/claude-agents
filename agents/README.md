# Agents — Role Reference

All 32 agents are installed to `~/.claude/agents/` and available globally in every Claude Code session.

- Relationships between agents (tiers, hand-offs, gates, routing boundaries) live in the machine-readable [`ontology.yaml`](./ontology.yaml), rendered to [`ONTOLOGY.md`](./ONTOLOGY.md) and to an interactive map, [`ontology.html`](./ontology.html) — self-contained and offline, with every agent's full role and routing boundaries. **Double-click [`../ontology.command`](../ontology.command)** to regenerate both and open the map.
- Project-authored agents (created inside a single engagement by `research-director`, **not** installed globally) are registered in [`project/README.md`](./project/README.md).

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
| No-build vanilla-JS/d3 web app + thin backend + Vercel deploy | `web-app-engineer` |
| Mechanical build gate before review (tsc, mypy, lint, emoji scan) | `tester` |
| Judgment review of a diff: scope, duplication, contract | `reviewer` |
| Verify math in code vs docstrings vs ALGORITHM.md | `math-reviewer` |
| Pre-merge audit: hardcoded values, pint, tooling, layout | `auditor` |
| Audit data provenance, manifests, licence, reproducibility | `provenance-auditor` |
| Two sources disagree — decide, and record the rule | `source-reconciliation-analyst` |
| Design / debug an MCP server tool surface | `mcp-server-engineer` |
| Build an app that embeds an LLM / Claude Agent SDK (RAG, guardrails, eval) | `agent-app-engineer` |
| Double-clickable launchers for non-technical users | `app-distribution-engineer` |
| Find a Korean dataset; establish what a Korean metric measures | `kr-power-data-scout` |
| Restructure code without changing behavior | `refactor-architect` |
| Diagnose and fix a bug / crash / wrong output | `debugger` |
| EDA, ML prototyping, schema alignment in code | `data-scientist` |
| LP/MILP/NLP optimization code (PyPSA, linopy, pyomo) | `optimization-modeller` |
| Stock-and-flow / feedback simulation (Vensim-style) | `system-dynamics-modeller` |
| Equilibrium / carbon-market / game-theoretic economics | `computational-economist` |
| Geospatial code: CRS, spatial joins, raster/vector | `gis-analyst` |
| Wind/solar resource, capacity factors from reanalysis | `renewable-resource-scientist` |
| Physical climate risk (CLIMADA) / NGFS transition risk | `climate-risk-modeller` |
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
- **`team/roster.md`** — which agents the project needs, and new agent definitions where a stage genuinely has no competent owner;
- **`reports/`** — the record of what was actually done, one report unit per process step, stage and phase.

Runs seven named passes: Inception → Design → Conformance (re-read the contract; catch a method that answers an easier question) → Tracking → Team → **Refresh** → **Reporting**. Does not compute figures, does not write code, does not talk to the client.

**Refresh** is the re-run pass, for when the process has already run once and the data or the logic then changes. It treats the engagement as a dependency graph: every stage declares what it *consumes* (register rows, assumption ids, method files, config, code paths, upstream stage outputs) and *produces*, each input is fingerprinted, and a stage is re-run only when a fingerprint actually moved. The rest follows:
- **Chain reaction** — the transitive downstream closure of every changed stage is re-run in topological order, because a moved fuel price moves the workbook, the runs, the interpretation and the figures behind them.
- **Output-hash cutoff** — a re-run stage whose output is byte-identical stops the propagation there. This is the only sound way to prune the closure, and it is what keeps a refresh cheap.
- **Skip with proof** — a skipped stage is recorded with the fingerprint that justified the skip. *"Same data as before"* asserted from memory is indistinguishable from a stage nobody remembered to run.
- **Fixpoint** — sweep until nothing is stale, capped at five sweeps. Non-convergence means an undeclared cycle or a **non-deterministic stage** (unpinned seed, timestamp in an output, unfixed solver tolerance) — itself the finding.
- **Gates re-arm** — anything re-run reverts `[verified]` → `[compute]`; a skipped stage keeps its verification, which is exactly what the fingerprint bought; objectives evidenced by a re-run stage are re-judged.
- Writes `.claude/skills/<project>-refresh/SKILL.md` — the project's own DAG, fingerprint commands, per-stage run commands, gates and stop condition — so the next refresh is a single invocation rather than a re-derivation.

**Reporting** turns the work into a record someone outside the project can reproduce. The unit is the **process step, the stage and the phase** — a *process* being a numbered step in a stage's runbook, so 3 phases with 3 stages of 4 steps produces **3 + 3 + 12 = 18** report units. One directory per unit, and the tree is the hierarchy:

```
claude-docs/reports/
  index.html                dashboard over the whole set
  build.py                  visualizer's generator
  ph-01/    ph-01.md · ph-01.xlsx · ph-01.html
  st-03/    st-03.md · st-03.xlsx · st-03.html      <- the stage report
    pr-01/  pr-01.md · pr-01.xlsx · pr-01.html      <- step 1 of stage 03
    pr-02/  pr-02.md · pr-02.xlsx · pr-02.html
```

Process reports **nest inside their stage**, so the path carries the scope and step ids restart at `pr-01` in every stage. Stages stay **siblings of phases, never nested under them** — stages serve phases many-to-many, and nesting would force the false one-to-one tree Pass 2 exists to prevent. Ids are lowercase, zero-padded and slug-free (`ph-01`, `st-03`, `pr-02`), deliberately unlike the specification set's `PH<n>-<slug>.md`, because a report and the spec it reports on should not be confusable at a glance. **There is no manifest file**: the tree is the register of what exists, the governance set is the register of what should exist, and the dashboard reports the difference.

Each unit gets the same triplet:
- **`.md`** — the article, in fixed section order: identity and traceability, abstract, background, data (every input a register-row id with units and licence), method (equations, symbols with units, citing the method file rather than restating it), **implementation** (literal commands, code commit, interpreter and package versions, solver, seeds, config keys — the replication core), results (every number gated `[verified]`/`[compute]`, ranges not point estimates), verification (re-derived by a different route against a tolerance stated *before* the comparison), limitations, what would change the conclusion, provenance and reproduction, references.
- **`.sqlite`** (relational or large) **or `.xlsx`** (a reviewer must open it without tooling) — never both. Fixed table names so any unit's file reads the same: `report_manifest`, `datasets`, `inputs`, `processed_*`, `outputs_*`, `numbers`, `figures`, `provenance`. Where inputs are too big or their licence forbids redistribution, `processed` and `outputs` are embedded and each raw input becomes a **reference row** with its checksum and the reason. The `numbers` table is what makes "every figure traces to a source" checkable by query rather than by reading prose.
- **`.html`** — the article rendered interactively. **Built by [`visualizer`](#visualizer), commissioned by `research-director`**, which specifies the page and reviews it but writes no HTML and no generator code — the pages carry the figures, and figures are that agent's craft. Generated by `reports/build.py` from the `.md` and the data file, never hand-written: self-contained and offline (no CDN, no build step), deterministic, with a TOC, collapsible sections, sortable tables, a `[verified]`/`[compute]` filter, and each figure beside the query that regenerates it. A page that would state a number absent from the data file's `numbers` table is a defect, not a gap to type in.

Plus one **`reports/index.html`** over the whole set — every unit, its status and gate state, the objective it evidences, and **which units are missing their report**, that last being the reason it is a dashboard and not a folder. Three levels, one home per fact: the process report holds the primitive record, the stage report **cites** its process reports, the phase report returns a verdict per objective. And the constraint holds throughout — `research-director` scaffolds, structures and gates the set; the owning agents supply the results; `visualizer` builds every page; the review chain moves a number to `[verified]`; `provenance-auditor` clears the licence and the trace before the set travels. It still never produces a figure, writes HTML, or marks a number `[verified]` itself.
- **Not for**: planning a single coding task → `planner-and-qc-lead`; client communication → `consultant`; the progress/team dashboards and process policing → `report-manager`; the internal lead *function* inside `energy-finance-team` is unrelated to this agent

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
The **rich** React + TypeScript + Vite browser client for scientific-modelling GUIs: React Flow canvases, Leaflet / d3-geo maps, Glide/TanStack data grids, hand-rolled SVG charts, resizable rails, plugin hosts. Honors the project's existing layout/interaction contract and design system, reuses CSS (no duplication, `:root` variables), keeps the backend↔frontend type contract exact, verifies in the running app, and never adds icons/emojis.
- **Not for**: no-build vanilla-JS/d3 web apps & thin backends → `web-app-engineer`; Python model code → `developer`; matplotlib/plotly figures → `visualizer`

### `web-app-engineer`
No-build, framework-less web apps end to end: vanilla-JS + d3 (topojson/world-atlas) or KaTeX single-file frontends, a thin FastAPI/uvicorn or stdlib `http.server` JSON backend serving the SPA (SQLite or Supabase/Postgres), and static/Vercel/Netlify deploy. Owns the backend↔frontend JSON contract for these apps. The portfolio's dominant web idiom.
- **Not for**: rich React+TS+Vite modelling GUIs → `frontend-developer`; scientific Python core → `developer`; MCP tool surface → `mcp-server-engineer`; double-click desktop launchers → `app-distribution-engineer`

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
LP / MILP / NLP model code using PyPSA, linopy, pyomo, cvxpy. Formulation correctness, infeasibility debugging, solver tuning, duality interpretation. Also PyPSA network construction, power flow (`n.pf()`) and calibration.
- **Not for**: stock-and-flow feedback → `system-dynamics-modeller`; market-clearing / game-theoretic equilibria → `computational-economist`; energy market research → `energy-finance-team`

### `system-dynamics-modeller`
Stock-and-flow simulation with feedback: integration schemes and dt/stiffness, loop-dominance analysis, Vensim `.mdl` semantics (SMOOTH/DELAY/TREND), unit-strict rates, Monte-Carlo sweeps, calibration. Integrates coupled ODEs of accumulating stocks — not an optimizer.
- **Not for**: LP/MILP/NLP → `optimization-modeller`; equilibria → `computational-economist`

### `computational-economist`
Equilibrium & mechanism modelling: partial/general-equilibrium market clearing (tâtonnement, mixed-complementarity), Nash-Cournot/Stackelberg games, Hotelling dynamics, carbon-market design (MSR, CBAM, output-based allocation, collars), welfare/incidence. Equilibrium is a fixed point, not a single optimum.
- **Not for**: a single LP/MILP/NLP program → `optimization-modeller`; feedback simulation → `system-dynamics-modeller`; market/policy research → `energy-finance-team`

### `gis-analyst`
Geospatial **code**: geopandas, shapely, rasterio, xarray. CRS audits (the #1 source of GIS errors), spatial-join pitfalls, raster/vector mismatches, choropleth binning.
- **Not for**: general charts for reports → `visualizer` or `writing-support-team`

### `renewable-resource-scientist`
Wind/solar resource from reanalysis and observations: ERA5/atlite cutouts, hub-height shear extrapolation, air-density-corrected power curves, quantile-mapping bias correction vs masts/buoys, capacity-factor series, zone→node aggregation, representative-year & complementarity, solar via pvlib.
- **Not for**: CRS/geo mechanics → pair with `gis-analyst`; the dispatch that consumes the profiles → `optimization-modeller`; dataset/metric meaning → `data-collector` / `kr-power-data-scout`

### `climate-risk-modeller`
Physical & transition climate-risk in code: CLIMADA hazard × exposure × vulnerability → impact, expected annual impact, return-period loss curves, Monte-Carlo uncertainty, adaptation cost-benefit; NGFS transition-risk carbon-cost passthrough. Owns the heavy GPL CLIMADA/GDAL stack as an isolated conda subprocess behind a JSON contract.
- **Not for**: CRS/raster mechanics → pair with `gis-analyst`; no-code climate research → `energy-finance-team`; the map UI → `web-app-engineer`

### `data-collector`
Builds **reusable, tested Python pipelines** for web scraping and API ingestion (OpenDART, Yahoo Finance, KOSIS, news APIs, government open data). Polite scraping, retry/backoff, pydantic/pandera schema validation, idempotent storage.
- **Not for**: one-off research lookups → `energy-finance-team` / `investment-asset-team`; analysing already-collected data → `data-scientist`

### `source-reconciliation-analyst`
For when two or more sources disagree about the same quantity and the build must pick a value. One rule: **never silently pick** — no `coalesce` across sources, no averaging the difference away, no "the newer one". Proves the join first (row and key counts, unmatched both directions), classifies the disagreement (missing / conflicting / unit / granularity / vintage / naming / definitional), quantifies the distribution rather than the count, presents representative cases for a decision, then **records the decision as a reusable rule** with an id so the next rebuild does not re-ask. Preserves the rejected value in a parallel column, implements the rule declaratively in config, and gates it with a tolerance test.
- **Not for**: acquiring the sources → `data-collector` / `kr-power-data-scout`; analysing the merged result → `data-scientist`

### `mcp-server-engineer`
The MCP server tool surface — often the *primary* interface to these projects, and sometimes one of several surfaces (MCP / CLI / HTTP) that must not drift. Owns tool granularity (a tool answers a question someone asks, never one tool per table), input schemas with descriptions and vocab-sourced enums, errors an LLM can recover from, **output token budgeting** with explicit truncation reporting, stdio correctness (stdout belongs to the protocol — a stray `print()` kills the client), client registration with an absolute interpreter path, and a parity test across surfaces.
- **Not for**: generic Python → `developer`; browser UI → `frontend-developer`; the pipeline behind a tool → `data-collector`

### `agent-app-engineer`
Applications that consume LLMs/agents at runtime: Claude Agent SDK orchestration and session lifecycle, a provider abstraction over the Claude API / `claude -p` CLI / local (Ollama), autonomy sliders with token & wall-clock budgets, PreToolUse approval gates and prompt-injection guards, worktree/venv/sandbox isolation, RAG and structured extraction, and an agent evaluation harness. The layer above the MCP tool surface.
- **Not for**: the MCP tool surface → `mcp-server-engineer`; the chat UI → `frontend-developer` / `web-app-engineer`; generic Python → `developer`

### `app-distribution-engineer`
The ten seconds between a double-click and a working app, for users who never open a terminal. `.command` / `.bat` / `.ps1` launchers, interpreter and venv bootstrap, first-run `.env` seeding that *names* what is missing instead of throwing, port selection and occupancy reporting, Gatekeeper and quarantine, readiness before opening the browser, log files, and one actionable sentence on every failure path. Keeps per-OS variants from drifting by sharing one launch implementation behind thin wrappers, and verifies with an empty-environment simulation rather than a developer shell.
- **Not for**: application code → `developer` / `frontend-developer`; cloud/static web deploy (Vercel/Netlify) → `web-app-engineer`; MCP client registration → `mcp-server-engineer`; README prose → `doc-writer`

### `visualizer`
Produces charts, maps, and dashboards **in code**: matplotlib, seaborn, plotly, folium, pydeck. Catches legend-off-canvas, log-scale zeros, twin-axis confusion, color-blind-unsafe palettes. Publication-ready figures.

Also **builds the research report pages** that `research-director`'s Reporting pass commissions: `claude-docs/reports/build.py`, every unit `.html`, and the `index.html` over the whole set — self-contained and offline, deterministic, rendered from each report's `.md` and data file. It generates rather than authors: a page that would state a number with no row in the data file's `numbers` table is reported as a defect, never filled in by hand.
- **Not for**: report narrative around a chart → `writing-support-team`; the report's prose or numbers → `research-director` and the unit's owning agent; the progress/team dashboards → `report-manager`

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
planner-and-qc-lead  →  developer / frontend-developer / web-app-engineer
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

### Energy model
```
kr-power-data-scout  →  data-collector  →  renewable-resource-scientist  →  optimization-modeller  →  math-reviewer  →  visualizer
```

### MCP surface
```
mcp-server-engineer  →  tester  →  reviewer
  (+ app-distribution-engineer if it ships with an install script)
```

### LLM / agent application
```
agent-app-engineer  →  mcp-server-engineer  →  web-app-engineer  →  tester  →  reviewer
```

### Before publishing a dataset or deliverable
```
provenance-auditor  →  auditor  →  (contract work) research-director Conformance pass
```

The complete relationship graph and every workflow are in [`ONTOLOGY.md`](./ONTOLOGY.md).

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
> Use the optimization-modeller subagent on gist2217/code/pypsa_model.py.
> Use the system-dynamics-modeller subagent on the stock-flow engine in systemdynamics.
> Use the computational-economist subagent on the K-ETS partial-equilibrium clearing in partial-equilibrium.
> Use the gis-analyst subagent on the spatial join in gisanalysis/process.py.
> Use the renewable-resource-scientist subagent on the ERA5 hub-height extrapolation for offshore wind.
> Use the climate-risk-modeller subagent on the CLIMADA impact pipeline in climaterisk.
> Use the visualizer subagent to fix the legend in a Ragnarok results chart in project_bifrost.
> Use the frontend-developer subagent to add a resizable properties rail in the pathwise frontend workspace.
> Use the web-app-engineer subagent to build the d3 dashboard and its FastAPI backend for landscape.
> Use the agent-app-engineer subagent to add the Claude Agent SDK copilot loop in project_bifrost.
> Use the tester subagent on the changed files, then the reviewer subagent on the diff.
> Use the data-collector subagent to build a DART filing ingestion pipeline.
> Use the doc-writer subagent to write the CLI manual for scripts/run_model.py.
```
