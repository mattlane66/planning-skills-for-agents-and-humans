#!/usr/bin/env python3
"""Compile accepted planning artifacts into one deterministic ProductIntentModel."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from planning_publisher_contract import clean_value, first_table, key_values, section
from publish_shaped_work import build_package

SCHEMA_VERSION = 1
ID_RE = re.compile(r"\\b(?:R|P|U|N|S|ST|TR|C|RUN|E|SP|TG|CUT|V|SK|DEC|INV|BIND)\\d+(?:\\.\\d+)?\\b")


class ProductIntentError(ValueError):
    pass


def _split_refs(value: str) -> list[str]:
    return list(dict.fromkeys(ID_RE.findall(value or "")))


def _split_list(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,;]", value)
    return [part.strip() for part in parts if part.strip()]


def _read_source(planning_dir: Path, source: str) -> str:
    path = (planning_dir / source).resolve()
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _requirements(package: dict) -> list[dict]:
    output = []
    for row in package["shaping"]["requirements"]:
        req_id = clean_value(row.get("ID"))
        if not req_id:
            continue
        output.append({
            "id": req_id,
            "statement": clean_value(row.get("Requirement")),
            "status": clean_value(row.get("Status")),
            "authority": clean_value(row.get("Authority")) or package["shaping"].get("requirements_authority", "Unknown"),
            "origin": clean_value(row.get("Origin")),
            "evidence_refs": _split_list(clean_value(row.get("Evidence refs"))),
            "notes": clean_value(row.get("Notes")),
        })
    return output


def _decision(package: dict, shaping_text: str) -> list[dict]:
    shaping = package["shaping"]
    if not shaping.get("selected_shape") and shaping.get("decision_status") != "selected":
        return []
    values = key_values(section(shaping_text, r"(?:Human )?Decision"))
    decision_id = clean_value(values.get("Decision ID")) or "DEC1"
    chosen = shaping.get("selected_shape", "")
    rejected = [
        item["id"]
        for item in shaping.get("shapes", [])
        if item.get("id") not in {"CURRENT", chosen}
    ]
    explicit_rejected = clean_value(values.get("Rejected directions"))
    if explicit_rejected:
        found = re.findall(r"\\b[A-Z][A-Z0-9_-]*\\b", explicit_rejected)
        rejected = [item for item in found if item not in {"CURRENT", chosen}] or rejected
    return [{
        "id": decision_id,
        "status": shaping.get("decision_status", "selected"),
        "selected": chosen,
        "rationale": shaping.get("decision_rationale", []),
        "rejected": list(dict.fromkeys(rejected)),
        "reopen_when": clean_value(values.get("Reopen when")),
        "supersedes": _split_refs(clean_value(values.get("Supersedes"))),
    }]


def _invariants(breadboard_text: str) -> list[dict]:
    rows = first_table(section(breadboard_text, r"Product invariants.*"))
    output = []
    for row in rows:
        inv_id = clean_value(row.get("ID"))
        if not inv_id:
            continue
        severity = clean_value(row.get("Severity")).lower() or "must"
        if severity not in {"must", "should"}:
            raise ProductIntentError(f"{inv_id}: invariant Severity must be 'must' or 'should'")
        output.append({
            "id": inv_id,
            "statement": clean_value(row.get("Invariant") or row.get("Statement")),
            "severity": severity,
            "protects": _split_refs(clean_value(row.get("Protects"))),
            "reopen_when": clean_value(row.get("Reopen when")),
            "verification": clean_value(row.get("Verification")),
        })
    return output


def _bindings(planning_dir: Path) -> tuple[list[dict], str | None]:
    path = planning_dir / "implementation-bindings.json"
    if not path.is_file():
        return [], None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProductIntentError(f"{path}: invalid JSON: {exc.msg}") from exc
    if payload.get("schema_version") != 1 or not isinstance(payload.get("bindings"), list):
        raise ProductIntentError(f"{path}: expected schema_version 1 and a bindings array")
    output = []
    for row in payload["bindings"]:
        binding = {
            "id": str(row.get("id", "")).strip(),
            "intent_refs": list(row.get("intent_refs") or []),
            "paths": list(row.get("paths") or []),
            "symbols": list(row.get("symbols") or []),
            "tests": list(row.get("tests") or []),
            "notes": str(row.get("notes", "")).strip(),
        }
        if not re.fullmatch(r"BIND\\d+", binding["id"]):
            raise ProductIntentError(f"Invalid binding id: {binding['id']!r}")
        if not binding["intent_refs"] or not binding["paths"]:
            raise ProductIntentError(f"{binding['id']}: intent_refs and paths are required")
        output.append(binding)
    return output, path.name


def _acceptance_tests(package: dict, planning_dir: Path) -> list[str]:
    source = (
        package.get("sources", {})
        .get("optional", {})
        .get("executable_breadboard")
    )
    if not source:
        return []
    text = _read_source(planning_dir, source)
    block = section(text, r"Acceptance tests")
    tests = []
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("- "):
            value = line[2:].strip()
            if value and value != "...":
                tests.append(value)
    return tests


def _known_ids(model: dict) -> set[str]:
    ids = {row["id"] for row in model["requirements"]}
    ids.update(row["id"] for row in model["invariants"])
    ids.update(row["id"] for row in model["decisions"])
    for key in ("places", "ui_affordances", "non_ui_affordances", "stores"):
        ids.update(clean_value(row.get("ID")) for row in model["selected_design"][key])
    return {value for value in ids if value}


def validate_model(model: dict) -> None:
    errors = []
    if model.get("schema_version") != 1 or model.get("kind") != "ProductIntentModel":
        errors.append("model must be ProductIntentModel schema_version 1")
    ids = _known_ids(model)
    for inv in model.get("invariants", []):
        unknown = [ref for ref in inv.get("protects", []) if ref not in ids]
        if unknown:
            errors.append(f"{inv['id']}: unknown protects refs: {', '.join(unknown)}")
    for binding in model.get("implementation_bindings", []):
        unknown = [ref for ref in binding.get("intent_refs", []) if ref not in ids]
        if unknown:
            errors.append(f"{binding['id']}: unknown intent refs: {', '.join(unknown)}")
    all_ids = []
    all_ids.extend(row["id"] for row in model.get("requirements", []))
    all_ids.extend(row["id"] for row in model.get("invariants", []))
    all_ids.extend(row["id"] for row in model.get("decisions", []))
    all_ids.extend(row["id"] for row in model.get("implementation_bindings", []))
    duplicates = sorted({item for item in all_ids if all_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate stable IDs: " + ", ".join(duplicates))
    if errors:
        raise ProductIntentError("\n".join(errors))


def compile_model(planning_dir: Path) -> dict:
    planning_dir = Path(planning_dir).resolve()
    package = build_package(planning_dir)
    shaping_text = _read_source(planning_dir, package["sources"]["shaping"])
    breadboard_text = _read_source(planning_dir, package["sources"]["breadboard"])
    bindings, bindings_source = _bindings(planning_dir)

    model = {
        "schema_version": SCHEMA_VERSION,
        "kind": "ProductIntentModel",
        "product": {
            "title": package.get("title", ""),
            "problem": package["frame"].get("problem", []),
            "outcome": package["frame"].get("outcome", []),
            "operating_model": (
                package["shaping"].get("operating_model")
                or package["frame"].get("operating_model")
                or {}
            ),
        },
        "authority": package.get("authority", {}),
        "requirements": _requirements(package),
        "decisions": _decision(package, shaping_text),
        "selected_design": {
            "shape": package["shaping"].get("selected_shape", ""),
            "places": package["breadboard"].get("places", []),
            "ui_affordances": package["breadboard"].get("ui", []),
            "non_ui_affordances": package["breadboard"].get("non_ui", []),
            "stores": package["breadboard"].get("stores", []),
            "behavior_traces": package["breadboard"].get("behavior_traces", []),
            "active_slice": package["breadboard"].get("active_slice", ""),
        },
        "invariants": _invariants(breadboard_text),
        "implementation_bindings": bindings,
        "verification": {
            "acceptance_tests": _acceptance_tests(package, planning_dir),
        },
        "sources": {
            **package.get("sources", {}),
            **({"implementation_bindings": bindings_source} if bindings_source else {}),
        },
    }
    validate_model(model)
    return model


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--planning-dir", type=Path, default=Path("planning"))
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when --output exists and differs from freshly compiled intent.",
    )
    args = parser.parse_args(argv)

    try:
        model = compile_model(args.planning_dir)
        rendered = json.dumps(model, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        output = args.output or (args.planning_dir / "product-intent.json")
        if args.check:
            if output.is_file() and output.read_text(encoding="utf-8") != rendered:
                raise ProductIntentError(
                    f"{output} is stale. Recompile it from the accepted planning artifacts."
                )
            print(
                "ProductIntentModel OK: "
                f"{len(model['requirements'])} requirements, "
                f"{len(model['decisions'])} decisions, "
                f"{len(model['invariants'])} invariants, "
                f"{len(model['implementation_bindings'])} bindings."
            )
            return 0
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
        return 0
    except (ProductIntentError, ValueError) as exc:
        print(f"Product intent error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
