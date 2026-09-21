#!/usr/bin/env python3
"""Compile planning Markdown into a normalized PlanningPackage and standalone shaped-work HTML."""

import argparse
import html
import json
import re
from pathlib import Path

SCHEMA_VERSION = 1


class PublisherError(ValueError):
    pass


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[end + 5 :]


def section(text, heading_pattern, level=2):
    marks = "#" * level
    match = re.search(
        rf"^{marks}\s+{heading_pattern}\s*$\n(.*?)(?=^{marks}\s+|\Z)",
        text,
        re.M | re.S | re.I,
    )
    return match.group(1).strip() if match else ""


def bullets(block):
    return [m.group(1).strip() for m in re.finditer(r"^\s*-\s+(.+)$", block, re.M)]


def key_values(block):
    result = {}
    for item in bullets(block):
        if ":" in item:
            key, value = item.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def table(block):
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    rows = [[cell.strip().strip(chr(96)) for cell in line.strip("|").split("|")] for line in lines]
    if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in rows[1]):
        return []
    header = rows[0]
    return [
        dict(zip(header, row + [""] * max(0, len(header) - len(row))))
        for row in rows[2:]
    ]


def first_table(block):
    lines = block.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().startswith("|")), None)
    if start is None:
        return []
    picked = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            break
        picked.append(line)
    return table("\n".join(picked))


def title(text, suffix):
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return (match.group(1).strip() if match else "Shaped Work").replace(suffix, "")


def discover(directory, role):
    files = sorted(directory.glob("*.md"))
    if role == "frame":
        matches = [p for p in files if "frame" in p.stem.lower()]
    elif role == "shaping":
        matches = [p for p in files if "shaping" in p.stem.lower()]
    else:
        matches = [p for p in files if "breadboard" in p.stem.lower() and "reflection" not in p.stem.lower()]
        selected = []
        for path in matches:
            meta, _ = frontmatter(path.read_text(encoding="utf-8"))
            if meta.get("mode") == "selected-design":
                selected.append(path)
        matches = selected or [p for p in matches if "candidate" not in p.stem.lower()] or matches
    if not matches:
        raise PublisherError(f"Could not discover {role} Markdown in {directory}")
    return matches[0]


def shapes(text):
    block = section(text, "Shapes")
    matches = list(re.finditer(r"^###\s+([A-Z][A-Z0-9_-]*):\s+(.+)$", block, re.M))
    output = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        output.append(
            {"id": match.group(1), "name": match.group(2).strip(), "parts": first_table(block[match.end():end])}
        )
    return output


def slices(text):
    block = section(text, "Candidate vertical slices")
    matches = list(re.finditer(r"^###\s+(V[\w.-]+)\s+[—-]\s+(.+)$", block, re.M))
    output = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        body = block[match.end():end]
        demo = re.search(r"Demo:\s*(.*?)(?=\nProduces:|\Z)", body, re.S | re.I)
        produced = re.search(r"Produces:\s*(.*?)(?=\n[A-Z][A-Za-z ]+:|\Z)", body, re.S | re.I)
        output.append(
            {
                "id": match.group(1),
                "name": match.group(2).strip(),
                "demo": bullets(demo.group(1) if demo else ""),
                "produces": " ".join(x.strip("- ").strip() for x in (produced.group(1) if produced else "").splitlines() if x.strip()),
            }
        )
    return output


def parse_frame(path):
    meta, text = frontmatter(path.read_text(encoding="utf-8"))
    return {
        "source": str(path),
        "title": title(text, " — Frame"),
        "problem": bullets(section(text, "Problem")),
        "outcome": bullets(section(text, "Outcome")),
        "transformation": key_values(section(text, r"Transformation frame.*")),
        "less_about": bullets(section(text, "Less about")),
        "more_about": bullets(section(text, "More about")),
        "meta": meta,
    }


def parse_shaping(path):
    meta, text = frontmatter(path.read_text(encoding="utf-8"))
    decision = section(text, "Human Decision")
    chosen = re.search(r"Recorded human choice:\s*\*\*([^*]+)\*\*", decision, re.I)
    picked = chosen.group(1).strip() if chosen else ""
    reason = re.search(r"Reason:\s*(.*)", decision, re.S | re.I)
    shape_list = shapes(text)
    for shape in shape_list:
        shape["selected"] = shape["id"] == picked
    return {
        "source": str(path),
        "title": title(text, " — Shaping"),
        "appetite": key_values(section(text, "Accepted Appetite")),
        "requirements": first_table(section(text, "Accepted Requirements")),
        "shapes": shape_list,
        "fit": first_table(section(text, "Fit Check")),
        "appetite_fit": first_table(section(text, "Appetite Fit")),
        "reverse_fit": first_table(section(text, "Reverse Fit Check")),
        "selected_shape": picked,
        "decision_rationale": bullets(reason.group(1) if reason else ""),
        "meta": meta,
    }, text


def parse_breadboard(path):
    meta, text = frontmatter(path.read_text(encoding="utf-8"))
    chosen = re.search(r"Recorded human choice:\s*\*\*([^*]+)\*\*", section(text, "Human slice selection"), re.I)
    chosen_text = chosen.group(1).strip() if chosen else ""
    slice_id = re.match(r"(V[\w.-]+)", chosen_text)
    return {
        "source": str(path),
        "title": title(text, " — Breadboard"),
        "mode": meta.get("mode", ""),
        "places": first_table(section(text, "Places")),
        "ui": first_table(section(text, "UI Affordances")),
        "non_ui": first_table(section(text, "Non-UI Affordances")),
        "stores": first_table(section(text, "Stores")),
        "behavior_traces": first_table(section(text, "Behavior traces")),
        "reverse_trace": first_table(section(text, "Reverse-trace audit")),
        "slices": slices(text),
        "active_slice": slice_id.group(1) if slice_id else "",
        "active_slice_text": chosen_text,
        "meta": meta,
    }


def known_ids(package):
    values = set()
    values.update(row.get("ID", "") for row in package["shaping"]["requirements"])
    for shape in package["shaping"]["shapes"]:
        values.add(shape["id"])
        values.update(row.get("Part", "") for row in shape["parts"])
    for key in ("places", "ui", "non_ui", "stores"):
        values.update(row.get("ID", "") for row in package["breadboard"][key])
    values.update(row["id"] for row in package["breadboard"]["slices"])
    return {value for value in values if value}


def default_presentation(package):
    bb = package["breadboard"]
    selected = next(
        (s for s in package["shaping"]["shapes"] if s["id"] == package["shaping"]["selected_shape"]),
        package["shaping"]["shapes"][0] if package["shaping"]["shapes"] else {"parts": []},
    )
    notes = [{"ref": p.get("Part", ""), "text": p.get("Mechanism", "")} for p in selected["parts"][:6] if p.get("Part")]
    return {
        "schema_version": 1,
        "hero_place": bb["places"][0].get("ID", "") if bb["places"] else "",
        "journey_scenarios": [row.get("Scenario", "") for row in bb["behavior_traces"][:4]],
        "featured_ids": [note["ref"] for note in notes],
        "annotations": notes,
    }


def validate_presentation(package, payload):
    if payload.get("schema_version", 1) != 1:
        raise PublisherError("Only presentation schema_version 1 is supported")
    refs = [payload.get("hero_place", "")] + payload.get("featured_ids", [])
    refs += [item.get("ref", "") for item in payload.get("annotations", [])]
    unknown = sorted({ref for ref in refs if ref and ref not in known_ids(package)})
    if unknown:
        raise PublisherError("Presentation references IDs absent from canonical planning artifacts: " + ", ".join(unknown))
    return payload


def load_presentation(path, package):
    payload = json.loads(path.read_text(encoding="utf-8")) if path and path.is_file() else default_presentation(package)
    return validate_presentation(package, payload)


def build_package(planning_dir, frame_path=None, shaping_path=None, breadboard_path=None, presentation_path=None):
    directory = Path(planning_dir).resolve()
    frame_path = Path(frame_path or discover(directory, "frame")).resolve()
    shaping_path = Path(shaping_path or discover(directory, "shaping")).resolve()
    breadboard_path = Path(breadboard_path or discover(directory, "breadboard")).resolve()
    shaping, shaping_text = parse_shaping(shaping_path)
    package = {
        "schema_version": SCHEMA_VERSION,
        "kind": "PlanningPackage",
        "frame": parse_frame(frame_path),
        "shaping": shaping,
        "breadboard": parse_breadboard(breadboard_path),
        "sources": {"frame": str(frame_path), "shaping": str(shaping_path), "breadboard": str(breadboard_path)},
    }
    package["title"] = shaping["title"] or package["frame"]["title"] or package["breadboard"]["title"]
    req_auth = {row.get("Authority", "") for row in shaping["requirements"] if row.get("Authority")}
    package["authority"] = {
        "frame": "Accepted" if "## Accepted transformation frame" in shaping_text else "Source",
        "requirements": "Accepted" if req_auth == {"Accepted"} else "Mixed",
        "appetite": "Accepted" if shaping["appetite"] else "Unknown",
        "shape": "Selected" if shaping["selected_shape"] else "Working",
        "breadboard": "Accepted selected-design" if package["breadboard"]["mode"] == "selected-design" else package["breadboard"]["mode"] or "Unknown",
        "slice": "Selected build scope" if package["breadboard"]["active_slice"] else "Unselected",
    }
    if presentation_path is None and (directory / "presentation.json").is_file():
        presentation_path = directory / "presentation.json"
    package["presentation"] = load_presentation(Path(presentation_path) if presentation_path else None, package)
    return package


def esc(value):
    return html.escape(str(value or ""), quote=True)


def data_id(value):
    return f' data-plan-id="{esc(value)}"' if value else ""


def mock_surface(package):
    bb = package["breadboard"]
    hero = package["presentation"].get("hero_place") or (bb["places"][0].get("ID", "") if bb["places"] else "")
    place = next((row for row in bb["places"] if row.get("ID") == hero), bb["places"][0] if bb["places"] else {})
    controls = []
    for row in [item for item in bb["ui"] if item.get("Place") == hero]:
        label, control, rid = row.get("Affordance", ""), row.get("Control", "").lower(), row.get("ID", "")
        if "type" in control:
            kind = "input"
        elif "display" in control:
            kind = "display"
        elif any(word in label.lower() for word in ("check", "toggle", "switch", "bought")):
            kind = "toggle"
        else:
            kind = "button"
        controls.append(f'<div class="wire {kind}"{data_id(rid)}><b>{esc(rid)}</b><span>{esc(label)}</span></div>')
    return f'<div class="mock"{data_id(hero)}><header><b>{esc(hero)}</b>{esc(place.get("Place","Primary place"))}<small>selected shape</small></header><div class="mock-body">{"".join(controls)}</div></div>'


def render_html(package):
    shape = next((s for s in package["shaping"]["shapes"] if s["id"] == package["shaping"]["selected_shape"]), {})
    problem = package["frame"]["problem"][0] if package["frame"]["problem"] else ""
    outcome = package["frame"]["outcome"][0] if package["frame"]["outcome"] else ""
    appetite = package["shaping"]["appetite"]
    notes = package["presentation"].get("annotations", [])
    midpoint = (len(notes) + 1) // 2
    note_html = lambda items: "".join(f'<article class="note"{data_id(x.get("ref",""))}><b>{esc(x.get("ref"))}</b>{esc(x.get("text"))}</article>' for x in items)
    desired = package["presentation"].get("journey_scenarios", [])
    traces = [row for row in package["breadboard"]["behavior_traces"] if row.get("Scenario") in desired] or package["breadboard"]["behavior_traces"][:4]
    journey = "".join(f'<article><b>{i:02d}</b><span><strong>{esc(row.get("Scenario"))}</strong><small>{esc(row.get("Entry"))} → {esc(row.get("Observable consequence"))}</small></span></article>' for i, row in enumerate(traces, 1))
    rail = "".join(f'<span{data_id(row.get("ID",""))}><b>{esc(row.get("ID"))}</b>{esc(row.get("Affordance"))}</span>' for row in package["breadboard"]["non_ui"][:8])
    rail += "".join(f'<span class="store"{data_id(row.get("ID",""))}><b>{esc(row.get("ID"))}</b>{esc(row.get("Store"))}</span>' for row in package["breadboard"]["stores"][:5])
    shape_cards = "".join(
        f'<article class="shape {"selected" if item["selected"] else ""}"><small>Shape {esc(item["id"])} · {"Selected" if item["selected"] else "Viable / not selected"}</small><h3>{esc(item["name"])}</h3><ul>'
        + "".join(f'<li{data_id(part.get("Part",""))}><b>{esc(part.get("Part"))}</b>{esc(part.get("Mechanism"))}</li>' for part in item["parts"])
        + "</ul></article>"
        for item in package["shaping"]["shapes"]
    )
    fit = {row.get("Req", ""): row for row in package["shaping"]["fit"]}
    heads = "".join(f"<th>{esc(item['id'])}</th>" for item in package["shaping"]["shapes"])
    req_rows = "".join(
        f'<tr{data_id(row.get("ID",""))}><td><b>{esc(row.get("ID"))}</b></td><td>{esc(row.get("Requirement"))}</td><td>{esc(row.get("Authority") or row.get("Status"))}</td>'
        + "".join(f"<td>{esc(fit.get(row.get('ID',''),{}).get(item['id'],''))}</td>" for item in package["shaping"]["shapes"])
        + "</tr>"
        for row in package["shaping"]["requirements"]
    )
    active = package["breadboard"]["active_slice"]
    slice_cards = "".join(
        f'<article class="slice {"active" if item["id"] == active else ""}"{data_id(item["id"])}><small>{esc(item["id"])} · {"Selected build scope" if item["id"] == active else "Deferred accepted behavior"}</small><h3>{esc(item["name"])}</h3><p>{esc(item["produces"])}</p></article>'
        for item in package["breadboard"]["slices"]
    )
    embedded = json.dumps(package, ensure_ascii=False).replace("</", "<\\/")
    css = """
:root{--ink:#102018;--muted:#647168;--paper:#f7f6ef;--card:#fffef9;--line:#d7d7ce;--accent:#1e5e43;--soft:#dceadf;--note:#fff4bf}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 Inter,system-ui,sans-serif}.page{max-width:1440px;margin:auto;padding:28px clamp(14px,4vw,56px) 70px}
.mast{display:flex;justify-content:space-between;gap:20px;align-items:end}.mast h1{font-size:clamp(30px,5vw,54px);letter-spacing:-.05em;line-height:.95;margin:4px 0}.eyebrow,small{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:800}.eyebrow{color:var(--accent)}
.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:24px 0}.card,.panel,.shape,.slice{background:var(--card);border:1px solid var(--line);border-radius:16px}.card{padding:15px;min-height:120px}.card h2{font-size:11px;text-transform:uppercase;color:var(--muted);letter-spacing:.08em}.panel{padding:clamp(15px,2.5vw,28px);margin-top:14px}.panel-head{display:flex;justify-content:space-between;gap:20px;align-items:end}.panel h2{font-size:clamp(22px,3vw,34px);margin:4px 0 18px}
.board{background:#efeee7;border:1px solid #d2d1c7;border-radius:16px;padding:16px}.journey{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.journey article{background:white;border:1px solid var(--line);border-radius:10px;padding:10px;display:flex;gap:8px}.journey b{color:var(--accent);font-size:10px}.journey strong,.journey small{display:block}.journey small{text-transform:none;letter-spacing:0;font-weight:500;margin-top:2px}
.board-main{display:grid;grid-template-columns:.8fr 1.6fr .8fr;gap:16px;align-items:center;min-height:420px}.notes{display:grid;gap:10px}.note{background:var(--note);border:1px solid #dcca75;padding:10px;border-radius:9px;transform:rotate(-1deg);font-size:13px}.note:nth-child(even){transform:rotate(1deg)}.note b{display:block;font-size:10px;color:#6a5615;margin-bottom:4px}
.mock{background:white;border:2px solid #26352c;border-radius:18px;overflow:hidden;box-shadow:0 15px 40px #1b2b221f}.mock header{padding:12px;display:grid;grid-template-columns:auto 1fr auto;gap:8px;border-bottom:1px solid var(--line)}.mock header b{color:var(--accent)}.mock-body{min-height:320px;padding:20px;display:grid;gap:10px;align-content:start}.wire{border:1px solid #7e8881;border-radius:8px;padding:11px;display:flex;gap:8px}.wire.button{background:#183f2f;color:white;border:0}.wire.toggle:before{content:'✓';border:1px solid #708078;border-radius:4px;width:20px;height:20px;display:grid;place-items:center}.wire.display{min-height:80px}.wire b{font-size:10px}
.rail{margin-top:18px;border-top:1px dashed #999f99;padding-top:12px;display:flex;gap:7px;flex-wrap:wrap}.rail span{background:white;border:1px solid var(--line);border-radius:999px;padding:6px 9px;font-size:12px}.rail .store{background:#e7f0e7}.rail b{font-size:10px;color:var(--accent);margin-right:5px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.shape,.slice{padding:15px}.shape.selected,.slice.active{border:2px solid var(--accent);background:#fbfffb}.shape h3,.slice h3{margin:8px 0}.shape li{margin:6px 0}.shape li b{display:inline-block;min-width:28px;color:var(--accent);font-size:10px}
.table{overflow:auto;border:1px solid var(--line);border-radius:12px}table{width:100%;border-collapse:collapse;min-width:700px;background:white}th,td{padding:10px;border-bottom:1px solid #e5e6e0;text-align:left}th{font-size:10px;text-transform:uppercase;color:var(--muted)}
[data-plan-id]{cursor:pointer}[data-plan-id].hit{outline:3px solid #d39f13;outline-offset:2px}.inspector{position:fixed;right:14px;bottom:14px;background:#102018;color:white;padding:10px 12px;border-radius:10px;display:none;max-width:330px}.inspector.show{display:block}
@media(max-width:900px){.summary,.journey{grid-template-columns:1fr 1fr}.board-main{grid-template-columns:1fr}.notes{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.mast,.panel-head{align-items:start;flex-direction:column}}
@media(max-width:560px){.page{padding:16px 10px 50px}.summary,.journey,.notes{grid-template-columns:1fr}.board{padding:10px}}
"""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(package["title"])} · Shaped Work</title><style>{css}</style></head><body>
<main class="page"><header class="mast"><div><div class="eyebrow">Planning Publisher · canonical artifacts → human view</div><h1>{esc(package["title"])}</h1></div><p>Derived projection. Canonical planning Markdown remains authoritative. Click a labeled element to trace its stable ID.</p></header>
<section class="summary"><article class="card"><h2>Problem</h2>{esc(problem)}</article><article class="card"><h2>Outcome</h2>{esc(outcome)}</article><article class="card"><h2>Appetite</h2>{esc(appetite.get("Time budget",""))}<p><b>Cut:</b> {esc(appetite.get("Cut line",""))}</p></article><article class="card"><h2>Selected shape</h2><b>{esc(package["shaping"]["selected_shape"])} · {esc(shape.get("name",""))}</b></article></section>
<section class="panel"><div class="panel-head"><div><div class="eyebrow">Composite shape board</div><h2>See the behavior, not just the Markdown.</h2></div><p>Journey first. Selected surface in the center. Mechanisms annotate the product. Hidden behavior stays on a secondary rail.</p></div><div class="board"><div class="journey">{journey}</div><div class="board-main"><div class="notes">{note_html(notes[:midpoint])}</div>{mock_surface(package)}<div class="notes">{note_html(notes[midpoint:])}</div></div><small>System rail · hidden consequences and stores</small><div class="rail">{rail}</div></div></section>
<section class="panel"><div class="eyebrow">Decision record</div><h2>Shapes and selected direction</h2><div class="grid">{shape_cards}</div></section>
<section class="panel"><div class="eyebrow">Judging criteria</div><h2>Requirements × shapes</h2><div class="table"><table><thead><tr><th>ID</th><th>Requirement</th><th>Authority</th>{heads}</tr></thead><tbody>{req_rows}</tbody></table></div></section>
<section class="panel"><div class="eyebrow">Build boundary</div><h2>Selected and deferred slices</h2><div class="grid">{slice_cards}</div></section></main>
<div class="inspector" id="inspector"></div><script type="application/json" id="planning-package">{embedded}</script><script>
const box=document.getElementById('inspector');document.addEventListener('click',e=>{{const t=e.target.closest('[data-plan-id]');document.querySelectorAll('.hit').forEach(x=>x.classList.remove('hit'));if(!t){{box.classList.remove('show');return}}const id=t.dataset.planId;document.querySelectorAll('[data-plan-id="'+CSS.escape(id)+'"]').forEach(x=>x.classList.add('hit'));box.textContent=id+' · stable planning ID. Edit canonical planning truth, then regenerate.';box.classList.add('show')}});
</script></body></html>"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--planning-dir", type=Path, default=Path("planning"))
    parser.add_argument("--frame", type=Path)
    parser.add_argument("--shaping", type=Path)
    parser.add_argument("--breadboard", type=Path)
    parser.add_argument("--presentation", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    package = build_package(args.planning_dir, args.frame, args.shaping, args.breadboard, args.presentation)
    if args.check:
        print(f"PlanningPackage OK: {len(package['shaping']['requirements'])} requirements, {len(package['shaping']['shapes'])} shapes, {len(package['breadboard']['behavior_traces'])} behavior traces.")
        return 0
    output = args.output or args.planning_dir / "shaped-work.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(package), encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
