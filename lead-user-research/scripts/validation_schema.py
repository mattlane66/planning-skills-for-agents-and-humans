#!/usr/bin/env python3
"""Schema constants and reusable structural checks for Lead User study registries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

LIST_REGISTRIES = (
    "trends.json",
    "candidates.json",
    "sources.json",
    "evidence.json",
    "lu_episodes.json",
    "lineage.json",
    "findings.json",
    "needs.json",
    "principles.json",
    "shaping_frame.json",
    "fit_criteria.json",
    "concepts.json",
    "hypotheses.json",
    "observability.json",
    "analysis_runs.json",
    "search_log.json",
    "change_log.json",
)

OBJECT_REGISTRIES = (
    "manifest.json",
    "decision.json",
    "coverage.json",
    "sufficiency.json",
    "freeze.json",
    "decision_outcome.json",
)

REGISTRY_CONTAINERS = {**{name: list for name in LIST_REGISTRIES}, **{name: dict for name in OBJECT_REGISTRIES}}


REGISTRY_FIELD_TYPES: dict[str, dict[str, tuple[str, ...]]] = {
    'trends.json': {
        'direction': ('str',),
        'evidence_refs': ('list',),
        'importance': ('str',),
        'observable_indicators': ('list',),
        'statement': ('str',),
        'status': ('str',),
        'trend_id': ('str',),
    },
    'candidates.json': {
        'candidate_id': ('str',),
        'candidate_ref': ('str',),
        'discovery_basis': ('str',),
        'discovery_path': ('str',),
        'disposition': ('str',),
        'target_attribute': ('str',),
    },
    'sources.json': {
        'access_date': ('str',),
        'community_norm': ('none', 'str'),
        'content_trust': ('str',),
        'coverage': ('str',),
        'coverage_note': ('str',),
        'creator': ('str',),
        'embedded_instruction_note': ('str',),
        'embedded_instruction_risk': ('str',),
        'immutable_identifier': ('none', 'str'),
        'outward_citation_allowed': ('bool',),
        'participant_role': ('none', 'str'),
        'platform_affordance': ('none', 'str'),
        'platform_or_community': ('none', 'str'),
        'selection_mechanism': ('none', 'str'),
        'source_id': ('str',),
        'source_type': ('str',),
        'thread_or_context': ('none', 'str'),
        'title': ('str',),
        'url': ('none', 'str'),
    },
    'evidence.json': {
        'bounded_observation': ('str',),
        'caveat': ('str',),
        'evidence_basis': ('str',),
        'evidence_id': ('str',),
        'evidence_type': ('str',),
        'exact_location': ('str',),
        'lu_id': ('none', 'str'),
        'public_summary': ('str',),
        'source_id': ('str',),
        'trend_id': ('none', 'str'),
        'user_entity': ('none', 'str'),
    },
    'lu_episodes.json': {
        'advancement_indicator': ('str',),
        'alternatives': ('list',),
        'baseline': ('str',),
        'benefit_signal': ('str',),
        'context': ('str',),
        'desired_progress': ('str',),
        'identity_surface_allowed': ('bool',),
        'identity_surface_rationale': ('str',),
        'lu1_evidence': ('list',),
        'lu1_rationale': ('str',),
        'lu2_evidence': ('list',),
        'lu2_rationale': ('str',),
        'lu_id': ('str',),
        'need_statement': ('str',),
        'observed_result': ('str',),
        'public_label': ('str',),
        'qualification_caveats': ('list',),
        'status': ('str',),
        'trace': ('dict',),
        'trend_id': ('str',),
        'unknowns': ('list',),
        'user_entity': ('str',),
        'user_response': ('str',),
    },
    'lineage.json': {
        'evidence_refs': ('list',),
        'independence': ('str',),
        'lineage_id': ('str',),
        'member_refs': ('list',),
        'rationale': ('str',),
        'relationship': ('str',),
    },
    'findings.json': {
        'claim': ('str',),
        'confidence_rationale': ('str',),
        'contradictions': ('list',),
        'epistemic_label': ('str',),
        'evidence_refs': ('list',),
        'finding_id': ('str',),
        'lu_refs': ('list',),
        'trace_refs': ('list',),
    },
    'needs.json': {
        'concept_gate_checks': ('dict',),
        'concept_gate_rationale': ('str',),
        'concept_gate_status': ('str',),
        'contradictions': ('list',),
        'finding_ids': ('list',),
        'need_id': ('str',),
        'propagation_status': ('str',),
        'relevant_trends': ('list',),
        'statement': ('str',),
        'trace_refs': ('list',),
        'transferability_assessment': ('dict',),
    },
    'principles.json': {
        'evidence_refs': ('list',),
        'need_id': ('str',),
        'principle': ('str',),
        'principle_id': ('str',),
        'status': ('str',),
    },
    'shaping_frame.json': {
        'acceptance_note': ('str',),
        'accepted_by_human': ('bool',),
        'boundaries': ('list',),
        'evidence_refs': ('list',),
        'f': ('dict',),
        'frame_id': ('str',),
        'gap': ('str',),
        'need_id': ('str',),
        'status': ('str',),
        'x': ('dict',),
        'y': ('dict',),
    },
    'fit_criteria.json': {
        'altitude_check': ('bool',),
        'causal_relevance': ('bool',),
        'evidence_refs': ('list',),
        'frame_ref': ('str',),
        'implementation_independence': ('bool',),
        'information_gain': ('bool',),
        'need_id': ('str',),
        'origin': ('str',),
        'requirement': ('str',),
        'requirement_id': ('str',),
        'solution_plurality': ('bool',),
        'status': ('str',),
        'traceability': ('bool',),
    },
    'concepts.json': {
        'assumptions': ('list',),
        'concept_id': ('str',),
        'evidence_needed_next': ('list',),
        'mechanism': ('str',),
        'need_id': ('str',),
        'parts': ('list',),
        'rejection_record': ('dict',),
        'requirement_fit': ('dict',),
        'requirement_ids': ('list',),
        'risks': ('list',),
        'rotation_status': ('str',),
        'selected_by_human': ('bool',),
        'selection_note': ('str',),
        'selection_status': ('str',),
    },
    'hypotheses.json': {
        'boundary_conditions': ('list',),
        'claim': ('str',),
        'contrastive_cases': ('list',),
        'evidence_against': ('list',),
        'evidence_for': ('list',),
        'hypothesis_id': ('str',),
        'observable_predictions': ('list',),
        'rival_explanations': ('list',),
        'scope': ('str',),
        'status': ('str',),
        'strongest_plausible_refuter': ('str',),
        'targeted_refutation_searches': ('list',),
        'update_rationale': ('str',),
    },
    'observability.json': {
        'acceptance_rationale': ('str',),
        'decision_critical': ('bool',),
        'evidence_refs': ('list',),
        'fieldwork_referral': ('str',),
        'observability_id': ('str',),
        'question': ('str',),
        'resolution': ('str',),
        'status': ('str',),
    },
    'analysis_runs.json': {
        'analysis_run_id': ('str',),
        'extraction_schema': ('str',),
        'model': ('str',),
        'model_version': ('str',),
        'prompt_or_workflow_version': ('str',),
        'sampled_validation': ('dict',),
        'task': ('str',),
    },
    'search_log.json': {
        'branch': ('str',),
        'evidentiary_role': ('str',),
        'hops': ('list',),
        'network_visibility': ('str',),
        'next_branch': ('str',),
        'pyramid_id': ('str',),
        'query_or_route': ('str',),
        'result_refs': ('list',),
        'search_id': ('str',),
        'search_type': ('str',),
        'starting_node': ('str',),
        'target_attribute': ('str',),
        'termination_criterion': ('str',),
        'termination_reason': ('str',),
    },
    'change_log.json': {
        'change': ('str',),
        'change_id': ('str',),
        'changed_at': ('str',),
        'phase': ('str',),
        'reason': ('str',),
    },
    'manifest.json': {
        'created_at': ('str',),
        'deterministic_validation': ('str',),
        'evidence_completion': ('str',),
        'fixture_type': ('str',),
        'human_review': ('str',),
        'interpretation_completion': ('str',),
        'interpretive_status': ('str',),
        'mode': ('str',),
        'model_check': ('str',),
        'phase': ('str',),
        'protocol_version': ('str',),
        'study_execution_basis': ('list',),
        'study_execution_level': ('str',),
        'study_status': ('str',),
        'updated_at': ('str',),
    },
    'decision.json': {
        'assumptions': ('list',),
        'brief_field_status': ('dict',),
        'candidate_profile_hypotheses': ('list',),
        'consequential_unknowns': ('list',),
        'decision': ('str',),
        'disconfirming_evidence': ('list',),
        'discovery_seeds': ('list',),
        'domain': ('str',),
        'innovation_altitude': ('str',),
        'questions_not_answered': ('list',),
        'scope': ('dict',),
        'search_constraints': ('list',),
        'starting_hypotheses': ('list',),
        'target_market': ('str',),
        'what_to_understand': ('str',),
    },
    'coverage.json': {
        'branch_independence': ('dict',),
        'corrective_actions': ('list',),
        'fieldwork_referrals': ('list',),
        'inaccessible_or_private': ('list',),
        'languages_or_regions_searched': ('list',),
        'likely_overrepresented': ('list',),
        'likely_underrepresented': ('list',),
    },
    'sufficiency.json': {
        'dimensions': ('dict',),
        'overall_rationale': ('str',),
        'repair_status': ('str',),
        'status': ('str',),
        'unresolved_actions': ('list',),
    },
    'freeze.json': {
        'evidence_count': ('int',),
        'evidence_fingerprint': ('none', 'str'),
        'frozen_at': ('none', 'str'),
        'independent_lineage_count': ('int',),
        'post_freeze_evidence': ('list',),
        'qualified_lu_count': ('int',),
        'status': ('str',),
        'unresolved_gaps': ('list',),
    },
    'decision_outcome.json': {
        'action_now': ('list',),
        'change_conditions': ('list',),
        'contradictions': ('list',),
        'critical_uncertainties': ('list',),
        'decisive_finding_refs': ('list',),
        'decisive_lu_refs': ('list',),
        'priority_human_review': ('list',),
        'recommendation': ('str',),
        'recommended_next_evidence': ('list',),
        'status': ('none', 'str'),
        'what_evidence_does_not_support': ('list',),
        'what_evidence_supports': ('list',),
        'why': ('list',),
    },
}

_TYPE_BY_NAME = {
    "str": str,
    "list": list,
    "dict": dict,
    "bool": bool,
    "int": int,
    "none": type(None),
}

def validate_registry_fields(name: str, value: Any, errors: list[str]) -> None:
    """Validate declared top-level field types without replacing deeper semantic checks."""
    schema = REGISTRY_FIELD_TYPES[name]
    rows = value if isinstance(value, list) else [value]
    if not isinstance(value, REGISTRY_CONTAINERS[name]):
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        owner = f"{name} row {index}" if REGISTRY_CONTAINERS[name] is list else name
        for field, allowed_names in schema.items():
            if field not in row:
                continue
            allowed = tuple(_TYPE_BY_NAME[type_name] for type_name in allowed_names)
            candidate = row[field]
            if bool in allowed and isinstance(candidate, bool):
                continue
            if int in allowed and isinstance(candidate, bool):
                errors.append(f"{owner} {field} has invalid type bool")
                continue
            if not isinstance(candidate, allowed):
                errors.append(
                    f"{owner} {field} has invalid type {type(candidate).__name__}; "
                    f"expected {'/'.join(allowed_names)}"
                )

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
EVIDENCE_COMPLETION = {"NOT_STARTED", "COMPLETED"}
BRIEF_FIELD_STATUS = {"USER_SUPPLIED", "PROVISIONAL", "UNKNOWN"}
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

ENUM_DOMAINS: dict[str, set[str]] = {
    name: value
    for name, value in globals().copy().items()
    if name in {
        "COVERAGE", "LU_STATUS", "EPISTEMIC", "GATE", "TRACE_STATUS", "SUFFICIENCY",
        "EXECUTION_LEVEL", "STUDY_STATUS", "PHASES", "HUMAN_REVIEW",
        "DETERMINISTIC_VALIDATION", "INTERPRETIVE_STATUS", "MODEL_CHECK", "FIXTURE_TYPE",
        "INTERPRETATION_COMPLETION", "EVIDENCE_COMPLETION", "BRIEF_FIELD_STATUS",
        "SUFFICIENCY_REPAIR", "SOURCE_INSTRUCTION_RISK", "SOURCE_CONTENT_TRUST", "PROPAGATION",
        "LINEAGE_RELATIONSHIP", "INDEPENDENCE", "FIT_STATUS", "TRACE_BASIS",
        "SHAPING_FRAME_STATUS", "REQUIREMENT_ORIGIN", "CONCEPT_SELECTION_STATUS",
        "ROTATION_STATUS", "HYPOTHESIS_STATUS", "CONTRAST_CASE_TYPES", "OBSERVABILITY_STATUS",
        "OBSERVABILITY_RESOLUTION", "ANALYSIS_VALIDATION", "DISCOVERY_PATH", "SEARCH_TYPE",
        "EVIDENTIARY_ROLE", "TRANSFERABILITY", "BRANCH_INDEPENDENCE", "REJECTION_LAYER",
        "EVIDENCE_BASIS",
    }
}

ENUM_RULES: tuple[tuple[str, str, str], ...] = (
    ('sources.json', '[].coverage', 'COVERAGE'),
    ('lu_episodes.json', '[].status', 'LU_STATUS'),
    ('trends.json', '[].status', 'EPISTEMIC'),
    ('findings.json', '[].epistemic_label', 'EPISTEMIC'),
    ('principles.json', '[].status', 'EPISTEMIC'),
    ('needs.json', '[].concept_gate_status', 'GATE'),
    ('lu_episodes.json', '[].trace.status', 'TRACE_STATUS'),
    ('sufficiency.json', 'status', 'SUFFICIENCY'),
    ('sufficiency.json', 'dimensions.*.status', 'SUFFICIENCY'),
    ('manifest.json', 'study_execution_level', 'EXECUTION_LEVEL'),
    ('manifest.json', 'study_status', 'STUDY_STATUS'),
    ('manifest.json', 'phase', 'PHASES'),
    ('manifest.json', 'human_review', 'HUMAN_REVIEW'),
    ('manifest.json', 'deterministic_validation', 'DETERMINISTIC_VALIDATION'),
    ('manifest.json', 'interpretive_status', 'INTERPRETIVE_STATUS'),
    ('manifest.json', 'model_check', 'MODEL_CHECK'),
    ('manifest.json', 'fixture_type', 'FIXTURE_TYPE'),
    ('manifest.json', 'interpretation_completion', 'INTERPRETATION_COMPLETION'),
    ('manifest.json', 'evidence_completion', 'EVIDENCE_COMPLETION'),
    ('decision.json', 'brief_field_status.*', 'BRIEF_FIELD_STATUS'),
    ('sufficiency.json', 'repair_status', 'SUFFICIENCY_REPAIR'),
    ('sources.json', '[].embedded_instruction_risk', 'SOURCE_INSTRUCTION_RISK'),
    ('sources.json', '[].content_trust', 'SOURCE_CONTENT_TRUST'),
    ('needs.json', '[].propagation_status', 'PROPAGATION'),
    ('lineage.json', '[].relationship', 'LINEAGE_RELATIONSHIP'),
    ('lineage.json', '[].independence', 'INDEPENDENCE'),
    ('fit_criteria.json', '[].status', 'FIT_STATUS'),
    ('lu_episodes.json', '[].trace.trace_basis', 'TRACE_BASIS'),
    ('shaping_frame.json', '[].status', 'SHAPING_FRAME_STATUS'),
    ('fit_criteria.json', '[].origin', 'REQUIREMENT_ORIGIN'),
    ('concepts.json', '[].selection_status', 'CONCEPT_SELECTION_STATUS'),
    ('concepts.json', '[].rotation_status', 'ROTATION_STATUS'),
    ('hypotheses.json', '[].status', 'HYPOTHESIS_STATUS'),
    ('hypotheses.json', '[].contrastive_cases[].case_type', 'CONTRAST_CASE_TYPES'),
    ('observability.json', '[].status', 'OBSERVABILITY_STATUS'),
    ('observability.json', '[].resolution', 'OBSERVABILITY_RESOLUTION'),
    ('analysis_runs.json', '[].sampled_validation.status', 'ANALYSIS_VALIDATION'),
    ('candidates.json', '[].discovery_path', 'DISCOVERY_PATH'),
    ('search_log.json', '[].search_type', 'SEARCH_TYPE'),
    ('search_log.json', '[].evidentiary_role', 'EVIDENTIARY_ROLE'),
    ('needs.json', '[].transferability_assessment.status', 'TRANSFERABILITY'),
    ('coverage.json', 'branch_independence.status', 'BRANCH_INDEPENDENCE'),
    ('concepts.json', '[].rejection_record.layer', 'REJECTION_LAYER'),
    ('evidence.json', '[].evidence_basis', 'EVIDENCE_BASIS'),
)

def _path_values(value: Any, path: str) -> list[Any]:
    current = [value]
    for token in path.split("."):
        next_values: list[Any] = []
        if token == "[]":
            for item in current:
                if isinstance(item, list):
                    next_values.extend(item)
        elif token.endswith("[]"):
            key = token[:-2]
            for item in current:
                if isinstance(item, dict) and isinstance(item.get(key), list):
                    next_values.extend(item[key])
        elif token == "*":
            for item in current:
                if isinstance(item, dict):
                    next_values.extend(item.values())
        else:
            for item in current:
                if isinstance(item, dict) and token in item:
                    next_values.append(item[token])
        current = next_values
    return current

def validate_registry_enums(name: str, value: Any, errors: list[str]) -> None:
    """Apply every declared enum rule for one registry, including nested enum fields."""
    for registry, path, domain_name in ENUM_RULES:
        if registry != name:
            continue
        allowed = ENUM_DOMAINS[domain_name]
        for candidate in _path_values(value, path):
            if candidate is None:
                continue
            if not valid_enum(candidate, allowed):
                errors.append(f"{name} {path} has invalid {domain_name} value {candidate!r}")


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
    "post_freeze_change_id": re.compile(r"^PF\d+$"),
}

FINGERPRINT_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")

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


def valid_enum(value: Any, allowed: set[str]) -> bool:
    return isinstance(value, str) and value in allowed


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

