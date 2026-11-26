#!/usr/bin/env python3
"""Prepare an offline packet or inspect isolated Behavioral Simulation returns."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
import sys

from counterfactuals import StudyBasis, inspect as inspect_counterfactuals, read_json
from report_safety import contains_private_identity, contains_sensitive_text, safe_outward_url
from study_fingerprint import canonical_digest


CONTRACT = "lur-simulation-handoff-v1"
FILE = "simulation.json"
REVIEWS_FILE = "simulation-reviews.json"
UPSTREAM = {
    "repository": "mattlane66/behavioral-simulation-for-agents-and-humans",
    "commit": "c11d29c8d121728306037dd799669bb0ef7cfabf",
    "schema_version": "0.1.0",
}
DISTANCES = ("IN_DISTRIBUTION", "NEAR_OOD", "FAR_OOD", "UNKNOWN")
MODES = ("PLAUSIBILITY_SPACE", "INDIVIDUAL_PROXY", "POPULATION_PREDICTION", "MULTI_AGENT_DYNAMICS")
GRADES = (
    "L0_ROLEPLAY", "L1_PERSON_GROUNDED", "L2_POPULATION_GROUNDED",
    "L3_HELD_OUT_VALIDATED", "L4_DECISION_CALIBRATED",
)
REQUEST_FIELDS = {"scenario_id", "mode", "target_grade", "permission_scope"}
RETURN_FIELDS = {
    "contract", "upstream", "study_ref", "scenario_id", "scenario_digest", "packet_digest",
    "evidence_fingerprint", "source_type", "run_id", "mode", "achieved_grade", "ran_at", "model",
    "model_version", "configuration", "assumptions", "run_count", "variation", "result_or_uncertainty",
    "distance", "validation_status", "artifact_urls", "caveats", "next_real_test", "validation",
    "calibration",
}
FORBIDDEN = (
    "Human observation, human sample count, qualification or sufficiency",
    "Concept gate, Fit Check, adoption, causal effect or design/build authorization",
)


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def allowed_grade(mode, grade) -> bool:
    if mode == "PLAUSIBILITY_SPACE":
        return grade == GRADES[0]
    if mode == "INDIVIDUAL_PROXY":
        return grade in (GRADES[1], GRADES[3], GRADES[4])
    return mode in MODES[2:] and grade in GRADES[2:]


def current_scenarios(root: Path) -> dict[str, dict]:
    rows, errors = inspect_counterfactuals(root)
    if errors:
        return {}
    return {row["scenario"]["scenario_id"]: row["scenario"] for row in rows if row["status"] == "CURRENT"}


def private_material(root: Path, packet: dict) -> bool:
    def packet_strings(value):
        if isinstance(value, dict):
            for item in value.values():
                yield from packet_strings(item)
        elif isinstance(value, list):
            for item in value:
                yield from packet_strings(item)
        elif isinstance(value, str):
            yield value

    text = "\n".join(packet_strings(packet))
    if re.search(r"\b(?:https?://|www\.|[\w.+-]+@[\w.-]+\.[a-z]{2,})", text, re.I):
        return True
    episodes = read_json(root, "lu_episodes.json", [])
    sources = read_json(root, "sources.json", [])
    evidence = read_json(root, "evidence.json", [])
    for row in episodes:
        if not row.get("identity_surface_allowed") and nonempty(row.get("user_entity")) \
                and contains_private_identity(text, row["user_entity"]):
            return True
    for row in sources:
        if not row.get("outward_citation_allowed"):
            for field in ("url", "immutable_identifier"):
                if nonempty(row.get(field)) and contains_sensitive_text(text, row[field]):
                    return True
    return any(
        isinstance(row.get("verbatim_excerpt"), str) and row["verbatim_excerpt"].strip()
        and contains_sensitive_text(text, row["verbatim_excerpt"])
        for row in evidence
    )


def packet_for(study: StudyBasis, scenario: dict, request: dict) -> dict:
    basis = scenario["basis"]
    assumptions = [scenario["critical_assumption"], scenario["rival_explanation"]]
    statement = (
        f'{scenario["intervention"]}. Changed conditions: {", ".join(scenario["changed_conditions"]) or "none"}. '
        f'Held constant: {", ".join(basis["held_constant"]) or "none stated"}. '
        f'Assumptions and rivals: {"; ".join(assumptions)}.'
    )
    upstream_input = {
        "schema_version": UPSTREAM["schema_version"], "decision": basis["decision"],
        "population": basis["target"], "baseline": basis["baseline"], "scenario": statement,
        "outcome_space": "; ".join(basis["outcome_space"]), "mode": request["mode"],
        "target_grade": request["target_grade"], "time_context": basis["time_horizon"],
        "consequence_if_wrong": basis["consequence_if_wrong"],
    }
    upstream_input["input_provenance"] = {
        key: "EXPLICITLY_PROVISIONAL"
        for key in ("decision", "population", "baseline", "scenario", "outcome_space",
                    "time_context", "consequence_if_wrong")
    }
    return {
        "contract": CONTRACT, "upstream": UPSTREAM, "study_ref": study.study_ref,
        "evidence_fingerprint": study.fingerprint, "scenario_id": scenario["scenario_id"],
        "synthetic_fixture": study.fixture,
        "scenario_digest": scenario["scenario_digest"], "purpose": scenario["purpose"],
        "research_refs": [f"{study.study_ref}:{ref}" for ref in [basis["episode_ref"], *basis["evidence_refs"]]],
        "frame_and_criteria_refs": [
            f"{study.study_ref}:{ref}" for ref in [basis["frame_ref"], *basis["requirement_refs"]] if ref
        ],
        "assumptions_and_rivals": assumptions, "distance": scenario["counterfactual_distance"],
        "disconfirming_observations": [scenario["refuter"]],
        "permission_scope": request["permission_scope"],
        "upstream_input": upstream_input,
    }


def prepared_packet(study: StudyBasis, scenario: dict, request: dict, *, permissions=None, preview=False) -> dict:
    if not study.freeze_current or scenario.get("human_review") != "REVIEWED":
        raise ValueError("A current evidence freeze and human-reviewed scenario are required")
    if set(request) - REQUEST_FIELDS:
        raise ValueError("Handoff approval contains unsupported fields")
    mode, grade = request.get("mode"), request.get("target_grade")
    if not allowed_grade(mode, grade):
        raise ValueError("Unsupported mode/target-grade pair")
    if request.get("permission_scope") != "REDACTED_SUMMARY_ONLY":
        raise ValueError("Only explicitly permitted redacted summaries cross this adapter")
    if scenario.get("counterfactual_distance") not in DISTANCES and mode != "PLAUSIBILITY_SPACE":
        raise ValueError("Use an upstream distance classification before grounded simulation")
    packet = packet_for(study, scenario, request)
    if packet["distance"] not in DISTANCES:
        packet["distance"] = "UNKNOWN"
    if private_material(study.root, packet):
        raise ValueError("Remove private material and URLs before preparing a portable handoff")
    digest = canonical_digest(packet)
    if not preview:
        receipt = (permissions or {}).get(digest)
        if not isinstance(receipt, dict) or receipt.get("permission_scope") != request["permission_scope"] \
                or not nonempty(receipt.get("approval_ref")):
            raise ValueError("Explicit processing permission must bind the exact minimized packet")
    return {**packet, "packet_digest": digest, "execution_status": "NOT_RUN"}


def load_requests(root: Path) -> dict:
    value = read_json(root, FILE, {})
    if not isinstance(value, dict) or value.get("contract") != CONTRACT or value.get("upstream") != UPSTREAM:
        raise ValueError("Unsupported simulation contract or upstream version")
    if set(value) - {"contract", "upstream", "study_ref", "execution_status", "handoffs", "returns"}:
        raise ValueError("Unknown simulation envelope fields")
    if value.get("execution_status") not in ("NOT_RUN", "UNAVAILABLE", "RETURN_RECORDED"):
        raise ValueError("Unsupported simulation execution status")
    return value


def load_review_receipts(root: Path) -> tuple[dict, dict]:
    receipts = read_json(root, REVIEWS_FILE, {})
    if not isinstance(receipts, dict) or set(receipts) - {"permissions", "returns"}:
        raise ValueError("Keep permission and review receipts under human control")
    permissions = receipts.get("permissions", {})
    returns = receipts.get("returns", {})
    if not isinstance(permissions, dict) or not isinstance(returns, dict):
        raise ValueError("Receipt registries must be digest-keyed objects")
    return permissions, returns


def reviewed_provenance(record: dict, reviews: dict) -> bool:
    """Check an independently recorded receipt. Empirical review belongs upstream."""
    digest = canonical_digest(record)
    review = reviews.get(digest)
    validation = record.get("validation")
    if not isinstance(review, dict) or not isinstance(validation, dict):
        return False
    if not nonempty(review.get("external_review_ref")) or review.get("status") != "REVIEWED":
        return False
    required = ("split_unit", "held_out_outcome_ref", "metric", "error", "baseline", "coverage",
                "task_scope", "subgroup_check", "freshness", "leakage_check")
    if not all(nonempty(validation.get(key)) for key in required) or validation.get("held_out") is not True:
        return False
    if record["distance"] in ("FAR_OOD", "UNKNOWN"):
        return False
    if record["achieved_grade"] != GRADES[4]:
        return record["validation_status"] == "HELD_OUT_REVIEWED"
    calibration = record.get("calibration")
    required = ("error_predictor", "metric", "predeclared_threshold", "subgroup_check",
                "freshness_policy", "calibration_artifact_ref")
    return (record["validation_status"] == "CALIBRATION_REVIEWED" and isinstance(calibration, dict)
            and all(nonempty(calibration.get(key)) for key in required))


def return_issue(record: dict, packet: dict, reviews: dict) -> str | None:
    if set(record) - RETURN_FIELDS or record.get("source_type") != "SIMULATED_ESTIMATE":
        return "unexpected fields or source type"
    for key in ("contract", "upstream", "study_ref", "scenario_id", "evidence_fingerprint",
                "scenario_digest", "packet_digest", "distance"):
        if record.get(key) != packet[key]:
            return "contract, scope or digest mismatch"
    mode, grade = record.get("mode"), record.get("achieved_grade")
    if mode != packet["upstream_input"]["mode"] or not allowed_grade(mode, grade) \
            or GRADES.index(grade) > GRADES.index(packet["upstream_input"]["target_grade"]):
        return "mode or grade exceeds the reviewed packet"
    for key in ("run_id", "ran_at", "model", "model_version", "configuration", "variation",
                "result_or_uncertainty", "next_real_test"):
        if not nonempty(record.get(key)):
            return "missing run provenance or test suggestion"
    if not re.fullmatch(r"R[0-9]{3,}", record["run_id"]):
        return "invalid upstream run ID"
    try:
        ran_at = datetime.fromisoformat(record["ran_at"])
        if ran_at.tzinfo is None:
            return "run date requires a time zone"
    except ValueError:
        return "invalid run date"
    if type(record.get("run_count")) is not int or record["run_count"] < 1 \
            or not strings(record.get("assumptions")) or not strings(record.get("caveats")):
        return "missing model variation, assumptions or caveats"
    if not strings(record.get("artifact_urls")) or not all(safe_outward_url(url) for url in record["artifact_urls"]):
        return "missing external artifact locations"
    if grade in GRADES[:3] and record.get("validation_status") != "NOT_VALIDATED":
        return "unvalidated mode claims validation"
    if grade in GRADES[3:] and not reviewed_provenance(record, reviews):
        return "no applicable reviewed holdout or calibration provenance"
    return None


def inspect(root: Path) -> list[dict]:
    """Return safe statuses only. Untrusted model text stays in the local sidecar."""
    if not (root / FILE).exists():
        return []
    try:
        state = load_requests(root)
        study = StudyBasis.load(root)
        if state.get("study_ref") != study.study_ref:
            raise ValueError("Wrong study namespace")
        requests, returns = state.get("handoffs"), state.get("returns")
        if not isinstance(requests, list) or not isinstance(returns, list):
            raise ValueError("Handoffs and returns must be lists")
        if not returns:
            status = "UNAVAILABLE" if state.get("execution_status") == "UNAVAILABLE" else "NOT_RUN"
            return [{"status": status}]
        permissions, reviews = load_review_receipts(root)
        current = current_scenarios(root)
        results: list[dict] = []
        seen: set[str] = set()
        for record in returns:
            try:
                scenario_id = record["scenario_id"]
                scenario = current[scenario_id]
                matching = [item for item in requests if isinstance(item, dict) and item.get("scenario_id") == scenario_id]
                if len(matching) != 1:
                    raise ValueError("Missing unique processing approval")
                packet = prepared_packet(study, scenario, matching[0], permissions=permissions)
                issue = return_issue(record, packet, reviews)
                if issue:
                    raise ValueError(issue)
                if record["run_id"] in seen:
                    raise ValueError("Duplicate upstream run ID")
                seen.add(record["run_id"])
            except (TypeError, ValueError, KeyError, AttributeError):
                results.append({"status": "QUARANTINED"})
                continue
            results.append({
                "status": "MODEL_DERIVED", "scenario_id": scenario_id, "grade": record["achieved_grade"],
                "validation": record["validation_status"], "allowed_use": "Suggest a real-world test",
                "forbidden_claims": FORBIDDEN,
            })
        return results
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return [{"status": "QUARANTINED"}]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--prepare", metavar="CF_ID")
    parser.add_argument("--preview", action="store_true", help="Inspect minimized packet locally before approval")
    args = parser.parse_args()
    if not args.prepare:
        print(json.dumps(inspect(args.workspace), indent=2))
        return 0
    validation = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("validate_study.py")), str(args.workspace), "--state-only"],
        capture_output=True, check=False,
    )
    if validation.returncode:
        parser.error("Handoff requires structurally valid study state. Run validate_study.py --state-only for the workspace.")
    try:
        requests = load_requests(args.workspace)
        study = StudyBasis.load(args.workspace)
        if study.study_ref != requests.get("study_ref"):
            raise ValueError("Wrong study namespace")
        scenario = current_scenarios(args.workspace)[args.prepare]
        choices = [row for row in requests["handoffs"] if row["scenario_id"] == args.prepare]
        if len(choices) != 1:
            raise ValueError("Specify one processing request for the scenario")
        permissions, _ = load_review_receipts(args.workspace)
        packet = prepared_packet(study, scenario, choices[0], permissions=permissions, preview=args.preview)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        parser.error(f"Handoff unavailable ({type(exc).__name__}). Check local state, scope and permission.")
    if args.preview:
        packet["execution_status"] = "LOCAL_PREVIEW_ONLY"
    print(json.dumps(packet, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
