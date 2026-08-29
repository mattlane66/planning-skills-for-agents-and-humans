#!/usr/bin/env python3
"""Structural validator for the file-backed Lead User research state."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from study_fingerprint import study_fingerprint

COVERAGE = {"FULL", "PARTIAL", "UNREADABLE", "UNKNOWN"}
LU_STATUS = {"CANDIDATE", "QUALIFIED", "REJECTED"}
EPISTEMIC = {"VERIFIED", "INFERRED", "SPECULATIVE", "UNKNOWN"}
GATE = {"PASS", "FAIL", "NOT_ASSESSED"}
TRACE_STATUS = {"NOT_ASSESSED", "PARTIAL", "SUFFICIENT"}
SUFFICIENCY = {"NOT_ASSESSED", "SUFFICIENT", "INSUFFICIENT"}
EXECUTION_LEVEL = {"DESK_RESEARCH", "FIELDWORK_ENRICHED", "FULL_LEAD_USER_PROJECT"}
STUDY_STATUS = {"IN_PROGRESS", "DECIDED", "COMPLETE"}
PHASES = set("ABCDEFGH")
HUMAN_REVIEW = {"REVIEWED", "NOT_REVIEWED"}
DETERMINISTIC_VALIDATION = {"PASSED", "FAILED", "NOT_RUN"}
INTERPRETIVE_STATUS = {"STABLE", "PROVISIONAL"}
MODEL_CHECK = {"COMPLETED", "NOT_RUN"}
SOURCE_INSTRUCTION_RISK = {"NONE", "PRESENT", "UNKNOWN"}
SOURCE_CONTENT_TRUST = {"UNTRUSTED_DATA"}
PROPAGATION = {
    "Strong propagation evidence",
    "Plausible propagation",
    "Lead-user-specific",
}
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
HYPOTHESIS_STATUS = {
    "UNTESTED",
    "SURVIVED_CURRENT_TESTS",
    "WEAKENED",
    "REJECTED",
    "UNTESTABLE",
}
CONTRAST_CASE_TYPES = {
    "PREDICTED_POSITIVE",
    "EXPOSED_NO_OUTCOME",
    "OUTCOME_WITHOUT_EXPOSURE",
    "ABANDONED_OR_REVERSED_SOLUTION",
}
OBSERVABILITY_STATUS = {
    "TRACE_OBSERVABLE",
    "PARTIALLY_OBSERVABLE",
    "NOT_OBSERVABLE",
    "UNKNOWN",
}
OBSERVABILITY_RESOLUTION = {
    "OPEN",
    "RESOLVED_BY_TRACES",
    "FIELDWORK_REFERRAL",
    "ACCEPTED_UNKNOWN",
}
ANALYSIS_VALIDATION = {"NOT_ASSESSED", "PASSED", "FAILED"}
EVIDENCE_BASIS = {
    "REAL_HUMAN_TRACE",
    "REAL_HUMAN_STATEMENT",
    "REAL_HUMAN_ARTIFACT",
    "INDEPENDENT_OBSERVATION",
    "EVENT_LOG",
    "NONHUMAN_CONTEXT",
    "SYNTHETIC_OR_SIMULATED",
}

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
    "action_id": re.compile(r"^A\d+$"),
    "hypothesis_id": re.compile(r"^H\d+$"),
    "observability_id": re.compile(r"^O\d+$"),
    "analysis_run_id": re.compile(r"^AR\d+$"),
}

SUFFICIENCY_DIMENSIONS = [
    "trend_support",
    "lu_qualification",
    "contradiction_search",
    "lineage_resolution",
    "pyramid_coverage",
    "marginal_value",
]


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


def require_string_list(
    row: dict[str, Any],
    field: str,
    owner: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    value = row.get(field)
    if not isinstance(value, list):
        errors.append(f"{owner} {field} must be a list")
        return []
    if nonempty and not value:
        errors.append(f"{owner} {field} must not be empty")
    valid: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner} {field}[{index}] must be a non-empty string")
        else:
            valid.append(item)
    return valid


def validate_action(row: Any, index: int, errors: list[str]) -> str | None:
    owner = f"decision_outcome action_now[{index}]"
    if not isinstance(row, dict):
        errors.append(f"{owner} must be an object")
        return None
    action_id = row.get("action_id")
    if not isinstance(action_id, str) or not ID_PATTERNS["action_id"].match(action_id):
        errors.append(f"{owner} has invalid action_id {action_id!r}")
        action_id = None
    for field in [
        "action",
        "owner",
        "timebox",
        "deliverable",
        "success_condition",
        "stop_condition",
        "decision_at_end",
    ]:
        require_nonempty_string(row, field, owner, errors)
    require_string_list(row, "evidence_to_collect", owner, errors, nonempty=True)
    return action_id


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
    hypotheses = load(root, "hypotheses.json", errors) if (root / "hypotheses.json").exists() else []
    observability = load(root, "observability.json", errors) if (root / "observability.json").exists() else []
    analysis_runs = load(root, "analysis_runs.json", errors) if (root / "analysis_runs.json").exists() else []

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
        ("hypotheses.json", hypotheses),
        ("observability.json", observability),
        ("analysis_runs.json", analysis_runs),
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
    hypotheses = hypotheses if isinstance(hypotheses, list) else []
    observability = observability if isinstance(observability, list) else []
    analysis_runs = analysis_runs if isinstance(analysis_runs, list) else []

    mode = manifest.get("mode") if isinstance(manifest, dict) else None

    trend_ids = ids(trends, "trend_id", errors)
    source_ids = ids(sources, "source_id", errors)
    evidence_ids = ids(evidence, "evidence_id", errors)
    lu_ids = ids(episodes, "lu_id", errors)
    lineage_ids = ids(lineage, "lineage_id", errors)
    finding_ids = ids(findings, "finding_id", errors)
    need_ids = ids(needs, "need_id", errors)
    principle_ids = ids(principles, "principle_id", errors)
    requirement_ids = ids(criteria, "requirement_id", errors)
    concept_ids = ids(concepts, "concept_id", errors)
    hypothesis_ids = ids(hypotheses, "hypothesis_id", errors)
    observability_ids = ids(observability, "observability_id", errors)
    analysis_run_ids = ids(analysis_runs, "analysis_run_id", errors)

    source_by_id = {
        row.get("source_id"): row
        for row in sources
        if isinstance(row, dict) and row.get("source_id")
    }
    evidence_by_id = {
        row.get("evidence_id"): row
        for row in evidence
        if isinstance(row, dict) and row.get("evidence_id")
    }
    episode_by_id = {
        row.get("lu_id"): row
        for row in episodes
        if isinstance(row, dict) and row.get("lu_id")
    }
    finding_by_id = {
        row.get("finding_id"): row
        for row in findings
        if isinstance(row, dict) and row.get("finding_id")
    }
    criterion_by_id = {
        row.get("requirement_id"): row
        for row in criteria
        if isinstance(row, dict) and row.get("requirement_id")
    }

    for source in sources:
        sid = source.get("source_id", "<unknown>")
        for field in ["title", "source_type", "access_date"]:
            require_nonempty_string(source, field, sid, errors)
        has_url = isinstance(source.get("url"), str) and bool(source["url"].strip())
        has_immutable_id = isinstance(source.get("immutable_identifier"), str) and bool(
            source["immutable_identifier"].strip()
        )
        if not has_url and not has_immutable_id:
            errors.append(f"{sid} requires url or immutable_identifier")
        if source.get("coverage") not in COVERAGE:
            errors.append(f"{sid} has invalid coverage {source.get('coverage')!r}")
        if source.get("coverage") in {"PARTIAL", "UNREADABLE", "UNKNOWN"}:
            require_nonempty_string(source, "coverage_note", sid, errors)
        access_date = source.get("access_date")
        if isinstance(access_date, str) and access_date.strip():
            try:
                datetime.fromisoformat(access_date)
            except ValueError:
                errors.append(f"{sid} access_date must be ISO-8601")
        instruction_risk = source.get("embedded_instruction_risk")
        if instruction_risk not in SOURCE_INSTRUCTION_RISK:
            errors.append(
                f"{sid} has invalid embedded_instruction_risk {instruction_risk!r}"
            )
        if instruction_risk in {"PRESENT", "UNKNOWN"}:
            require_nonempty_string(source, "embedded_instruction_note", sid, errors)
        if source.get("content_trust") not in SOURCE_CONTENT_TRUST:
            errors.append(f"{sid} content_trust must be 'UNTRUSTED_DATA'")
        require_bool(source, "outward_citation_allowed", sid, errors)
        if source.get("outward_citation_allowed") is True and not source.get("url"):
            errors.append(f"{sid} outward citation requires a URL")
        for field in [
            "platform_or_community",
            "participant_role",
            "thread_or_context",
            "community_norm",
            "platform_affordance",
            "selection_mechanism",
        ]:
            if field in source and source.get(field) not in (None, ""):
                require_nonempty_string(source, field, sid, errors)

    analysis_run_by_id = {
        row.get("analysis_run_id"): row
        for row in analysis_runs
        if isinstance(row, dict) and row.get("analysis_run_id")
    }

    for row in evidence:
        eid = row.get("evidence_id", "<unknown>")
        sid = row.get("source_id")
        if sid not in source_ids:
            errors.append(f"{eid} references missing source_id: {sid}")
        elif source_by_id[sid].get("coverage") not in {"FULL", "PARTIAL"}:
            errors.append(
                f"{eid} cannot cite source {sid} with coverage "
                f"{source_by_id[sid].get('coverage')!r}"
            )
        require_nonempty_string(row, "evidence_type", eid, errors)
        basis = row.get("evidence_basis")
        if basis is not None and basis not in EVIDENCE_BASIS:
            errors.append(f"{eid} has invalid evidence_basis {basis!r}")
        if basis == "SYNTHETIC_OR_SIMULATED":
            errors.append(
                f"{eid} synthetic or simulated material cannot be persisted as human evidence"
            )
        analysis_run_id = row.get("analysis_run_id")
        if analysis_run_id not in (None, "") and analysis_run_id not in analysis_run_ids:
            errors.append(f"{eid} references missing analysis_run_id: {analysis_run_id}")
        excerpt = row.get("verbatim_excerpt")
        observation = row.get("bounded_observation")
        if not (
            isinstance(excerpt, str) and excerpt.strip()
        ) and not (
            isinstance(observation, str) and observation.strip()
        ):
            errors.append(f"{eid} requires verbatim_excerpt or bounded_observation")
        public_summary = row.get("public_summary")
        if public_summary is not None and (
            not isinstance(public_summary, str) or not public_summary.strip()
        ):
            errors.append(f"{eid} public_summary must be a non-empty string when present")
        tid = row.get("trend_id")
        if tid not in (None, "") and tid not in trend_ids:
            errors.append(f"{eid} references missing trend_id: {tid}")
        luid = row.get("lu_id")
        if luid not in (None, "") and luid not in lu_ids:
            errors.append(f"{eid} references missing lu_id: {luid}")
        private_episode = episode_by_id.get(luid, {})
        private_identity = private_episode.get("user_entity")
        if (
            isinstance(public_summary, str)
            and isinstance(private_identity, str)
            and private_episode.get("identity_surface_allowed") is not True
            and private_identity.casefold() in public_summary.casefold()
        ):
            errors.append(f"{eid} public_summary exposes private user_entity")

    for row in hypotheses:
        hid = row.get("hypothesis_id", "<unknown>")
        require_nonempty_string(row, "claim", hid, errors)
        status = row.get("status")
        if status not in HYPOTHESIS_STATUS:
            errors.append(f"{hid} has invalid status {status!r}")
        predictions = require_string_list(row, "observable_predictions", hid, errors)
        require_string_list(row, "rival_explanations", hid, errors)
        require_string_list(row, "targeted_refutation_searches", hid, errors)
        require_string_list(row, "boundary_conditions", hid, errors)
        refs_exist(row.get("evidence_for", []), evidence_ids, "supporting evidence", hid, errors)
        refs_exist(row.get("evidence_against", []), evidence_ids, "challenging evidence", hid, errors)
        cases = row.get("contrastive_cases", [])
        if not isinstance(cases, list):
            errors.append(f"{hid} contrastive_cases must be a list")
            cases = []
        for index, case in enumerate(cases):
            owner = f"{hid} contrastive_cases[{index}]"
            if not isinstance(case, dict):
                errors.append(f"{owner} must be an object")
                continue
            if case.get("case_type") not in CONTRAST_CASE_TYPES:
                errors.append(f"{owner} has invalid case_type {case.get('case_type')!r}")
            refs_exist(case.get("evidence_refs", []), evidence_ids, "evidence", owner, errors)
            require_nonempty_string(case, "interpretation", owner, errors)
        if status in {"SURVIVED_CURRENT_TESTS", "WEAKENED", "REJECTED"}:
            if not predictions:
                errors.append(f"{hid} assessed status requires observable_predictions")
            require_nonempty_string(row, "strongest_plausible_refuter", hid, errors)
            require_nonempty_string(row, "update_rationale", hid, errors)
            if not row.get("evidence_for") and not row.get("evidence_against"):
                errors.append(f"{hid} assessed status requires evidence_for or evidence_against")
            if not cases:
                errors.append(f"{hid} assessed status requires at least one contrastive case")
        if status == "UNTESTABLE":
            require_nonempty_string(row, "update_rationale", hid, errors)

    for row in observability:
        oid = row.get("observability_id", "<unknown>")
        require_nonempty_string(row, "question", oid, errors)
        require_bool(row, "decision_critical", oid, errors)
        if row.get("status") not in OBSERVABILITY_STATUS:
            errors.append(f"{oid} has invalid status {row.get('status')!r}")
        if row.get("resolution") not in OBSERVABILITY_RESOLUTION:
            errors.append(f"{oid} has invalid resolution {row.get('resolution')!r}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", oid, errors)
        if row.get("resolution") == "FIELDWORK_REFERRAL":
            require_nonempty_string(row, "fieldwork_referral", oid, errors)
        if row.get("resolution") == "ACCEPTED_UNKNOWN":
            require_nonempty_string(row, "acceptance_rationale", oid, errors)
        if row.get("status") in {"NOT_OBSERVABLE", "PARTIALLY_OBSERVABLE", "UNKNOWN"} and row.get("resolution") == "RESOLVED_BY_TRACES":
            errors.append(f"{oid} cannot be RESOLVED_BY_TRACES with status {row.get('status')}")

    for row in analysis_runs:
        arid = row.get("analysis_run_id", "<unknown>")
        for field in [
            "task",
            "model",
            "model_version",
            "prompt_or_workflow_version",
            "extraction_schema",
        ]:
            require_nonempty_string(row, field, arid, errors)
        validation = row.get("sampled_validation")
        if not isinstance(validation, dict):
            errors.append(f"{arid} sampled_validation must be an object")
            validation = {}
        if validation.get("status") not in ANALYSIS_VALIDATION:
            errors.append(
                f"{arid} sampled_validation has invalid status {validation.get('status')!r}"
            )
        if validation.get("status") in {"PASSED", "FAILED"}:
            sample_size = validation.get("sample_size")
            if not isinstance(sample_size, int) or sample_size <= 0:
                errors.append(f"{arid} sampled_validation sample_size must be a positive integer")
            require_nonempty_string(
                validation,
                "agreement_or_error_summary",
                f"{arid} sampled_validation",
                errors,
            )

    for row in trends:
        tid = row.get("trend_id", "<unknown>")
        for field in ["statement", "direction", "importance"]:
            require_nonempty_string(row, field, tid, errors)
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", tid, errors)
        status = row.get("status")
        if status is not None and status not in EPISTEMIC:
            errors.append(f"{tid} has invalid status {status!r}")
        if status == "VERIFIED" and not row.get("evidence_refs"):
            errors.append(f"{tid} is VERIFIED without evidence_refs")
        indicators = require_string_list(
            row, "observable_indicators", tid, errors,
            nonempty=status in {"VERIFIED", "INFERRED"},
        )
        if status in {"VERIFIED", "INFERRED"} and not indicators:
            errors.append(f"{tid} {status} requires observable_indicators")

    for row in episodes:
        luid = row.get("lu_id", "<unknown>")
        for field in ["user_entity", "need_statement", "context"]:
            require_nonempty_string(row, field, luid, errors)
        require_bool(row, "identity_surface_allowed", luid, errors)
        public_label = row.get("public_label")
        internal_identity = row.get("user_entity")
        if (
            row.get("identity_surface_allowed") is False
            and isinstance(public_label, str)
            and isinstance(internal_identity, str)
            and internal_identity.casefold() in public_label.casefold()
        ):
            errors.append(f"{luid} public_label exposes private user_entity")
        if row.get("identity_surface_allowed") is True:
            require_nonempty_string(row, "public_label", luid, errors)
            require_nonempty_string(row, "identity_surface_rationale", luid, errors)
        if row.get("status") not in LU_STATUS:
            errors.append(f"{luid} has invalid status {row.get('status')!r}")
        if row.get("trend_id") not in trend_ids:
            errors.append(f"{luid} references missing trend_id: {row.get('trend_id')}")
        refs_exist(row.get("lu1_evidence", []), evidence_ids, "LU1 evidence", luid, errors)
        refs_exist(row.get("lu2_evidence", []), evidence_ids, "LU2 evidence", luid, errors)
        caveats = row.get("qualification_caveats", [])
        if not isinstance(caveats, list):
            errors.append(f"{luid} qualification_caveats must be a list")
        else:
            require_string_list(row, "qualification_caveats", luid, errors)

        if row.get("status") == "QUALIFIED":
            if not row.get("lu1_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU1 evidence")
            if not row.get("lu2_evidence"):
                errors.append(f"{luid} is QUALIFIED without LU2 evidence")
            require_nonempty_string(row, "lu1_rationale", luid, errors)
            require_nonempty_string(row, "advancement_indicator", luid, errors)
            require_nonempty_string(row, "lu2_rationale", luid, errors)
            require_nonempty_string(row, "benefit_signal", luid, errors)
            for ref in row.get("lu1_evidence", []) + row.get("lu2_evidence", []):
                evidence_row = evidence_by_id.get(ref, {})
                if evidence_row.get("evidence_basis") == "SYNTHETIC_OR_SIMULATED":
                    errors.append(f"{luid} qualification cannot use synthetic or simulated evidence {ref}")
                evidence_trend = evidence_row.get("trend_id")
                if evidence_trend not in (None, "", row.get("trend_id")):
                    errors.append(
                        f"{luid} qualification evidence {ref} belongs to trend {evidence_trend}"
                    )
                evidence_lu = evidence_row.get("lu_id")
                if evidence_lu not in (None, "", luid):
                    errors.append(
                        f"{luid} qualification evidence {ref} belongs to {evidence_lu}"
                    )

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
                    for field in ["step_id", "action", "context", "result"]:
                        require_nonempty_string(
                            step,
                            field,
                            f"{luid} trace step {index}",
                            errors,
                        )
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
                    for field in [
                        "initiating_condition",
                        "prior_approach",
                        "switch_or_change_trigger",
                        "expected_improvement",
                        "actual_outcome",
                    ]:
                        require_nonempty_string(trace, field, f"{luid} trace", errors)
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
    independent_member_sets: set[frozenset[str]] = set()
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
                errors.append(f"{lid} is INDEPENDENT without direct lineage evidence refs")
            members = row.get("member_refs")
            if isinstance(members, list) and all(isinstance(ref, str) for ref in members):
                member_set = frozenset(members)
                if member_set in independent_member_sets:
                    errors.append(f"{lid} duplicates an independent lineage member set")
                independent_member_sets.add(member_set)
        if relationship == "INDEPENDENT_REDISCOVERY" and independence != "INDEPENDENT":
            errors.append(
                f"{lid} INDEPENDENT_REDISCOVERY requires independence=INDEPENDENT"
            )
        if relationship in {
            "SAME_CREATOR",
            "FORK",
            "DEPENDENCY",
            "ADAPTATION",
            "COPIED_TECHNIQUE",
            "COMMON_UPSTREAM",
        } and independence == "INDEPENDENT":
            errors.append(f"{lid} relationship {relationship} cannot be INDEPENDENT")

    for row in findings:
        fid = row.get("finding_id", "<unknown>")
        require_nonempty_string(row, "claim", fid, errors)
        require_nonempty_string(row, "confidence_rationale", fid, errors)
        label = row.get("epistemic_label")
        if label not in EPISTEMIC:
            errors.append(f"{fid} has invalid epistemic_label {label!r}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", fid, errors)
        refs_exist(row.get("lu_refs", []), lu_ids, "LU", fid, errors)
        refs_exist(
            row.get("contradictions", []),
            finding_ids,
            "contradictory finding",
            fid,
            errors,
        )
        if label == "VERIFIED" and not row.get("evidence_refs"):
            errors.append(f"{fid} is VERIFIED without evidence_refs")

    for row in needs:
        nid = row.get("need_id", "<unknown>")
        require_nonempty_string(row, "statement", nid, errors)
        refs_exist(row.get("finding_ids", []), finding_ids, "finding", nid, errors)
        refs_exist(row.get("relevant_trends", []), trend_ids, "trend", nid, errors)
        refs_exist(
            row.get("contradictions", []),
            finding_ids,
            "contradictory finding",
            nid,
            errors,
        )
        if row.get("propagation_status") not in PROPAGATION:
            errors.append(
                f"{nid} has invalid propagation_status {row.get('propagation_status')!r}"
            )
        gate = row.get("concept_gate_status", "NOT_ASSESSED")
        if gate not in GATE:
            errors.append(f"{nid} has invalid concept_gate_status {gate!r}")
        gate_checks = row.get("concept_gate_checks")
        if not isinstance(gate_checks, dict):
            errors.append(f"{nid} concept_gate_checks must be an object")
            gate_checks = {}
        for field in [
            "credible_trend",
            "qualified_lu_support",
            "need_workaround_separation",
            "fitness_evidence_sufficient",
            "no_blocking_contradiction",
        ]:
            require_bool(gate_checks, field, f"{nid} concept_gate_checks", errors)
        if gate == "PASS":
            require_nonempty_string(row, "concept_gate_rationale", nid, errors)
            if not row.get("finding_ids"):
                errors.append(f"{nid} PASS requires supporting finding_ids")
            if not row.get("relevant_trends"):
                errors.append(f"{nid} PASS requires relevant_trends")
            for field in [
                "credible_trend",
                "qualified_lu_support",
                "need_workaround_separation",
                "fitness_evidence_sufficient",
                "no_blocking_contradiction",
            ]:
                if gate_checks.get(field) is not True:
                    errors.append(f"{nid} PASS requires concept_gate_checks.{field}=true")
            supporting_lus = {
                lu_ref
                for finding_ref in row.get("finding_ids", [])
                for lu_ref in finding_by_id.get(finding_ref, {}).get("lu_refs", [])
            }
            qualified_lus = {
                episode.get("lu_id")
                for episode in episodes
                if episode.get("status") == "QUALIFIED"
            }
            if not supporting_lus.intersection(qualified_lus):
                errors.append(f"{nid} PASS requires a qualified LU through its findings")

    for row in principles:
        spid = row.get("principle_id", "<unknown>")
        require_nonempty_string(row, "principle", spid, errors)
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{spid} references missing need_id: {nid}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", spid, errors)
        status = row.get("status")
        if status not in EPISTEMIC:
            errors.append(f"{spid} has invalid status {status!r}")
        if status in {"VERIFIED", "INFERRED"} and not row.get("evidence_refs"):
            errors.append(f"{spid} {status} requires evidence_refs")

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
        require_nonempty_string(row, "requirement", rid, errors)
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
        require_nonempty_string(row, "mechanism", mid, errors)
        nid = row.get("need_id")
        if nid not in need_ids:
            errors.append(f"{mid} references missing need_id: {nid}")
        refs_exist(row.get("requirement_ids", []), requirement_ids, "requirement", mid, errors)
        if not row.get("requirement_ids"):
            errors.append(f"{mid} requires requirement_ids")
        for ref in row.get("requirement_ids", []):
            if criterion_by_id.get(ref, {}).get("status") != "PASS":
                errors.append(f"{mid} references non-PASS requirement {ref}")
        for field in ["assumptions", "risks", "evidence_needed_next"]:
            require_string_list(row, field, mid, errors)

    all_structured_refs = (
        trend_ids
        | source_ids
        | evidence_ids
        | lu_ids
        | lineage_ids
        | finding_ids
        | need_ids
        | principle_ids
        | requirement_ids
        | concept_ids
        | hypothesis_ids
        | observability_ids
        | analysis_run_ids
    )

    if not isinstance(sufficiency, dict):
        errors.append("sufficiency.json must contain a JSON object")
    else:
        if sufficiency.get("status") not in SUFFICIENCY:
            errors.append(f"sufficiency.json has invalid status {sufficiency.get('status')!r}")
        dimensions = sufficiency.get("dimensions")
        if not isinstance(dimensions, dict):
            errors.append("sufficiency.json dimensions must be an object")
            dimensions = {}
        for field in SUFFICIENCY_DIMENSIONS:
            dimension = dimensions.get(field)
            owner = f"sufficiency.json dimensions.{field}"
            if not isinstance(dimension, dict):
                errors.append(f"{owner} must be an object")
                continue
            if dimension.get("status") not in SUFFICIENCY:
                errors.append(
                    f"{owner} has invalid status {dimension.get('status')!r}"
                )
            if dimension.get("status") != "NOT_ASSESSED":
                require_nonempty_string(dimension, "rationale", owner, errors)
            refs = require_string_list(
                dimension, "supporting_refs", owner, errors
            )
            for ref in refs:
                if ref not in all_structured_refs:
                    errors.append(f"{owner} references missing supporting ref: {ref}")
            require_string_list(dimension, "next_actions", owner, errors)
        if sufficiency.get("status") == "SUFFICIENT":
            for field in SUFFICIENCY_DIMENSIONS:
                if dimensions.get(field, {}).get("status") != "SUFFICIENT":
                    errors.append(
                        "sufficiency status SUFFICIENT requires "
                        f"dimensions.{field}.status=SUFFICIENT"
                    )
            require_nonempty_string(
                sufficiency,
                "overall_rationale",
                "sufficiency status SUFFICIENT",
                errors,
            )
        if sufficiency.get("status") == "INSUFFICIENT":
            if not any(
                dimensions.get(field, {}).get("status") == "INSUFFICIENT"
                for field in SUFFICIENCY_DIMENSIONS
            ):
                errors.append(
                    "sufficiency status INSUFFICIENT requires an INSUFFICIENT dimension"
                )
            require_string_list(
                sufficiency,
                "unresolved_actions",
                "sufficiency status INSUFFICIENT",
                errors,
                nonempty=True,
            )

    if not isinstance(freeze, dict):
        errors.append("freeze.json must contain a JSON object")
    else:
        if freeze.get("status") not in {"OPEN", "FROZEN"}:
            errors.append(f"freeze.json has invalid status {freeze.get('status')!r}")
        if freeze.get("status") == "FROZEN":
            if not isinstance(sufficiency, dict) or sufficiency.get("status") != "SUFFICIENT":
                errors.append("Evidence Freeze requires sufficiency.status = SUFFICIENT")
            frozen_at = freeze.get("frozen_at")
            if not isinstance(frozen_at, str) or not frozen_at.strip():
                errors.append("Evidence Freeze requires frozen_at")
            else:
                try:
                    datetime.fromisoformat(frozen_at.replace("Z", "+00:00"))
                except ValueError:
                    errors.append("Evidence Freeze frozen_at must be ISO-8601")
            qualified_count = sum(1 for row in episodes if row.get("status") == "QUALIFIED")
            expected_counts = {
                "evidence_count": len(evidence),
                "qualified_lu_count": qualified_count,
                "independent_lineage_count": independent_lineage_count,
            }
            for field, expected in expected_counts.items():
                if freeze.get(field) != expected:
                    errors.append(f"freeze {field}={freeze.get(field)!r} does not match actual {expected}")
            open_critical = [
                row.get("observability_id", "<unknown>")
                for row in observability
                if isinstance(row, dict)
                and row.get("decision_critical") is True
                and row.get("resolution") == "OPEN"
            ]
            if open_critical:
                errors.append(
                    "Evidence Freeze cannot leave decision-critical observability questions OPEN: "
                    + ", ".join(open_critical)
                )
            referenced_analysis_runs = {
                row.get("analysis_run_id")
                for row in evidence
                if isinstance(row, dict) and row.get("analysis_run_id")
            }
            for arid in sorted(referenced_analysis_runs):
                validation = analysis_run_by_id.get(arid, {}).get("sampled_validation", {})
                if validation.get("status") != "PASSED":
                    errors.append(
                        f"Evidence Freeze requires sampled validation PASSED for analysis run {arid}"
                    )

    if (
        mode in {"STANDARD", "FULL"}
        and (findings or needs or principles)
        and isinstance(freeze, dict)
    ):
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

    study_status = (
        manifest.get("study_status") if isinstance(manifest, dict) else None
    )
    decision_brief_text: str | None = None

    if isinstance(coverage, dict):
        for field in [
            "likely_overrepresented",
            "likely_underrepresented",
            "inaccessible_or_private",
            "languages_or_regions_searched",
            "corrective_actions",
            "fieldwork_referrals",
        ]:
            require_string_list(coverage, field, "coverage.json", errors)
        if not coverage.get("likely_underrepresented"):
            warnings.append("coverage likely_underrepresented is empty")
        if not coverage.get("corrective_actions") and not coverage.get("fieldwork_referrals"):
            warnings.append("coverage corrective_actions and fieldwork_referrals are empty")
        if mode in {"STANDARD", "FULL"} and study_status in {"DECIDED", "COMPLETE"}:
            if not coverage.get("likely_underrepresented"):
                errors.append(
                    "decided STANDARD/FULL study requires likely_underrepresented coverage"
                )
            if not coverage.get("corrective_actions") and not coverage.get("fieldwork_referrals"):
                errors.append(
                    "decided STANDARD/FULL study requires corrective discovery or fieldwork referrals"
                )
    else:
        errors.append("coverage.json must contain a JSON object")

    if not isinstance(decision, dict):
        errors.append("decision.json must contain a JSON object")
    else:
        if not decision.get("domain"):
            errors.append("decision.json must contain a non-empty domain")
        if not decision.get("decision"):
            errors.append("decision.json must contain a non-empty decision")
        for field in ["what_to_understand", "target_market", "innovation_altitude"]:
            if not decision.get(field):
                if study_status in {"DECIDED", "COMPLETE"}:
                    errors.append(f"decided study requires decision.json {field}")
                else:
                    warnings.append(
                        f"decision.json {field} is empty; Phase A should make it explicit"
                    )
        scope = decision.get("scope")
        if not isinstance(scope, dict):
            errors.append("decision.json scope must be an object")
        else:
            require_string_list(scope, "in", "decision.json scope", errors)
            require_string_list(scope, "out", "decision.json scope", errors)
        for field in [
            "assumptions",
            "consequential_unknowns",
            "disconfirming_evidence",
            "questions_not_answered",
        ]:
            require_string_list(decision, field, "decision.json", errors)
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

    if not isinstance(manifest, dict):
        errors.append("manifest.json must contain a JSON object")
    else:
        if mode not in {"SCOUT", "STANDARD", "FULL"}:
            errors.append(f"manifest has invalid mode {mode!r}")
        if manifest.get("protocol_version") != "1.7":
            errors.append(
                f"manifest requires protocol_version '1.7', got {manifest.get('protocol_version')!r}"
            )
        if manifest.get("phase") not in PHASES:
            errors.append(f"manifest has invalid phase {manifest.get('phase')!r}")
        if study_status not in STUDY_STATUS:
            errors.append(f"manifest has invalid study_status {study_status!r}")
        if manifest.get("human_review") not in HUMAN_REVIEW:
            errors.append(
                f"manifest has invalid human_review {manifest.get('human_review')!r}"
            )
        if manifest.get("deterministic_validation") not in DETERMINISTIC_VALIDATION:
            errors.append(
                "manifest has invalid deterministic_validation "
                f"{manifest.get('deterministic_validation')!r}"
            )
        if manifest.get("interpretive_status") not in INTERPRETIVE_STATUS:
            errors.append(
                f"manifest has invalid interpretive_status {manifest.get('interpretive_status')!r}"
            )
        if manifest.get("model_check") not in MODEL_CHECK:
            errors.append(
                f"manifest has invalid model_check {manifest.get('model_check')!r}"
            )
        if study_status in {"DECIDED", "COMPLETE"} and manifest.get("phase") not in {"G", "H"}:
            errors.append("decided or complete study must be in phase G or H")
        if study_status == "COMPLETE":
            if manifest.get("phase") != "H":
                errors.append("complete study must be in phase H")
            if manifest.get("model_check") != "COMPLETED":
                errors.append("complete study requires model_check COMPLETED")
            decision_brief = root / "outputs" / "decision-brief.md"
            try:
                decision_brief_text = decision_brief.read_text(encoding="utf-8")
            except OSError:
                decision_brief_text = None
            if not decision_brief_text or not decision_brief_text.strip():
                errors.append(
                    "complete study requires non-empty outputs/decision-brief.md"
                )
        level = manifest.get("study_execution_level")
        if level not in EXECUTION_LEVEL:
            errors.append(f"manifest has invalid study_execution_level {level!r}")
        basis = manifest.get("study_execution_basis", [])
        if not isinstance(basis, list):
            errors.append("manifest study_execution_basis must be a list")
            basis = []
        valid_basis: set[str] = set()
        for index, item in enumerate(basis):
            if not isinstance(item, str) or not item.strip():
                errors.append(
                    f"manifest study_execution_basis[{index}] must be a non-empty string"
                )
                continue
            valid_basis.add(item)
        if level == "FIELDWORK_ENRICHED" and not valid_basis:
            errors.append("FIELDWORK_ENRICHED requires study_execution_basis")
        if level == "FULL_LEAD_USER_PROJECT":
            required_basis = {
                "direct_lead_user_participation",
                "direct_concept_development_participation",
            }
            if not required_basis.issubset(valid_basis):
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
        if study_status in {"DECIDED", "COMPLETE"} and status is None:
            errors.append("decided or complete study requires decision_outcome status")
        if study_status == "IN_PROGRESS" and status is not None:
            errors.append("decision_outcome status requires study_status DECIDED or COMPLETE")
        if status is not None:
            if status not in allowed:
                errors.append(f"decision_outcome status {status!r} invalid for mode {mode}")
            require_nonempty_string(decision_outcome, "recommendation", "decision_outcome", errors)
            string_list_fields = [
                "why",
                "decisive_finding_refs",
                "decisive_lu_refs",
                "critical_uncertainties",
                "change_conditions",
                "what_evidence_supports",
                "what_evidence_does_not_support",
                "contradictions",
                "recommended_next_evidence",
                "priority_human_review",
            ]
            for field in string_list_fields:
                require_string_list(decision_outcome, field, "decision_outcome", errors)
            actions = decision_outcome.get("action_now")
            if not isinstance(actions, list):
                errors.append("decision_outcome action_now must be a list")
                actions = []
            action_ids: set[str] = set()
            for index, action in enumerate(actions):
                action_id = validate_action(action, index, errors)
                if action_id:
                    if action_id in action_ids:
                        errors.append(f"duplicate action_id: {action_id}")
                    action_ids.add(action_id)
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
            if status == "ACT":
                if not isinstance(freeze, dict) or freeze.get("status") != "FROZEN":
                    errors.append("ACT requires Evidence Freeze")
                if not isinstance(sufficiency, dict) or sufficiency.get("status") != "SUFFICIENT":
                    errors.append("ACT requires sufficient research")
                if not decision_outcome.get("decisive_finding_refs") and not decision_outcome.get("decisive_lu_refs"):
                    errors.append("ACT requires decisive evidence refs")
                if not isinstance(manifest, dict) or manifest.get("interpretive_status") != "STABLE":
                    errors.append("ACT requires interpretive_status STABLE")
            if (
                status == "TEST"
                and mode in {"STANDARD", "FULL"}
                and isinstance(freeze, dict)
                and freeze.get("status") == "OPEN"
                and isinstance(sufficiency, dict)
                and sufficiency.get("status") != "INSUFFICIENT"
            ):
                errors.append(
                    "TEST with OPEN evidence requires sufficiency.status INSUFFICIENT"
                )

    if study_status == "COMPLETE" and decision_brief_text:
        try:
            fingerprint_marker = f"- State fingerprint: {study_fingerprint(root)}"
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            fingerprint_marker = None
            errors.append(f"cannot compute complete-study state fingerprint: {exc}")
        expected_markers = [
            "- Current phase: H",
            "- Study status: COMPLETE",
            "- Model checklist: COMPLETED",
        ]
        if fingerprint_marker:
            expected_markers.append(fingerprint_marker)
        if isinstance(decision_outcome, dict) and decision_outcome.get("status"):
            expected_markers.append(
                f"## Recommendation — {decision_outcome['status']}"
            )
            for action in decision_outcome.get("action_now", []):
                if isinstance(action, dict) and isinstance(action.get("action_id"), str):
                    expected_markers.append(f"### {action['action_id']} —")
        for marker in expected_markers:
            if marker not in decision_brief_text:
                errors.append(
                    f"complete Decision Brief is stale or missing marker: {marker}"
                )

        for episode in episodes:
            if not isinstance(episode, dict) or episode.get("identity_surface_allowed") is True:
                continue
            internal_identity = episode.get("user_entity")
            if (
                isinstance(internal_identity, str)
                and internal_identity.strip()
                and re.search(
                    re.escape(internal_identity.strip()),
                    decision_brief_text,
                    flags=re.IGNORECASE,
                )
            ):
                errors.append(
                    f"complete Decision Brief exposes private identity for {episode.get('lu_id')}"
                )
        for source in sources:
            if not isinstance(source, dict) or source.get("outward_citation_allowed") is True:
                continue
            url = source.get("url")
            if isinstance(url, str) and url and url in decision_brief_text:
                errors.append(
                    f"complete Decision Brief exposes withheld URL for {source.get('source_id')}"
                )
        for evidence_row in evidence:
            if not isinstance(evidence_row, dict):
                continue
            excerpt = evidence_row.get("verbatim_excerpt")
            if (
                isinstance(excerpt, str)
                and len(excerpt.strip()) >= 20
                and excerpt.strip() in decision_brief_text
            ):
                errors.append(
                    "complete Decision Brief reproduces raw excerpt for "
                    f"{evidence_row.get('evidence_id')}"
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
