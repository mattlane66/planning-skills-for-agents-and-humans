#!/usr/bin/env python3
"""Compile canonical planning artifacts into agent JSON and human shaped-work views."""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from planning_publisher_contract import (
    ContractError,
    clean_value,
    discover,
    discover_slices_artifact,
    parse_breadboard,
    parse_frame,
    parse_shaping,
    parse_slices_artifact,
    validate_package,
)
from planning_publisher_ext import (
    augment_package,
    render_enhanced_html,
    render_with_cairosvg,
    write_svg_assets,
)

SCHEMA_VERSION = 2


class PublisherError(ContractError):
    pass


def portable_source(path, directory):
    path = Path(path).resolve()
    directory = Path(directory).resolve()
    try:
        return str(path.relative_to(directory))
    except ValueError:
        return path.name


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
    breadboard = package["breadboard"]
    selected = next(
        (
            shape
            for shape in package["shaping"]["shapes"]
            if shape["id"] == package["shaping"]["selected_shape"]
        ),
        None,
    )
    parts = selected["parts"] if selected else []
    notes = [
        {"ref": part.get("Part", ""), "text": part.get("Mechanism", "")}
        for part in parts[:6]
        if part.get("Part")
    ]
    return {
        "schema_version": 2,
        "hero_place": breadboard["places"][0].get("ID", "") if breadboard["places"] else "",
        "journey_scenarios": [
            row.get("Scenario", "") for row in breadboard["behavior_traces"][:4]
        ],
        "featured_ids": [note["ref"] for note in notes],
        "annotations": notes,
    }


def validate_presentation(package, payload):
    if payload.get("schema_version", 1) not in (1, 2):
        raise PublisherError("Only presentation schema_version 1 or 2 is supported")
    refs = [payload.get("hero_place", "")] + list(payload.get("featured_ids", []))
    refs += [item.get("ref", "") for item in payload.get("annotations", [])]
    unknown = sorted({ref for ref in refs if ref and ref not in known_ids(package)})
    if unknown:
        raise PublisherError(
            "Presentation references IDs absent from canonical planning artifacts: "
            + ", ".join(unknown)
        )
    return payload


def load_presentation(path, package):
    if path and Path(path).is_file():
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PublisherError(f"{path}: invalid presentation JSON: {exc.msg}") from exc
    else:
        payload = default_presentation(package)
    return validate_presentation(package, payload)


def _frame_authority(frame, shaping_text):
    status = clean_value(frame["meta"].get("status")).lower()
    if status in {"accepted", "selected"} or "## Accepted transformation frame" in shaping_text:
        return "Accepted"
    return "Source"


def _breadboard_authority(breadboard):
    if breadboard["mode"] != "selected-design":
        return breadboard["mode"] or "Unknown"
    artifact_type = clean_value(breadboard["meta"].get("artifact_type")).lower()
    if artifact_type != "breadboard":
        return "Accepted selected-design"
    accepted = (
        clean_value(breadboard["meta"].get("source_of_truth")).lower() == "true"
        and breadboard.get("requirements_authority") == "Accepted"
        and breadboard.get("appetite_authority") == "Accepted"
    )
    return "Accepted selected-design" if accepted else "selected-design (draft)"


def build_package(
    planning_dir,
    frame_path=None,
    shaping_path=None,
    breadboard_path=None,
    presentation_path=None,
):
    directory = Path(planning_dir).resolve()
    frame_path = Path(frame_path or discover(directory, "frame")).resolve()
    shaping_path = Path(shaping_path or discover(directory, "shaping")).resolve()
    breadboard_path = Path(breadboard_path or discover(directory, "breadboard")).resolve()

    frame, _frame_text = parse_frame(frame_path)
    shaping, shaping_text = parse_shaping(shaping_path)
    breadboard, _breadboard_text = parse_breadboard(breadboard_path)

    slices_path = discover_slices_artifact(directory)
    slices_artifact = parse_slices_artifact(slices_path)
    if slices_artifact:
        if slices_artifact["slices"]:
            breadboard["slices"] = slices_artifact["slices"]
        if slices_artifact["active_slice"]:
            breadboard["active_slice"] = slices_artifact["active_slice"]
            breadboard["active_slice_text"] = slices_artifact["active_slice_text"]

    frame["source"] = portable_source(frame_path, directory)
    shaping["source"] = portable_source(shaping_path, directory)
    breadboard["source"] = portable_source(breadboard_path, directory)

    package = {
        "schema_version": SCHEMA_VERSION,
        "kind": "PlanningPackage",
        "frame": frame,
        "shaping": shaping,
        "breadboard": breadboard,
        "sources": {
            "frame": frame["source"],
            "shaping": shaping["source"],
            "breadboard": breadboard["source"],
        },
    }
    if slices_path:
        package["sources"]["slices"] = portable_source(slices_path, directory)

    package["title"] = shaping["title"] or frame["title"] or breadboard["title"]
    package["authority"] = {
        "frame": _frame_authority(frame, shaping_text),
        "requirements": shaping.get("requirements_authority", "Unknown"),
        "appetite": shaping.get("appetite_authority", "Unknown"),
        "shape": "Selected" if shaping["selected_shape"] else "Working",
        "breadboard": _breadboard_authority(breadboard),
        "slice": "Selected build scope" if breadboard["active_slice"] else "Unselected",
    }

    validate_package(package)

    if presentation_path is None and (directory / "presentation.json").is_file():
        presentation_path = directory / "presentation.json"
    package["presentation"] = load_presentation(presentation_path, package)
    try:
        package = augment_package(package, directory)
    except ValueError as exc:
        raise PublisherError(str(exc)) from exc
    validate_package(package)
    return package


render_html = render_enhanced_html


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--planning-dir", type=Path, default=Path("planning"))
    parser.add_argument("--frame", type=Path)
    parser.add_argument("--shaping", type=Path)
    parser.add_argument("--breadboard", type=Path)
    parser.add_argument("--presentation", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--svg-dir", type=Path)
    parser.add_argument("--png-dir", type=Path)
    parser.add_argument("--pdf-output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    try:
        package = build_package(
            args.planning_dir,
            args.frame,
            args.shaping,
            args.breadboard,
            args.presentation,
        )
        if args.check:
            print(
                "PlanningPackage OK: "
                f"{len(package['shaping']['requirements'])} requirements, "
                f"{len(package['shaping']['shapes'])} shapes, "
                f"{len(package['breadboard']['behavior_traces'])} behavior traces, "
                f"{len(package['breadboard']['slices'])} slices, "
                f"{len(package['artifacts'])} optional artifacts."
            )
            return 0

        output = args.output or args.planning_dir / "shaped-work.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_html(package), encoding="utf-8")

        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(
                json.dumps(package, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        svg_paths = []
        if args.svg_dir or args.png_dir or args.pdf_output:
            svg_dir = args.svg_dir or output.parent / "shaped-work-assets"
            svg_paths = write_svg_assets(package, svg_dir)
            render_with_cairosvg(svg_paths, args.png_dir, args.pdf_output)

        print(output)
        if svg_paths:
            print(f"Wrote {len(svg_paths)} SVG board(s) to {svg_paths[0].parent}")
        return 0
    except (ContractError, PublisherError, ValueError) as exc:
        print(f"Planning Publisher error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
