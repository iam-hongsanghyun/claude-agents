# Project-scoped agents — registry

Agents created inside one engagement, living in that project's `.claude/agents/`. Mirrored here for
visibility only; `scripts/sync-to-local.sh` never installs them. The engagement's copy is authoritative.

A project agent is justified only when no user-level agent fits (see the bar in
[`../README.md`](../README.md)). A near-copy of a user-level agent is retired: use the user-level agent
and give it the project context instead.

## Active

| Project | Agent | Gap it closes |
|---|---|---|
| IRI-P1 | [`maritime-regulation-analyst`](IRI-P1/maritime-regulation-analyst.md) | Primary-source IMO text — adopted vs draft, GFI/RU/SU basis, vessel-activity data |
| IRI-P1 | [`shipping-transition-expert`](IRI-P1/shipping-transition-expert.md) | Marine-fuel transition authority; carries PLANiT's published shipping position |
| IRI-P1 | [`data-analyst`](IRI-P1/data-analyst.md) | Verbatim transcription with locator into the project sqlite register |
| OEP-OffshoreWind | [`system-value-analyst`](OEP-OffshoreWind/system-value-analyst.md) | System LCOE, curtailment, LCoS — metrics as scenario differences |
| OEP-OffshoreWind | [`dispatch-engineer`](OEP-OffshoreWind/dispatch-engineer.md) | KPG193 network build, 2024 calibration gate, run matrix |
| OEP-OffshoreWind | [`data-acquisition-engineer`](OEP-OffshoreWind/data-acquisition-engineer.md) | SKR-0008 fetchers, credential broker, human-input inbox |
| project_bifrost | [`leader`](project_bifrost/leader.md) | Feature triage → developer → reviewer → merge |

## Retired — delete from the engagement's `.claude/agents/`

| Project | Agent | Use instead |
|---|---|---|
| OEP-OffshoreWind | `resource-scientist` | `renewable-resource-scientist` |
| OEP-OffshoreWind | `interim-reporter` | `log-reporter` (stage log) + `result-reporter` (gate report) |
| OEP-OffshoreWind | `korea-policy-strategist` | `policy-analyst` |
| OEP-OffshoreWind | `pipeline-orchestrator` | `research-director` (stage plan, tracker) + `planner-and-qc-lead` (dispatch) |
| OEP-OffshoreWind | `oep-contract-compliance` | `research-director` gate check against the contract + `provenance-auditor` |

Watch: `system-value-analyst` and `data-acquisition-engineer` sit close to `optimization-modeller` and
`data-collector`. Retire them if the next engagement finds the user-level agents sufficient.
