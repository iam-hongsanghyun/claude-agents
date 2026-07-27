#!/usr/bin/env python3
"""Render agents/ONTOLOGY.md from agents/ontology.yaml.

Usage (from anywhere):
    uv run --with pyyaml python scripts/render_ontology.py
    # or, if PyYAML is already importable:
    python scripts/render_ontology.py

ONTOLOGY.md is a GENERATED artefact. Edit agents/ontology.yaml and re-run this script;
never hand-edit ONTOLOGY.md. Output is deterministic (no timestamps) so a re-run on an
unchanged source produces an identical file — a clean `git diff` means the doc is in sync.
"""
from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.exit(
        "PyYAML not found. Run:  uv run --with pyyaml python scripts/render_ontology.py"
    )

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "agents" / "ontology.yaml"
OUT = REPO / "agents" / "ONTOLOGY.md"

TIER_ORDER = ["0", "1", "2", "3", "4"]


def node_key(agent_id: str) -> str:
    """A Mermaid-safe node id (hyphens are not safe in Mermaid identifiers)."""
    return agent_id.replace("-", "_")


def render(data: dict) -> str:
    agents = data["agents"]
    relations = data["relations"]
    tiers = data["tiers"]
    rel_types = data["relation_types"]
    workflows = data["workflows"]

    by_id = {a["id"]: a for a in agents}
    user = [a for a in agents if a["scope"] == "user"]
    proj = [a for a in agents if a["scope"] == "project"]
    tier_name = {t["id"]: t["name"] for t in tiers}

    out: list[str] = []
    w = out.append

    w("# Agent Ontology")
    w("")
    w(
        "> **Generated file — do not edit by hand.** Source of truth: "
        "[`ontology.yaml`](ontology.yaml). Regenerate with "
        "`uv run --no-project --with pyyaml python scripts/render_ontology.py`."
    )
    w("")
    w(
        "> For the **interactive version** — a clickable map with each agent's full role and "
        "routing boundaries — open [`ontology.html`](ontology.html) (self-contained, offline, "
        "opens by double-click; regenerate with "
        "`uv run --no-project --with pyyaml python scripts/render_ontology_html.py`)."
    )
    w("")
    w(
        f"{len(user)} user-level agents (installed to `~/.claude/agents/`) and {len(proj)} "
        "project-scoped agents (mirrored under [`project/`](project/README.md), not installed "
        "globally). Nodes are agents; edges are typed relationships. The full role reference is "
        "[`README.md`](README.md); this document is the machine-readable relationship graph."
    )
    w("")

    # --- Tiers ---
    w("## Tiers")
    w("")
    w("| Tier | Name | When |")
    w("|---|---|---|")
    for t in tiers:
        w(f"| {t['id']} | {t['name']} | {t['when']} |")
    w("")

    # --- Relationship types ---
    w("## Relationship types")
    w("")
    w("| Edge | Meaning |")
    w("|---|---|")
    for k, v in rel_types.items():
        w(f"| `{k}` | {v} |")
    w("")

    # --- Mermaid: flow & gates over the user-level pack ---
    w("## Flow & gates (user-level pack)")
    w("")
    w(
        "Solid = `hands_off_to`; thick = `gates`; dotted = `pairs_with`. Boundary routing "
        "(`delegates_to`) is listed exhaustively in the tables below and omitted from the diagram "
        "for legibility."
    )
    w("")
    w("```mermaid")
    w("flowchart LR")
    for tid in TIER_ORDER:
        members = [a for a in user if a["tier"] == tid]
        if not members:
            continue
        w(f'  subgraph T{tid}["Tier {tid} &middot; {tier_name[tid]}"]')
        for a in members:
            w(f'    {node_key(a["id"])}["{a["id"]}"]')
        w("  end")
    for r in relations:
        a, b = r["from"], r["to"]
        if a not in by_id or b not in by_id:
            continue
        if by_id[a]["scope"] != "user" or by_id[b]["scope"] != "user":
            continue
        ka, kb = node_key(a), node_key(b)
        if r["type"] == "hands_off_to":
            w(f"  {ka} --> {kb}")
        elif r["type"] == "gates":
            w(f"  {ka} ==>|gate| {kb}")
        elif r["type"] == "pairs_with":
            w(f"  {ka} -.- {kb}")
    w("```")
    w("")

    # --- Mermaid: project layer ---
    w("## Project layer")
    w("")
    w(
        "The 12 project-authored agents and how they relate to the pack: `authored` by "
        "`research-director`, `specializes` a user-level agent, or was `generalized_as` a new one."
    )
    w("")
    w("```mermaid")
    w("flowchart LR")
    proj_by_project: dict[str, list[dict]] = {}
    for a in proj:
        proj_by_project.setdefault(a.get("project", "other"), []).append(a)
    for project, members in proj_by_project.items():
        w(f'  subgraph P_{node_key(project)}["{project}"]')
        for a in members:
            w(f'    {node_key(a["id"])}["{a["id"]}"]')
        w("  end")
    # user-level targets referenced by project edges
    referenced: set[str] = set()
    link_types = {"authored", "specializes", "generalized_as"}
    for r in relations:
        if r["type"] not in link_types:
            continue
        for end in (r["from"], r["to"]):
            if by_id.get(end, {}).get("scope") == "user":
                referenced.add(end)
    for uid in sorted(referenced):
        w(f'  {node_key(uid)}["{uid}"]')
    for r in relations:
        if r["type"] not in link_types:
            continue
        ka, kb = node_key(r["from"]), node_key(r["to"])
        if r["type"] == "authored":
            w(f"  {ka} -->|authored| {kb}")
        elif r["type"] == "specializes":
            w(f"  {ka} -.->|specializes| {kb}")
        elif r["type"] == "generalized_as":
            w(f"  {ka} ==>|generalized| {kb}")
    w("```")
    w("")

    # --- Node catalogue ---
    w("## Agents")
    w("")
    w("### User-level")
    w("")
    w("| Agent | Tier | Model | Access | Role |")
    w("|---|---|---|---|---|")
    for a in sorted(user, key=lambda x: (x["tier"], x["id"])):
        w(
            f"| [`{a['id']}`]({a['id']}.md) | {a['tier']} | {a['model']} | "
            f"{a['access']} | {a['role']} |"
        )
    w("")
    w("### Project-scoped")
    w("")
    w("| Agent | Project | Tier | Model | Role |")
    w("|---|---|---|---|---|")
    for a in sorted(proj, key=lambda x: (x.get("project", ""), x["id"])):
        proj_dir = a.get("project", "")
        w(
            f"| [`{a['id']}`](project/{proj_dir}/{a['id']}.md) | {proj_dir} | "
            f"{a['tier']} | {a['model']} | {a['role']} |"
        )
    w("")

    # --- Edge catalogue, grouped by type ---
    w("## Relationships")
    w("")
    for rtype in rel_types:
        edges = [r for r in relations if r["type"] == rtype]
        if not edges:
            continue
        w(f"### `{rtype}`")
        w("")
        for r in edges:
            note = f" — {r['note']}" if r.get("note") else ""
            w(f"- `{r['from']}` &rarr; `{r['to']}`{note}")
        w("")

    # --- Workflows ---
    w("## Workflows")
    w("")
    w("Named sequences the edges above compose into.")
    w("")
    for wf in workflows:
        w(f"### {wf['id']}")
        w("")
        for step in wf["steps"]:
            w(f"1. {step}")
        w("")

    w("---")
    w("")
    w("Index: [`README.md`](README.md) · Project registry: [`project/README.md`](project/README.md)")
    w("")
    return "\n".join(out)


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    OUT.write_text(render(data), encoding="utf-8")
    n_user = sum(1 for a in data["agents"] if a["scope"] == "user")
    n_proj = sum(1 for a in data["agents"] if a["scope"] == "project")
    n_edges = len(data["relations"])
    print(f"Wrote {OUT.relative_to(REPO)} — {n_user} user + {n_proj} project agents, {n_edges} edges.")


if __name__ == "__main__":
    main()
