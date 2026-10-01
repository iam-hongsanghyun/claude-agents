# CLAUDE.md

Scientific modelling project (data science / energy / finance / economic).
Full team handbook: `docs/HANDBOOK.md`. Algorithm docs: `docs/ALGORITHM.md`.

## Commands

```bash
uv sync --all-extras           # install
uv run pytest                  # tests
uv run pytest --cov=src        # tests + coverage
uv run ruff check . --fix      # lint + autofix
uv run ruff format .           # format
uv run mypy src/               # type-check
```

If `uv` is not yet adopted, fall back to `pip install -e ".[dev]"` and `pytest` / `ruff` / `mypy` directly. Don't introduce `setup.py`, `requirements.txt`, `flake8`, or `black` configs — `pyproject.toml` is the single source of truth.

Where the project has a browser client or an MCP server, `npm run dev` / `npm run build` / `npx tsc --noEmit` sit alongside the above, and the backend↔frontend type contract is part of the definition of done. Verify a UI change in the running app, not only in tests — and against a server actually serving current code.

## Conventions

- **Python 3.11+**, type hints mandatory on public functions, Google-style docstrings.
- **Math docstrings**: include an `Algorithm:` section with LaTeX (`$$...$$`) primary and an ASCII fallback line. Define every symbol with units.
- **Variable names**: descriptive in general (`temperature_kelvin`), but **single letters are OK** when they mirror equations (`T`, `x`, `ε`, `dt`, `i`, `j`). Don't fight the math.
- **No hardcoded values**: load via `src/<pkg>/config.py` from `.env`. Mirror every var into `.env.example`.
- **Reproducibility**: pin random seeds (`numpy.random.default_rng(seed)` over the legacy global API). Commit `uv.lock`. Pin upstream versions.
- **Units**: use `pint` for any quantity with physical units (energy, power, currency rates, time-of-day). Don't pass bare floats across module boundaries when units matter.
- **Numerical correctness**: when changing math, add a test against an analytical solution OR a captured baseline (`np.testing.assert_allclose` with explicit `rtol`/`atol`).

## Logging

Use `src/<pkg>/logger.py`. Log shape and dtype, never full arrays. Never log secrets, PII, or raw data rows.

| level | use for |
|-------|---------|
| DEBUG | branch decisions, scalar values, shapes |
| INFO  | milestones (data loaded, fit complete) |
| WARNING | recoverable degradation |
| ERROR | failure that returns or skips |
| CRITICAL | abort |

## Tests

Pytest. New features need tests. Aim for **meaningful** coverage of math correctness, not a line-coverage %. For numerical code, regression tests against analytical solutions beat 100% line coverage every time.

## Git workflow

- Feature branch → PR → CI green → merge to main → delete branch.
- **Conventional commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.
- **Self-review before merge**: re-read the diff. For math changes, paste before/after equations into the PR description. CI passing ≠ math correct.
- Never `--force` push to main. Use `git revert` to undo merged commits.

## Project layout

```
src/<pkg>/
  core/       algorithms (no I/O)
  data/       loaders, validators, transforms
  config.py   loads .env, validates types
  logger.py   centralized logging
tests/        mirrors src/
docs/         ALGORITHM.md (math), HANDBOOK.md (team standards), API.md
.env, .env.example
pyproject.toml    single source of truth
```

See `docs/HANDBOOK.md` for: full directory layout, docstring template, ready-to-copy `config.py` / `logger.py` / CI workflow, code review checklist, deprecation strategy, experiment tracking patterns.

## Documentation hygiene

Markdown sprawl is the failure mode: a pile of documents nobody reads because none is authoritative.

- **One index per documentation set**, and **every document is reachable from it** by following links. A document that isn't reachable has no purpose — delete it.
- **One concern per document, one home per fact.** Specifications, current status, and history are three different documents. A fact copied into a second document will be wrong within a week.
- **No `_v2`, `_final`, `_old`, or dated duplicates.** A superseded document is deleted or archived, never left beside its replacement. No `ALL_CAPS_` filename prefixes.
- Before creating a document, search for one that already covers it and extend that instead.

## Agent team

The user-level subagent pack lives in `~/github/claude-md/agents/`; its index, routing and authoring standard are `agents/README.md` (`~/.claude/agents/` is a synced copy — never edit it). Each agent's boundaries live once, in its `description`. Route by the question:

| Question | Agent |
|---|---|
| What does this dataset or company disclosure actually measure? Build it or buy it? | `data-scout` |
| What does the policy require, and what will a policymaker do with the finding? | `policy-analyst` (before anyone computes) |
| Where does a metric sit against GHG Protocol / PCAF / ISSB / CSRD? | `esg-disclosure-analyst` |
| Does a vehicle or shipping emissions methodology hold? | `transport-emissions-reviewer` (read-only) |
| Is this coefficient an effect? | `econometrician` — the only licensed causal claim |
| Energy market, climate and company research | `energy-finance-team` |
| Portfolio, valuation, credit, ownership chains | `investment-asset-team` |
| The finished report, brief or deck, KO/EN | `writing-support-team` |

Analysts return findings, never code. Reviewers are read-only and cite file:line. A new agent — user-level or project-scoped — names the existing agents it considered and why each was inadequate; a near-copy of an existing agent is never created.

## Contracted research engagements

Where work is bound by a contract, proposal or funding agreement, the **contract is the truth source** and governance lives under `claude-docs/`. Governance is **proportional**: start minimal and add a document only when its trigger fires. The hygiene rules above win over any governance habit.

Default set — every engagement:

```
claude-docs/
  README.md        index
  charter.md       purpose, deliverables (id, due, acceptance), obligations, exclusions — quoted from the
                   contract with its section numbers — and the stage plan as one table
  tracker.md       current state only: stages, deliverables, blockers, next action
  log.md           append-only: decisions, and what each stage did and what failed
  register.csv     one row per source a published figure uses: source, locator (page/table), retrieved, licence
  assumptions.md   numbered assumptions with their basis
  reports/         one result report per phase gate or deliverable — not per stage or step
```

Add only on trigger:

| Add | Only when |
|---|---|
| `stages/<stage>.md` | the stage's method is contractually specified or not obvious from one table row |
| `phases/` | the contract defines three or more milestone or payment gates |
| `engagement/` | `consultant` is managing client correspondence in the repo |
| `team/roster.md` | a project-scoped agent is created |
| progress dashboard | the user or client asks for one |
| refresh skill | the user asks, or the pipeline is re-run end to end more than occasionally |

Agents: `research-director` sets up and keeps the set proportional; `consultant` drafts everything client-facing and never sends; `log-reporter` appends to `log.md`; `result-reporter` writes the gate and deliverable reports; `report-manager` refreshes status on request; `provenance-auditor` runs once before anything leaves the team.

Throughout: every published figure traces to a `register.csv` row or an `assumptions.md` number — no other ID scheme; nothing is hardcoded; findings are associations, not causes; a range is reported where the uncertainty is material.
