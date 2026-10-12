#!/usr/bin/env python3
"""Project existing Product Intent gate evidence into a read-only Shaping Board view.

Consumes a compiled PlanningPackage and the actual output of product-intent/gate.py.
Does not infer new requirements, create bindings, run code, or assert untested behavior.
"""
import argparse
import json
from pathlib import Path

VALID = {"PASS", "REVIEW", "DRIFT"}


def build(package, gate):
    model = package.get("product_intent")
    if not isinstance(model, dict):
        raise ValueError("Compiled PlanningPackage has no opted-in product_intent model")
    if gate.get("verdict") not in VALID:
        raise ValueError("Expected a real PASS, REVIEW or DRIFT Product Intent gate report")
    records = model.get("planning_records", []) + model.get("extension_records", [])
    by_uid = {r["uid"]: r for r in records}
    by_id = {r["id"]: r for r in records}
    bindings = model.get("bindings", [])
    impacts = []
    impacted = gate.get("affected") or {}
    changed = gate.get("accepted_contract_changes") or []
    all_keys = set(impacted) | set(changed)
    scenarios = (gate.get("behavior_checks") or {}).get("results") or []

    for key in sorted(all_keys):
        rec = by_uid.get(key) or by_id.get(key)
        if rec is None:
            for binding in bindings:
                if binding.get("intent_id") == key:
                    rec = by_uid.get(binding.get("resolved_intent_uid"))
                    if rec:
                        break
        linked = rec.get("resolved_refs") or rec.get("refs", []) if rec else []
        refs = [ref.split(":", 1)[-1] for ref in linked]
        if rec and rec.get("kind") == "requirement":
            refs.insert(0, rec["id"])
        related = [s for s in scenarios if key in s.get("intent_ids", [])]
        result_codes = [s.get("status") for s in related]
        if key in changed:
            status = "REVIEW"
            reason = "Accepted intent changed relative to baseline; human review required"
        elif "DRIFT" in result_codes:
            status = "DRIFT"
            reason = "Trusted scenario returned an unexpected result"
        elif not related or any(s != "PASS" for s in result_codes):
            status = "REVIEW"
            reason = "No complete successful scenario coverage for this intent"
        elif gate["verdict"] != "PASS":
            status = "REVIEW"
            reason = "Scenario passed, but the overall gate still needs review or detected drift"
        else:
            status = "PASS"
            reason = "Covered approved cases passed, not proof of all behavior"

        impacts.append({
            "id": rec.get("id", key) if rec else key,
            "uid": rec.get("uid", key) if rec else key,
            "kind": rec.get("kind", "unknown") if rec else "unknown",
            "title": (rec.get("title") or (rec.get("data") or {}).get("Requirement") or rec.get("id", key)) if rec else key,
            "statement": rec.get("statement") or (rec.get("data") or {}).get("Requirement", "") if rec else "",
            "refs": list(dict.fromkeys(refs)),
            "changed_paths": impacted.get(key, {}).get("paths", []),
            "status": status,
            "reason": reason,
            "scenarios": [{"scenario": s.get("scenario", ""), "case": s.get("case", ""),
                           "status": s.get("status", "")} for s in related],
        })
    return {
        "schema_version": 1,
        "kind": "ShapingBoardProductStatus",
        "product": model.get("product", ""),
        "verdict": gate["verdict"],
        "impacts": impacts,
        "unmapped_changed_paths": gate.get("unmapped_changed_paths") or [],
        "accepted_contract_changes": changed,
        "bindings_changed": bool(gate.get("bindings_changed")),
        "trusted_baseline_missing": bool(gate.get("trusted_baseline_missing")),
        "unlinked_accepted_requirements": model.get("unlinked_accepted_requirements") or [],
        "source": "Read-only projection of compiled Product Intent plus trusted gate output. Review is not a failed behavior; PASS only covers tested, confirmed bindings. Do not treat agent-authored JSON as trusted evidence.",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--package", type=Path, required=True)
    p.add_argument("--gate-report", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = build(json.loads(args.package.read_text(encoding="utf-8")),
                   json.loads(args.gate_report.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Projected {len(report['impacts'])} affected intent records ({report['verdict']}) to {args.output}")


if __name__ == "__main__":
    main()
