#!/usr/bin/env python3
"""Stable fingerprint for the structured state behind a Decision Brief."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


STATE_FILES = (
    "manifest.json",
    "decision.json",
    "coverage.json",
    "sufficiency.json",
    "freeze.json",
    "decision_outcome.json",
    "trends.json",
    "candidates.json",
    "sources.json",
    "evidence.json",
    "lu_episodes.json",
    "lineage.json",
    "search_log.json",
    "hypotheses.json",
    "observability.json",
    "analysis_runs.json",
    "change_log.json",
    "findings.json",
    "needs.json",
    "principles.json",
    "shaping_frame.json",
    "fit_criteria.json",
    "concepts.json",
)

EVIDENCE_STATE_FILES = (
    "decision.json",
    "coverage.json",
    "sufficiency.json",
    "trends.json",
    "candidates.json",
    "sources.json",
    "evidence.json",
    "lu_episodes.json",
    "lineage.json",
    "search_log.json",
    "hypotheses.json",
    "observability.json",
    "analysis_runs.json",
    "change_log.json",
)

VALIDATOR_MANAGED_MANIFEST_FIELDS = {
    "deterministic_validation",
    "updated_at",
}


def _normalized_state(root: Path, filenames: tuple[str, ...]) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for filename in filenames:
        path = root / filename
        if not path.exists():
            continue
        value = json.loads(path.read_text(encoding="utf-8"))
        if filename == "manifest.json" and isinstance(value, dict):
            value = {
                key: item
                for key, item in value.items()
                if key not in VALIDATOR_MANAGED_MANIFEST_FIELDS
            }
        state[filename] = value
    return state


def canonical_digest(value: Any) -> str:
    canonical = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def shaping_basis_digest(frame: dict, criteria: list[dict]) -> str:
    """Bind fixed x/y and boundaries to the actual set of PASS requirements."""
    frame_fields = ("frame_id", "need_id", "x", "y", "gap", "boundaries", "evidence_refs")
    criterion_fields = ("requirement_id", "frame_ref", "need_id", "origin",
                        "requirement", "evidence_refs")
    requirements = [
        {key: row.get(key) for key in criterion_fields}
        for row in criteria if row.get("status") == "PASS" and row.get("frame_ref") == frame.get("frame_id")
    ]
    return canonical_digest({
        "frame": {key: frame.get(key) for key in frame_fields},
        "requirements": sorted(requirements, key=lambda row: str(row["requirement_id"])),
    })


def study_fingerprint(root: Path) -> str:
    return canonical_digest(_normalized_state(root, STATE_FILES))


def evidence_fingerprint(root: Path) -> str:
    """Fingerprint only the decision-relative evidence state frozen in Phase D."""
    return canonical_digest(_normalized_state(root, EVIDENCE_STATE_FILES))
