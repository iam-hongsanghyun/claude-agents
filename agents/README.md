# Agents — Role Reference

All 40 agents are installed to `~/.claude/agents/` and available globally in every Claude Code session.

- Relationships between agents (tiers, hand-offs, gates, routing boundaries) live in the machine-readable [`ontology.yaml`](./ontology.yaml), rendered to [`ONTOLOGY.md`](./ONTOLOGY.md) and to an interactive map, [`ontology.html`](./ontology.html) — self-contained and offline, with every agent's full role and routing boundaries. **Double-click [`../ontology.command`](../ontology.command)** to regenerate both and open the map.
- Project-authored agents (created inside a single engagement by `research-director`, **not** installed globally) are registered in [`project/README.md`](./project/README.md).

---

## Quick-pick: given task X, call agent Y

| Task | Agent |
|---|---|
| Set up / govern a contracted or funded research engagement | `research-director` |
| Talk to the customer; turn output into plain language | `consultant` |
| Progress dashboards; check the process is being followed | `report-manager` |
| Record what was done and what failed, for a step/stage/phase | `log-reporter` |
| Write the analysis up: article + conference deck + figures | `result-reporter` |
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
| Design or defend a plugin contract; extract a module into its own package | `plugin-framework-architect` |
| Build an app that embeds an LLM / Claude Agent SDK (RAG, guardrails, eval) | `agent-app-engineer` |
| Double-clickable launchers, or a `.mcpb` bundle, for non-technical users | `app-distribution-engineer` |
| Find a Korean dataset; establish what a Korean metric measures | `kr-power-data-scout` |
| Restructure code without changing behavior | `refactor-architect` |
| Diagnose and fix a bug / crash / wrong output | `debugger` |
| EDA, ML prototyping, schema alignment in code | `data-scientist` |
| Estimate an effect — DiD, event study, panel FE, IV, RD, pass-through | `econometrician` |
| LP/MILP/NLP optimization code (PyPSA, linopy, pyomo) | `optimization-modeller` |
| Stock-and-flow / feedback simulation (Vensim-style); SFC / E-SFC accounting | `system-dynamics-modeller` |
| Equilibrium / carbon-market / game-theoretic economics | `computational-economist` |
| Geospatial code: CRS, spatial joins, raster/vector | `gis-analyst` |
| Wind/solar resource, capacity factors from reanalysis | `renewable-resource-scientist` |
| Physical climate risk (CLIMADA) / NGFS transition risk | `climate-risk-modeller` |
| Build a data-ingestion pipeline in code | `data-collector` |
| Charts, maps, dashboards in code | `visualizer` |
| README, CLI manual, tutorial, troubleshooting guide | `doc-writer` |
| Energy market / ESG performance / climate / company research → report | `energy-finance-team` |
| What a company's reported number measures (retail vs wholesale vs production, plant- vs market-side, region, powertrain); build or buy the dataset | `ir-disclosure-analyst` |
| Review a transport-emissions methodology before publication (segment ratio, real-world factors, grid rule, lifetime, WtW/TtW, P10/P50/P90) | `transport-emissions-reviewer` |
| Position a metric against GHG Protocol / Scope 3 Cat. 11 / avoided emissions / PCAF / ISSB; read a disclosure for boundary and assurance | `esg-disclosure-analyst` |
| What a policy requires; a target's anatomy; the storyline and framing for policymakers, before computing | `policy-analyst` |
| Portfolio, equity, bond, risk analysis → report | `investment-asset-team` |
| Research report, memo, white paper, presentation | `writing-support-team` |

---

## Tier 0 — Engagement Governance

For work that is bound by a **contract, proposal, or funding agreement** rather than by a backlog. Tier 0 answers *what is the research, who is on it, is it on track, and what does the client see* — Tiers 1–4 answer *how is the work done*.

The roles are deliberately separated, because in practice one person doing all of them quietly drops the least urgent: designing the process, checking it is followed, recording what happened, writing up what was found, and facing the client are different jobs with different failure modes.

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
- **`reports/`** — the two report families, defined and gated here but written by `log-reporter` and `result-reporter`.

Runs six named passes: Inception → Design → Conformance (re-read the contract; catch a method that answers an easier question) → Tracking → Team → **Refresh**. Does not compute figures, does not write code, does not talk to the client. **Interim reporting is not a pass** — it runs step by step throughout, and is delegated (below).

**Refresh** is the re-run pass, for when the process has already run once and the data or the logic then changes. It treats the engagement as a dependency graph: every stage declares what it *consumes* (register rows, assumption ids, method files, config, code paths, upstream stage outputs) and *produces*, each input is fingerprinted, and a stage is re-run only when a fingerprint actually moved. The rest follows:
- **Chain reaction** — the transitive downstream closure of every changed stage is re-run in topological order, because a moved fuel price moves the workbook, the runs, the interpretation and the figures behind them.
- **Output-hash cutoff** — a re-run stage whose output is byte-identical stops the propagation there. This is the only sound way to prune the closure, and it is what keeps a refresh cheap.
- **Skip with proof** — a skipped stage is recorded with the fingerprint that justified the skip. *"Same data as before"* asserted from memory is indistinguishable from a stage nobody remembered to run.
- **Fixpoint** — sweep until nothing is stale, capped at five sweeps. Non-convergence means an undeclared cycle or a **non-deterministic stage** (unpinned seed, timestamp in an output, unfixed solver tolerance) — itself the finding.
- **Gates re-arm** — anything re-run reverts `[verified]` → `[compute]`; a skipped stage keeps its verification, which is exactly what the fingerprint bought; objectives evidenced by a re-run stage are re-judged.
- Writes `.claude/skills/<project>-refresh/SKILL.md` — the project's own DAG, fingerprint commands, per-stage run commands, gates and stop condition — so the next refresh is a single invocation rather than a re-derivation.

**Interim reporting** is a standing responsibility, not a pass, and it runs **step by step** — a report lands at every process-step completion, stage exit and phase gate, while the work is fresh. A set assembled at the end is written from memory, and memory is where the failures and the drop rates go missing.

`research-director` **defines and gates** the set but writes neither family:

| | **log report** — [`log-reporter`](#log-reporter) | **result report** — [`result-reporter`](#result-reporter) |
|---|---|---|
| Answers | What did we do, and what failed? | What did we find, and how solid is it? |
| Reader | The team, an auditor, future-you | The client, a reviewer, an audience |
| `.md` | The work record — commands, errors, dead ends | **A journal article** — why the analysis was run, methods, results |
| `.html` | A navigable record | **A conference presentation** |
| Figures | Only for a diagnostic | **Central** — charts carry the findings |
| Travels to the client | No | Yes |

Every unit gets a log report; a unit gets a result report **when it produced an analytical result** — a pure acquisition step has no finding, so it records `result: n/a — no analytical output` rather than shipping a hollow document. The layout splits the families at the top, so shipping to a client is a directory decision rather than a per-file filter:

```
claude-docs/reports/
  index.html                master dashboard over both families
  _build/                   the generator — visualizer's
  log/     ph-01/ · st-03/ · st-03/pr-01/      each: <unit>.md · .xlsx · .html
  result/  index.html  (audience-facing; travels on its own)
           ph-01/ · st-03/ · st-03/pr-01/      each: <unit>.md · .xlsx · .html · figures/
```

Process reports **nest inside their stage** (`st-03/pr-02/` *is* step 2 of stage 03, so the path carries the scope and step ids restart each stage). Stages stay **siblings of phases, never nested** — they serve phases many-to-many, and nesting would force the false one-to-one tree Pass 2 exists to prevent. Ids are lowercase, zero-padded and slug-free. **There is no manifest**: the tree registers what exists, the governance set registers what should exist, and the dashboard reports the difference.

`research-director` gates completeness — log triplet present, result triplet present or explicitly `n/a`, no empty section, every stated number carried in that unit's `numbers` table, at least one figure per result report — and names the incomplete units. It never fills a results table, never marks a number `[verified]`, and never writes HTML.
- **Not for**: planning a single coding task → `planner-and-qc-lead`; client communication → `consultant`; the progress/team dashboards and process policing → `report-manager`; the internal lead *function* inside `energy-finance-team` is unrelated to this agent

### `log-reporter`
Writes the **log report** for a unit — `claude-docs/reports/log/<unit>/`. The operational record: what was done chronologically, the literal commands with environment, versions and seeds, inputs and outputs with fingerprints, deviations from the stage runbook, timing and cost, the one command that reproduces the unit, and what the next stage receives. Its centre of gravity is **What failed** — errors, retries, dead ends, abandoned approaches, a portal that changed, a solve that would not converge — each with what it cost and what was done instead. *A log with no failures recorded is a log nobody kept.* Direct and complete rather than polished; nobody presents from it.
- **Not for**: the analysis, its statistics or figures → `result-reporter`; progress dashboards and process conformance → `report-manager`; data provenance and licence → `provenance-auditor`

### `result-reporter`
Writes the **result report** for a unit — `claude-docs/reports/result/<unit>/`. This is the family that travels to the client. The `.md` is a **journal article**: why the analysis was conducted, the data, the **data-handling result** (rows in and out per step, drops and their reasons, join match rates, reconciliation residuals, imputation extent), the **descriptive statistics** (distributions, missingness, coverage, outliers), the methods, and the results carried by **figures** — every number gated `[verified]`/`[compute]`, given as a range, with absolute magnitudes beside every percentage. The `.html` is a **conference presentation**: one idea per slide, figure-dominant, legible from the back of a room, keyboard-navigable, printable one slide per page, with speaker notes for the caveats a slide cannot show. A unit with no analytical output declares `result: n/a` rather than shipping a hollow report.
- **Not for**: commands, errors and dead ends → `log-reporter`; building the figures or the deck → pair with `visualizer`; client correspondence and framing → `consultant`

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
- **Not for**: fixing code → `developer`; whether the equations are the *right* ones for a transport-emissions model (segment ratio, real-world factors, grid rule, lifetime) → `transport-emissions-reviewer`

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
- **Not for**: internet research → `energy-finance-team` / `investment-asset-team`; charts → `visualizer`; a coefficient that will be reported as an effect → `econometrician`; a fleet-emissions result about to publish → `transport-emissions-reviewer` first

### `econometrician`
Reduced-form causal inference in code: difference-in-differences, event studies, panel fixed effects, IV, regression discontinuity, pass-through and elasticities — with `statsmodels` / `linearmodels` / `pyfixest`. It owns the **estimand**: which comparison the estimator actually makes, which assumption licenses reading that number as an effect, and what would break the reading.

Three things make it a distinct role rather than a corner of `data-scientist`:
- **It is the pack's one licensed exception to "associations, not causes"** — and it earns the exception by never letting the claim travel without the design and the assumption attached, and by downgrading its own language to association where the design does not support a cause.
- **Staggered adoption is a trap that returns a clean number.** With units treated at different dates, two-way fixed effects is a negatively-weighted average that can carry the wrong sign while every underlying effect is positive. Tabulating treatment timing *before* choosing an estimator, and reaching for Callaway–Sant'Anna / Sun–Abraham instead, is the headline error this agent exists to prevent.
- **Inference is half the job** — clustering at the level treatment is assigned (not the level that gives smaller errors), few-cluster corrections with the cluster count reported, multiple-hypothesis adjustment, and pre-trend evidence produced *before* the headline estimate so it cannot be read charitably after the fact.

Results are a range with the interval, never a point with stars.
- **Not for**: structural equilibrium or mechanism modelling → `computational-economist`; simulation calibration → `system-dynamics-modeller`; EDA, descriptive statistics, ML prediction → `data-scientist`; solver numerics → `math-reviewer`; no-code research → `energy-finance-team`; what the policy requires and how to frame it → `policy-analyst`

### `optimization-modeller`
LP / MILP / NLP model code using PyPSA, linopy, pyomo, cvxpy. Formulation correctness, infeasibility debugging, solver tuning, duality interpretation. Also PyPSA network construction, power flow (`n.pf()`) and calibration.
- **Not for**: stock-and-flow feedback → `system-dynamics-modeller`; market-clearing / game-theoretic equilibria → `computational-economist`; energy market research → `energy-finance-team`

### `system-dynamics-modeller`
Stock-and-flow simulation with feedback: integration schemes and dt/stiffness, loop-dominance analysis, Vensim `.mdl` semantics (SMOOTH/DELAY/TREND), unit-strict rates, Monte-Carlo sweeps, calibration. Integrates coupled ODEs of accumulating stocks — not an optimizer.

Also owns **stock-flow-consistent (SFC / ecological E-SFC) macro-financial models**, where accounting consistency plays the role unit consistency plays elsewhere: the balance-sheet and transaction-flow matrices must sum to zero along *both* dimensions, quadruple entry means a flow written without its counterparty is a bug that runs and drifts, and the redundant equation is **evaluated every step, never imposed** — imposing it makes the check vacuous. Money is endogenous (loans create deposits), and a central-bank tool acts inside the credit loop rather than as an exogenous injection.
- **Not for**: LP/MILP/NLP → `optimization-modeller`; equilibria → `computational-economist`; a parameter that must carry a causal reading → `econometrician` (consume the estimate across its interval, not at its point)

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
- **Not for**: CRS/raster mechanics → pair with `gis-analyst`; no-code climate research → `energy-finance-team`; the map UI → `web-app-engineer`; reviewing a transport-emissions methodology before publication → `transport-emissions-reviewer`

### `data-collector`
Builds **reusable, tested Python pipelines** for web scraping and API ingestion (OpenDART, Yahoo Finance, KOSIS, news APIs, government open data). Polite scraping, retry/backoff, pydantic/pandera schema validation, idempotent storage.
- **Not for**: one-off research lookups → `energy-finance-team` / `investment-asset-team`; analysing already-collected data → `data-scientist`; what a company's reported figure measures before it is ingested → `ir-disclosure-analyst`

### `source-reconciliation-analyst`
For when two or more sources disagree about the same quantity and the build must pick a value. One rule: **never silently pick** — no `coalesce` across sources, no averaging the difference away, no "the newer one". Proves the join first (row and key counts, unmatched both directions), classifies the disagreement (missing / conflicting / unit / granularity / vintage / naming / definitional), quantifies the distribution rather than the count, presents representative cases for a decision, then **records the decision as a reusable rule** with an id so the next rebuild does not re-ask. Preserves the rejected value in a parallel column, implements the rule declaratively in config, and gates it with a tolerance test.
- **Not for**: acquiring the sources → `data-collector` / `kr-power-data-scout` / `ir-disclosure-analyst`; analysing the merged result → `data-scientist`

### `mcp-server-engineer`
The MCP server tool surface — often the *primary* interface to these projects, and sometimes one of several surfaces (MCP / CLI / HTTP) that must not drift. Owns tool granularity (a tool answers a question someone asks, never one tool per table), input schemas with descriptions and vocab-sourced enums, errors an LLM can recover from, **output token budgeting** with explicit truncation reporting, stdio correctness (stdout belongs to the protocol — a stray `print()` kills the client), client registration with an absolute interpreter path, and a parity test across surfaces.
- **Not for**: generic Python → `developer`; browser UI → `frontend-developer`; the pipeline behind a tool → `data-collector`

### `plugin-framework-architect`
The contract between a host/kernel and the plugins that extend it — the recurring architecture in this portfolio (an umbrella framework composing independently-versioned Modules into shippable Tools; a manifest-declared plugin whose config schema renders into a host UI).

The judgement it exists to force: **is this a plugin or just a module?** A module is imported — the host knows its name and they are one release unit. A plugin is *discovered* — the host has never heard of it and must still work when it is absent, incompatible, or crashes on load. A host with a hardcoded list of what it composes has a decorative extension point, and that list is the real architecture.

What it owns: the SDK surface a plugin may depend on (and the extension bag that keeps additive changes additive), two-phase entry-point discovery that declares before it imports so an incompatible plugin can be *skipped with a reason* rather than crash the scan, contract-version negotiation against a stated semver bump policy, isolation guards checked **in both directions** (a stale allowlist row fails the build too, or the allowlist rots into permission), conflict detection when two plugins claim the same key, a composition anchor proving the default build did not move, keeping a lean install genuinely lean (verified by resolving it in a clean environment), and strangler extraction that inverts the dependency rather than carrying it.
- **Not for**: the MCP tool surface → `mcp-server-engineer`; generic Python inside one plugin → `developer`; behavior-preserving restructure within a single package → `refactor-architect`; the browser UI hosting plugin panels → `frontend-developer`; launchers and bundles → `app-distribution-engineer`

### `agent-app-engineer`
Applications that consume LLMs/agents at runtime: Claude Agent SDK orchestration and session lifecycle, a provider abstraction over the Claude API / `claude -p` CLI / local (Ollama), autonomy sliders with token & wall-clock budgets, PreToolUse approval gates and prompt-injection guards, worktree/venv/sandbox isolation, RAG and structured extraction, and an agent evaluation harness. The layer above the MCP tool surface.
- **Not for**: the MCP tool surface → `mcp-server-engineer`; the chat UI → `frontend-developer` / `web-app-engineer`; generic Python → `developer`

### `app-distribution-engineer`
The ten seconds between a double-click and a working app, for users who never open a terminal. `.command` / `.bat` / `.ps1` launchers, interpreter and venv bootstrap, first-run `.env` seeding that *names* what is missing instead of throwing, port selection and occupancy reporting, Gatekeeper and quarantine, readiness before opening the browser, log files, and one actionable sentence on every failure path. Keeps per-OS variants from drifting by sharing one launch implementation behind thin wrappers, and verifies with an empty-environment simulation rather than a developer shell.

Also owns **installable bundles** — an MCP `.mcpb` connector a user installs by double-click instead of hand-editing a client's JSON config: the manifest as install UX, configuration asked for through `user_config` (typed, with a default that works) rather than a hand-edited path, never a secret in the manifest, and bundle leanness *proved by inspecting the built archive* — shipping a `.venv` or a forgotten data directory is the default outcome. Installed from the artifact into a clean client profile, never from the working tree.
- **Not for**: application code → `developer` / `frontend-developer`; cloud/static web deploy (Vercel/Netlify) → `web-app-engineer`; which tools an MCP server exposes and their schemas → `mcp-server-engineer`; README prose → `doc-writer`

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

> The correlation-not-causation rule holds for everything these teams produce. The single exception in the pack is `econometrician`, which may make a causal claim — and only because it names the design, states the identifying assumption, shows the evidence that the assumption is not obviously violated, and keeps the assumption attached to the claim wherever it travels. If a Tier 4 report wants to say a policy *caused* something, that is a hand-off to `econometrician`, not a wording choice.

### `energy-finance-team`
Functional research team (PLANiT Institute) — Research Director plus Energy Markets, Financial Markets, and Policy & Regulatory functions — delivering structured reports on energy markets, ESG, climate finance, and energy policy. Uses web search, Yahoo Finance, and DART.
- **Not for**: optimization model code → `optimization-modeller`; data pipelines → `data-collector`; investment portfolio analysis → `investment-asset-team`; what a specific instrument requires, a target's anatomy, the policy storyline → `policy-analyst`; disclosure-standard conformance → `esg-disclosure-analyst`; a company's operating releases as data → `ir-disclosure-analyst`

### `investment-asset-team`
Functional investment-analysis team — Investment Lead plus Portfolio, Equity, Fixed-Income, Risk, and **Ownership & Stewardship** functions — covering allocation, valuation, credit, risk, and whether a stated commitment shows up in the holdings. Outputs structured, non-directive investment reports using Yahoo Finance, DART, and web research.

The Ownership & Stewardship function exists because the holding chain is where these numbers go wrong: beneficial vs registered vs custodial holder, nominee and depositary layers, funds vs their managers — a manager-level and a fund-level holding are different numbers and must never be summed. It also codes pledge strength onto an ordered scale (coverage, whether it binds subsidiaries, interim vs terminal date, escape clauses, whether it is reported against), reads the proxy-voting record rather than the stewardship report, and carries the as-of date and vintage on every figure, since holdings are disclosed with a lag and later revised.
- **Not for**: energy/policy research → `energy-finance-team`; model code or data pipelines → `developer` / `data-collector`; estimating an effect from the resulting panel → `econometrician`; how a disclosure conforms to GHG Protocol / PCAF / ISSB → `esg-disclosure-analyst`; operating (non-financial) releases as data → `ir-disclosure-analyst`

### `kr-power-data-scout`
Finds Korean datasets and — the part that saves the project — establishes **what a Korean metric actually measures** before anyone builds on it: 설비용량 vs 발전용량, 발전기현황 vs 설비현황, 발전단 vs 송전단, SMP vs 정산단가, 잠정 vs 확정, 회계연도 vs 역년, 호기 granularity. Covers KPX/EPSIS, KEPCO statistics, 전기본 and the transmission plan, KOSIS, data.go.kr, OpenDART, KEEI, KMA, GIR/K-ETS, and the legal sources. Searches sibling repositories *before* the web, classifies access honestly (api / credential / browser / human / unavailable) **and at what data level**, and settles the 공공누리 (KOGL) licence at discovery rather than at publication. Returns a sourced dossier per dataset; never code.
- **Not for**: building the fetcher → `data-collector`; analysing the acquired data → `data-scientist`; policy or market commentary → `energy-finance-team`; company IR and operating releases → `ir-disclosure-analyst`

### `writing-support-team`
Functional writing team — Lead Editor plus Research Writer, Technical Writer, Copy Editor, and a **Bilingual Editor (KO/EN)** — for research reports, white papers, policy briefs, business memos, executive summaries, presentations, and methodology descriptions for non-code audiences. Bilingual deliverables are parallel work with a maintained terminology glossary, never a translation pass at the end.
- **Not for**: code-facing docs (README, CLI, tutorials) → `doc-writer`; domain energy/investment analysis → those teams; the policy storyline and framing rules → `policy-analyst` first; standard-mapped text against GHG Protocol / ISSB / PCAF → `esg-disclosure-analyst`

### `ir-disclosure-analyst`
Reads a company's investor-relations and operating disclosures **as data** — monthly and quarterly sales and production releases, IR workbooks and decks, annual and sustainability reports, OpenDART / EDGAR filings — and establishes **five attributes** for every reported figure before it enters a model: **basis** (retail vs wholesale vs production vs deliveries vs registrations), **boundary** (plant-side vs market-side, brands, JVs, consolidated or parent), **period** (calendar vs fiscal, cumulative vs period, preliminary vs final), **granularity** (country vs region, model vs brand, powertrain split or an "eco-friendly" aggregate), **vintage** (restatements, retroactive region reclassification). Builds the nameplate and powertrain crosswalk with the unmatched counted. "IR" here means operating releases, not valuation.

It exists because the automotive trade-impact study stalled on exactly this — one exporter's workbook plant-side, another's regional and half-year, neither split by powertrain — and the roster had rejected the role as covered by `data-collector` + `source-reconciliation-analyst`. Its distinctive output is the **build-vs-buy verdict**: when no release publishes the needed grain on the needed basis, it names the licensed dataset that does (S&P Global Mobility, MarkLines, JATO, Dataforce; Clarksons for shipping), its licence class and lead time, and the claims that fall out of scope without it. Returns dossiers; never code.
- **Not for**: financial IR (valuation, guidance, capital structure) → `investment-asset-team`; building the fetcher → `data-collector`; two sources that disagree → `source-reconciliation-analyst`; Korean public statistics → `kr-power-data-scout`; standard conformance of a climate disclosure → `esg-disclosure-analyst`

### `transport-emissions-reviewer`
The specialist brought in **before publication, not full time**: an ICCT / EEA / IMO-type reviewer of the *methodology* of a road-fleet or shipping emissions model, where `math-reviewer` checks the code against its equations and this agent checks that the equations are the right ones. Every methodological choice — documented or found in a default argument — ends in one of four states: **settled with source**, **defensible but must be disclosed**, **wrong**, or **undecidable without a client ruling** — and every row has an owner. Its standing brief: the **segment ratio** between a company's mix and the fleet benchmark (1.0 is an assumption that decides signs, not a neutral default); test-cycle to real-world correction (WLTP / EPA / NEDC / CLTC gaps, OBFCM, **PHEV utility factors** — the largest single error in most models); the **grid-intensity rule** for BEVs, including what happens where a target is already met; lifetime as a **survival schedule** rather than a mean age, distance by age, cohort-year capping; indexing to a base year with the target's own gas basket and sector boundary; **WtW vs TtW**, g↔t, GWP vintage and adopted-vs-draft text for shipping; and whether a promised **P10/P50/P90** is propagated or is three scenarios wearing percentile labels. **Read-only** — reports with file:line or cell precision, and every settled call becomes a numbered assumption in the register, never a literal in code.
- **Not for**: code vs its equations → `math-reviewer`; whether figures trace → `provenance-auditor`; the reporting standard the result sits under → `esg-disclosure-analyst`; the sales or fleet data itself → `ir-disclosure-analyst`

### `esg-disclosure-analyst`
Corporate climate and sustainability **disclosure standards**: GHG Protocol (boundary and consolidation approach, Scope 2 location- vs market-based, the Scope 3 categories and **Category 11** use-of-sold-products assumptions), avoided-emissions / "Scope 4" guidance (WBCSD — separate from the inventory, with the counterfactual type deciding which tests apply), **PCAF** financed and facilitated emissions (attribution factor, data-quality score), **ISSB IFRS S1/S2** and its jurisdictional adoptions (AASB S2, KSSB, UK, Japan SSBJ), TCFD and the Transition Plan Taskforce, **CSRD/ESRS**, SBTi validation status, CDP, and **taxonomy-based sustainable CapEx / revenue** (eligible vs aligned; sum the components, never lift a headline share). Three jobs: **position a methodology** against the provisions it touches (inside, beside, against, or silent — and "additional to Scope 3 Category 11, never netting" checked in every table); **read a disclosure** for its eight attributes (boundary, Scope 2 method, Scope 3 coverage, base year and restatements, targets, transition plan, assurance scope, sustainable CapEx components) before any figure from it is used; and **write for standard-setters** — the provision, the gap, the proposal, the evidence, the cost. Earns its place at the white-paper and peer-review stage, after the case study is defensible. States the edition and date of every provision; gives no legal advice; does no ESG scoring.
- **Not for**: ESG performance research or scoring across companies → `energy-finance-team`; whether a pledge shows up in the holdings → `investment-asset-team`; vehicle or vessel emissions methodology → `transport-emissions-reviewer`; policy instruments and targets → `policy-analyst`; operating releases as data → `ir-disclosure-analyst`

### `policy-analyst`
Owns **what the policy actually says** and **what the study says to a policymaker**, as distinct from what it computes — the role invented three times before it was written down (OEP's `korea-policy-strategist`, the Climate Arc workshop's `policy-strategist`, the trade-impact NDC anchors). Two artefacts. The **instrument register**: statute → decree → notice (the 고시 carries the number the law gestures at) → guidance; adopted vs draft vs proposed vs repealed; effective and compliance dates and phase-in cohorts; coverage; mechanism; enforcement and flexibility; version read — primary text cited to the clause, with anything recalled treated as a candidate to verify. The **target anatomy**: base year, form (absolute / intensity / BAU-relative), gas basket and GWP vintage, sector boundary, LULUCF, conditionality, legal status, version — and from it the pathway rules the analyst may use (time-matched, pro-rata as a *named* assumption, no target in force = explicit exclusion, target already met = a recorded rule). Then the **storyline, shaped before anyone computes**: the decision the audience faces, one message per figure as a comparison, the counterfactual structure led with, the boundary stated before someone in the room states it, two tiers where the audience has an existing frame, the caveat inside the sentence the presenter will say, and the change the finding is meant to produce. Decides which **policy use-cases** the data honestly serves (monitoring, targeting — rarely evaluation, never causation). Exploratory not predictive; comparison not advocacy; no causal claim about a policy — that sentence is `econometrician`'s.
- **Not for**: estimating a policy's effect → `econometrician`; disclosure standards → `esg-disclosure-analyst`; energy-market and company research → `energy-finance-team`; the finished brief, deck or report → `writing-support-team` / `result-reporter`; client communication → `consultant`

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
policy-analyst / esg-disclosure-analyst   (framing rules and standard positioning first, where the report faces policymakers or standard-setters)
→  energy-finance-team  or  investment-asset-team
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

### Causal estimation (an effect, not an association)
```
econometrician  (estimand + design + identifying assumption — stated BEFORE any fit)
  →  econometrician   (treatment-timing table → estimator; TWFE only if adoption is common)
  →  econometrician   (pre-trend & placebo evidence BEFORE the headline estimate)
  →  visualizer       (event-study figure with confidence intervals)
  →  econometrician   (the pre-specified robustness set, reported in full)
  →  result-reporter  (as a range with the assumption attached; downgraded to an
                       association where the design does not license a cause)
```

### Plugin contract change
```
plugin-framework-architect  (classify: additive / breaking / internal → the semver move)
  →  plugin-framework-architect  (the change + a guard that fails when the boundary is re-crossed)
  →  plugin-framework-architect  (composition anchor + result parity: the default build must not move)
  →  tester    (guards on every invocation; CI matrix over everything / lean / empty)
  →  reviewer
  →  plugin-framework-architect  (template plugin + conformance kit, same commit)
```

### MCP surface
```
mcp-server-engineer  →  tester  →  reviewer
  (+ app-distribution-engineer if it ships with an install script or a .mcpb bundle)
```

### LLM / agent application
```
agent-app-engineer  →  mcp-server-engineer  →  web-app-engineer  →  tester  →  reviewer
```

### Company operating disclosures → dataset
```
ir-disclosure-analyst  (five attributes per release: basis, boundary, period, granularity, vintage;
                        reporting-basis map across companies; build-vs-buy verdict on a licensed dataset)
  →  data-collector                 (the fetcher, or the pinned hand-gathered file under the project's source policy)
  →  source-reconciliation-analyst (where two releases disagree on the same quantity)
  →  provenance-auditor             (terms of use and republication grain)
  →  data-scientist
```

### Transport-emissions methodology, before publication
```
transport-emissions-reviewer  (methodology register — every choice settled / disclose / wrong / client ruling, with an owner)
  →  math-reviewer            (code vs its equations)
  →  esg-disclosure-analyst   (where the metric sits against GHG Protocol / Scope 3 Cat. 11 / avoided emissions / PCAF)
  →  provenance-auditor       (every figure traces)
  →  result-reporter          (the disclosures travel beside the headline figure)
```

### Policy storyline (message before computing)
```
policy-analyst  (instrument register + target anatomy + use-case fit + the message — BEFORE anyone computes)
  →  data-scientist / econometrician  (compute to the message; a causal sentence only via econometrician)
  →  visualizer                       (one figure per message)
  →  result-reporter / writing-support-team  (the deck or brief, with the sentences the presenter may say)
  →  consultant                       (to the client)
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
