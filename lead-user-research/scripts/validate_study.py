#!/usr/bin/env python3
"""Structural validator for the file-backed Lead User research state."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COVERAGE = {"FULL", "PARTIAL", "UNREADABLE", "UNKNOWN"}
LU_STATUS = {"CANDIDATE", "QUALIFIED", "REJECTED"}
EPISTEMIC = {"VERIFIED", "INFERRED", "SPECULATIVE", "UNKNOWN"}
GATE = {"PASS", "FAIL", "NOT_ASSESSED"}
TRACE_STATUS = {"NOT_ASSESSED", "PARTIAL", "SUFFICIENT"}
SUFFICIENCY = {"NOT_ASSESSED", "SUFFICIENT", "INSUFFICIENT"}
EXECUTION_LEVEL = {"DESK_RESEARCH", "FIELDWORK_ENRICHED", "FULL_LEAD_USER_PROJECT"}
LINEAGE_RELATIONSHIP = {
    "SAME_CREATOR",
    "FORK",
    "DEPENDENCY",
    "ADAPTATION",
    "COPIED_TECHNIQUE",
    "COMMON_UPSTREAM",
    "SHARED_ORGANIZATION",
    "SHARED_COMMUNITY",
    "INDEPENDENT_REDISCOVERY",
    "OTHER",
}
INDEPENDENCE = {"INDEPENDENT", "DERIVATIVE", "RELATED", "UNKNOWN"}
FIT_STATUS = {"PASS", "FAIL", "PROVISIONAL"}

ID_PATTERNS = {
    "trend_id": re.compile(r"^T\d+$"),
    "source_id": re.compile(r"^SRC\d+$"),
    "evidence_id": re.compile(r"^E\d+$"),
    "lu_id": re.compile(r"^LU\d+$"),
    "lineage_id": re.compile(r"^L\d+$"),
    "finding_id": re.compile(r"^F\d+$"),
    "need_id": re.compile(r"^N\d+$"),
    "principle_id": re.compile(r"^SP\d+$"),
    "requirement_id": re.compile(r"^R\d+$"),
    "concept_id": re.compile(r"^M\d+$"),
}


def load(root: Path, name: str, errors: list[str]) -> Any:
    path = root / name
    if not path.exists():
        errors.append(f"missing {name}")
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {name}: {exc}")
        return []


def ids(rows: list[dict[str, Any]], key: str, errors: list[str]) -> set[str]:
    result: set[str] = set()
    pattern = ID_PATTERNS[key]
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{key} row {index} must be an object")
            continue
        value = row.get(key)
        if not isinstance(value, str) or not pattern.match(value):
            errors.append(f"{key} invalid at row {index}: {value!r}")
            continue
        if value in result:
            errors.append(f"duplicate {key}: {value}")
        result.add(value)
    return result


def refs_exist(
    values: Any,
    valid: set[str],
    label: str,
    owner: str,
    errors: list[str],
) -> None:
    if values in (None, ""):
        return
    if not isinstance(values, list):
        errors.append(f"{owner} {label} must be a list")
        return
    for value in values:
        if value not in valid:
            errors.append(f"{owner} references missing {label}: {value}")


def require_nonempty_string(row: dict[str, Any], field: str, owner: str, errors: list[str]) -> None:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner} requires non-empty {field}")


def require_bool(row: dict[str, Any], field: str, owner: str, errors: list[str]) -> None:
    if not isinstance(row.get(field), bool):
        errors.append(f"{owner} {field} must be boolean")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_study.py <workspace>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    errors: list[str] = []
    warnings: list[str] = []

    manifest = load(root, "manifest.json", errors)
    decision = load(root, "decision.json", errors)
    trends = load(root, "trends.json", errors)
    sources = load(root, "sources.json", errors)
    evidence = load(root, "evidence.json", errors)
    episodes = load(root, "lu_episodes.json", errors)
    lineage = load(root, "lineage.json", errors)
    findings = load(root, "findings.json", errors)
    needs = load(root, "needs.json", errors)
    principles = load(root, "principles.json", errors)
    criteria = load(root, "fit_criteria.json", errors)
    concepts = load(root, "concepts.json", errors)
    coverage = load(root, "coverage.json", errors)
    sufficiency = load(root, "sufficiency.json", errors)
    freeze = load(root, "freeze.json", errors)
    decision_outcome = load(root, "decision_outcome.json", errors)

    list_files = [
        ("trends.json", trends),
        ("sources.json", sources),
        ("evidence.json", evidence),
        ("lu_episodes.json", episodes),
        ("lineage.json", lineage),
        ("findings.json", findings),
        ("needs.json", needs),
        ("principles.json", principles),
        ("fit_criteria.json", criteria),
        ("concepts.json", concepts),
    ]
    for name, value in list_files:
        if not isinstance(value, list):
            errors.append(f"{name} must contain a JSON array")

    trends = trends if isinstance(trends, list) else []
    sources = sources if isinstance(sources, list) else []
    evidence = evidence if isinstance(evidence, list) else []
    episodes = episodes if isinstance(episodes, list) else []
    lineage = lineage if isinstance(lineage, list) else []
    findings = findings if isinstance(findings, list) else []
    needs = needs if isinstance(needs, list) else []
    principles = principles if isinstance(principles, list) else []
    criteria = criteria if isinstance(criteria, list) else []
    concepts = concepts if isinstance(concepts, list) else []

    trend_ids = ids(trends, "trend_id", errors)
    source_ids = ids(sources, "source_id", errors)
    evidence_ids = ids(evidence, "evidence_id", errors)
    lu_ids = ids(episodes, "lu_id", errors)
    ids(lineage, "lineage_id", errors)
    finding_ids = ids(findings, "finding_id", errors)
    need_ids = ids(needs, "need_id", errors)
    ids(principles, "principle_id", errors)
    requirement_ids = ids(criteria, "requirement_id", errors)
    ids(concepts, "concept_id", errors)

    for source in sources:
        sid = source.get("source_id", "<unknown>")
        if source.get("coverage") not in COVERAGE:
            errors.append(f"{sid} has invalid coverage {source.get('coverage')!r}")

    for row in evidence:
        eid = row.get("evidence_id", "<unknown>")
        sid = row.get("source_id")
        if sid not in source_ids:
            errors.append(f"{eid} references missing source_id: {sid}")
        tid = row.get("trend_id")
        if tid not in (None, "") and tid not in trend_ids:
            errors.append(f"{eid} references missing trend_id: {tid}")
        luid = row.get("lu_id")
        if luid not in (None, "") and luid not in lu_ids:
            errors.append(f"{eid} references missing lu_id: {luid}")

    for row in trends:
        tid = row.get("trend_id", "<unknown>")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", tid, errors)
        status = row.get("status")
        if status is not None and status not in EPISTEMIC:
            errors.append(f"{tid} has invalid status {status!r}")
        if status == "VERIFIED" and not row.get("evidence_refs"):
            errors.append(f"{tid} is VERIFIED without evidence_refs")
        if status in {"VERIFIED", "INFERRED"}:
            require_nonempty_string(row, "importance", tid, errors)

    for row in episodes:
        luid = row.get("lu_id", "<unknown>")
        if row.get("status") not in LU_STATUS:
            errors.append(f"{luid} has invalid status {row.get('status')!r}")
        if row.get("trend_id") not in trend_ids:
            errors.append(f"{luid} references missing trend_id: {row.get('trend_id')}")
        refs_exist(row.get("lu1_evidence", []), evidence_ids, "LU1 evidence", luid, errors)
        refs_exist(row.get("lu2_evidence", []), evidence_ids, "LU2 evidence", luid, errors)
        caveats = row.get("qualification_caveats", [])
        if not isinstance(caveats, list):
            errors.append(f"{luid} qualification_caveats must be a list")

        if row.get("status") == "QUALIFIED":
            if not row.get("lu1_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU1 evidence")
            if not row.get("lu2_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU2 evidence")
            require_nonempty_string(row, "lu1_rationale", luid, errors)
            require_nonempty_string(row, "advancement_indicator", luid, errors)
            require_nonempty_string(row, "lu2_rationale", luid, errors)
            require_nonempty_string(row, "benefit_signal", luid, errors)

        trace = row.get("trace")
        if trace is not None:
            if not isinstance(trace, dict):
                errors.append(f"{luid} trace must be an object")
            else:
                trace_status = trace.get("status", "NOT_ASSESSED")
                if trace_status not in TRACE_STATUS:
                    errors.append(f"{luid} has invalid trace status {trace_status!r}")

                refs_exist(
                    trace.get("evidence_refs", []),
                    evidence_ids,
                    "trace evidence",
                    luid,
                    errors,
                )

                sequence = trace.get("sequence", [])
                if not isinstance(sequence, list):
                    errors.append(f"{luid} trace sequence must be a list")
                    sequence = []
                for index, step in enumerate(sequence):
                    if not isinstance(step, dict):
                        errors.append(f"{luid} trace sequence row {index} must be an object")
                        continue
                    refs_exist(
                        step.get("evidence_refs", []),
                        evidence_ids,
                        "trace step evidence",
                        f"{luid} trace step {index}",
                        errors,
                    )

                fit_points = trace.get("fit_points", [])
                if not isinstance(fit_points, list):
                    errors.append(f"{luid} trace fit_points must be a list")
                    fit_points = []
                for index, point in enumerate(fit_points):
                    if not isinstance(point, dict):
                        errors.append(f"{luid} trace fit point {index} must be an object")
                        continue
                    refs_exist(
                        point.get("evidence_refs", []),
                        evidence_ids,
                        "trace fit-point evidence",
                        f"{luid} trace fit point {index}",
                        errors,
                    )

                if trace_status == "SUFFICIENT":
                    trace_ref_count = len(trace.get("evidence_refs", [])) if isinstance(trace.get("evidence_refs", []), list) else 0
                    trace_ref_count += sum(
                        len(step.get("evidence_refs", []))
                        for step in sequence
                        if isinstance(step, dict) and isinstance(step.get("evidence_refs", []), list)
                    )
                    trace_ref_count += sum(
                        len(point.get("evidence_refs", []))
                        for point in fit_points
                        if isinstance(point, dict) and isinstance(point.get("evidence_refs", []), list)
                    )
                    if not sequence:
                        errors.append(f"{luid} trace is SUFFICIENT without any sequence steps")
                    if trace_ref_count == 0:
                        errors.append(f"{luid} trace is SUFFICIENT without trace evidence refs")

    valid_lineage_refs = source_ids | lu_ids
    independent_lineage_count = 0
    for row in lineage:
        lid = row.get("lineage_id", "<unknown>")
        relationship = row.get("relationship")
        independence = row.get("independence")
        if relationship not in LINEAGE_RELATIONSHIP:
            errors.append(f"{lid} has invalid relationship {relationship!r}")
        if independence not in INDEPENDENCE:
            errors.append(f"{lid} has invalid independence {independence!r}")
        refs_exist(row.get("member_refs", []), valid_lineage_refs, "member", lid, errors)
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", lid, errors)
        if not row.get("member_refs"):
            errors.append(f"{lid} has no member_refs")
        require_nonempty_string(row, "rationale", lid, errors)
        if independence == "INDEPENDENT":
            independent_lineage_count += 1
            if not row.get("evidence_refs"):
                warnings.append(f"{lid} is INDEPENDENT without direct lineage evidence refs")

    for row in findings:
        fid = row.get("finding_id", "<unknown>")
        label = row.get("epistemic_label")
        if label not in EPISTEMIC:
            errors.append(f"{fid} has invalid epistemic_label {label!r}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", fid, errors)
        refs_exist(row.get("lu_refs", []), lu_ids, "LU", fid, errors)
        if label == "VERIFIED" and not row.get("evidence_refs"):
            errors.append(f"{fid} is VERIFIED without evidence_refs")

    for row in needs:
        nid = row.get("need_id", "<unknown>")
        refs_exist(row.get("finding_ids", []), finding_ids, "finding", nid, errors)
        gate = row.get("concept_gate_status", "NOT_ASSESSED")
        if gate not in GATE:
            errors.append(f"{nid} has invalid concept_gate_status {gate!r}")

    fit_checks = [
        "traceability",
        "implementation_independence",
        "solution_plurality",
        "causal_relevance",
        "altitude_check",
        "information_gain",
    ]
    for row in criteria:
        rid = row.get("requirement_id", "<unknown>")
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{rid} references missing need_id: {nid}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", rid, errors)
        status = row.get("status")
        if status not in FIT_STATUS:
            errors.append(f"{rid} has invalid status {status!r}")
        for field in fit_checks:
            require_bool(row, field, rid, errors)
        if status == "PASS":
            if not row.get("evidence_refs"):
                errors.append(f"{rid} PASS requires evidence_refs")
            for field in fit_checks:
                if row.get(field) is not True:
                    errors.append(f"{rid} PASS requires {field}=true")

    for row in concepts:
        mid = row.get("concept_id", "<unknown>")
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{mid} references missing need_id: {nid}")
        refs_exist(row.get("requirement_ids", []), requirement_ids, "requirement", mid, errors)

    if not isinstance(sufficiency, dict):
        errors.append("sufficiency.json must contain a JSON object")
    else:
        if sufficiency.get("status") not in SUFFICIENCY:
            errors.append(f"sufficiency.json has invalid status {sufficiency.get('status')!r}")
        for field in [
            "trend_support",
            "lu_qualification",
            "contradiction_search",
            "lineage_resolution",
            "pyramid_coverage",
            "marginal_value",
        ]:
            if sufficiency.get(field) not in SUFFICIENCY:
                errors.append(f"sufficiency.json {field} has invalid value {sufficiency.get(field)!r}")
        if sufficiency.get("status") == "SUFFICIENT":
            for field in [
                "trend_support",
                "lu_qualification",
                "contradiction_search",
                "lineage_resolution",
                "pyramid_coverage",
                "marginal_value",
            ]:
                if sufficiency.get(field) != "SUFFICIENT":
                    errors.append(f"sufficiency status SUFFICIENT requires {field}=SUFFICIENT")
            if not isinstance(sufficiency.get("rationale"), str) or not sufficiency.get("rationale", "").strip():
                errors.append("sufficiency status SUFFICIENT requires a rationale")

    if not isinstance(freeze, dict):
        errors.append("freeze.json must contain a JSON object")
    else:
        if freeze.get("status") not in {"OPEN", "FROZEN"}:
            errors.append(f"freeze.json has invalid status {freeze.get('status')!r}")
        if freeze.get("status") == "FROZEN":
            if not isinstance(sufficiency, dict) or sufficiency.get("status") != "SUFFICIENT":
                errors.append("Evidence Freeze requires sufficiency.status = SUFFICIENT")
            qualified_count = sum(1 for row in episodes if row.get("status") == "QUALIFIED")
            expected_counts = {
                "evidence_count": len(evidence),
                "qualified_lu_count": qualified_count,
                "independent_lineage_count": independent_lineage_count,
            }
            for field, expected in expected_counts.items():
                if freeze.get(field) != expected:
                    errors.append(f"freeze {field}={freeze.get(field)!r} does not match actual {expected}")

    if (findings or needs or principles) and isinstance(freeze, dict):
        if freeze.get("status") != "FROZEN":
            errors.append("interpretive artifacts exist before Evidence Freeze")

    if criteria or concepts:
        passing = {
            row.get("need_id")
            for row in needs
            if row.get("concept_gate_status") == "PASS"
        }
        for row in criteria:
            if row.get("need_id") not in passing:
                errors.append(
                    f"{row.get('requirement_id')} exists for need that did not PASS concept gate"
                )
        for row in concepts:
            if row.get("need_id") not in passing:
                errors.append(
                    f"{row.get('concept_id')} exists for need that did not PASS concept gate"
                )

    if isinstance(coverage, dict):
        if not coverage.get("likely_underrepresented"):
            warnings.append("coverage likely_underrepresented is empty")
        if not coverage.get("corrective_actions"):
            warnings.append("coverage corrective_actions is empty")
    else:
        errors.append("coverage.json must contain a JSON object")

    if not isinstance(decision, dict):
        errors.append("decision.json must contain a JSON object")
    else:
        if not decision.get("domain"):
            errors.append("decision.json must contain a non-empty domain")
        if not decision.get("decision"):
            errors.append("decision.json must contain a non-empty decision")
        if not decision.get("what_to_understand"):
            warnings.append("decision.json what_to_understand is empty; Phase A should make the learning objective explicit")
        if not decision.get("target_market"):
            warnings.append("decision.json target_market is empty; Phase A should preserve or draft the target market")
        if not decision.get("innovation_altitude"):
            warnings.append("decision.json innovation_altitude is empty; Phase A should preserve or draft the desired altitude")
        optional_list_fields = {
            "starting_hypotheses": "starting hypotheses",
            "discovery_seeds": "discovery seeds",
            "candidate_profile_hypotheses": "candidate-profile hypotheses",
            "search_constraints": "search constraints",
        }
        for field, label in optional_list_fields.items():
            if field not in decision:
                warnings.append(f"decision.json {field} is missing; use an empty list when no {label} were supplied")
                continue
            value = decision.get(field)
            if not isinstance(value, list):
                errors.append(f"decision.json {field} must be a list")
                continue
            for index, item in enumerate(value):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"decision.json {field}[{index}] must be a non-empty string")

    mode = None
    if not isinstance(manifest, dict):
        errors.append("manifest.json must contain a JSON object")
    else:
        mode = manifest.get("mode")
        if mode not in {"SCOUT", "STANDARD", "FULL"}:
            errors.append(f"manifest has invalid mode {mode!r}")
        level = manifest.get("study_execution_level")
        if level not in EXECUTION_LEVEL:
            errors.append(f"manifest has invalid study_execution_level {level!r}")
        basis = manifest.get("study_execution_basis", [])
        if not isinstance(basis, list):
            errors.append("manifest study_execution_basis must be a list")
            basis = []
        if level == "FIELDWORK_ENRICHED" and not basis:
            errors.append("FIELDWORK_ENRICHED requires study_execution_basis")
        if level == "FULL_LEAD_USER_PROJECT":
            required_basis = {
                "direct_lead_user_participation",
                "direct_concept_development_participation",
            }
            if not required_basis.issubset(set(basis)):
                errors.append(
                    "FULL_LEAD_USER_PROJECT requires direct_lead_user_participation and "
                    "direct_concept_development_participation in study_execution_basis"
                )
            if not concepts:
                errors.append("FULL_LEAD_USER_PROJECT requires concept-development state")

    if not isinstance(decision_outcome, dict):
        errors.append("decision_outcome.json must contain a JSON object")
    else:
        status = decision_outcome.get("status")
        allowed = {"STOP", "INVESTIGATE", "ESCALATE"} if mode == "SCOUT" else {"ACT", "TEST", "HOLD", "REJECT"}
        if status is not None:
            if status not in allowed:
                errors.append(f"decision_outcome status {status!r} invalid for mode {mode}")
            require_nonempty_string(decision_outcome, "recommendation", "decision_outcome", errors)
            for field in [
                "why",
                "decisive_finding_refs",
                "decisive_lu_refs",
                "critical_uncertainties",
                "action_now",
                "change_conditions",
                "what_evidence_supports",
                "what_evidence_does_not_support",
                "contradictions",
                "recommended_next_evidence",
                "priority_human_review",
            ]:
                if not isinstance(decision_outcome.get(field), list):
                    errors.append(f"decision_outcome {field} must be a list")
            refs_exist(
                decision_outcome.get("decisive_finding_refs", []),
                finding_ids,
                "finding",
                "decision_outcome",
                errors,
            )
            refs_exist(
                decision_outcome.get("decisive_lu_refs", []),
                lu_ids,
                "LU",
                "decision_outcome",
                errors,
            )
            if not decision_outcome.get("why"):
                errors.append("decision_outcome with a status requires why")
            if not decision_outcome.get("action_now"):
                errors.append("decision_outcome with a status requires action_now")
            if not decision_outcome.get("change_conditions"):
                errors.append("decision_outcome with a status requires change_conditions")
            if (
                not decision_outcome.get("decisive_finding_refs")
                and not decision_outcome.get("decisive_lu_refs")
                and not decision_outcome.get("critical_uncertainties")
            ):
                errors.append(
                    "decision_outcome requires decisive evidence refs or critical uncertainties"
                )

    if isinstance(manifest, dict):
        manifest["deterministic_validation"] = "FAILED" if errors else "PASSED"
        manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
        try:
            (root / "manifest.json").write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except Exception as exc:
            warnings.append(f"could not update manifest validation status: {exc}")

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Lead User study structural validation passed.")
    if warnings:
        print(f"{len(warnings)} warning(s) remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
