#!/usr/bin/env python3
"""Render agents/ontology.html — a self-contained, offline agent-ontology map.

Usage:
    uv run --no-project --with pyyaml python scripts/render_ontology_html.py

Reads two sources and joins them, so no fact is typed twice:
  * agents/ontology.yaml      — tiers, nodes, typed edges, workflows (the graph)
  * agents/**/<agent>.md      — each agent's own `description` frontmatter (the role text)

Output is ONE file with no external requests: no CDN, no build step, no fonts to fetch.
It opens by double-click from the filesystem and works offline, the same contract the
project dashboards hold. Layout is computed here (deterministic), so the SVG renders even
with JavaScript disabled; JS adds filtering, selection and the detail panel only.
"""

from __future__ import annotations

import html
import json
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.exit(
        "PyYAML not found. Run: uv run --no-project --with pyyaml python scripts/render_ontology_html.py"
    )

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "agents" / "ontology.yaml"
AGENT_DIR = REPO / "agents"
OUT = REPO / "agents" / "ontology.html"

TIER_ORDER = ["0", "1", "2", "3", "4"]

# Layout constants (px, SVG user units)
COL_W, NODE_W, NODE_H, V_GAP, TOP, LEFT = 272, 210, 30, 42, 92, 30

FLOW_TYPES = {"hands_off_to", "gates", "pairs_with"}


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def load_descriptions() -> dict[str, str]:
    """Pull each agent's `description` frontmatter — the authoritative routing text."""
    out: dict[str, str] = {}
    files = [p for p in AGENT_DIR.glob("*.md") if p.name not in ("README.md", "ONTOLOGY.md")]
    files += [p for p in AGENT_DIR.glob("project/*/*.md") if p.name != "README.md"]
    for p in files:
        txt = p.read_text(encoding="utf-8")
        if not txt.startswith("---\n"):
            continue
        end = txt.find("\n---\n", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(txt[4 : end + 1]) or {}
        except yaml.YAMLError:
            continue
        if isinstance(fm, dict) and fm.get("name"):
            out[str(fm["name"])] = str(fm.get("description", "")).strip()
    return out


def layout(agents: list[dict], scope: str) -> tuple[dict[str, dict], int, int]:
    """Assign each node a tier column and a row. Deterministic: input order is preserved."""
    pos: dict[str, dict] = {}
    counts = dict.fromkeys(TIER_ORDER, 0)
    for a in agents:
        if a["scope"] != scope:
            continue
        t = a["tier"]
        row = counts[t]
        counts[t] += 1
        col = TIER_ORDER.index(t)
        pos[a["id"]] = {
            "x": LEFT + col * COL_W,
            "y": TOP + row * V_GAP,
            "col": col,
            "tier": t,
        }
    tallest = max(counts.values()) if counts else 1
    width = LEFT * 2 + (len(TIER_ORDER) - 1) * COL_W + NODE_W
    height = TOP + tallest * V_GAP + 30
    return pos, width, height


def edge_path(a: dict, b: dict) -> str:
    """Cubic bezier between two node boxes; routes forward, backward or same-column."""
    ay, by = a["y"] + NODE_H / 2, b["y"] + NODE_H / 2
    if b["col"] > a["col"]:
        x1, x2 = a["x"] + NODE_W, b["x"]
        dx = max(30, (x2 - x1) * 0.45)
        return f"M{x1},{ay} C{x1 + dx},{ay} {x2 - dx},{by} {x2},{by}"
    if b["col"] < a["col"]:
        x1, x2 = a["x"], b["x"] + NODE_W
        dx = max(30, (x1 - x2) * 0.45)
        return f"M{x1},{ay} C{x1 - dx},{ay} {x2 + dx},{by} {x2},{by}"
    x1 = a["x"] + NODE_W
    x2 = b["x"] + NODE_W
    bulge = 34 + abs(ay - by) * 0.12
    return f"M{x1},{ay} C{x1 + bulge},{ay} {x2 + bulge},{by} {x2},{by}"


def svg_map(
    agents: list[dict], relations: list[dict], tier_name: dict[str, str], scope: str, svg_id: str
) -> str:
    pos, width, height = layout(agents, scope)
    by_id = {a["id"]: a for a in agents}
    parts: list[str] = []
    parts.append(
        f'<svg id="{svg_id}" viewBox="0 0 {width} {height}" '
        f'preserveAspectRatio="xMidYMin meet" role="img" '
        f'aria-label="Agent ontology map">'
    )
    parts.append(
        "<defs>"
        '<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>'
        "</defs>"
    )
    # tier headers + column bands
    for t in TIER_ORDER:
        col = TIER_ORDER.index(t)
        if not any(p["tier"] == t for p in pos.values()):
            continue
        cx = LEFT + col * COL_W
        parts.append(
            f'<rect class="band" x="{cx - 12}" y="52" width="{NODE_W + 24}" '
            f'height="{height - 74}" rx="10"/>'
        )
        parts.append(
            f'<text class="tierhdr" x="{cx + NODE_W / 2}" y="40" text-anchor="middle">'
            f"Tier {esc(t)}</text>"
        )
        parts.append(
            f'<text class="tiersub" x="{cx + NODE_W / 2}" y="58" text-anchor="middle">'
            f"{esc(tier_name[t])}</text>"
        )
    # edges first, so nodes sit above them
    parts.append('<g class="edges">')
    for r in relations:
        a, b = r["from"], r["to"]
        if a not in pos or b not in pos:
            continue
        if by_id[a]["scope"] != scope or by_id[b]["scope"] != scope:
            continue
        hidden = "" if r["type"] in FLOW_TYPES else ' data-off="1"'
        parts.append(
            f'<path class="edge e-{esc(r["type"])}" data-type="{esc(r["type"])}" '
            f'data-from="{esc(a)}" data-to="{esc(b)}"{hidden} '
            f'marker-end="url(#arw)" d="{edge_path(pos[a], pos[b])}"/>'
        )
    parts.append("</g>")
    # nodes
    parts.append('<g class="nodes">')
    for a in agents:
        if a["scope"] != scope:
            continue
        p = pos[a["id"]]
        parts.append(
            f'<g class="node t{esc(a["tier"])}" data-id="{esc(a["id"])}" tabindex="0" '
            f'role="button" aria-label="{esc(a["id"])}">'
            f'<rect x="{p["x"]}" y="{p["y"]}" width="{NODE_W}" height="{NODE_H}" rx="7"/>'
            f'<text x="{p["x"] + NODE_W / 2}" y="{p["y"] + NODE_H / 2 + 4}" '
            f'text-anchor="middle">{esc(a["id"])}</text></g>'
        )
    parts.append("</g></svg>")
    return "".join(parts)


def render(data: dict, desc: dict[str, str]) -> str:
    agents = data["agents"]
    relations = data["relations"]
    tier_name = {t["id"]: t["name"] for t in data["tiers"]}
    tier_when = {t["id"]: t["when"] for t in data["tiers"]}
    rel_types = data["relation_types"]
    workflows = data["workflows"]

    user = [a for a in agents if a["scope"] == "user"]
    proj = [a for a in agents if a["scope"] == "project"]

    payload = {
        "agents": [
            {
                "id": a["id"],
                "tier": a["tier"],
                "scope": a["scope"],
                "model": a["model"],
                "access": a["access"],
                "project": a.get("project", ""),
                "role": a["role"],
                "description": desc.get(a["id"], ""),
            }
            for a in agents
        ],
        "relations": relations,
        "relationTypes": rel_types,
        "tierName": tier_name,
    }
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    h: list[str] = []
    a = h.append
    a('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width,initial-scale=1">')
    a("<title>Agent Ontology</title>")
    a("<style>")
    a("""
:root{
  --bg:#fbfbfa; --panel:#fff; --ink:#1a1a19; --muted:#6b6b66; --line:#e4e3df;
  --band:#f4f3f0; --accent:#3d5a80; --code:#f0efec;
  --t0:#8c5a3c; --t1:#6b6b3c; --t2:#3d5a80; --t3:#40695c; --t4:#6b4a70;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#16171a; --panel:#1e2024; --ink:#e8e7e3; --muted:#9b9a94; --line:#2f3238;
    --band:#1a1c20; --accent:#8fb0d4; --code:#25282e;
    --t0:#c99a75; --t1:#b3b36b; --t2:#8fb0d4; --t3:#79b3a1; --t4:#b58cbc;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding:32px 24px 72px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:-.01em}
h2{font-size:18px;margin:38px 0 12px;letter-spacing:-.01em}
h3{font-size:14px;margin:22px 0 8px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.lede{color:var(--muted);margin:0 0 22px;max-width:78ch}
code,kbd{background:var(--code);padding:1px 5px;border-radius:4px;
  font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
a{color:var(--accent)}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 14px}
.stat b{display:block;font-size:19px}
.stat span{font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px}
.controls label{display:inline-flex;align-items:center;gap:6px;background:var(--panel);
  border:1px solid var(--line);border-radius:7px;padding:5px 11px;font-size:12.5px;cursor:pointer}
.controls .hint{color:var(--muted);font-size:12.5px}
.mapwrap{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:8px;overflow-x:auto}
svg{width:100%;height:auto;min-width:1180px;display:block}
.band{fill:var(--band)}
.tierhdr{font-size:12px;font-weight:600;fill:var(--ink)}
.tiersub{font-size:10.5px;fill:var(--muted)}
.node rect{fill:var(--panel);stroke:var(--line);stroke-width:1.5;transition:stroke .12s,fill .12s}
.node text{font-size:11.5px;fill:var(--ink);pointer-events:none}
.node{cursor:pointer}
.node.t0 rect{stroke:var(--t0)} .node.t1 rect{stroke:var(--t1)} .node.t2 rect{stroke:var(--t2)}
.node.t3 rect{stroke:var(--t3)} .node.t4 rect{stroke:var(--t4)}
.node:hover rect,.node:focus rect{stroke-width:2.5;outline:none}
.edge{fill:none;stroke:var(--muted);stroke-width:1.4;opacity:.42}
.e-gates{stroke-width:2.6;opacity:.7}
.e-pairs_with{stroke-dasharray:4 3}
.e-delegates_to{stroke-dasharray:2 4;opacity:.3}
.e-authored,.e-specializes,.e-generalized_as{opacity:.5}
.edge[data-off]{display:none}
svg.sel .node rect{opacity:.32} svg.sel .node.on rect{opacity:1;stroke-width:2.6}
svg.sel .node text{opacity:.32} svg.sel .node.on text{opacity:1}
svg.sel .edge{opacity:.06} svg.sel .edge.on{opacity:.95;stroke:var(--accent);stroke-width:2.2}
.detail{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;margin-top:14px;min-height:96px}
.detail .ph{color:var(--muted)}
.detail h4{margin:0 0 4px;font-size:16px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px}
.chip{font-size:11.5px;border:1px solid var(--line);border-radius:20px;padding:2px 10px;color:var(--muted)}
.rel{font-size:13px;margin:3px 0}
.rel .rt{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;
  color:var(--accent);margin-right:6px}
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:6px 0 4px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600}
td.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;white-space:nowrap}
tr.t0 td.mono{color:var(--t0)} tr.t1 td.mono{color:var(--t1)} tr.t2 td.mono{color:var(--t2)}
tr.t3 td.mono{color:var(--t3)} tr.t4 td.mono{color:var(--t4)}
.desc{color:var(--muted);font-size:12.5px}
.wf{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:0 0 10px}
.wf b{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}
.wf ol{margin:6px 0 0;padding-left:20px;font-size:13px;color:var(--muted)}
footer{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);
  color:var(--muted);font-size:12.5px}
""")
    a('</style></head><body><div class="wrap">')

    a("<h1>Agent Ontology</h1>")
    a(
        '<p class="lede">How this pack\'s agents relate: who hands work to whom, which checks '
        "gate a merge, and where each agent's own description routes a neighbouring task away. "
        "Generated from <code>agents/ontology.yaml</code> and each agent's <code>description</code> "
        "frontmatter — regenerate with "
        "<code>uv run --no-project --with pyyaml python scripts/render_ontology_html.py</code>.</p>"
    )

    a('<div class="stats">')
    a(f'<div class="stat"><b>{len(user)}</b><span>user-level agents</span></div>')
    a(f'<div class="stat"><b>{len(proj)}</b><span>project-scoped</span></div>')
    a(f'<div class="stat"><b>{len(relations)}</b><span>relationships</span></div>')
    a(f'<div class="stat"><b>{len(data["tiers"])}</b><span>tiers</span></div>')
    a(f'<div class="stat"><b>{len(workflows)}</b><span>workflows</span></div>')
    a("</div>")

    a("<h2>Ontology map</h2>")
    a('<div class="controls">')
    for rt, on in (
        ("hands_off_to", True),
        ("gates", True),
        ("pairs_with", True),
        ("delegates_to", False),
    ):
        chk = " checked" if on else ""
        a(f'<label><input type="checkbox" class="ef" value="{rt}"{chk}> <code>{rt}</code></label>')
    a(
        '<span class="hint">Click an agent to isolate its relationships. Esc or click blank space to clear.</span>'
    )
    a("</div>")
    a('<div class="mapwrap">')
    a(svg_map(agents, relations, tier_name, "user", "map"))
    a("</div>")
    a(
        '<div class="detail" id="detail"><p class="ph">Select an agent in the map for its role, '
        "routing boundaries and full description.</p></div>"
    )

    a("<h2>Project layer</h2>")
    a(
        '<p class="lede">Agents <code>research-director</code> created inside a single engagement. '
        "They are <b>not</b> installed globally — they are mirrored in the repo for visibility, and "
        "each either specializes a user-level agent or was generalized into one.</p>"
    )
    a('<div class="mapwrap">')
    a(svg_map(agents, relations, tier_name, "project", "pmap"))
    a("</div>")

    # tiers
    a("<h2>Tiers</h2><table><tr><th>Tier</th><th>Name</th><th>When</th></tr>")
    for t in TIER_ORDER:
        a(
            f'<tr class="t{esc(t)}"><td class="mono">{esc(t)}</td><td>{esc(tier_name[t])}</td>'
            f'<td class="desc">{esc(tier_when[t])}</td></tr>'
        )
    a("</table>")

    # relationship legend
    a("<h2>Relationship types</h2><table><tr><th>Edge</th><th>Meaning</th></tr>")
    for k, v in rel_types.items():
        a(f'<tr><td class="mono">{esc(k)}</td><td class="desc">{esc(v)}</td></tr>')
    a("</table>")

    # role catalogue
    a("<h2>Agent roles</h2>")
    a(
        '<p class="lede">Every agent, its role in one line, and the full <code>description</code> '
        "that decides when it is chosen.</p>"
    )
    for scope, group, title in (("user", user, "User-level"), ("project", proj, "Project-scoped")):
        a(f"<h3>{title}</h3>")
        a(
            "<table><tr><th>Agent</th><th>Tier</th><th>Model</th>"
            f"<th>{'Access' if scope == 'user' else 'Project'}</th><th>Role</th></tr>"
        )
        for ag in sorted(group, key=lambda x: (x["tier"], x["id"])):
            fourth = ag["access"] if scope == "user" else ag.get("project", "")
            full = desc.get(ag["id"], "")
            a(
                f'<tr class="t{esc(ag["tier"])}"><td class="mono">{esc(ag["id"])}</td>'
                f'<td>{esc(ag["tier"])}</td><td class="desc">{esc(ag["model"])}</td>'
                f'<td class="desc">{esc(fourth)}</td>'
                f'<td>{esc(ag["role"])}<div class="desc" style="margin-top:5px">{esc(full)}</div></td></tr>'
            )
        a("</table>")

    # workflows
    a("<h2>Workflows</h2>")
    for wf in workflows:
        a(f'<div class="wf"><b>{esc(wf["id"])}</b><ol>')
        for step in wf["steps"]:
            a(f"<li>{esc(step)}</li>")
        a("</ol></div>")

    a(
        "<footer>Generated from <code>agents/ontology.yaml</code>. "
        "Do not edit this file by hand — edit the YAML and re-run "
        "<code>scripts/render_ontology_html.py</code>. "
        "Markdown twin: <code>agents/ONTOLOGY.md</code>.</footer>"
    )
    a("</div>")
    a(f'<script type="application/json" id="data">{blob}</script>')
    a("""<script>
(function(){
  var D = JSON.parse(document.getElementById('data').textContent);
  var byId = {}; D.agents.forEach(function(a){ byId[a.id]=a; });
  var detail = document.getElementById('detail');

  function applyFilters(){
    var on = {};
    document.querySelectorAll('.ef').forEach(function(c){ on[c.value]=c.checked; });
    document.querySelectorAll('#map .edge').forEach(function(e){
      var t = e.getAttribute('data-type');
      if(on[t]) e.removeAttribute('data-off'); else e.setAttribute('data-off','1');
    });
  }
  document.querySelectorAll('.ef').forEach(function(c){
    c.addEventListener('change', applyFilters);
  });
  applyFilters();

  function clear(){
    document.querySelectorAll('svg').forEach(function(s){ s.classList.remove('sel'); });
    document.querySelectorAll('.node.on,.edge.on').forEach(function(n){ n.classList.remove('on'); });
    detail.innerHTML = '<p class="ph">Select an agent in the map for its role, routing '
      + 'boundaries and full description.</p>';
  }

  function esc(s){ var d=document.createElement('div'); d.textContent=s==null?'':s; return d.innerHTML; }

  function select(id, svg){
    document.querySelectorAll('svg').forEach(function(s){ s.classList.remove('sel'); });
    document.querySelectorAll('.node.on,.edge.on').forEach(function(n){ n.classList.remove('on'); });
    svg.classList.add('sel');
    var self = svg.querySelector('.node[data-id="'+id+'"]');
    if(self) self.classList.add('on');
    var outs=[], ins=[];
    D.relations.forEach(function(r){
      if(r.from===id) outs.push(r);
      if(r.to===id) ins.push(r);
    });
    svg.querySelectorAll('.edge').forEach(function(e){
      var f=e.getAttribute('data-from'), t=e.getAttribute('data-to');
      if(f===id||t===id){
        if(e.hasAttribute('data-off')) return;
        e.classList.add('on');
        var other = f===id ? t : f;
        var n = svg.querySelector('.node[data-id="'+other+'"]');
        if(n) n.classList.add('on');
      }
    });
    var a = byId[id]; if(!a) return;
    var h = '<h4>'+esc(a.id)+'</h4>';
    h += '<div class="chips"><span class="chip">Tier '+esc(a.tier)+' &middot; '
       + esc(D.tierName[a.tier])+'</span><span class="chip">'+esc(a.model)+'</span>'
       + '<span class="chip">'+esc(a.access)+'</span>'
       + (a.project?'<span class="chip">'+esc(a.project)+'</span>':'')
       + '<span class="chip">'+esc(a.scope)+'-level</span></div>';
    h += '<p style="margin:0 0 10px">'+esc(a.role)+'</p>';
    if(a.description) h += '<p class="desc" style="margin:0 0 12px">'+esc(a.description)+'</p>';
    function list(rs, dir){
      if(!rs.length) return '';
      var s = '<h3 style="margin:12px 0 4px">'+dir+'</h3>';
      rs.forEach(function(r){
        var other = dir==='Outgoing' ? r.to : r.from;
        s += '<div class="rel"><span class="rt">'+esc(r.type)+'</span>'+esc(other)
           + (r.note?' <span class="desc">— '+esc(r.note)+'</span>':'')+'</div>';
      });
      return s;
    }
    h += list(outs,'Outgoing') + list(ins,'Incoming');
    detail.innerHTML = h;
  }

  document.querySelectorAll('.node').forEach(function(n){
    var svg = n.closest('svg');
    function go(ev){ ev.stopPropagation(); select(n.getAttribute('data-id'), svg); }
    n.addEventListener('click', go);
    n.addEventListener('keydown', function(ev){
      if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); go(ev); }
    });
  });
  document.querySelectorAll('svg').forEach(function(s){
    s.addEventListener('click', clear);
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') clear(); });
})();
</script>""")
    a("</body></html>")
    return "".join(h)


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    desc = load_descriptions()
    OUT.write_text(render(data, desc), encoding="utf-8")
    missing = [a["id"] for a in data["agents"] if a["id"] not in desc]
    kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT.relative_to(REPO)} ({kb:.0f} KB, self-contained).")
    if missing:
        print("  WARNING: no description frontmatter found for: " + ", ".join(missing))


if __name__ == "__main__":
    main()
