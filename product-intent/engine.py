"""Compile an accepted PlanningPackage and opt-in intent extension into one typed model.

The PlanningPackage is canonical for its existing IDs. The extension may add new
invariants/decisions but may not redefine a planner-owned requirement or affordance.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

class IntentCompileError(ValueError):
    pass

def _validate_overlay(path):
    import_path = Path(__file__).with_name("intent.py")
    spec = importlib.util.spec_from_file_location("planning_product_intent_validator", import_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        overlay = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntentCompileError(f"Invalid product intent extension {path}: {exc}") from exc
    errors = mod.validate(overlay)
    if errors:
        raise IntentCompileError("Invalid product intent extension:\n- " + "\n- ".join(errors))
    return overlay

def _value(row, *keys):
    for key in keys:
        if isinstance(row, dict) and row.get(key):
            return str(row[key]).strip()
    return ""

def _record(kind, raw_id, row, source, authority):
    if not raw_id:
        return None
    return {
        "uid": f"{kind}:{raw_id}",
        "id": raw_id,
        "kind": kind,
        "status": authority,
        "source": source,
        "data": row,
    }

def _planning_records(package):
    shaping = package["shaping"]
    breadboard = package["breadboard"]
    records = []
    requirement_status = "accepted" if str(package["authority"].get("requirements", "")).lower() == "accepted" else "working"
    selected = shaping.get("selected_shape")
    for row in shaping.get("requirements", []):
        records.append(_record("requirement", _value(row,"ID","id"), row,
                               package["sources"]["shaping"], requirement_status))
    for shape in shaping.get("shapes", []):
        records.append(_record("shape", _value(shape,"id","ID"), shape,
                               package["sources"]["shaping"],
                               "accepted" if selected and shape.get("id") == selected else "candidate"))
    selected_design = package["authority"].get("breadboard") == "Accepted selected-design"
    kind_by_table = {"places":"place","ui":"affordance","non_ui":"non_ui_affordance","stores":"store"}
    for table, kind in kind_by_table.items():
        for row in breadboard.get(table, []):
            records.append(_record(kind, _value(row, "ID", "id"), row,
                                   package["sources"]["breadboard"],
                                   "accepted" if selected_design else "working"))
    for artifact, kind, table in (("statechart","state","states"),
                                  ("statechart","transition","transitions"),
                                  ("interface_contracts","interface","contracts")):
        data = package.get("artifacts", {}).get(artifact) or {}
        for row in data.get(table, []):
            records.append(_record(kind, _value(row,"ID","Id","id","State","Transition","Contract"),
                                   row, data.get("source",""),
                                   "derived"))
    return [r for r in records if r is not None]

def compile_into_package(package, planning_dir):
    """Mutate PlanningPackage only if product-intent.json exists, preserving old callers."""
    directory = Path(planning_dir)
    overlay_file = directory / "product-intent.json"
    if not overlay_file.is_file():
        return package
    overlay = _validate_overlay(overlay_file)
    planner = _planning_records(package)
    by_raw = {}
    by_uid = {}
    for record in planner:
        by_uid[record["uid"]] = record
        by_raw.setdefault(record["id"], []).append(record["uid"])
    extension = []
    for record in overlay["records"]:
        if record["id"] in by_raw:
            raise IntentCompileError(
                f"{record['id']}: cannot duplicate a PlanningPackage ID in product-intent.json")
        derived = dict(record)
        derived["uid"] = f"extension:{record['id']}"
        derived["source"] = overlay_file.name
        extension.append(derived)
        by_uid[derived["uid"]] = derived
        by_raw.setdefault(record["id"], []).append(derived["uid"])
    for record in extension:
        normalized = []
        for raw in record["refs"]:
            if raw in by_uid:
                normalized.append(raw)
                continue
            candidates = by_raw.get(raw, [])
            if not candidates:
                raise IntentCompileError(f"{record['id']}: unknown intent ref {raw!r}")
            if len(candidates) != 1:
                raise IntentCompileError(f"{record['id']}: ambiguous ref {raw!r}; use a typed UID ({', '.join(candidates)})")
            normalized.append(candidates[0])
        record["resolved_refs"] = normalized
        if record["status"] == "accepted":
            for ref in normalized:
                target = by_uid[ref]
                if target.get("status") in ("working", "candidate", "inferred", "rejected", "superseded"):
                    raise IntentCompileError(f"{record['id']}: accepted intent depends on unaccepted {ref}")
    normalized_bindings = []
    for binding in overlay.get("bindings", []):
        target = binding["intent_id"]
        if target in by_uid:
            uid = target
        else:
            options = by_raw.get(target, [])
            if len(options) != 1:
                raise IntentCompileError(f"Binding target {target!r} is missing or ambiguous; use typed UID")
            uid = options[0]
        entry = dict(binding)
        entry["resolved_intent_uid"] = uid
        normalized_bindings.append(entry)
    approved = [r for r in extension if r["status"] == "accepted"]
    referenced = {ref for r in approved for ref in r["resolved_refs"]}
    uncovered = [r["uid"] for r in planner if r["kind"]=="requirement" and r["status"]=="accepted"
                 and r["uid"] not in referenced]
    payload = {
        "kind": "ProductIntentModel",
        "schema_version": 1,
        "product": overlay["product"],
        "planning_package_schema_version": package["schema_version"],
        "source": overlay_file.name,
        "planning_records": planner,
        "extension_records": extension,
        "bindings": normalized_bindings,
        "unlinked_accepted_requirements": sorted(uncovered),
    }
    payload["content_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",",":")).encode("utf-8")).hexdigest()
    package["product_intent"] = payload
    package["sources"]["product_intent"] = overlay_file.name
    return package
