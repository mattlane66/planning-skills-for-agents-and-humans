#!/usr/bin/env python3
"""Convert canonical Planning Skills Markdown into editable Shaping Board JSON.

Read-only adapter: never modifies a planning artifact or promotes its authority.
Missing candidate breadboards remain empty/placeholder, not invented mechanisms.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planning_publisher_contract import discover, parse_frame, parse_shaping, parse_breadboard, ContractError


def value(row, *names):
    return next((str(row[key]).strip() for key in names if row.get(key)), "")


def refs(text):
    return re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", text or "")


def candidate_diagram(path):
    """Project existing source tables into an inspection diagram, retaining IDs."""
    bb, _ = parse_breadboard(path)
    nodes, edges, seen = [], set(), set()
    def put(ident, kind, title, detail, system):
        if not ident or ident in seen:
            return
        seen.add(ident)
        def safe(x):
            return str(x or "").replace("|", "/").replace("\n", " ").strip()
        nodes.append(f"{ident} | {kind} | {safe(title) or ident} | {safe(detail)} | {safe(system)}")

    for place in bb["places"]:
        put(value(place, "ID"), "place", value(place, "Place"), value(place, "Description"), "Existing planning")
    for ui in bb["ui"]:
        put(value(ui, "ID"), "action", value(ui, "Affordance"), value(ui, "Control"), "UI")
        p = value(ui, "Place")
        if p and p != "—":
            edges.add((p, value(ui, "ID"), "contains"))
    for non in bb["non_ui"]:
        put(value(non, "ID"), "action", value(non, "Affordance"), value(non, "Control"), "System")
    for store in bb["stores"]:
        put(value(store, "ID"), "store", value(store, "Store"), value(store, "Description"), "State")

    for row in [*bb["ui"], *bb["non_ui"]]:
        src = value(row, "ID")
        for target in refs(value(row, "Wires Out")):
            if src in seen and target in seen:
                edges.add((src, target, ""))
        for target in refs(value(row, "Returns To")):
            if src in seen and target in seen:
                edges.add((src, target, "return"))
    for trace in bb["behavior_traces"]:
        path_ids = refs(value(trace, "Control path"))
        for start, end in zip(path_ids, path_ids[1:]):
            if start in seen and end in seen:
                edges.add((start, end, "trace"))
    lines = nodes + [f"{a} -> {b}" + (f" : {label}" if label else "")
                     for a, b, label in sorted(edges)]
    return "\n".join(lines), bb


def build(directory):
    directory = Path(directory).resolve()
    try:
        frame, _ = parse_frame(discover(directory, "frame"))
        shaping, _ = parse_shaping(discover(directory, "shaping"))
    except ContractError as exc:
        raise SystemExit(f"Shaping Board import: {exc}") from exc

    shapes = [s for s in shaping["shapes"] if s["id"] != "CURRENT"]
    if not shapes:
        raise SystemExit("Shaping Board import: shaping.md has no candidate shapes")
    if len(shapes) > 10:
        raise SystemExit("Shaping Board supports at most 10 candidates")
    if any(not re.fullmatch(r"[A-J]", s["id"]) for s in shapes):
        raise SystemExit("Candidate shape IDs must be A through J for the current board")

    existing = []
    for path in directory.glob("*.md"):
        if "breadboard" not in path.name.lower() or "reflection" in path.name.lower():
            continue
        try:
            bb, _ = parse_breadboard(path)
        except (ValueError, OSError):
            continue
        if bb["mode"] in ("candidate-shape", "selected-design"):
            existing.append((path, bb))
    options = []
    candidate_source = {}
    for s in shapes:
        for path, bb in existing:
            name = path.stem
            if re.search(r"(?:candidate[-_]?|breadboard[-_]?)(%s)(?:[-_]|$)" % s["id"], name, re.I):
                candidate_source[s["id"]] = path
                break
        if s["id"] == shaping["selected_shape"] and s["id"] not in candidate_source:
            selected = [p for p, bb in existing if bb["mode"] == "selected-design"]
            if selected:
                candidate_source[s["id"]] = selected[0]
        dsl = candidate_diagram(candidate_source[s["id"]])[0] if s["id"] in candidate_source else ""
        options.append(dict(id=s["id"], title=s["name"], promise="", risk="",
                            cuts="", placeholder=not bool(dsl), dsl=dsl))
    required = shaping["requirements"]
    fit_map = {row.get("Req", ""): row for row in shaping["fit"]}
    requirements = []
    for i, row in enumerate(required):
        rid = value(row, "ID") or f"R{i+1}"
        values = []
        for opt in options:
            mark = fit_map.get(rid, {}).get(opt["id"], "")
            values.append("y" if "✅" in mark else "n" if "❌" in mark else "u")
        requirements.append(dict(id=rid, text=value(row, "Requirement"),
            status=value(row, "Status") or "Undecided",
            auth=value(row, "Authority") or "Working",
            src=value(row, "Origin"), why=value(row, "Notes"),
            chk=value(row, "Evidence refs"), star=False, f="".join(values),
            l=[""]*len(options)))
    appetite = shaping["appetite"]
    selected = shaping["selected_shape"] or None
    frame_status = str(frame["meta"].get("status", "")).lower()
    return dict(
        schema_version=3,
        name=shaping["title"].replace(" — Shaping", ""),
        problem=frame["problem"], outcome=frame["outcome"],
        appetite=value(appetite, "Time budget"),
        appetiteAuthority=shaping["appetite_authority"] if shaping["appetite_authority"] in ("Unset", "Working", "Accepted") else "Working",
        frameAuthority="Accepted" if frame_status == "accepted" else "Working",
        cut=value(appetite, "Cut line"), slice="", why="; ".join(shaping["decision_rationale"]),
        pick=selected,
        selectionAuthority="Accepted" if selected and shaping["requirements_authority"] == "Accepted" and shaping["appetite_authority"] == "Accepted" else "Working",
        options=options, stories=[], reqs=requirements,
        things=[], slices=[], drift=[], rel=[],
        import_note="Read-only projection of planning Markdown. Re-exported Markdown is a proposal; review changes against existing source files. Missing candidate diagrams have not been fabricated.",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--planning-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(args.planning_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(result['options'])} candidate shapes to {args.output}")


if __name__ == "__main__":
    main()
