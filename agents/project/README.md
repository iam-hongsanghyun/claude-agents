# Project-authored agents — registry

Agents that `research-director` created **inside a specific engagement** to close a gap no
user-level agent covered. They live in that project's `.claude/agents/` and are **scoped to that
project**. This directory is a **version-managed mirror** so they can be reviewed and managed from
`claude-md` (the source of truth for agent work) rather than being visible only inside each repo.

Two things to keep straight:

- **These are NOT installed globally.** `scripts/sync-to-local.sh` copies only the user-level pack
  (`agents/*.md`) into `~/.claude/agents/`. Nothing under `agents/project/` is synced — a
  contract-conformance gate for one contract has no business firing in every session.
- **Provenance.** Each was authored in-engagement against that project's charter, stages and decision
  log; the copy here is a snapshot. When an engagement's copy and this mirror diverge, the engagement's
  `.claude/agents/` is authoritative for *that project*, and this mirror is refreshed from it. The
  justification for each (the "bar for a new agent" record — which existing agents were considered and
  why each was inadequate) lives in that engagement's `claude-docs/team/roster.md`, not here.

**Why mirror them at all.** Three reasons: (1) visibility — one place to see every specialist role the
portfolio has grown; (2) reuse — a project agent is the field prototype for a user-level one (see
*Disposition* below); (3) drift control — a role that exists only inside one repo is invisible to the
next engagement that needs the same capability.

---

## Disposition

`local` — stays engagement-specific by design (tied to one contract, dataset, or governance set); promoting
it would split knowledge across two definitions and both would rot.
`generalized → X` — a user-level agent `X` in the pack was distilled from this prototype; use `X` for new
work, and keep this copy as the worked example.

### IRI-P1 — Taiwan shipping decarbonization (IRI × PLANiT, contracted)

| Agent | Model | Gap it closes | Disposition |
|---|---|---|---|
| [`maritime-regulation-analyst`](IRI-P1/maritime-regulation-analyst.md) | opus | Primary-source IMO regulation — adopted-vs-draft text, NZF GFI/RU/SU accounting basis, vessel-activity datasets (AIS, EU MRV) | local (maritime domain, one active engagement) |
| [`shipping-transition-expert`](IRI-P1/shipping-transition-expert.md) | opus | Sector authority: marine-fuel transition, dual-fuel retrofit feasibility, EEXI/CII/MARPOL/EU-ETS/FuelEU; carries PLANiT's published shipping position | local (routes to the PLANiT MCP corpus; one engagement) |
| [`data-analyst`](IRI-P1/data-analyst.md) | opus | Transcription-with-provenance into a sqlite register — verbatim quote + exact locator, refuses to fill a gap | local (bound to that project's `data/reference/` and charter P-28/P-29) |

### OEP-OffshoreWind — Korean offshore-wind system value (SKR-0008, contracted)

| Agent | Model | Gap it closes | Disposition |
|---|---|---|---|
| [`resource-scientist`](OEP-OffshoreWind/resource-scientist.md) | opus | Offshore-wind resource: ERA5 → hub-height shear → bias-correction vs buoys → capacity factor → complementarity | **generalized → [`renewable-resource-scientist`](../renewable-resource-scientist.md)** |
| [`system-value-analyst`](OEP-OffshoreWind/system-value-analyst.md) | opus | System LCOE, curtailment, LCoS, surplus absorption, negative pricing — metrics as differences between scenarios | local (folds into `optimization-modeller`'s broadened scope for now) |
| [`dispatch-engineer`](OEP-OffshoreWind/dispatch-engineer.md) | opus | KPG193 network build, 2024 calibration gate, scenario encoding, ensembled run matrix (drives Ragnarok) | local (project network + calibration gate) |
| [`data-acquisition-engineer`](OEP-OffshoreWind/data-acquisition-engineer.md) | sonnet | Project acquisition layer: ERA5/KMA/EPSIS/KPX/GEBCO/Overpass fetchers + credential broker + human-input inbox | local (specializes `data-collector` to SKR-0008 sources) |
| [`korea-policy-strategist`](OEP-OffshoreWind/korea-policy-strategist.md) | opus | Storyline for MCEE/KPX/National-Assembly audiences; the three contract-required Korea insights | local (engagement narrative) |
| [`oep-contract-compliance`](OEP-OffshoreWind/oep-contract-compliance.md) | sonnet | Pre-submission PASS/BLOCK vs Schedules 1/2/3, payment gateways, KPIs | local (inherently per-contract) |
| [`pipeline-orchestrator`](OEP-OffshoreWind/pipeline-orchestrator.md) | opus | "START HERE" project lead: reads pipeline state, dispatches to role agents, batches asks (holds the `Agent` tool) | local (project orchestrator; cf. `planner-and-qc-lead`) |
| [`interim-reporter`](OEP-OffshoreWind/interim-reporter.md) | sonnet | Stage reports that lead with the ask and are honest about failure | local (specializes `report-manager`/`writing-support-team`) |

### project_bifrost — embedded AI copilot for Ragnarok (PyPSA GUI)

| Agent | Model | Gap it closes | Disposition |
|---|---|---|---|
| [`leader`](project_bifrost/leader.md) | (inherit) | Feature triage → scoped task to `developer` → `reviewer` → commit/push/merge | local (project orchestrator) |

---

## Patterns worth watching

Two capabilities were invented independently in more than one engagement — the signal that a user-level
agent is earning its place:

- **Renewable-resource science** (OEP `resource-scientist`) → now the user-level
  [`renewable-resource-scientist`](../renewable-resource-scientist.md).
- **Embedded LLM/agent applications** — project_bifrost's Bifrost copilot and pathwise's in-app assistant
  drove the user-level [`agent-app-engineer`](../agent-app-engineer.md).
- **Pipeline-lead / dispatch orchestration** (OEP `pipeline-orchestrator`, bifrost `leader`) — a recurring
  shape not yet promoted; `planner-and-qc-lead` covers the planning half. Watch for a third instance.

Index: [`../README.md`](../README.md) · Ontology: [`../ONTOLOGY.md`](../ONTOLOGY.md) ·
Interactive map: [`../ontology.html`](../ontology.html)
