#!/usr/bin/env python3
"""Structural validator for the file-backed Lead User research state."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from report_safety import contains_private_identity, safe_outward_url
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
FIXTURE_TYPE = {"NONE", "SYNTHETIC_REFERENCE"}
INTERPRETATION_COMPLETION = {"NOT_STARTED", "COMPLETED"}
SUFFICIENCY_REPAIR = {"NOT_REQUIRED", "REQUIRED", "COMPLETED"}
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
TRACE_BASIS = {
    "DIRECT_OBSERVATION",
    "DETAILED_FIRST_PERSON_ACCOUNT",
    "EVIDENCE_BACKED_ARTIFACT_RECONSTRUCTION",
    "EVENT_LOG_RECONSTRUCTION",
    "FRAGMENTARY_EVIDENCE",
}
SHAPING_FRAME_STATUS = {"PROVISIONAL", "ACCEPTED"}
REQUIREMENT_ORIGIN = {"FROM_X", "FROM_Y", "FROM_GAP", "FROM_BOUNDARY"}
CONCEPT_SELECTION_STATUS = {"CANDIDATE", "SELECTED", "REJECTED"}
ROTATION_STATUS = {"NOT_RUN", "RUN"}
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
DISCOVERY_PATH = {"TARGET_MARKET", "ADVANCED_ANALOG", "ATTRIBUTE_SPECIFIC"}
SEARCH_TYPE = {"GENERAL", "REFUTATION", "WEB_NEED_SOLUTION", "ENABLER_SCAN"}
EVIDENTIARY_ROLE = {"DISCOVERY_SIGNAL", "CONTEXT", "EVIDENCE_SEARCH"}
TRANSFERABILITY = {"SUPPORTED", "PLAUSIBLE", "LEAD_USER_BOUND", "UNKNOWN"}
BRANCH_INDEPENDENCE = {"NOT_ASSESSED", "SUFFICIENT", "INSUFFICIENT", "NOT_APPLICABLE"}
REJECTION_LAYER = {"NEED", "PRINCIPLE", "REQUIREMENT", "MECHANISM", "IMPLEMENTATION_PART"}
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
    "frame_id": re.compile(r"^SF\d+$"),
    "requirement_id": re.compile(r"^R\d+$"),
    "concept_id": re.compile(r"^M\d+$"),
    "action_id": re.compile(r"^A\d+$"),
    "hypothesis_id": re.compile(r"^H\d+$"),
    "observability_id": re.compile(r"^O\d+$"),
    "analysis_run_id": re.compile(r"^AR\d+$"),
    "candidate_id": re.compile(r"^C\d+$"),
    "search_id": re.compile(r"^Q\d+$"),
    "pyramid_id": re.compile(r"^PY\d+$"),
    "change_id": re.compile(r"^CH\d+$"),
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
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{owner} has invalid {label} reference: {value!r}")
            continue
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


def as_list(value: Any) -> list[Any]:
    """Keep schema errors reportable instead of crashing on a non-list value."""
    return value if isinstance(value, list) else []


def as_string_list(value: Any) -> list[str]:
    return [item for item in as_list(value) if isinstance(item, str)]


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
    candidates = load(root, "candidates.json", errors)
    sources = load(root, "sources.json", errors)
    evidence = load(root, "evidence.json", errors)
    episodes = load(root, "lu_episodes.json", errors)
    lineage = load(root, "lineage.json", errors)
    findings = load(root, "findings.json", errors)
    needs = load(root, "needs.json", errors)
    principles = load(root, "principles.json", errors)
    shaping_frames = load(root, "shaping_frame.json", errors)
    criteria = load(root, "fit_criteria.json", errors)
    concepts = load(root, "concepts.json", errors)
    coverage = load(root, "coverage.json", errors)
    sufficiency = load(root, "sufficiency.json", errors)
    freeze = load(root, "freeze.json", errors)
    decision_outcome = load(root, "decision_outcome.json", errors)
    hypotheses = load(root, "hypotheses.json", errors)
    observability = load(root, "observability.json", errors)
    analysis_runs = load(root, "analysis_runs.json", errors)
    search_log = load(root, "search_log.json", errors)
    change_log = load(root, "change_log.json", errors)

    list_files = [
        ("trends.json", trends),
        ("candidates.json", candidates),
        ("sources.json", sources),
        ("evidence.json", evidence),
        ("lu_episodes.json", episodes),
        ("lineage.json", lineage),
        ("findings.json", findings),
        ("needs.json", needs),
        ("principles.json", principles),
        ("shaping_frame.json", shaping_frames),
        ("fit_criteria.json", criteria),
        ("concepts.json", concepts),
        ("hypotheses.json", hypotheses),
        ("observability.json", observability),
        ("analysis_runs.json", analysis_runs),
        ("search_log.json", search_log),
        ("change_log.json", change_log),
    ]
    for name, value in list_files:
        if not isinstance(value, list):
            errors.append(f"{name} must contain a JSON array")

    trends = trends if isinstance(trends, list) else []
    candidates = candidates if isinstance(candidates, list) else []
    sources = sources if isinstance(sources, list) else []
    evidence = evidence if isinstance(evidence, list) else []
    episodes = episodes if isinstance(episodes, list) else []
    lineage = lineage if isinstance(lineage, list) else []
    findings = findings if isinstance(findings, list) else []
    needs = needs if isinstance(needs, list) else []
    principles = principles if isinstance(principles, list) else []
    shaping_frames = shaping_frames if isinstance(shaping_frames, list) else []
    criteria = criteria if isinstance(criteria, list) else []
    concepts = concepts if isinstance(concepts, list) else []
    hypotheses = hypotheses if isinstance(hypotheses, list) else []
    observability = observability if isinstance(observability, list) else []
    analysis_runs = analysis_runs if isinstance(analysis_runs, list) else []
    search_log = search_log if isinstance(search_log, list) else []
    change_log = change_log if isinstance(change_log, list) else []

    mode = manifest.get("mode") if isinstance(manifest, dict) else None
    fixture_type = manifest.get("fixture_type") if isinstance(manifest, dict) else None
    is_synthetic_fixture = fixture_type == "SYNTHETIC_REFERENCE"

    trend_ids = ids(trends, "trend_id", errors)
    candidate_ids = ids(candidates, "candidate_id", errors)
    source_ids = ids(sources, "source_id", errors)
    evidence_ids = ids(evidence, "evidence_id", errors)
    lu_ids = ids(episodes, "lu_id", errors)
    lineage_ids = ids(lineage, "lineage_id", errors)
    finding_ids = ids(findings, "finding_id", errors)
    need_ids = ids(needs, "need_id", errors)
    principle_ids = ids(principles, "principle_id", errors)
    frame_ids = ids(shaping_frames, "frame_id", errors)
    requirement_ids = ids(criteria, "requirement_id", errors)
    concept_ids = ids(concepts, "concept_id", errors)
    hypothesis_ids = ids(hypotheses, "hypothesis_id", errors)
    observability_ids = ids(observability, "observability_id", errors)
    analysis_run_ids = ids(analysis_runs, "analysis_run_id", errors)
    trend_by_id = {
        row.get("trend_id"): row
        for row in trends
        if isinstance(row, dict) and isinstance(row.get("trend_id"), str)
    }

    for row in candidates:
        if not isinstance(row, dict):
            continue
        cid = row.get("candidate_id", "<unknown>")
        for field in ["candidate_ref", "discovery_basis", "disposition"]:
            require_nonempty_string(row, field, cid, errors)
        discovery_path = row.get("discovery_path")
        if discovery_path is not None and discovery_path not in DISCOVERY_PATH:
            errors.append(f"{cid} has invalid discovery_path {discovery_path!r}")
        if discovery_path == "ATTRIBUTE_SPECIFIC":
            require_nonempty_string(row, "target_attribute", cid, errors)
        for field in ["technical_expertise", "community_resources"]:
            if field not in row:
                continue
            value = row.get(field)
            if isinstance(value, str):
                if not value.strip():
                    errors.append(f"{cid} {field} must not be empty when present")
            elif isinstance(value, list):
                require_string_list(row, field, cid, errors, nonempty=True)
            else:
                errors.append(f"{cid} {field} must be a non-empty string or string list")

    search_ids: set[str] = set()
    pyramid_ids: set[str] = set()
    search_refs_to_check: list[tuple[Any, str, str]] = []
    for index, row in enumerate(search_log):
        owner = f"search_log.json row {index}"
        if not isinstance(row, dict):
            continue
        search_id = row.get("search_id")
        pyramid_id = row.get("pyramid_id")
        if bool(search_id) == bool(pyramid_id):
            errors.append(f"{owner} requires exactly one of search_id or pyramid_id")
            continue
        if search_id:
            if not isinstance(search_id, str) or not ID_PATTERNS["search_id"].match(search_id):
                errors.append(f"{owner} has invalid search_id {search_id!r}")
            elif search_id in search_ids:
                errors.append(f"duplicate search_id: {search_id}")
            else:
                search_ids.add(search_id)
            owner = str(search_id)
            for field in ["branch", "query_or_route", "next_branch"]:
                require_nonempty_string(row, field, owner, errors)
            search_type = row.get("search_type")
            if search_type is not None and search_type not in SEARCH_TYPE:
                errors.append(f"{owner} has invalid search_type {search_type!r}")
            evidentiary_role = row.get("evidentiary_role")
            if evidentiary_role is not None and evidentiary_role not in EVIDENTIARY_ROLE:
                errors.append(f"{owner} has invalid evidentiary_role {evidentiary_role!r}")
            if search_type == "WEB_NEED_SOLUTION" and evidentiary_role != "DISCOVERY_SIGNAL":
                errors.append(f"{owner} WEB_NEED_SOLUTION requires evidentiary_role DISCOVERY_SIGNAL")
            if search_type == "ENABLER_SCAN" and evidentiary_role != "CONTEXT":
                errors.append(f"{owner} ENABLER_SCAN requires evidentiary_role CONTEXT")
            for field in ["semantic_expansions", "interest_signals"]:
                if field in row:
                    require_string_list(row, field, owner, errors)
            require_string_list(row, "result_refs", owner, errors)
            search_refs_to_check.append((row.get("result_refs", []), "result", owner))
            continue

        if not isinstance(pyramid_id, str) or not ID_PATTERNS["pyramid_id"].match(pyramid_id):
            errors.append(f"{owner} has invalid pyramid_id {pyramid_id!r}")
        elif pyramid_id in pyramid_ids:
            errors.append(f"duplicate pyramid_id: {pyramid_id}")
        else:
            pyramid_ids.add(pyramid_id)
        owner = str(pyramid_id)
        for field in [
            "target_attribute",
            "starting_node",
            "network_visibility",
            "termination_criterion",
        ]:
            require_nonempty_string(row, field, owner, errors)
        termination_reason = row.get("termination_reason")
        if termination_reason is not None and (
            not isinstance(termination_reason, str) or not termination_reason.strip()
        ):
            errors.append(f"{owner} termination_reason must be null or a non-empty string")
        hops = row.get("hops")
        if not isinstance(hops, list):
            errors.append(f"{owner} hops must be a list")
            hops = []
        for hop_index, hop in enumerate(hops):
            hop_owner = f"{owner} hop {hop_index}"
            if not isinstance(hop, dict):
                errors.append(f"{hop_owner} must be an object")
                continue
            for field in [
                "from_node",
                "referral_rationale",
                "next_node",
                "advancement_rationale",
            ]:
                require_nonempty_string(hop, field, hop_owner, errors)
            require_string_list(hop, "supporting_refs", hop_owner, errors)
            search_refs_to_check.append((hop.get("supporting_refs", []), "supporting", hop_owner))

    change_ids: set[str] = set()
    for index, row in enumerate(change_log):
        owner = f"change_log.json row {index}"
        if not isinstance(row, dict):
            continue
        change_id = row.get("change_id")
        if not isinstance(change_id, str) or not ID_PATTERNS["change_id"].match(change_id):
            errors.append(f"{owner} has invalid change_id {change_id!r}")
        elif change_id in change_ids:
            errors.append(f"duplicate change_id: {change_id}")
        else:
            change_ids.add(change_id)
        changed_at = row.get("changed_at")
        if not isinstance(changed_at, str) or not changed_at.strip():
            errors.append(f"{owner} requires non-empty changed_at")
        else:
            try:
                datetime.fromisoformat(changed_at.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{owner} changed_at must be ISO-8601")
        if row.get("phase") not in PHASES:
            errors.append(f"{owner} has invalid phase {row.get('phase')!r}")
        for field in ["change", "reason"]:
            require_nonempty_string(row, field, owner, errors)

    source_by_id = {
        row.get("source_id"): row
        for row in sources
        if isinstance(row, dict) and isinstance(row.get("source_id"), str)
    }
    evidence_by_id = {
        row.get("evidence_id"): row
        for row in evidence
        if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
    }
    episode_by_id = {
        row.get("lu_id"): row
        for row in episodes
        if isinstance(row, dict) and isinstance(row.get("lu_id"), str)
    }
    finding_by_id = {
        row.get("finding_id"): row
        for row in findings
        if isinstance(row, dict) and isinstance(row.get("finding_id"), str)
    }
    shaping_frame_by_id = {
        row.get("frame_id"): row
        for row in shaping_frames
        if isinstance(row, dict) and isinstance(row.get("frame_id"), str)
    }
    criterion_by_id = {
        row.get("requirement_id"): row
        for row in criteria
        if isinstance(row, dict) and isinstance(row.get("requirement_id"), str)
    }

    for source in sources:
        if not isinstance(source, dict):
            continue
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
        if source.get("outward_citation_allowed") is True:
            if safe_outward_url(source.get("url")) is None:
                errors.append(f"{sid} outward citation requires a safe HTTP(S) URL")
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
        if isinstance(row, dict) and isinstance(row.get("analysis_run_id"), str)
    }

    for row in evidence:
        if not isinstance(row, dict):
            continue
        eid = row.get("evidence_id", "<unknown>")
        sid = row.get("source_id")
        if not isinstance(sid, str) or sid not in source_ids:
            errors.append(f"{eid} references missing source_id: {sid}")
        elif source_by_id[sid].get("coverage") not in {"FULL", "PARTIAL"}:
            errors.append(
                f"{eid} cannot cite source {sid} with coverage "
                f"{source_by_id[sid].get('coverage')!r}"
            )
        require_nonempty_string(row, "evidence_type", eid, errors)
        basis = row.get("evidence_basis")
        if basis not in EVIDENCE_BASIS:
            errors.append(f"{eid} has invalid evidence_basis {basis!r}")
        if basis == "SYNTHETIC_OR_SIMULATED" and not is_synthetic_fixture:
            errors.append(
                f"{eid} synthetic or simulated material cannot be persisted as human evidence"
            )
        analysis_run_id = row.get("analysis_run_id")
        if analysis_run_id not in (None, "") and (
            not isinstance(analysis_run_id, str)
            or analysis_run_id not in analysis_run_ids
        ):
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
        if tid not in (None, "") and (
            not isinstance(tid, str) or tid not in trend_ids
        ):
            errors.append(f"{eid} references missing trend_id: {tid}")
        luid = row.get("lu_id")
        if luid not in (None, "") and (
            not isinstance(luid, str) or luid not in lu_ids
        ):
            errors.append(f"{eid} references missing lu_id: {luid}")
        if isinstance(public_summary, str):
            for private_episode in episodes:
                if (
                    not isinstance(private_episode, dict)
                    or private_episode.get("identity_surface_allowed") is True
                ):
                    continue
                private_identity = private_episode.get("user_entity")
                if (
                    isinstance(private_identity, str)
                    and contains_private_identity(public_summary, private_identity)
                ):
                    errors.append(
                        f"{eid} public_summary exposes private user_entity for "
                        f"{private_episode.get('lu_id', '<unknown>')}"
                    )

    for row in hypotheses:
        if not isinstance(row, dict):
            continue
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

    if isinstance(decision, dict) and isinstance(decision.get("starting_hypotheses"), list):
        ledger_claims = {
            " ".join(row.get("claim", "").split()).casefold()
            for row in hypotheses
            if isinstance(row, dict) and isinstance(row.get("claim"), str)
        }
        for index, claim in enumerate(decision.get("starting_hypotheses", [])):
            if not isinstance(claim, str) or not claim.strip():
                continue
            if " ".join(claim.split()).casefold() not in ledger_claims:
                errors.append(
                    f"decision.json starting_hypotheses[{index}] has no matching hypotheses.json claim"
                )

    for row in observability:
        if not isinstance(row, dict):
            continue
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
        if not isinstance(row, dict):
            continue
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
        if not isinstance(row, dict):
            continue
        tid = row.get("trend_id", "<unknown>")
        for field in ["statement", "direction", "importance"]:
            require_nonempty_string(row, field, tid, errors)
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", tid, errors)
        status = row.get("status")
        if status is not None and status not in EPISTEMIC:
            errors.append(f"{tid} has invalid status {status!r}")
        if status in {"VERIFIED", "INFERRED"} and not row.get("evidence_refs"):
            errors.append(f"{tid} {status} requires evidence_refs")
        indicators = require_string_list(
            row, "observable_indicators", tid, errors,
            nonempty=status in {"VERIFIED", "INFERRED"},
        )
        if status in {"VERIFIED", "INFERRED"} and not indicators:
            errors.append(f"{tid} {status} requires observable_indicators")

    trace_ref_ids: set[str] = set()

    for row in episodes:
        if not isinstance(row, dict):
            continue
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
            and contains_private_identity(public_label, internal_identity)
        ):
            errors.append(f"{luid} public_label exposes private user_entity")
        if row.get("identity_surface_allowed") is True:
            require_nonempty_string(row, "public_label", luid, errors)
            require_nonempty_string(row, "identity_surface_rationale", luid, errors)
        if row.get("status") not in LU_STATUS:
            errors.append(f"{luid} has invalid status {row.get('status')!r}")
        if not isinstance(row.get("trend_id"), str) or row.get("trend_id") not in trend_ids:
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
            qualification_refs = as_string_list(row.get("lu1_evidence")) + as_string_list(
                row.get("lu2_evidence")
            )
            for ref in qualification_refs:
                evidence_row = evidence_by_id.get(ref, {})
                if (
                    evidence_row.get("evidence_basis") == "SYNTHETIC_OR_SIMULATED"
                    and not is_synthetic_fixture
                ):
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
                trace_basis = trace.get("trace_basis")
                if trace_basis not in TRACE_BASIS:
                    errors.append(f"{luid} has invalid trace_basis {trace_basis!r}")
                if trace_status == "SUFFICIENT" and trace_basis == "FRAGMENTARY_EVIDENCE":
                    errors.append(f"{luid} trace cannot be SUFFICIENT from FRAGMENTARY_EVIDENCE")

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
                step_ids: set[str] = set()
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
                    step_id = step.get("step_id")
                    if isinstance(step_id, str) and step_id.strip():
                        if step_id in step_ids:
                            errors.append(f"{luid} trace has duplicate step_id {step_id}")
                        step_ids.add(step_id)
                        trace_ref_ids.add(f"{luid}:{step_id}")
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
                fit_point_ids: set[str] = set()
                for index, point in enumerate(fit_points):
                    if not isinstance(point, dict):
                        errors.append(f"{luid} trace fit point {index} must be an object")
                        continue
                    require_nonempty_string(point, "fit_point_id", f"{luid} trace fit point {index}", errors)
                    fit_point_id = point.get("fit_point_id")
                    if isinstance(fit_point_id, str) and fit_point_id.strip():
                        if not re.match(r"^FP\d+$", fit_point_id):
                            errors.append(f"{luid} trace fit point {index} has invalid fit_point_id {fit_point_id!r}")
                        if fit_point_id in fit_point_ids:
                            errors.append(f"{luid} trace has duplicate fit_point_id {fit_point_id}")
                        fit_point_ids.add(fit_point_id)
                        trace_ref_ids.add(f"{luid}:{fit_point_id}")
                    step_ref = point.get("step_ref")
                    if not isinstance(step_ref, str) or step_ref not in step_ids:
                        errors.append(f"{luid} trace fit point {index} references missing step_ref: {step_ref}")
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
    member_independence: dict[str, set[str]] = {}
    for row in lineage:
        if not isinstance(row, dict):
            continue
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
        elif isinstance(row.get("member_refs"), list) and independence in INDEPENDENCE:
            for member_ref in row["member_refs"]:
                if isinstance(member_ref, str):
                    member_independence.setdefault(member_ref, set()).add(independence)
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
        if independence == "DERIVATIVE" and not row.get("evidence_refs"):
            errors.append(f"{lid} is DERIVATIVE without direct lineage evidence refs")
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

    for member_ref, assessments in sorted(member_independence.items()):
        if "DERIVATIVE" in assessments and "INDEPENDENT" in assessments:
            errors.append(
                f"lineage member {member_ref} cannot be counted as both DERIVATIVE and INDEPENDENT"
            )

    for row in findings:
        if not isinstance(row, dict):
            continue
        fid = row.get("finding_id", "<unknown>")
        require_nonempty_string(row, "claim", fid, errors)
        require_nonempty_string(row, "confidence_rationale", fid, errors)
        label = row.get("epistemic_label")
        if label not in EPISTEMIC:
            errors.append(f"{fid} has invalid epistemic_label {label!r}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", fid, errors)
        refs_exist(row.get("lu_refs", []), lu_ids, "LU", fid, errors)
        refs_exist(row.get("trace_refs", []), trace_ref_ids, "trace ref", fid, errors)
        refs_exist(
            row.get("contradictions", []),
            finding_ids,
            "contradictory finding",
            fid,
            errors,
        )
        if label in {"VERIFIED", "INFERRED"} and not (
            row.get("evidence_refs") or row.get("lu_refs") or row.get("trace_refs")
        ):
            errors.append(f"{fid} {label} requires evidence, LU, or trace refs")

    for row in needs:
        if not isinstance(row, dict):
            continue
        nid = row.get("need_id", "<unknown>")
        require_nonempty_string(row, "statement", nid, errors)
        refs_exist(row.get("finding_ids", []), finding_ids, "finding", nid, errors)
        refs_exist(row.get("relevant_trends", []), trend_ids, "trend", nid, errors)
        refs_exist(row.get("trace_refs", []), trace_ref_ids, "trace ref", nid, errors)
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
            "transferability_supported",
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
                "transferability_supported",
                "no_blocking_contradiction",
            ]:
                if gate_checks.get(field) is not True:
                    errors.append(f"{nid} PASS requires concept_gate_checks.{field}=true")
            supporting_lus = {
                lu_ref
                for finding_ref in as_string_list(row.get("finding_ids"))
                for lu_ref in as_string_list(
                    finding_by_id.get(finding_ref, {}).get("lu_refs")
                )
            }
            qualified_lus = {
                episode.get("lu_id")
                for episode in episodes
                if isinstance(episode, dict) and episode.get("status") == "QUALIFIED"
            }
            if not supporting_lus.intersection(qualified_lus):
                errors.append(f"{nid} PASS requires a qualified LU through its findings")
            relevant_trends = set(as_string_list(row.get("relevant_trends")))
            credible_trends = {
                trend.get("trend_id")
                for trend in trends
                if isinstance(trend, dict)
                and trend.get("trend_id") in relevant_trends
                and trend.get("status") in {"VERIFIED", "INFERRED"}
                and bool(trend.get("evidence_refs"))
            }
            if not credible_trends:
                errors.append(f"{nid} PASS requires an evidence-backed VERIFIED or INFERRED relevant trend")
            aligned_support = False
            finding_refs = as_string_list(row.get("finding_ids"))
            for finding_ref in finding_refs:
                finding = finding_by_id.get(finding_ref, {})
                if finding.get("epistemic_label") not in {"VERIFIED", "INFERRED"}:
                    continue
                finding_has_atomic_support = bool(finding.get("evidence_refs"))
                for lu_ref in as_string_list(finding.get("lu_refs")):
                    episode = episode_by_id.get(lu_ref, {})
                    if episode.get("status") != "QUALIFIED":
                        continue
                    if episode.get("trend_id") not in credible_trends:
                        continue
                    if finding_has_atomic_support or episode.get("lu1_evidence") or episode.get("lu2_evidence"):
                        aligned_support = True
            if not aligned_support:
                errors.append(
                    f"{nid} PASS requires a supporting finding with an atomic evidence path to a qualified LU on a credible relevant trend"
                )
            transferability = row.get("transferability_assessment")
            if not isinstance(transferability, dict):
                errors.append(f"{nid} PASS requires transferability_assessment")
            else:
                transfer_status = transferability.get("status")
                if transfer_status not in TRANSFERABILITY:
                    errors.append(f"{nid} has invalid transferability status {transfer_status!r}")
                if transfer_status not in {"SUPPORTED", "PLAUSIBLE"}:
                    errors.append(f"{nid} PASS requires transferability SUPPORTED or PLAUSIBLE")
                require_nonempty_string(transferability, "rationale", f"{nid} transferability_assessment", errors)
                require_string_list(
                    transferability,
                    "target_market_differences",
                    f"{nid} transferability_assessment",
                    errors,
                    nonempty=True,
                )
                transferability_refs = require_string_list(
                    transferability,
                    "evidence_refs",
                    f"{nid} transferability_assessment",
                    errors,
                    nonempty=True,
                )
                refs_exist(
                    transferability_refs,
                    evidence_ids | finding_ids,
                    "transferability evidence",
                    f"{nid} transferability_assessment",
                    errors,
                )

    for row in principles:
        if not isinstance(row, dict):
            continue
        spid = row.get("principle_id", "<unknown>")
        require_nonempty_string(row, "principle", spid, errors)
        nid = row.get("need_id")
        if not isinstance(nid, str) or nid not in need_ids:
            errors.append(f"{spid} references missing need_id: {nid}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", spid, errors)
        status = row.get("status")
        if status not in EPISTEMIC:
            errors.append(f"{spid} has invalid status {status!r}")
        if status in {"VERIFIED", "INFERRED"} and not row.get("evidence_refs"):
            errors.append(f"{spid} {status} requires evidence_refs")

    for row in shaping_frames:
        if not isinstance(row, dict):
            continue
        sfid = row.get("frame_id", "<unknown>")
        nid = row.get("need_id")
        if not isinstance(nid, str) or nid not in need_ids:
            errors.append(f"{sfid} references missing need_id: {nid}")
        x = row.get("x")
        if not isinstance(x, dict):
            errors.append(f"{sfid} x must be an object")
            x = {}
        for field in ["trigger_or_context", "current_approach", "current_result"]:
            require_nonempty_string(x, field, f"{sfid} x", errors)
        require_string_list(x, "breakdowns", f"{sfid} x", errors, nonempty=True)
        f_value = row.get("f")
        if not isinstance(f_value, dict) or f_value.get("status") != "UNSPECIFIED":
            errors.append(f"{sfid} f.status must be UNSPECIFIED")
        y = row.get("y")
        if not isinstance(y, dict):
            errors.append(f"{sfid} y must be an object")
            y = {}
        require_nonempty_string(y, "desired_outcome", f"{sfid} y", errors)
        require_nonempty_string(row, "gap", sfid, errors)
        require_string_list(row, "boundaries", sfid, errors)
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", sfid, errors)
        status = row.get("status")
        if status not in SHAPING_FRAME_STATUS:
            errors.append(f"{sfid} has invalid shaping frame status {status!r}")
        require_bool(row, "accepted_by_human", sfid, errors)
        if status == "ACCEPTED":
            if row.get("accepted_by_human") is not True:
                errors.append(f"{sfid} ACCEPTED requires accepted_by_human=true")
            require_nonempty_string(row, "acceptance_note", sfid, errors)
            if not row.get("evidence_refs"):
                errors.append(f"{sfid} ACCEPTED requires evidence_refs")
        elif row.get("accepted_by_human") is True:
            errors.append(f"{sfid} PROVISIONAL cannot have accepted_by_human=true")

    fit_checks = [
        "traceability",
        "implementation_independence",
        "solution_plurality",
        "causal_relevance",
        "altitude_check",
        "information_gain",
    ]
    for row in criteria:
        if not isinstance(row, dict):
            continue
        rid = row.get("requirement_id", "<unknown>")
        require_nonempty_string(row, "requirement", rid, errors)
        nid = row.get("need_id")
        if not isinstance(nid, str) or nid not in need_ids:
            errors.append(f"{rid} references missing need_id: {nid}")
        frame_ref = row.get("frame_ref")
        if not isinstance(frame_ref, str) or frame_ref not in frame_ids:
            errors.append(f"{rid} references missing frame_ref: {frame_ref}")
        else:
            frame = shaping_frame_by_id.get(frame_ref, {})
            if frame.get("need_id") != nid:
                errors.append(f"{rid} frame_ref {frame_ref} belongs to need {frame.get('need_id')}")
        origin = row.get("origin")
        if origin not in REQUIREMENT_ORIGIN:
            errors.append(f"{rid} has invalid origin {origin!r}")
        refs_exist(row.get("evidence_refs", []), evidence_ids, "evidence", rid, errors)
        status = row.get("status")
        if status not in FIT_STATUS:
            errors.append(f"{rid} has invalid status {status!r}")
        for field in fit_checks:
            require_bool(row, field, rid, errors)
        if status == "PASS":
            if not row.get("evidence_refs"):
                errors.append(f"{rid} PASS requires evidence_refs")
            frame = shaping_frame_by_id.get(row.get("frame_ref"), {})
            if frame.get("status") != "ACCEPTED" or frame.get("accepted_by_human") is not True:
                errors.append(f"{rid} PASS requires an accepted human-reviewed shaping frame")
            for field in fit_checks:
                if row.get(field) is not True:
                    errors.append(f"{rid} PASS requires {field}=true")

    selected_by_need: dict[str, int] = {}
    for row in concepts:
        if not isinstance(row, dict):
            continue
        mid = row.get("concept_id", "<unknown>")
        require_nonempty_string(row, "mechanism", mid, errors)
        nid = row.get("need_id")
        if not isinstance(nid, str) or nid not in need_ids:
            errors.append(f"{mid} references missing need_id: {nid}")
        concept_requirement_ids = require_string_list(
            row, "requirement_ids", mid, errors
        )
        refs_exist(concept_requirement_ids, requirement_ids, "requirement", mid, errors)
        if not concept_requirement_ids:
            errors.append(f"{mid} requires requirement_ids")
        for ref in concept_requirement_ids:
            if criterion_by_id.get(ref, {}).get("status") != "PASS":
                errors.append(f"{mid} references non-PASS requirement {ref}")
            if criterion_by_id.get(ref, {}).get("need_id") != nid:
                errors.append(f"{mid} requirement {ref} belongs to another need")

        pass_requirements = {
            ref
            for ref, criterion in criterion_by_id.items()
            if criterion.get("need_id") == nid and criterion.get("status") == "PASS"
        }
        requirement_fit = row.get("requirement_fit")
        if not isinstance(requirement_fit, dict):
            errors.append(f"{mid} requirement_fit must be an object")
            requirement_fit = {}
        if set(requirement_fit) != pass_requirements:
            errors.append(f"{mid} requirement_fit must cover every frozen PASS requirement for its need")
        for ref, value in requirement_fit.items():
            if ref not in pass_requirements:
                errors.append(f"{mid} requirement_fit references non-PASS or foreign requirement {ref}")
            if not isinstance(value, bool):
                errors.append(f"{mid} requirement_fit[{ref}] must be boolean")
        passed_refs = {ref for ref, value in requirement_fit.items() if value is True}
        if set(concept_requirement_ids) != passed_refs:
            errors.append(f"{mid} requirement_ids must match true requirement_fit entries")

        selection_status = row.get("selection_status")
        if selection_status not in CONCEPT_SELECTION_STATUS:
            errors.append(f"{mid} has invalid selection_status {selection_status!r}")
        require_bool(row, "selected_by_human", mid, errors)
        rotation_status = row.get("rotation_status")
        if rotation_status not in ROTATION_STATUS:
            errors.append(f"{mid} has invalid rotation_status {rotation_status!r}")
        parts = row.get("parts")
        if not isinstance(parts, list):
            errors.append(f"{mid} parts must be a list")
            parts = []

        served_by_parts: set[str] = set()
        part_ids: set[str] = set()
        for index, part in enumerate(parts):
            if not isinstance(part, dict):
                errors.append(f"{mid} part {index} must be an object")
                continue
            require_nonempty_string(part, "part_id", f"{mid} part {index}", errors)
            require_nonempty_string(part, "mechanism", f"{mid} part {index}", errors)
            part_id = part.get("part_id")
            if isinstance(part_id, str) and part_id.strip():
                if not re.match(rf"^{re.escape(str(mid))}P\d+$", part_id):
                    errors.append(f"{mid} part {index} has invalid part_id {part_id!r}")
                if part_id in part_ids:
                    errors.append(f"{mid} has duplicate part_id {part_id}")
                part_ids.add(part_id)
            part_owner = f"{mid} part {index}"
            part_refs = require_string_list(
                part, "requirement_ids", part_owner, errors
            )
            refs_exist(part_refs, requirement_ids, "requirement", part_owner, errors)
            if not part_refs:
                errors.append(f"{mid} part {index} must serve at least one requirement")
            for ref in part_refs:
                if ref not in pass_requirements:
                    errors.append(f"{mid} part {index} references non-PASS or foreign requirement {ref}")
                served_by_parts.add(ref)

        if selection_status == "SELECTED":
            selected_by_need[nid] = selected_by_need.get(nid, 0) + 1
            if row.get("selected_by_human") is not True:
                errors.append(f"{mid} SELECTED requires selected_by_human=true")
            require_nonempty_string(row, "selection_note", mid, errors)
            if rotation_status != "RUN":
                errors.append(f"{mid} SELECTED requires rotation_status RUN")
            if not parts:
                errors.append(f"{mid} SELECTED requires rotated parts")
            missing_support = pass_requirements - served_by_parts
            if missing_support:
                errors.append(f"{mid} SELECTED rotated fit leaves requirements unsupported: {sorted(missing_support)}")
        else:
            if row.get("selected_by_human") is True:
                errors.append(f"{mid} {selection_status} cannot have selected_by_human=true")
            if rotation_status == "RUN":
                errors.append(f"{mid} rotation_status RUN requires selection_status SELECTED")

        rejection = row.get("rejection_record")
        if rejection is not None:
            if not isinstance(rejection, dict):
                errors.append(f"{mid} rejection_record must be an object")
            else:
                layer = rejection.get("layer")
                if layer not in REJECTION_LAYER:
                    errors.append(f"{mid} has invalid rejection layer {layer!r}")
                require_nonempty_string(rejection, "rationale", f"{mid} rejection_record", errors)
                require_string_list(rejection, "evidence_refs", f"{mid} rejection_record", errors)
        for field in ["assumptions", "risks", "evidence_needed_next"]:
            require_string_list(row, field, mid, errors)

    for nid, selected_count in selected_by_need.items():
        if selected_count > 1:
            errors.append(f"{nid} has more than one SELECTED concept")

    all_structured_refs = (
        trend_ids
        | source_ids
        | evidence_ids
        | lu_ids
        | lineage_ids
        | finding_ids
        | need_ids
        | principle_ids
        | frame_ids
        | requirement_ids
        | concept_ids
        | hypothesis_ids
        | observability_ids
        | analysis_run_ids
        | candidate_ids
        | search_ids
        | pyramid_ids
        | change_ids
    )

    for values, label, owner in search_refs_to_check:
        refs_exist(values, all_structured_refs, label, owner, errors)

    if not isinstance(sufficiency, dict):
        errors.append("sufficiency.json must contain a JSON object")
    else:
        if sufficiency.get("status") not in SUFFICIENCY:
            errors.append(f"sufficiency.json has invalid status {sufficiency.get('status')!r}")
        repair_status = sufficiency.get("repair_status")
        if repair_status not in SUFFICIENCY_REPAIR:
            errors.append(f"sufficiency.json has invalid repair_status {repair_status!r}")
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
            if repair_status != "NOT_REQUIRED":
                errors.append("sufficiency status SUFFICIENT requires repair_status NOT_REQUIRED")
            for field in SUFFICIENCY_DIMENSIONS:
                dimension = dimensions.get(field)
                if not isinstance(dimension, dict) or dimension.get("status") != "SUFFICIENT":
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
            if repair_status not in {"REQUIRED", "COMPLETED"}:
                errors.append(
                    "sufficiency status INSUFFICIENT requires repair_status REQUIRED or COMPLETED"
                )
            if not any(
                isinstance(dimensions.get(field), dict)
                and dimensions[field].get("status") == "INSUFFICIENT"
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
        if sufficiency.get("status") == "NOT_ASSESSED" and repair_status != "NOT_REQUIRED":
            errors.append("sufficiency status NOT_ASSESSED requires repair_status NOT_REQUIRED")
        pyramid_dimension = dimensions.get("pyramid_coverage", {})
        if not isinstance(pyramid_dimension, dict):
            pyramid_dimension = {}
        if pyramid_dimension.get("status") == "SUFFICIENT":
            supporting_refs = as_string_list(
                pyramid_dimension.get("supporting_refs")
            )
            has_pyramid_ref = bool(set(supporting_refs).intersection(pyramid_ids))
            no_pyramid_reason = pyramid_dimension.get("not_applicable_rationale")
            if not has_pyramid_ref and not (
                isinstance(no_pyramid_reason, str) and no_pyramid_reason.strip()
            ):
                errors.append(
                    "sufficiency pyramid_coverage SUFFICIENT requires a PY## supporting ref or not_applicable_rationale"
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
            qualified_count = sum(
                1
                for row in episodes
                if isinstance(row, dict) and row.get("status") == "QUALIFIED"
            )
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
                if isinstance(row, dict)
                and isinstance(row.get("analysis_run_id"), str)
                and row.get("analysis_run_id")
            }
            for arid in sorted(referenced_analysis_runs):
                validation = analysis_run_by_id.get(arid, {}).get("sampled_validation", {})
                if not isinstance(validation, dict):
                    validation = {}
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
            if isinstance(row, dict) and row.get("concept_gate_status") == "PASS"
        }
        for row in criteria:
            if not isinstance(row, dict):
                continue
            if row.get("need_id") not in passing:
                errors.append(
                    f"{row.get('requirement_id')} exists for need that did not PASS concept gate"
                )
        for row in concepts:
            if not isinstance(row, dict):
                continue
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
        branch_independence = coverage.get("branch_independence")
        if branch_independence is not None:
            if not isinstance(branch_independence, dict):
                errors.append("coverage.json branch_independence must be an object")
            else:
                branch_status = branch_independence.get("status")
                if branch_status not in BRANCH_INDEPENDENCE:
                    errors.append(
                        f"coverage.json branch_independence has invalid status {branch_status!r}"
                    )
                for field in ["branches", "correlated_or_shared_visibility", "next_actions"]:
                    require_string_list(
                        branch_independence,
                        field,
                        "coverage.json branch_independence",
                        errors,
                    )
                require_nonempty_string(
                    branch_independence,
                    "rationale",
                    "coverage.json branch_independence",
                    errors,
                )
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
        if fixture_type not in FIXTURE_TYPE:
            errors.append(f"manifest has invalid fixture_type {fixture_type!r}")
        if manifest.get("interpretation_completion") not in INTERPRETATION_COMPLETION:
            errors.append(
                "manifest has invalid interpretation_completion "
                f"{manifest.get('interpretation_completion')!r}"
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
            if mode in {"STANDARD", "FULL"} and manifest.get("interpretation_completion") != "COMPLETED":
                errors.append("complete STANDARD/FULL study requires interpretation_completion COMPLETED")
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
        if is_synthetic_fixture:
            if level != "DESK_RESEARCH":
                errors.append("SYNTHETIC_REFERENCE requires study_execution_level DESK_RESEARCH")
            nonsynthetic = [
                row.get("evidence_id", "<unknown>")
                for row in evidence
                if isinstance(row, dict)
                and row.get("evidence_basis") != "SYNTHETIC_OR_SIMULATED"
            ]
            if nonsynthetic:
                errors.append(
                    "SYNTHETIC_REFERENCE requires every evidence row to use SYNTHETIC_OR_SIMULATED: "
                    + ", ".join(nonsynthetic)
                )
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

        interpretation_completion = manifest.get("interpretation_completion")
        if (findings or needs or principles) and interpretation_completion != "COMPLETED":
            errors.append(
                "interpretive artifacts require manifest.interpretation_completion COMPLETED"
            )

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
                for ref in as_string_list(decision_outcome.get("decisive_finding_refs")):
                    finding = finding_by_id.get(ref, {})
                    if finding.get("epistemic_label") not in {"VERIFIED", "INFERRED"}:
                        errors.append(
                            f"ACT decisive finding {ref} must be VERIFIED or INFERRED"
                        )
                    direct_support = bool(finding.get("evidence_refs"))
                    qualified_lu_support = any(
                        episode_by_id.get(lu_ref, {}).get("status") == "QUALIFIED"
                        and bool(
                            episode_by_id.get(lu_ref, {}).get("lu1_evidence")
                            or episode_by_id.get(lu_ref, {}).get("lu2_evidence")
                        )
                        and trend_by_id.get(
                            episode_by_id.get(lu_ref, {}).get("trend_id"), {}
                        ).get("status")
                        in {"VERIFIED", "INFERRED"}
                        and bool(
                            trend_by_id.get(
                                episode_by_id.get(lu_ref, {}).get("trend_id"), {}
                            ).get("evidence_refs")
                        )
                        for lu_ref in as_string_list(finding.get("lu_refs"))
                    )
                    if not direct_support and not qualified_lu_support:
                        errors.append(
                            f"ACT decisive finding {ref} lacks a transitive atomic evidence path"
                        )
                for ref in as_string_list(decision_outcome.get("decisive_lu_refs")):
                    episode = episode_by_id.get(ref, {})
                    if episode.get("status") != "QUALIFIED" or not (
                        episode.get("lu1_evidence") and episode.get("lu2_evidence")
                    ):
                        errors.append(
                            f"ACT decisive LU {ref} must be QUALIFIED with LU1 and LU2 evidence"
                        )
                    trend = trend_by_id.get(episode.get("trend_id"), {})
                    if trend.get("status") not in {"VERIFIED", "INFERRED"} or not trend.get(
                        "evidence_refs"
                    ):
                        errors.append(
                            f"ACT decisive LU {ref} requires an evidence-backed VERIFIED or INFERRED trend"
                        )
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
            for action in as_list(decision_outcome.get("action_now")):
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
                and contains_private_identity(decision_brief_text, internal_identity)
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
