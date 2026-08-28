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

ID_PATTERNS = {
    "trend_id": re.compile(r"^T\d+$"),
    "source_id": re.compile(r"^SRC\d+$"),
    "evidence_id": re.compile(r"^E\d+$"),
    "lu_id": re.compile(r"^LU\d+$"),
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
    findings = load(root, "findings.json", errors)
    needs = load(root, "needs.json", errors)
    principles = load(root, "principles.json", errors)
    criteria = load(root, "fit_criteria.json", errors)
    concepts = load(root, "concepts.json", errors)
    coverage = load(root, "coverage.json", errors)
    freeze = load(root, "freeze.json", errors)

    for name, value in [
        ("trends.json", trends),
        ("sources.json", sources),
        ("evidence.json", evidence),
        ("lu_episodes.json", episodes),
        ("findings.json", findings),
        ("needs.json", needs),
        ("principles.json", principles),
        ("fit_criteria.json", criteria),
        ("concepts.json", concepts),
    ]:
        if not isinstance(value, list):
            errors.append(f"{name} must contain a JSON array")

    trends = trends if isinstance(trends, list) else []
    sources = sources if isinstance(sources, list) else []
    evidence = evidence if isinstance(evidence, list) else []
    episodes = episodes if isinstance(episodes, list) else []
    findings = findings if isinstance(findings, list) else []
    needs = needs if isinstance(needs, list) else []
    principles = principles if isinstance(principles, list) else []
    criteria = criteria if isinstance(criteria, list) else []
    concepts = concepts if isinstance(concepts, list) else []

    trend_ids = ids(trends, "trend_id", errors)
    source_ids = ids(sources, "source_id", errors)
    evidence_ids = ids(evidence, "evidence_id", errors)
    lu_ids = ids(episodes, "lu_id", errors)
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

    for row in episodes:
        luid = row.get("lu_id", "<unknown>")
        if row.get("status") not in LU_STATUS:
            errors.append(f"{luid} has invalid status {row.get('status')!r}")
        if row.get("trend_id") not in trend_ids:
            errors.append(f"{luid} references missing trend_id: {row.get('trend_id')}")
        refs_exist(row.get("lu1_evidence", []), evidence_ids, "LU1 evidence", luid, errors)
        refs_exist(row.get("lu2_evidence", []), evidence_ids, "LU2 evidence", luid, errors)
        if row.get("status") == "QUALIFIED":
            if not row.get("lu1_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU1 evidence")
            if not row.get("lu2_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU2 evidence")

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

    for row in criteria:
        rid = row.get("requirement_id", "<unknown>")
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{rid} references missing need_id: {nid}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", rid, errors)

    for row in concepts:
        mid = row.get("concept_id", "<unknown>")
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{mid} references missing need_id: {nid}")
        refs_exist(row.get("requirement_ids", []), requirement_ids, "requirement", mid, errors)

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
        if "starting_hypotheses" not in decision:
            warnings.append("decision.json starting_hypotheses is missing; use an empty list when none were supplied")

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
