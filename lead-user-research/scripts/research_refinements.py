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
