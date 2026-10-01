# Agents

The user-level subagent pack. `scripts/sync-to-local.sh` copies `agents/*.md` into `~/.claude/agents/`;
never edit that copy. Project-scoped agents live in each engagement's `.claude/agents/` and are listed in
[`project/README.md`](project/README.md).

This file is the index: the roster and routing below, plus the authoring standard every agent follows.
Routing boundaries have **one home, the agent's `description`**. This file summarises them and must not
contradict them; if it does, the description wins.

## Roster (36)

| Group | Agent | Owns | Model |
|---|---|---|---|
| Governance | `research-director` | Contract → charter, stage plan, tracker; scales governance to the engagement | opus |
| | `consultant` | Everything client-facing; drafts only, never sends | sonnet |
| | `report-manager` | Progress status and dashboard, on request; process conformance | haiku |
| | `log-reporter` | What was done and what failed — one running log per stage | haiku |
| | `result-reporter` | The analysis write-up at a phase gate or deliverable | sonnet |
| Orchestration | `planner-and-qc-lead` | Plan one non-trivial task, QC checklist, routing | opus |
| Code | `developer` | Python features, refactors, docstrings | sonnet |
| | `web-developer` | Browser clients (React/Vite or no-build vanilla JS), thin backends, static deploy | sonnet |
| | `debugger` | Reproduce → root cause → minimal fix | sonnet |
| Gates (read-only) | `tester` | Mechanical: type-check, lint, tests | haiku |
| | `reviewer` | Diff vs the task asked + CLAUDE.md conventions → APPROVE/REJECT | sonnet |
| | `math-reviewer` | Code vs its equations | opus |
| | `provenance-auditor` | Figures trace to source; licence permits release — once, before delivery | haiku |
| Modelling | `data-scientist` | EDA, statistics, ML, schema alignment, reconciling disagreeing sources | sonnet |
| | `econometrician` | Causal estimation — the only role that may call a coefficient an effect | sonnet |
| | `optimization-modeller` | LP/MILP/NLP, PyPSA build, power flow, calibration | sonnet |
| | `system-dynamics-modeller` | Stock-and-flow simulation, SFC models | sonnet |
| | `computational-economist` | Equilibrium and mechanism models | sonnet |
| | `renewable-resource-scientist` | Wind/solar resource → capacity factors | sonnet |
| | `climate-risk-modeller` | CLIMADA physical risk, NGFS transition risk | sonnet |
| | `gis-analyst` | CRS, spatial joins, raster/vector | sonnet |
| Data & output | `data-collector` | Ingestion pipelines in code | sonnet |
| | `pipeline-builder` | dataflow pipeline specs: traced IO → steps and artifacts; check, curate, modify | sonnet |
| | `visualizer` | Figures, maps, report pages | sonnet |
| | `doc-writer` | README, CLI manual, tutorial, CHANGELOG | haiku |
| Platform | `mcp-server-engineer` | MCP tool surface | sonnet |
| | `agent-app-engineer` | Apps that run an LLM inside the product | sonnet |
| | `plugin-framework-architect` | Host ↔ plugin contract | sonnet |
| | `app-distribution-engineer` | Launchers and bundles for non-technical users | haiku |
| Research (no code) | `data-scout` | What a dataset or disclosure actually measures; build vs buy | sonnet |
| | `energy-finance-team` | Energy market, climate and company research | sonnet |
| | `investment-asset-team` | Portfolio, valuation, credit, ownership chains | sonnet |
| | `esg-disclosure-analyst` | GHG Protocol, PCAF, ISSB, CSRD, taxonomies | sonnet |
| | `policy-analyst` | What a policy requires; the storyline for policymakers | sonnet |
| | `transport-emissions-reviewer` | Vehicle/shipping emissions methodology, before publication (read-only) | sonnet |
| | `writing-support-team` | Reports, briefs, decks for non-code readers; KO/EN | sonnet |

Model rule: Sonnet by default; Haiku where the procedure is mechanical; Opus only for research design,
task decomposition and mathematical verification. Escalate one task, not the agent.

## Common chains

```
feature    planner-and-qc-lead → developer | web-developer → tester → reviewer (+ math-reviewer if math changed)
bug        debugger → tester → reviewer
pipeline   data-scout → data-collector → pipeline-builder → data-scientist
research   policy-analyst (message) → energy-finance-team | data-scientist → writing-support-team
delivery   result-reporter → provenance-auditor → consultant
```

## House rules (apply to every agent; not repeated in agent bodies)

- Follow the project's `CLAUDE.md`. Agents do not restate its conventions (types, docstrings, pint, config,
  seeds, logging); they name only the domain-specific checks CLAUDE.md cannot know.
- Research analysts return findings, never code. Reviewers are read-only and cite file:line.
- A figure that leaves the team traces to a data-register row or a numbered assumption. A figure is
  tagged `[verified]` once checked against that source, otherwise `[compute]`; `[compute]` is never presented as final.
- Findings are associations unless `econometrician` licensed the causal reading.
- Report a range where the uncertainty is material; do not manufacture P10/P50/P90 where it is not.

## Authoring standard

Every agent file has this shape and nothing else.

```markdown
---
name: kebab-case
description: "<What it does, one sentence>. Use when <trigger>. NOT for <task> — use <agent>; ..."
tools: <minimum set>
model: haiku | sonnet | opus
---

<Role in 1–3 sentences: what it owns and the one discipline it enforces.>

## Procedure
1. … (at most 7 steps)

## Rules
- … (non-negotiables, at most 8)

## Traps
- … (domain failures that pass silently, one line each, at most 10)

## Output
<a fenced template>
```

Limits, enforced in review:

| | Description | Body |
|---|---|---|
| Gate (tester, reviewer, auditors) | ≤ 60 words | ≤ 450 words |
| Specialist | ≤ 70 words | ≤ 800 words |
| research-director | ≤ 70 words | ≤ 1,100 words |

What does not belong in an agent file:

- Origin stories ("this role was invented three times…"), motivation, or why the agent exists.
- Routing prose ("Where this sits", "Distinct from…"). Boundaries go in the description's NOT-for clauses
  only — at most four, each naming the one agent that owns the task.
- Restated house rules or CLAUDE.md conventions.
- Generic advice any competent engineer already follows. A trap earns its line only if it fails silently.
- An output format that creates a new document. Agents write into the project's existing documents
  (see the governance set in `CLAUDE.md`), never a document of their own per run.

New agent bar: name the existing agents considered and why each is inadequate. A project agent that is a
near-copy of a user-level one is not created — use the user-level agent with project context instead.
