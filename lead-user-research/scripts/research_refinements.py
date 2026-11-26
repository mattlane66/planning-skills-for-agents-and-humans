"""Checks for additive research records in a version 1.7 study."""

from __future__ import annotations

from typing import Any

from validation_schema import as_string_list, refs_exist, require_nonempty_string, require_string_list


def optional_object(row: dict[str, Any], field: str, owner: str, errors: list[str]) -> dict | None:
    if field not in row:
        return None
    value = row[field]
    if not isinstance(value, dict):
        errors.append(f"{owner} {field} must be an object")
        return None
    return value


def validate_rare_search(row: dict, owner: str, refs: set[str], errors: list[str]) -> None:
    check = optional_object(row, "rare_signal_check", owner, errors)
    if check is None:
        return
    label = f"{owner} rare_signal_check"
    for field in ("channel", "access_limits", "likely_missing", "batch_bound"):
        require_nonempty_string(check, field, label, errors)
    for field in ("signals", "methods"):
        require_string_list(check, field, label, errors, nonempty=True)
    for field in ("inspected_original_refs", "low_rank_sample_refs"):
        values = require_string_list(check, field, label, errors)
        refs_exist(values, refs, field, label, errors)
    originals = set(as_string_list(check.get("inspected_original_refs")))
    sampled = set(as_string_list(check.get("low_rank_sample_refs")))
    if not sampled.issubset(originals):
        errors.append(f"{label} low-rank sample must reference inspected originals")
    if not check.get("low_rank_sample_refs"):
        require_nonempty_string(check, "low_rank_sample_rationale", label, errors)


def validate_analog(row: dict, owner: str, evidence_ids: set[str], errors: list[str]) -> None:
    mapping = optional_object(row, "structural_analog", owner, errors)
    if mapping is None:
        return
    label = f"{owner} structural_analog"
    if row.get("discovery_path") != "ADVANCED_ANALOG":
        errors.append(f"{label} requires discovery_path ADVANCED_ANALOG")
    for field in ("context", "relationship", "bottleneck", "constraints", "desired_outcome",
                  "hypothesized_mechanism", "analog_domain", "correspondence", "disanalogy",
                  "potential_principle", "break_condition"):
        require_nonempty_string(mapping, field, label, errors)
    status = mapping.get("status")
    if status not in ("SPECULATIVE", "OBSERVED_ANALOG"):
        errors.append(f"{label} status must be SPECULATIVE or OBSERVED_ANALOG")
    values = require_string_list(mapping, "evidence_refs", label, errors,
                                 nonempty=status == "OBSERVED_ANALOG")
    refs_exist(values, evidence_ids, "analog evidence", label, errors)


AUDIT_DIMENSIONS = ("access", "attribution", "context", "claim_type", "entailment",
                    "independent_support", "contradictions")
AUDIT_STATES = ("PASS", "FAIL", "UNKNOWN", "NOT_RUN", "NOT_APPLICABLE")


def validate_hypothesis_contrast(row: dict, evidence_ids: set[str], errors: list[str]) -> None:
    owner = row.get("hypothesis_id", "hypothesis")
    contrast = optional_object(row, "contrast", owner, errors)
    if contrast is None:
        return
    label = f"{owner} contrast"
    kind = contrast.get("kind")
    if kind == "NOT_APPLICABLE":
        require_nonempty_string(contrast, "rationale", label, errors)
        return
    if kind not in ("NULL", "RIVAL"):
        errors.append(f"{label} requires NULL, RIVAL or NOT_APPLICABLE")
    for field in ("alternative", "discriminating_observation", "refuter"):
        require_nonempty_string(contrast, field, label, errors)
    require_string_list(contrast, "observable_predictions", label, errors, nonempty=True)
    require_string_list(contrast, "primary_predictions", label, errors, nonempty=True)
    primary = set(as_string_list(contrast.get("primary_predictions")))
    alternative = set(as_string_list(contrast.get("observable_predictions")))
    if primary and primary == alternative:
        errors.append(f"{label} requires different predictions for the competing explanations")
    for field in ("evidence_for_alternative", "evidence_against_alternative"):
        refs = require_string_list(contrast, field, label, errors)
        refs_exist(refs, evidence_ids, field, label, errors)


def validate_claim_audit(row: dict, sources: dict, evidence_ids: set[str], errors: list[str]) -> None:
    owner = row.get("evidence_id", "evidence")
    audit = optional_object(row, "claim_audit", owner, errors)
    if audit is None:
        return
    label = f"{owner} claim_audit"
    if audit.get("decision_use") not in ("PIVOTAL", "EXCLUDED", "EXPLORATORY"):
        errors.append(f"{label} requires a decision_use")
    if audit.get("human_review") not in ("REVIEWED", "NOT_REVIEWED"):
        errors.append(f"{label} requires independent human_review status")
    if audit.get("human_review") == "REVIEWED":
        require_nonempty_string(audit, "review_ref", label, errors)
    require_nonempty_string(row, "exact_location", label, errors)
    checks = audit.get("checks")
    if not isinstance(checks, dict) or set(checks) != set(AUDIT_DIMENSIONS):
        errors.append(f"{label} requires exactly the stated audit dimensions")
        return

    for name, check in checks.items():
        dimension = f"{label}.{name}"
        if not isinstance(check, dict):
            errors.append(f"{dimension} must be an object")
            continue
        status = check.get("status")
        if status not in AUDIT_STATES or (
            status == "NOT_APPLICABLE" and name not in ("independent_support", "contradictions")
        ):
            errors.append(f"{dimension} invalid status for this dimension")
        require_nonempty_string(check, "rationale", dimension, errors)
        refs = require_string_list(check, "refs", dimension, errors, nonempty=status == "PASS")
        refs_exist(refs, evidence_ids | set(sources), "audit source or evidence", dimension, errors)
        source_id = row.get("source_id")
        if name == "access" and status == "PASS" and (
            not isinstance(source_id, str) or source_id not in refs
            or sources.get(source_id, {}).get("coverage") not in ("FULL", "PARTIAL")
        ):
            errors.append(f"{dimension} PASS requires the accessible underlying source")


def claim_can_support_decision(row: dict) -> bool:
    if "claim_audit" not in row:
        return True  # Existing studies and exploratory records have no new mandatory fields.
    audit = row["claim_audit"]
    if not isinstance(audit, dict) or audit.get("decision_use") not in ("PIVOTAL", "EXPLORATORY"):
        return False
    checks = audit.get("checks")
    return isinstance(checks, dict) and all(
        isinstance(checks.get(name), dict)
        and (checks[name].get("status") == "PASS" or (
            name in ("independent_support", "contradictions")
            and checks[name].get("status") == "NOT_APPLICABLE"
        ))
        for name in AUDIT_DIMENSIONS
    )


def pivotal_claim_blockers(evidence: list) -> list[str]:
    return [
        str(row.get("evidence_id", "evidence"))
        for row in evidence
        if isinstance(row, dict) and isinstance(row.get("claim_audit"), dict)
        and row["claim_audit"].get("decision_use") == "PIVOTAL"
        and not claim_can_support_decision(row)
    ]


def validate_conditional_mechanism(row: dict, episode_ids: set[str], hypothesis_ids: set[str],
                                   errors: list[str]) -> None:
    owner = row.get("principle_id", "principle")
    mechanism = optional_object(row, "conditional_mechanism", owner, errors)
    if mechanism is None:
        return
    label = f"{owner} conditional_mechanism"
    for field in ("condition", "behavioral_relation", "discriminating_observation"):
        require_nonempty_string(mechanism, field, label, errors)
    if mechanism.get("status") != "PROPOSED":
        errors.append(f"{label} is a PROPOSED interpretation")
    for field in ("supporting_episodes", "conflicting_episodes", "unassessed_episodes"):
        refs = require_string_list(mechanism, field, label, errors)
        refs_exist(refs, episode_ids, field, label, errors)
    refs = require_string_list(mechanism, "rival_hypothesis_refs", label, errors, nonempty=True)
    refs_exist(refs, hypothesis_ids, "rival hypothesis", label, errors)


def validate_transfer_contrasts(row: dict, evidence: dict, findings: dict, errors: list[str]) -> None:
    assessment = row.get("transferability_assessment")
    if not isinstance(assessment, dict) or "contrasts" not in assessment:
        return
    owner = f"{row.get('need_id', 'need')} transferability contrasts"
    contrasts = assessment["contrasts"]
    if not isinstance(contrasts, list) or not contrasts:
        errors.append(f"{owner} requires at least one contrast")
        return
    for index, contrast in enumerate(contrasts, 1):
        label = f"{owner} row {index}"
        if not isinstance(contrast, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("dimension", "lead_user_situation", "target_situation", "refuter"):
            require_nonempty_string(contrast, field, label, errors)
        load_bearing = contrast.get("load_bearing")
        if type(load_bearing) is not bool:
            errors.append(f"{label} load_bearing must be boolean")
        status = contrast.get("status")
        if status not in ("SUPPORTED", "CONTRADICTED", "UNKNOWN"):
            errors.append(f"{label} invalid status")
        refs = require_string_list(contrast, "evidence_refs", label, errors,
                                   nonempty=status in ("SUPPORTED", "CONTRADICTED"))
        refs_exist(refs, set(evidence) | set(findings), "transfer evidence", label, errors)
        if row.get("concept_gate_status") != "PASS" or load_bearing is not True:
            continue
        atomic = [
            atomic_ref for ref in refs for atomic_ref in (
                [ref] if ref in evidence else as_string_list(findings.get(ref, {}).get("evidence_refs"))
            )
        ]
        if status != "SUPPORTED" or not atomic or any(
            not claim_can_support_decision(evidence[ref]) for ref in atomic if ref in evidence
        ):
            errors.append(f"{label} unresolved load-bearing contrast blocks concept gate PASS")


def validate_generation(row: dict, frames: dict, criteria: dict, seen: set[tuple[str, str]],
                        errors: list[str]) -> None:
    from study_fingerprint import shaping_basis_digest

    owner = row.get("concept_id", "concept")
    generation = optional_object(row, "generation", owner, errors)
    if generation is None:
        return
    label = f"{owner} generation"
    for field in ("branch", "functional_key", "basis_digest", "boundary_status",
                  "predicted_behavior", "distinctness_rationale"):
        require_nonempty_string(generation, field, label, errors)
    require_string_list(generation, "collapsed_alternatives", label, errors)
    if generation.get("boundary_status") not in ("PASS", "FAIL"):
        errors.append(f"{label} boundary_status must be PASS or FAIL")
    if generation.get("boundary_status") == "FAIL" and row.get("selection_status") != "REJECTED":
        errors.append(f"{label} boundary violation requires a rejected candidate")
    frame_ref = generation.get("frame_ref")
    frame = frames.get(frame_ref) if isinstance(frame_ref, str) else None
    if not frame or frame.get("status") != "ACCEPTED" or frame.get("accepted_by_human") is not True \
            or frame.get("need_id") != row.get("need_id"):
        errors.append(f"{label} requires the accepted frame for this need")
        return
    need_criteria = [
        item for item in criteria.values()
        if item.get("need_id") == row.get("need_id") and item.get("status") == "PASS"
    ]
    if not need_criteria or any(item.get("frame_ref") != frame_ref for item in need_criteria):
        errors.append(f"{label} requires a single frame for all frozen PASS criteria")
    if generation.get("basis_digest") != shaping_basis_digest(frame, need_criteria):
        errors.append(f"{label} comparison basis is stale")
    key = generation.get("functional_key")
    if isinstance(key, str) and row.get("selection_status") != "REJECTED":
        entry = (frame_ref, key.strip().casefold())
        if entry in seen:
            errors.append(f"{label} duplicates a functional mechanism on the same frame")
        seen.add(entry)
