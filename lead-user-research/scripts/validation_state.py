#!/usr/bin/env python3
"""Study-level phase/state checks for the Lead User validator."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from study_fingerprint import evidence_fingerprint
from validation_schema import (
    ANALYSIS_VALIDATION,
    BRIEF_FIELD_STATUS,
    DETERMINISTIC_VALIDATION,
    EVIDENCE_COMPLETION,
    EXECUTION_LEVEL,
    FINGERPRINT_PATTERN,
    FIXTURE_TYPE,
    HUMAN_REVIEW,
    ID_PATTERNS,
    INTERPRETATION_COMPLETION,
    INTERPRETIVE_STATUS,
    MODEL_CHECK,
    PHASES,
    STUDY_STATUS,
    SUFFICIENCY,
    SUFFICIENCY_DIMENSIONS,
    SUFFICIENCY_REPAIR,
    as_string_list,
    require_nonempty_string,
    require_string_list,
    valid_enum,
)

def validate_sufficiency_state(
    sufficiency: Any,
    all_structured_refs: set[str],
    pyramid_ids: set[str],
    errors: list[str],
) -> None:
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


def validate_freeze_state(
    root: Path,
    freeze: Any,
    sufficiency: Any,
    episodes: list[Any],
    evidence: list[Any],
    independent_lineage_count: int,
    observability: list[Any],
    analysis_run_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
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
            base_fingerprint = freeze.get("evidence_fingerprint")
            if not isinstance(base_fingerprint, str) or not FINGERPRINT_PATTERN.match(base_fingerprint):
                errors.append("Evidence Freeze requires a sha256 evidence_fingerprint")
            post_freeze = freeze.get("post_freeze_evidence")
            expected_fingerprint = base_fingerprint
            if not isinstance(post_freeze, list):
                errors.append("freeze post_freeze_evidence must be a list")
                post_freeze = []
            post_freeze_ids: set[str] = set()
            for index, change in enumerate(post_freeze):
                owner = f"freeze post_freeze_evidence row {index}"
                if not isinstance(change, dict):
                    errors.append(f"{owner} must be an object")
                    continue
                change_id = change.get("change_id")
                if (
                    not isinstance(change_id, str)
                    or not ID_PATTERNS["post_freeze_change_id"].match(change_id)
                ):
                    errors.append(f"{owner} has invalid change_id {change_id!r}")
                elif change_id in post_freeze_ids:
                    errors.append(f"duplicate post-freeze change_id: {change_id}")
                else:
                    post_freeze_ids.add(change_id)
                for field in ["sought_because", "triggering_question_or_interpretation"]:
                    require_nonempty_string(change, field, owner, errors)
                require_string_list(change, "state_changes", owner, errors, nonempty=True)
                require_string_list(change, "affected_interpretation_refs", owner, errors)
                resulting = change.get("resulting_evidence_fingerprint")
                if not isinstance(resulting, str) or not FINGERPRINT_PATTERN.match(resulting):
                    errors.append(f"{owner} requires a sha256 resulting_evidence_fingerprint")
                else:
                    expected_fingerprint = resulting
            try:
                current_evidence_fingerprint = evidence_fingerprint(root)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"cannot compute frozen evidence fingerprint: {exc}")
            else:
                if current_evidence_fingerprint != expected_fingerprint:
                    errors.append(
                        "frozen evidence changed without a matching post_freeze_evidence fingerprint"
                    )
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


def validate_manifest_state(
    root: Path,
    manifest: Any,
    mode: Any,
    fixture_type: Any,
    is_synthetic_fixture: bool,
    study_status: Any,
    evidence: list[Any],
    concepts: list[Any],
    findings: list[Any],
    needs: list[Any],
    principles: list[Any],
    errors: list[str],
) -> str | None:
    decision_brief_text: str | None = None
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
        if not valid_enum(manifest.get("evidence_completion"), EVIDENCE_COMPLETION):
            errors.append(
                "manifest has invalid evidence_completion "
                f"{manifest.get('evidence_completion')!r}"
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
            if manifest.get("evidence_completion") != "COMPLETED":
                errors.append("complete study requires evidence_completion COMPLETED")
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

    return decision_brief_text
