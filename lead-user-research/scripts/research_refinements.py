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
