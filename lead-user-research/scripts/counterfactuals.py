#!/usr/bin/env python3
"""Validate and compare optional analyst hypotheses without invoking a model."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import re

from research_refinements import claim_can_support_decision
from study_fingerprint import canonical_digest, evidence_fingerprint, shaping_basis_digest
from validation_schema import FINGERPRINT_PATTERN, as_string_list, require_nonempty_string, require_string_list


CONTRACT = "lur-counterfactuals-v1"
FILE = "counterfactuals.json"
PURPOSES = ("TRANSFER_STRESS", "INTERVENTION_COMPARE", "EDGE_CASE", "TEST_PRIORITY")
CF_ID = re.compile(r"CF[0-9]+\Z")
STUDY_ID = re.compile(r"[a-f0-9]{32}\Z")
BASIS_FIELDS = (
    "need_ref", "frame_ref", "frame_digest", "requirement_refs", "episode_ref", "evidence_refs",
    "decision", "owner", "consequence_if_wrong", "target", "baseline", "unknowns",
    "held_constant", "time_horizon", "outcome_space",
)
SCENARIO_FIELDS = (
    "scenario_id", "comparison_id", "purpose", "basis", "intervention", "changed_conditions",
    "candidate_ref", "candidate_digest", "critical_assumption", "predicted_behavior", "rival_explanation",
    "refuter", "if_disproved", "smallest_test", "provenance", "counterfactual_distance",
)


def reject_non_finite(value: str):
    raise ValueError(f"Non-finite value in JSON: {value}")


def read_json(root: Path, filename: str, default=None):
    path = root / filename
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_non_finite)


def indexed(root: Path, filename: str, id_field: str) -> dict[str, dict]:
    rows = read_json(root, filename, [])
    return {
        row[id_field]: row for row in rows
        if isinstance(row, dict) and isinstance(row.get(id_field), str)
    } if isinstance(rows, list) else {}


@dataclass
class StudyBasis:
    root: Path
    study_ref: str | None
    fingerprint: str
    freeze_current: bool
    fixture: bool
    evidence: dict = field(repr=False)
    episodes: dict = field(repr=False)
    needs: dict = field(repr=False)
    findings: dict = field(repr=False)
    frames: dict = field(repr=False)
    criteria: dict = field(repr=False)
    concepts: dict = field(repr=False)

    @classmethod
    def load(cls, root: Path) -> StudyBasis:
        manifest = read_json(root, "manifest.json", {})
        study_id = manifest.get("study_id")
        study_ref = f"LUR:{study_id}" if isinstance(study_id, str) and STUDY_ID.fullmatch(study_id) else None
        freeze = read_json(root, "freeze.json", {})
        fingerprint = evidence_fingerprint(root)
        changes = freeze.get("post_freeze_evidence", [])
        expected = changes[-1].get("resulting_evidence_fingerprint") if changes else freeze.get("evidence_fingerprint")
        frozen_at = freeze.get("frozen_at")
        try:
            dated_freeze = isinstance(frozen_at, str) and datetime.fromisoformat(frozen_at) is not None
        except ValueError:
            dated_freeze = False
        freeze_current = freeze.get("status") == "FROZEN" and expected == fingerprint and dated_freeze
        return cls(
            root, study_ref, fingerprint, freeze_current,
            manifest.get("fixture_type") == "SYNTHETIC_REFERENCE",
            indexed(root, "evidence.json", "evidence_id"), indexed(root, "lu_episodes.json", "lu_id"),
            indexed(root, "needs.json", "need_id"), indexed(root, "findings.json", "finding_id"),
            indexed(root, "shaping_frame.json", "frame_id"),
            indexed(root, "fit_criteria.json", "requirement_id"), indexed(root, "concepts.json", "concept_id"),
        )

    def pass_criteria(self, frame_ref: str) -> list[dict]:
        return [
            row for row in self.criteria.values()
            if row.get("frame_ref") == frame_ref and row.get("status") == "PASS"
        ]


def scenario_digest(study_ref: str, fingerprint: str, scenario: dict) -> str:
    return canonical_digest({
        "contract": CONTRACT, "study_ref": study_ref, "evidence_fingerprint": fingerprint,
        "scenario": {key: scenario.get(key) for key in SCENARIO_FIELDS},
    })


def check_basis(study: StudyBasis, scenario: dict, basis: dict, owner: str,
                errors: list[str], stale: list[str]) -> None:
    need_ref = basis.get("need_ref")
    episode_ref = basis.get("episode_ref")
    need = study.needs.get(need_ref) if isinstance(need_ref, str) else None
    episode = study.episodes.get(episode_ref) if isinstance(episode_ref, str) else None
    if need is None or not episode or episode.get("status") != "QUALIFIED":
        errors.append(f"{owner} requires a local interpreted need and qualified episode")
    elif not any(
        episode_ref in as_string_list(study.findings.get(ref, {}).get("lu_refs"))
        for ref in as_string_list(need.get("finding_ids"))
    ) and not any(
        ref.startswith(f"{episode_ref}:") for ref in as_string_list(need.get("trace_refs"))
    ):
        errors.append(f"{owner} episode is unlinked to the interpreted need")
    refs = set(as_string_list(basis.get("evidence_refs")))
    qualification = set(as_string_list((episode or {}).get("lu1_evidence"))) | set(
        as_string_list((episode or {}).get("lu2_evidence"))
    )
    if not qualification or not qualification.issubset(refs):
        errors.append(f"{owner} baseline requires the episode's atomic LU1 and LU2 support")
    for ref in sorted(refs):
        row = study.evidence.get(ref)
        if row is None or not claim_can_support_decision(row):
            errors.append(f"{owner} has missing or unresolved grounding {ref}")
        elif row.get("evidence_basis") == "SYNTHETIC_OR_SIMULATED" and not study.fixture:
            errors.append(f"{owner} grounding {ref} is simulated")
    if not study.fixture and not any(
        study.evidence.get(ref, {}).get("evidence_basis") in {
            "REAL_HUMAN_TRACE", "REAL_HUMAN_STATEMENT", "REAL_HUMAN_ARTIFACT", "INDEPENDENT_OBSERVATION", "EVENT_LOG",
        }
        for ref in qualification
    ):
        errors.append(f"{owner} requires human episode grounding")

    frame_ref = basis.get("frame_ref")
    if frame_ref is None:
        if basis.get("frame_digest") is not None or basis.get("requirement_refs") or scenario.get("candidate_ref"):
            errors.append(f"{owner} frame-free comparison cannot cite shape criteria or a candidate")
        if scenario.get("purpose") == "INTERVENTION_COMPARE":
            errors.append(f"{owner} intervention comparison requires an accepted shaping frame")
        return
    if not need or need.get("concept_gate_status") != "PASS":
        stale.append("existing concept gate is closed")
    frame = study.frames.get(frame_ref) if isinstance(frame_ref, str) else None
    if not frame or frame.get("status") != "ACCEPTED" or frame.get("accepted_by_human") is not True:
        stale.append("accepted shaping frame is unavailable")
        return
    if frame.get("need_id") != need_ref:
        errors.append(f"{owner} shaping frame belongs to another need")
    criteria = study.pass_criteria(frame_ref)
    all_need_criteria = {
        ref for ref, row in study.criteria.items()
        if row.get("need_id") == need_ref and row.get("status") == "PASS"
    }
    if not criteria or {row["requirement_id"] for row in criteria} != all_need_criteria \
            or all_need_criteria != set(as_string_list(basis.get("requirement_refs"))) \
            or basis.get("frame_digest") != shaping_basis_digest(frame, criteria):
        stale.append("accepted shaping frame or PASS criteria changed")

    candidate_ref = scenario.get("candidate_ref")
    intervention = scenario.get("intervention")
    if candidate_ref is None:
        if intervention != "STATUS_QUO" and scenario.get("purpose") == "INTERVENTION_COMPARE":
            errors.append(f"{owner} named intervention must reference a local candidate")
        return
    candidate = study.concepts.get(candidate_ref) if isinstance(candidate_ref, str) else None
    if not candidate or candidate.get("need_id") != need_ref:
        stale.append("candidate is missing or belongs to a different need")
    elif candidate.get("selection_status") == "REJECTED" or not all(
        candidate.get("requirement_fit", {}).get(ref) is True for ref in all_need_criteria
    ):
        stale.append("candidate was rejected or no longer fits the fixed requirements")
    elif scenario.get("candidate_digest") != candidate_digest(candidate):
        stale.append("candidate intervention changed")


def candidate_digest(candidate: dict) -> str:
    return canonical_digest({key: candidate.get(key) for key in ("concept_id", "mechanism", "parts", "requirement_fit")})


def inspect(root: Path) -> tuple[list[dict], list[str]]:
    """Return reviewer-facing status and structural errors. Stale records are archival."""
    if not (root / FILE).exists():
        return [], []
    try:
        sidecar = read_json(root, FILE)
        study = StudyBasis.load(root)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        return [], [f"Cannot read counterfactual study state ({type(exc).__name__})"]
    if not isinstance(sidecar, dict) or sidecar.get("contract") != CONTRACT:
        return [], ["counterfactuals.json has an unsupported contract"]
    if study.study_ref is None or sidecar.get("study_ref") != study.study_ref:
        return [], ["counterfactuals.json requires this study's LUR namespace"]
    rows = sidecar.get("scenarios")
    if not isinstance(rows, list):
        return [], ["counterfactuals.json scenarios must be a list"]

    results: list[dict] = []
    errors: list[str] = []
    ids: set[str] = set()
    for index, scenario in enumerate(rows, 1):
        owner = f"counterfactuals.json scenario {index}"
        if not isinstance(scenario, dict):
            errors.append(f"{owner} must be an object")
            continue
        scenario_id = scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not CF_ID.fullmatch(scenario_id) or scenario_id in ids:
            errors.append(f"{owner} requires a unique CF## scenario_id")
            continue
        ids.add(scenario_id)
        owner = scenario_id
        start_errors = len(errors)
        allowed_fields = set(SCENARIO_FIELDS) | {"evidence_fingerprint", "scenario_digest",
                                                 "human_review", "review_ref", "review_digest"}
        if set(scenario) - allowed_fields:
            errors.append(f"{owner} has unsupported scenario fields")
        for name in ("comparison_id", "intervention", "critical_assumption", "predicted_behavior",
                     "rival_explanation", "refuter", "if_disproved", "smallest_test",
                     "counterfactual_distance"):
            require_nonempty_string(scenario, name, owner, errors)
        if scenario.get("purpose") not in PURPOSES or scenario.get("provenance") != "ANALYST_HYPOTHESIS":
            errors.append(f"{owner} requires a supported purpose and ANALYST_HYPOTHESIS provenance")
        changed = require_string_list(scenario, "changed_conditions", owner, errors)
        if bool(changed) == (scenario.get("intervention") == "STATUS_QUO"):
            errors.append(f"{owner} must name changed conditions, or use an unchanged STATUS_QUO")
        basis = scenario.get("basis")
        if not isinstance(basis, dict) or set(basis) != set(BASIS_FIELDS):
            errors.append(f"{owner} must define precisely the comparison basis fields")
            continue
        for name in ("need_ref", "episode_ref", "decision", "owner", "consequence_if_wrong",
                     "target", "baseline", "time_horizon"):
            require_nonempty_string(basis, name, owner, errors)
        for name in ("evidence_refs", "requirement_refs", "unknowns", "held_constant", "outcome_space"):
            require_string_list(basis, name, owner, errors, nonempty=name in ("evidence_refs", "outcome_space"))
        fingerprint = scenario.get("evidence_fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT_PATTERN.fullmatch(fingerprint):
            errors.append(f"{owner} requires an evidence fingerprint")
            continue
        try:
            digest = scenario_digest(study.study_ref, fingerprint, scenario)
        except (TypeError, ValueError, UnicodeError):
            errors.append(f"{owner} contains invalid JSON content")
            continue
        if scenario.get("scenario_digest") != digest:
            errors.append(f"{owner} scenario digest does not match its content")
        if scenario.get("human_review") not in ("NOT_REVIEWED", "REVIEWED"):
            errors.append(f"{owner} requires human_review status")
        if scenario.get("human_review") == "REVIEWED":
            require_nonempty_string(scenario, "review_ref", owner, errors)
            if scenario.get("review_digest") != digest:
                errors.append(f"{owner} human review must bind this scenario digest")
        stale: list[str] = []
        if fingerprint != study.fingerprint:
            stale.append("evidence changed")
        elif not study.freeze_current:
            stale.append("no current evidence freeze")
        else:
            try:
                check_basis(study, scenario, basis, owner, errors, stale)
            except (TypeError, ValueError, AttributeError):
                errors.append(f"{owner} references malformed structured state")
        status = "INVALID" if len(errors) != start_errors else "STALE" if stale else "CURRENT"
        results.append({"scenario": scenario, "status": status, "reasons": stale})

    groups: dict[str, list[dict]] = {}
    for result in results:
        if result["status"] == "CURRENT":
            groups.setdefault(result["scenario"]["comparison_id"], []).append(result)
    for group in groups.values():
        bases = {canonical_digest(row["scenario"]["basis"]) for row in group}
        purposes = {row["scenario"]["purpose"] for row in group}
        if len(bases) > 1 or len(purposes) > 1:
            for row in group:
                row["status"] = "NONCOMPARABLE"
                row["reasons"] = ["comparison basis or purpose differs"]
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--basis", metavar="FRAME_REF", help="Print current evidence and frame digests")
    parser.add_argument("--digests", metavar="CF_ID", help="Print scenario and basis bindings for local review")
    arguments = parser.parse_args()
    if arguments.digests:
        try:
            study = StudyBasis.load(arguments.workspace)
            sidecar = read_json(arguments.workspace, FILE)
            scenario, = [row for row in sidecar.get("scenarios", []) if row.get("scenario_id") == arguments.digests]
            if not study.study_ref or sidecar.get("study_ref") != study.study_ref:
                raise ValueError("Study identity mismatch")
            candidate = study.concepts.get(scenario.get("candidate_ref"))
            print(json.dumps({
                "evidence_fingerprint": study.fingerprint,
                "candidate_digest": candidate_digest(candidate) if candidate else None,
                "scenario_digest": scenario_digest(study.study_ref, study.fingerprint, scenario),
            }, indent=2))
        except (ValueError, KeyError, TypeError, AttributeError, OSError):
            parser.error("Expected one local draft with a study identity")
        return 0
    if arguments.basis:
        study = StudyBasis.load(arguments.workspace)
        frame = study.frames.get(arguments.basis)
        if frame is None or not study.study_ref:
            parser.error("Need a local frame and manifest study_id")
        print(json.dumps({
            "study_ref": study.study_ref, "evidence_fingerprint": study.fingerprint,
            "frame_digest": shaping_basis_digest(frame, study.pass_criteria(arguments.basis)),
        }, indent=2))
        return 0
    rows, errors = inspect(arguments.workspace)
    print(json.dumps({"comparisons": [
        {"scenario_id": row["scenario"]["scenario_id"], "status": row["status"], "reasons": row["reasons"]}
        for row in rows
    ], "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
