"""Normalization and visual rendering helpers for publish_shaped_work.py."""

import base64
import html
import json
import re
from pathlib import Path

OPTIONAL_ARTIFACTS = {
    "appetite": ("appetite",),
    "slices": ("slices",),
    "statechart": ("statechart",),
    "interface_contracts": ("interface-contract", "contracts"),
    "executable_breadboard": ("executable-breadboard",),
    "dumplink": ("dumplink",),
    "kickoff": ("kickoff",),
    "context_packet": ("context-packet", "context_packet"),
}
TYPED_TABLES = {
    "statechart": {"states": "State inventory", "transitions": "Transition table"},
    "interface_contracts": {"contracts": "Contract summary"},
    "executable_breadboard": {"selected_slice": "Selected slice", "contracts": "Interface contracts", "edge_cases": "Edge cases"},
    "dumplink": {
        "tasks": "Task dump", "task_groups": "Vertical task groups", "dependencies": "Dependency map",
        "sequence": "Build sequence", "cuts": "Scope cuts", "acceptance_checks": "Acceptance checks",
    },
}


def _frontmatter(text):
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
    return meta, text[end + 5:]


def _section(text, heading):
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)", text, re.M | re.S | re.I)
    return match.group(1).strip() if match else ""


def _table(block):
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    rows = [[cell.strip().strip(chr(96)) for cell in line.strip("|").split("|")] for line in lines]
    if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in rows[1]):
        return []
    header = rows[0]
    return [dict(zip(header, row + [""] * max(0, len(header) - len(row)))) for row in rows[2:]]


def _first_table(block):
    lines = block.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().startswith("|")), None)
    if start is None:
        return []
    picked = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            break
        picked.append(line)
    return _table("\n".join(picked))


def _title(text, fallback):
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else fallback


def _portable(path, directory):
    try:
        return str(path.relative_to(directory))
    except ValueError:
        return path.name


def _discover_optional(directory, excluded):
    found = {}
    for kind, tokens in OPTIONAL_ARTIFACTS.items():
        for path in sorted(directory.glob("*.md")):
            if path.resolve() in excluded:
                continue
            if any(token in path.stem.lower() for token in tokens):
                found[kind] = path.resolve()
                break
    return found


def _parse_optional(path, kind, directory):
    meta, text = _frontmatter(path.read_text(encoding="utf-8"))
    artifact = {
        "kind": kind,
        "source": _portable(path, directory),
        "title": _title(text, path.stem),
        "meta": meta,
        "stable_ids": sorted(set(re.findall(r"\b(?:R|P|U|N|S|ST|TR|C|RUN|E|SP|TG|CUT|V|SK)\d+(?:\.\d+)?\b", text))),
    }
    for key, heading in TYPED_TABLES.get(kind, {}).items():
        artifact[key] = _first_table(_section(text, heading))
    return artifact


def _targeted_sketches(path):
    _, text = _frontmatter(path.read_text(encoding="utf-8"))
    block = _section(text, "Targeted sketches")
    rows = _first_table(block)
    if rows:
        return [
            {
                "id": row.get("Sketch", ""),
                "refs": re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", row.get("Elaborates", "")),
                "label": row.get("Question resolved", "") or row.get("Elaborates", ""),
                "states_controls": row.get("States / controls shown", ""),
                "status": row.get("Status", ""),
            }
            for row in rows
            if re.fullmatch(r"SK\d+", row.get("Sketch", ""))
        ]
    output = []
    for match in re.finditer(r"^\s*(SK\d+)\s*(?:→|->|:)\s*(.+)$", block, re.M):
        output.append({
            "id": match.group(1),
            "refs": re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", match.group(2)),
            "label": match.group(2).strip(),
            "states_controls": "",
            "status": "",
        })
    return output


def _all_ids(package):
    ids = set()
    ids.update(row.get("ID", "") for row in package["shaping"]["requirements"])
    for shape in package["shaping"]["shapes"]:
        ids.add(shape["id"])
        ids.update(row.get("Part", "") for row in shape["parts"])
    for key in ("places", "ui", "non_ui", "stores"):
        ids.update(row.get("ID", "") for row in package["breadboard"][key])
    ids.update(row["id"] for row in package["breadboard"]["slices"])
    ids.update(item["id"] for item in package["breadboard"].get("targeted_sketches", []))
    for artifact in package.get("artifacts", {}).values():
        ids.update(artifact.get("stable_ids", []))
    return {value for value in ids if value}


def _kind(row):
    label = (row.get("Affordance") or row.get("Place") or "").lower()
    control = row.get("Control", "").lower()
    if row.get("ID", "").startswith("P"):
        return "screen"
    if "type" in control or "input" in label:
        return "input"
    if "display" in control:
        return "display"
    if any(word in label for word in ("check", "toggle", "switch", "bought")):
        return "toggle"
    return "button"


def _default_hints(package):
    hints = {}
    for order, row in enumerate(package["breadboard"]["places"], 1):
        hints[row.get("ID", "")] = {"kind": "screen", "region": "body", "order": order}
    for order, row in enumerate(package["breadboard"]["ui"], 1):
        hints[row.get("ID", "")] = {"kind": _kind(row), "region": "body", "order": order}
    return {key: value for key, value in hints.items() if key}


def _trace_refs(row):
    return set(re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", " ".join(row.values())))


def _default_scopes(package):
    scopes = {}
    traces = package["breadboard"]["behavior_traces"]
    primary = package["breadboard"]["places"][0].get("ID", "") if package["breadboard"]["places"] else ""
    for item in package["breadboard"]["slices"]:
        words = set(re.findall(r"[a-z0-9]+", (item["name"] + " " + " ".join(item["demo"])).lower()))
        refs = {primary} if primary else set()
        for trace in traces:
            if words & set(re.findall(r"[a-z0-9]+", " ".join(trace.values()).lower())):
                refs.update(_trace_refs(trace))
        scopes[item["id"]] = sorted(refs)
    return scopes


def _visual_model(package):
    presentation = package["presentation"]
    places = []
    for place in package["breadboard"]["places"]:
        pid = place.get("ID", "")
        hint = presentation.get("visual_hints", {}).get(pid, {})
        affordances = []
        for row in package["breadboard"]["ui"]:
            if row.get("Place") != pid:
                continue
            ref = row.get("ID", "")
            ui_hint = presentation.get("visual_hints", {}).get(ref, {})
            affordances.append({
                "id": ref,
                "kind": ui_hint.get("kind", _kind(row)),
                "region": ui_hint.get("region", "body"),
                "order": ui_hint.get("order", 999),
            })
        places.append({
            "id": pid,
            "kind": hint.get("kind", "screen"),
            "order": hint.get("order", 999),
            "hero": pid == presentation.get("hero_place"),
            "affordances": sorted(affordances, key=lambda item: (item["order"], item["id"])),
        })
    slices = []
    active = package["breadboard"]["active_slice"]
    for item in package["breadboard"]["slices"]:
        slices.append({
            "id": item["id"],
            "name": item["name"],
            "scope": presentation.get("slice_scopes", {}).get(item["id"], []),
            "authority": "selected-build-scope" if item["id"] == active else "deferred-accepted",
        })
    journey = []
    desired = set(presentation.get("journey_scenarios", []))
    for row in package["breadboard"]["behavior_traces"]:
        if desired and row.get("Scenario") not in desired:
            continue
        journey.append({
            "scenario": row.get("Scenario", ""),
            "refs": list(dict.fromkeys(re.findall(
                r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b",
                " ".join(str(value) for value in row.values()),
            ))),
        })
    return {
        "schema_version": 1,
        "places": sorted(places, key=lambda item: (0 if item["hero"] else 1, item["order"], item["id"])),
        "system_rail": [
            row.get("ID", "") for row in package["breadboard"]["non_ui"] + package["breadboard"]["stores"] if row.get("ID")
        ],
        "journey": journey,
        "annotations": presentation.get("annotations", []),
        "sketches": package["breadboard"].get("targeted_sketches", []),
        "slices": slices,
    }


def augment_package(package, planning_dir):
    directory = Path(planning_dir).resolve()
    core = {directory / source for source in package["sources"].values() if isinstance(source, str)}
    optional = _discover_optional(directory, {path.resolve() for path in core})
    package["schema_version"] = 2
    package["artifacts"] = {kind: _parse_optional(path, kind, directory) for kind, path in optional.items()}
    package["sources"]["optional"] = {kind: _portable(path, directory) for kind, path in optional.items()}
    package["breadboard"]["targeted_sketches"] = _targeted_sketches(directory / package["sources"]["breadboard"])

    presentation = package["presentation"]
    presentation["schema_version"] = 2
    presentation.setdefault("visual_hints", _default_hints(package))
    presentation.setdefault("slice_scopes", _default_scopes(package))
    presentation.setdefault("annotations", [])
    presentation.setdefault("featured_ids", [])
    presentation.setdefault("journey_scenarios", [])
    presentation.setdefault("sketch_assets", {})

    embedded_assets = {}
    for sketch_id, relative in presentation["sketch_assets"].items():
        candidate = (directory / relative).resolve()
        if directory not in (candidate, *candidate.parents):
            raise ValueError(f"Sketch asset for {sketch_id} must stay inside the planning directory")
        if not candidate.is_file():
            raise ValueError(f"Sketch asset for {sketch_id} does not exist: {relative}")
        suffix = candidate.suffix.lower()
        mime = {
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(suffix)
        if not mime:
            raise ValueError(f"Unsupported sketch asset type for {sketch_id}: {suffix}")
        payload = base64.b64encode(candidate.read_bytes()).decode("ascii")
        embedded_assets[sketch_id] = f"data:{mime};base64,{payload}"
    presentation["embedded_sketch_assets"] = embedded_assets

    known = _all_ids(package)
    refs = [presentation.get("hero_place", "")] + list(presentation.get("featured_ids", []))
    refs += [item.get("ref", "") for item in presentation.get("annotations", [])]
    refs += list(presentation["visual_hints"].keys())
    refs += list(presentation["sketch_assets"].keys())
    for hint in presentation["visual_hints"].values():
        if not isinstance(hint, dict):
            raise ValueError("Every visual hint must be an object")
        refs += hint.get("refs", [])
    canonical_slices = {item["id"] for item in package["breadboard"]["slices"]}
    for slice_id, slice_refs in presentation["slice_scopes"].items():
        if slice_id not in canonical_slices:
            raise ValueError(f"Presentation slice scope {slice_id} is not a canonical slice")
        refs += slice_refs
    unknown = sorted({ref for ref in refs if ref and ref not in known})
    if unknown:
        raise ValueError("Presentation references IDs absent from canonical planning artifacts: " + ", ".join(unknown))
    package["visual_model"] = _visual_model(package)
    return package


def _e(value):
    return html.escape(str(value or ""), quote=True)


def _data(ref):
    return f' data-plan-id="{_e(ref)}"' if ref else ""


def _hint(package, ref):
    return package["presentation"].get("visual_hints", {}).get(ref, {})


def _affordance(package, row):
    ref = row.get("ID", "")
    hint = _hint(package, ref)
    kind = hint.get("kind", _kind(row))
    wire_meta = " · ".join(value for value in (row.get("Control",""), row.get("Wires Out",""), row.get("Returns To","")) if value and value != "—")
    return (
        f'<div class="wire {_e(kind)}"{_data(ref)}><b>{_e(ref)}</b>'
        f'<span>{_e(row.get("Affordance"))}</span><small>{_e(wire_meta)}</small></div>'
    )


def _place(package, place, scope=None):
    pid = place.get("ID", "")
    hint = _hint(package, pid)
    rows = [row for row in package["breadboard"]["ui"] if row.get("Place") == pid]
    if scope is not None:
        rows = [row for row in rows if row.get("ID") in scope]
    rows.sort(key=lambda row: (_hint(package, row.get("ID", "")).get("order", 999), row.get("ID", "")))
    regions = {}
    for row in rows:
        regions.setdefault(_hint(package, row.get("ID", "")).get("region", "body"), []).append(_affordance(package, row))
    body = "".join(
        f'<div class="place-region region-{_e(region)}">{"".join(items)}</div>'
        for region, items in regions.items()
    ) or '<div class="empty">No user-facing affordance in this scope.</div>'
    return (
        f'<article class="place-card {_e(hint.get("kind","screen"))}"{_data(pid)}>'
        f'<header><span><b>{_e(pid)}</b>{_e(place.get("Place"))}</span><small>{_e(hint.get("kind","screen"))}</small></header>'
        f'<p>{_e(place.get("Description"))}</p><div class="place-body">{body}</div></article>'
    )


def _system_board(package, scope=None):
    scope = set(scope) if scope else None
    places = package["breadboard"]["places"]
    if scope:
        places = [row for row in places if row.get("ID") in scope] or places[:1]
    hero = package["presentation"].get("hero_place")
    places = sorted(places, key=lambda row: (0 if row.get("ID") == hero else 1, _hint(package, row.get("ID","")).get("order",999)))
    cards = "".join(_place(package, row, scope) for row in places)
    system = package["breadboard"]["non_ui"]
    stores = package["breadboard"]["stores"]
    if scope:
        system = [row for row in system if row.get("ID") in scope]
        stores = [row for row in stores if row.get("ID") in scope]
    rail = "".join(
        f'<span{_data(row.get("ID",""))}><b>{_e(row.get("ID"))}</b>{_e(row.get("Affordance"))}'
        + (f'<small>{_e(row.get("Wires Out",""))}</small>' if row.get("Wires Out") and row.get("Wires Out") != "—" else "")
        + '</span>' for row in system[:12]
    ) + "".join(
        f'<span class="store"{_data(row.get("ID",""))}><b>{_e(row.get("ID"))}</b>{_e(row.get("Store"))}</span>' for row in stores[:8]
    )
    sketches = package["breadboard"].get("targeted_sketches", [])
    if scope:
        sketches = [item for item in sketches if set(item["refs"]) & scope]
    assets = package["presentation"].get("embedded_sketch_assets", {})
    sketch_html = "".join(
        f'<article class="sketch"{_data(item["id"])}><b>{_e(item["id"])}</b>'
        + (f'<img src="{assets[item["id"]]}" alt="{_e(item["id"])} targeted sketch">' if item["id"] in assets else "")
        + f'<span>{_e(item["label"])}</span><small>{" · ".join(_e(ref) for ref in item["refs"])}</small>'
        + (f'<small>{_e(item.get("states_controls",""))}</small>' if item.get("states_controls") else "")
        + '</article>' for item in sketches
    )
    return (
        f'<div class="place-grid">{cards}</div><div class="rail-label">System rail · hidden consequences and stores</div>'
        f'<div class="rail">{rail or "<em>None in this scope</em>"}</div>'
        + (f'<div class="sketch-grid">{sketch_html}</div>' if sketch_html else "")
    )


def _slice_views(package):
    scopes = package["presentation"].get("slice_scopes", {})
    active = package["breadboard"]["active_slice"]
    cards = []
    for item in package["breadboard"]["slices"]:
        scope = set(scopes.get(item["id"], []))
        traces = [row for row in package["breadboard"]["behavior_traces"] if not scope or _trace_refs(row) & scope]
        trace_html = "".join(
            f'<li><b>{_e(row.get("Scenario"))}</b><span>{_e(row.get("Entry"))} → {_e(row.get("Observable consequence"))}</span></li>'
            for row in traces[:4]
        )
        cards.append(
            f'<article class="slice-detail {"active" if item["id"]==active else ""}"{_data(item["id"])}>'
            f'<header><div><small>{_e(item["id"])} · {"Selected build scope" if item["id"]==active else "Deferred accepted behavior"}</small>'
            f'<h3>{_e(item["name"])}</h3><p>{_e(item["produces"])}</p></div>'
            f'<button class="scope-button" data-scope="{_e(item["id"])}">Isolate on board</button></header>'
            f'<div class="slice-board">{_system_board(package, scope or None)}</div>'
            f'<ul class="slice-traces">{trace_html}</ul></article>'
        )
    return "".join(cards)


def _optional_cards(package):
    cards = []
    for kind, artifact in package.get("artifacts", {}).items():
        counts = [f"{len(artifact[key])} {key.replace('_',' ')}" for key in TYPED_TABLES.get(kind,{}) if artifact.get(key)]
        cards.append(
            f'<article class="artifact-card"><small>{_e(kind.replace("_"," "))}</small><h3>{_e(artifact["title"])}</h3>'
            f'<p>{_e(" · ".join(counts) or str(len(artifact["stable_ids"])) + " stable IDs")}</p><code>{_e(artifact["source"])}</code></article>'
        )
    return "".join(cards)


CSS = r"""
:root{--ink:#132018;--muted:#68736c;--paper:#f6f5ee;--card:#fffef9;--line:#d6d7ce;--accent:#245b43;--note:#fff3b7}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 Inter,system-ui,sans-serif}.page{max-width:1480px;margin:auto;padding:28px clamp(14px,4vw,56px) 80px}
.mast{display:flex;justify-content:space-between;gap:20px;align-items:end}.mast h1{font-size:clamp(32px,5vw,56px);letter-spacing:-.055em;line-height:.95;margin:4px 0}.eyebrow,small{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:800}.eyebrow{color:var(--accent)}
.authority-strip{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0 4px}.authority-chip{border:1px solid var(--line);background:white;border-radius:999px;padding:6px 9px;font-size:11px}.authority-chip b{margin-right:5px}.authority-chip.accepted,.authority-chip.selected{background:#dcefe4;border-color:#9ab9a5}.authority-chip.working,.authority-chip.candidate-shape{background:#fff3b7;border-color:#dcca75}.authority-chip.unselected{background:#ecece7;color:#626a64}.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0 24px}.card,.panel,.shape,.slice-detail,.artifact-card{background:var(--card);border:1px solid var(--line);border-radius:16px}.card,.shape,.artifact-card{padding:15px}.panel{padding:clamp(15px,2.5vw,28px);margin-top:14px}.panel h2{font-size:clamp(22px,3vw,34px);margin:4px 0 18px}.panel-head,.slice-detail>header{display:flex;justify-content:space-between;gap:20px;align-items:start}
.board,.slice-board{background:#eeede6;border:1px solid #d2d1c7;border-radius:16px;padding:14px}.journey{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}.journey article{background:white;border:1px solid var(--line);border-radius:10px;padding:10px}.journey strong,.journey small{display:block}.journey small{text-transform:none;letter-spacing:0}.path-ribbon{display:flex;gap:4px;align-items:center;flex-wrap:wrap;margin-top:7px}.path-ribbon button{font:inherit;font-size:10px;border:1px solid #b9c1bb;background:#f7f9f7;border-radius:999px;padding:3px 6px;cursor:pointer}.path-ribbon i{font-style:normal;color:var(--muted);font-size:10px}
.annotation-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}.note{background:var(--note);border:1px solid #dcca75;padding:10px;border-radius:9px}.note.decision{background:#dcefe4}.note.unknown,.note.rabbit-hole{background:#ffe1d8}.note.cut{background:#e7e4f4}.note b{display:block;font-size:10px}
.place-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;align-items:start}.place-card{background:white;border:1px solid #abb2ac;border-radius:14px;overflow:hidden;min-height:210px}.place-card:first-child{grid-column:span 2;border:2px solid #31443a}.place-card header{padding:10px 12px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between}.place-card header b{color:var(--accent);margin-right:8px}.place-card>p{font-size:12px;color:var(--muted);padding:0 12px}.place-body,.place-region{display:grid;gap:8px}.place-body{padding:12px}.region-header{border-bottom:1px dashed #c9cdc8;padding-bottom:8px}.region-footer{border-top:1px dashed #c9cdc8;padding-top:8px}
.wire{border:1px solid #7e8881;border-radius:8px;padding:10px;display:grid;grid-template-columns:auto 1fr auto;gap:8px}.wire.button{background:#183f2f;color:white}.wire b{font-size:10px}.wire small{text-transform:none;letter-spacing:0}.rail-label{margin-top:14px;font-size:10px;text-transform:uppercase;color:var(--muted)}.rail{border-top:1px dashed #999f99;padding-top:10px;display:flex;gap:7px;flex-wrap:wrap}.rail span{background:white;border:1px solid var(--line);border-radius:999px;padding:6px 9px;font-size:12px}.rail span small{display:block;text-transform:none;letter-spacing:0;margin-left:25px}.rail .store{background:#e7f0e7}.rail b{color:var(--accent);margin-right:5px;font-size:10px}
.sketch-grid,.grid,.artifact-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.sketch{border:1px dashed #727970;background:#fffef6;border-radius:10px;padding:12px}.sketch b,.sketch span,.sketch small{display:block}.sketch img{display:block;width:100%;max-height:360px;object-fit:contain;margin:8px 0;border:1px solid var(--line);background:white;border-radius:8px}.shape.selected,.slice-detail.active{border:2px solid var(--accent);background:#fbfffb}.shape li b{display:inline-block;min-width:28px;color:var(--accent);font-size:10px}.shape-alt{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:0}.shape-alt summary{padding:15px;cursor:pointer;font-weight:700}.shape-alt .shape-body{padding:0 15px 15px}.shape-alt small{display:block;margin-bottom:5px}
.table{overflow:auto;border:1px solid var(--line);border-radius:12px}table{width:100%;border-collapse:collapse;min-width:700px;background:white}th,td{padding:10px;border-bottom:1px solid #e5e6e0;text-align:left}th{font-size:10px;text-transform:uppercase;color:var(--muted)}
.slice-stack{display:grid;gap:14px}.slice-detail{padding:16px}.slice-board .place-card:first-child{grid-column:span 1}.slice-traces{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding:0;list-style:none}.slice-traces li{border:1px solid var(--line);border-radius:9px;padding:9px}.slice-traces b,.slice-traces span{display:block}.scope-button{border:1px solid var(--accent);background:white;color:var(--accent);border-radius:999px;padding:8px 11px;font-weight:700;cursor:pointer}.scope-button.active{background:var(--accent);color:white}
[data-plan-id]{cursor:pointer;transition:opacity .15s}[data-plan-id].hit{outline:3px solid #d39f13;outline-offset:2px}body.scope-mode [data-plan-id].dim{opacity:.18;filter:grayscale(1)}.inspector{position:fixed;right:14px;bottom:14px;background:#102018;color:white;padding:10px 12px;border-radius:10px;display:none;max-width:350px;z-index:5}.inspector.show{display:block}
@media(max-width:900px){.summary,.journey,.place-grid,.annotation-grid{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr}.place-card:first-child{grid-column:span 2}}
@media(max-width:620px){.page{padding:16px 10px 60px}.summary,.journey,.place-grid,.annotation-grid,.grid,.artifact-grid,.sketch-grid,.slice-traces{grid-template-columns:1fr}.place-card:first-child{grid-column:span 1}.mast,.panel-head,.slice-detail>header{align-items:start;flex-direction:column}}
"""


def render_enhanced_html(package):
    shape = next((s for s in package["shaping"]["shapes"] if s["id"] == package["shaping"]["selected_shape"]), {})
    problem = package["frame"]["problem"][0] if package["frame"]["problem"] else ""
    outcome = package["frame"]["outcome"][0] if package["frame"]["outcome"] else ""
    appetite = package["shaping"]["appetite"]
    selected = package["shaping"]["selected_shape"]
    label = selected + " · " + shape.get("name", "") if selected else "No human-selected shape"
    desired = package["presentation"].get("journey_scenarios", [])
    traces = [row for row in package["breadboard"]["behavior_traces"] if row.get("Scenario") in desired] or package["breadboard"]["behavior_traces"][:4]
    journey_parts = []
    for i, row in enumerate(traces, 1):
        path_text = " ".join(
            value for value in (
                row.get("Entry",""),
                row.get("Control path",""),
                row.get("State / data effect",""),
                row.get("Observable consequence",""),
            ) if value
        )
        ordered = []
        for ref in re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", path_text):
            if not ordered or ordered[-1] != ref:
                ordered.append(ref)
        ribbon = '<div class="path-ribbon">' + '<i>→</i>'.join(
            f'<button type="button" data-jump-id="{_e(ref)}">{_e(ref)}</button>' for ref in ordered[:12]
        ) + '</div>'
        journey_parts.append(
            f'<article><b>{i:02d}</b><strong>{_e(row.get("Scenario"))}</strong>'
            f'<small>{_e(row.get("Entry"))} → {_e(row.get("Observable consequence"))}</small>{ribbon}</article>'
        )
    journey = "".join(journey_parts)
    annotations = "".join(
        f'<article class="note {_e(item.get("kind","note"))}"{_data(item.get("ref",""))}><b>{_e(item.get("ref"))}</b>{_e(item.get("text"))}</article>'
        for item in package["presentation"].get("annotations", [])
    )
    shape_blocks = []
    for item in package["shaping"]["shapes"]:
        parts = "".join(f'<li{_data(part.get("Part",""))}><b>{_e(part.get("Part"))}</b>{_e(part.get("Mechanism"))}</li>' for part in item["parts"])
        if item["selected"]:
            shape_blocks.append(
                f'<article class="shape selected"><small>Shape {_e(item["id"])} · Selected</small><h3>{_e(item["name"])}</h3><ul>{parts}</ul></article>'
            )
        else:
            shape_blocks.append(
                f'<details class="shape-alt"><summary>Shape {_e(item["id"])} · {_e(item["name"])}</summary><div class="shape-body"><small>Unselected candidate · collapsed by default</small><ul>{parts}</ul></div></details>'
            )
    shapes = "".join(shape_blocks)
    fit = {row.get("Req",""): row for row in package["shaping"]["fit"]}
    heads = "".join(f"<th>{_e(item['id'])}</th>" for item in package["shaping"]["shapes"])
    requirements = "".join(
        f'<tr{_data(row.get("ID",""))}><td><b>{_e(row.get("ID"))}</b></td><td>{_e(row.get("Requirement"))}</td><td>{_e(row.get("Authority") or row.get("Status"))}</td>'
        + "".join(f"<td>{_e(fit.get(row.get('ID',''),{}).get(item['id'],''))}</td>" for item in package["shaping"]["shapes"]) + "</tr>"
        for row in package["shaping"]["requirements"]
    )
    optional = _optional_cards(package)
    authority = package.get("authority", {})
    authority_items = [
        ("Frame", authority.get("frame", "Unknown")),
        ("Requirements", authority.get("requirements", "Unknown")),
        ("Shape", authority.get("shape", "Unknown")),
        ("Breadboard", authority.get("breadboard", "Unknown")),
        ("Slice", authority.get("slice", "Unknown")),
    ]
    authority_html = "".join(
        f'<span class="authority-chip {_e(value.lower().replace(" ","-"))}"><b>{_e(name)}</b>{_e(value)}</span>'
        for name, value in authority_items
    )
    embedded = json.dumps(package, ensure_ascii=False).replace("</", "<\\/")
    optional_section = f'<section class="panel"><div class="eyebrow">Supporting artifacts</div><h2>Downstream shaped-work context</h2><div class="artifact-grid">{optional}</div></section>' if optional else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{_e(package["title"])} · Shaped Work</title><style>{CSS}</style></head><body>
<main class="page"><header class="mast"><div><div class="eyebrow">Planning Publisher · canonical artifacts → human view</div><h1>{_e(package["title"])}</h1></div><p>Derived projection. Canonical planning Markdown remains authoritative. Click stable IDs or isolate a slice.</p></header>
<div class="authority-strip">{authority_html}</div>
<section class="summary"><article class="card"><small>Problem</small><p>{_e(problem)}</p></article><article class="card"><small>Outcome</small><p>{_e(outcome)}</p></article><article class="card"><small>Appetite</small><p>{_e(appetite.get("Time budget",""))}</p><p><b>Cut:</b> {_e(appetite.get("Cut line",""))}</p></article><article class="card"><small>Selected shape</small><p><b>{_e(label)}</b></p></article></section>
<section class="panel"><div class="panel-head"><div><div class="eyebrow">Composite shape board</div><h2>See the shaped behavior as one system.</h2></div><button class="scope-button" data-scope="">Show full system</button></div><div class="board"><div class="journey">{journey}</div><div class="annotation-grid">{annotations}</div>{_system_board(package)}</div></section>
<section class="panel"><div class="eyebrow">Decision record</div><h2>Shapes and selected direction</h2><div class="grid">{shapes}</div></section>
<section class="panel"><div class="eyebrow">Judging criteria</div><h2>Requirements × shapes</h2><div class="table"><table><thead><tr><th>ID</th><th>Requirement</th><th>Authority</th>{heads}</tr></thead><tbody>{requirements}</tbody></table></div></section>
<section class="panel"><div class="eyebrow">Slice views</div><h2>Zoom from the whole shape into build boundaries.</h2><div class="slice-stack">{_slice_views(package)}</div></section>{optional_section}</main>
<div class="inspector" id="inspector"></div><script type="application/json" id="planning-package">{embedded}</script><script>
const pkg=JSON.parse(document.getElementById('planning-package').textContent),box=document.getElementById('inspector');
function clearScope(){{document.body.classList.remove('scope-mode');document.querySelectorAll('[data-plan-id]').forEach(x=>x.classList.remove('dim'));document.querySelectorAll('.scope-button').forEach(x=>x.classList.remove('active'))}}
function applyScope(id,b){{clearScope();if(!id)return;const s=new Set(pkg.presentation.slice_scopes[id]||[]);s.add(id);document.body.classList.add('scope-mode');document.querySelectorAll('[data-plan-id]').forEach(x=>{{if(!s.has(x.dataset.planId))x.classList.add('dim')}});b?.classList.add('active');document.querySelector('.board')?.scrollIntoView({{behavior:'smooth',block:'start'}})}}
document.addEventListener('click',e=>{{const b=e.target.closest('.scope-button');if(b){{applyScope(b.dataset.scope||'',b);return}}const jump=e.target.closest('[data-jump-id]');if(jump){{const id=jump.dataset.jumpId;document.querySelectorAll('.hit').forEach(x=>x.classList.remove('hit'));const nodes=[...document.querySelectorAll('[data-plan-id="'+CSS.escape(id)+'"]')];nodes.forEach(x=>x.classList.add('hit'));nodes[0]?.scrollIntoView({{behavior:'smooth',block:'center'}});box.textContent=id+' · traced from representative behavior.';box.classList.add('show');return}}const t=e.target.closest('[data-plan-id]');document.querySelectorAll('.hit').forEach(x=>x.classList.remove('hit'));if(!t){{box.classList.remove('show');return}}const id=t.dataset.planId;document.querySelectorAll('[data-plan-id="'+CSS.escape(id)+'"]').forEach(x=>x.classList.add('hit'));box.textContent=id+' · stable planning ID. Edit canonical planning truth, then regenerate.';box.classList.add('show')}});
</script></body></html>"""


def render_svg(package, scope=None, suffix=""):
    scope = set(scope or [])
    places = package["breadboard"]["places"]
    if scope:
        places = [p for p in places if p.get("ID") in scope] or places[:1]
    width, card_w, gap = 1400, 400, 28
    cols = min(3, max(1, len(places)))
    rows = (len(places) + cols - 1) // cols
    height = 720 + max(0, rows - 1) * 330
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;fill:#132018}.id{fill:#245b43;font-weight:bold}.card{fill:#fffef9;stroke:#9ea8a0;stroke-width:2}.wire{fill:#fff;stroke:#abb2ac}.rail{fill:#e7f0e7;stroke:#abb2ac}</style>',
        '<rect width="100%" height="100%" fill="#f6f5ee"/>',
        f'<text x="50" y="58" font-size="34" font-weight="700">{_e(package["title"] + suffix)}</text>',
    ]
    for index, place in enumerate(places):
        x = 50 + (index % cols) * (card_w + gap)
        y = 110 + (index // cols) * 330
        pid = place.get("ID","")
        parts += [f'<rect class="card" x="{x}" y="{y}" rx="14" width="{card_w}" height="290"/>',
                  f'<text class="id" x="{x+18}" y="{y+30}" font-size="13">{_e(pid)}</text>',
                  f'<text x="{x+55}" y="{y+30}" font-size="18" font-weight="700">{_e(place.get("Place",""))}</text>']
        ui = [r for r in package["breadboard"]["ui"] if r.get("Place")==pid and (not scope or r.get("ID") in scope)]
        for pos, row in enumerate(ui[:6]):
            yy = y + 58 + pos * 34
            parts += [f'<rect class="wire" x="{x+18}" y="{yy}" rx="6" width="{card_w-36}" height="26"/>',
                      f'<text class="id" x="{x+28}" y="{yy+18}" font-size="10">{_e(row.get("ID",""))}</text>',
                      f'<text x="{x+64}" y="{yy+18}" font-size="12">{_e(row.get("Affordance",""))}</text>']
    rail_y = 460 + max(0, rows - 1) * 330
    rail_items = package["breadboard"]["non_ui"] + package["breadboard"]["stores"]
    if scope:
        rail_items = [r for r in rail_items if r.get("ID") in scope]
    for idx, row in enumerate(rail_items[:12]):
        x, y = 50 + (idx % 6) * 215, rail_y + (idx // 6) * 42
        label = row.get("Affordance") or row.get("Store") or ""
        parts += [f'<rect class="rail" x="{x}" y="{y}" rx="12" width="200" height="30"/>',
                  f'<text class="id" x="{x+10}" y="{y+20}" font-size="10">{_e(row.get("ID",""))}</text>',
                  f'<text x="{x+44}" y="{y+20}" font-size="11">{_e(label[:30])}</text>']
    parts.append("</svg>")
    return "".join(parts)


def write_svg_assets(package, directory):
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    overview = directory / "shape-overview.svg"
    overview.write_text(render_svg(package), encoding="utf-8")
    written.append(overview)
    scopes = package["presentation"].get("slice_scopes", {})
    for item in package["breadboard"]["slices"]:
        slug = re.sub(r"[^a-z0-9]+", "-", item["name"].lower()).strip("-")
        path = directory / f"{item['id']}-{slug}.svg"
        path.write_text(render_svg(package, scopes.get(item["id"], []), f" · {item['id']} {item['name']}"), encoding="utf-8")
        written.append(path)
    return written


def render_with_cairosvg(svg_paths, png_dir=None, pdf_output=None):
    if not png_dir and not pdf_output:
        return
    try:
        import cairosvg
    except ImportError as exc:
        raise ValueError("PNG/PDF export requires optional dependency: pip install cairosvg") from exc
    if png_dir:
        png_dir.mkdir(parents=True, exist_ok=True)
        for path in svg_paths:
            cairosvg.svg2png(url=str(path), write_to=str(png_dir / f"{path.stem}.png"))
    if pdf_output:
        cairosvg.svg2pdf(url=str(svg_paths[0]), write_to=str(pdf_output))
