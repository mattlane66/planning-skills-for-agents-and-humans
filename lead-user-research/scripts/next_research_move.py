#!/usr/bin/env python3
"""Recommend the next valid Lead User research move from persisted study state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PHASE_COMMANDS = {
    "A": "/lead-user-frame",
    "B": "/lead-user-discover",
    "C": "/lead-user-evidence",
    "D": "/lead-user-freeze",
    "E": "/lead-user-interpret",
    "F": "/lead-user-shape",
    "G": "/lead-user-decide",
    "H": "/lead-user-deliver",
}

DISCOVERY_DIMENSIONS = {"trend_support", "pyramid_coverage"}


def load_json(root: Path, name: str, default: Any) -> Any:
    path = root / name
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {name}: {exc}") from exc


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def result(
    *,
    current_phase: str,
    state: str,
    next_phase: str | None,
    reason: str,
    blockers: list[str] | None = None,
    human_gate: str = "None",
    conditional_next_skill: str | None = None,
) -> dict[str, Any]:
    return {
        "state": state,
        "current_phase": current_phase,
        "next_phase": next_phase,
        "next_skill": "lead-user-research" if next_phase else None,
        "recommended_command": PHASE_COMMANDS.get(next_phase),
        "reason": reason,
        "blockers": blockers or [],
        "human_gate": human_gate,
        "conditional_next_skill": conditional_next_skill,
    }


def recommend(root: Path) -> dict[str, Any]:
    manifest = load_json(root, "manifest.json", {})
    if not isinstance(manifest, dict):
        raise ValueError("manifest.json must contain an object")
    current_phase = manifest.get("phase", "A")
    if current_phase not in PHASE_COMMANDS:
        raise ValueError(f"manifest.json has invalid phase {current_phase!r}")

    decision = load_json(root, "decision.json", {})
    required_brief = [
        "domain",
        "target_market",
        "what_to_understand",
        "decision",
        "innovation_altitude",
    ]
    missing_brief = [field for field in required_brief if not decision.get(field)] if isinstance(decision, dict) else required_brief
    if missing_brief:
        return result(
            current_phase=current_phase,
            state="BLOCKED",
            next_phase="A",
            reason="The reusable research brief is incomplete.",
            blockers=[f"decision.json requires {field}" for field in missing_brief],
            human_gate="Confirm supplied or explicitly provisional research-brief fields before discovery.",
        )

    trends = load_json(root, "trends.json", [])
    candidates = load_json(root, "candidates.json", [])
    pyramids = load_json(root, "pyramids.json", [])
    search_log = load_json(root, "search_log.json", [])
    missing_discovery = [
        label
        for label, value in [
            ("a trend map", trends),
            ("candidate or referral paths", candidates),
            ("a search log", search_log),
        ]
        if not nonempty_list(value)
    ]
    if missing_discovery:
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="B",
            reason="Trend-first discovery is the smallest next move.",
            blockers=[f"Phase B has not yet recorded {item}" for item in missing_discovery],
        )

    sources = load_json(root, "sources.json", [])
    evidence = load_json(root, "evidence.json", [])
    episodes = load_json(root, "lu_episodes.json", [])
    missing_evidence = [
        label
        for label, value in [
            ("source records", sources),
            ("atomic evidence", evidence),
            ("Lead User Need Episodes", episodes),
        ]
        if not nonempty_list(value)
    ]
    if missing_evidence:
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="C",
            reason="Inspect the next bounded evidence batch before judging sufficiency.",
            blockers=[f"Phase C has not yet recorded {item}" for item in missing_evidence],
        )

    if manifest.get("mode") == "SCOUT":
        outcome = load_json(root, "decision_outcome.json", {})
        if not isinstance(outcome, dict) or not outcome.get("status"):
            return result(
                current_phase=current_phase,
                state="READY",
                next_phase="G",
                reason="The bounded SCOUT evidence pass is ready to answer whether further investigation is warranted.",
                blockers=[],
                human_gate="The agent prepares STOP, INVESTIGATE, or ESCALATE evidence; the human authorizes consequential follow-through.",
            )
        if manifest.get("study_status") != "COMPLETE":
            return result(
                current_phase=current_phase,
                state="READY",
                next_phase="H",
                reason="The SCOUT decision is recorded; validate and render the compact supported deliverable.",
                blockers=[],
                human_gate="Choose whether a proposed research-to-frame handoff is useful.",
            )
        return result(
            current_phase=current_phase,
            state="COMPLETE",
            next_phase=None,
            reason="The SCOUT study is complete. Its implications do not become accepted planning truth automatically.",
            blockers=[],
            human_gate="Accept, reject, or revise the proposed research-to-frame implications before invoking framing.",
            conditional_next_skill="framing-doc",
        )

    sufficiency = load_json(root, "sufficiency.json", {})
    freeze = load_json(root, "freeze.json", {})
    sufficiency_status = sufficiency.get("status") if isinstance(sufficiency, dict) else None
    dimensions = sufficiency.get("dimensions", {}) if isinstance(sufficiency, dict) else {}
    if sufficiency_status == "INSUFFICIENT":
        insufficient = {
            name
            for name, value in dimensions.items()
            if isinstance(value, dict) and value.get("status") == "INSUFFICIENT"
        }
        next_phase = "B" if insufficient.intersection(DISCOVERY_DIMENSIONS) else "C"
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase=next_phase,
            reason=(
                "Research sufficiency requires another discovery branch."
                if next_phase == "B"
                else "Research sufficiency requires another bounded evidence batch."
            ),
            blockers=[f"Insufficient dimension: {name}" for name in sorted(insufficient)],
        )
    if sufficiency_status != "SUFFICIENT" or not isinstance(freeze, dict) or freeze.get("status") != "FROZEN":
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="D",
            reason="Assess decision-relative sufficiency and freeze only if every dimension is sufficient.",
            blockers=[] if sufficiency_status == "NOT_ASSESSED" else ["Evidence Freeze is not complete"],
            human_gate="Do not freeze evidence merely because a source or user quota has been reached.",
        )

    findings = load_json(root, "findings.json", [])
    needs = load_json(root, "needs.json", [])
    principles = load_json(root, "principles.json", [])
    if not (nonempty_list(findings) and nonempty_list(needs) and nonempty_list(principles)):
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="E",
            reason="Frozen evidence is ready for interpretation into findings, needs, and principles.",
            blockers=[],
        )

    unassessed_needs = [
        row.get("need_id", "<unknown>")
        for row in needs
        if isinstance(row, dict) and row.get("concept_gate_status", "NOT_ASSESSED") == "NOT_ASSESSED"
    ]
    if unassessed_needs:
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="E",
            reason="Interpretation is incomplete until each need has an explicit Concept Generation Gate result.",
            blockers=[f"Concept Generation Gate not assessed: {need_id}" for need_id in unassessed_needs],
        )

    passing_need_ids = {
        row.get("need_id")
        for row in needs
        if isinstance(row, dict) and row.get("concept_gate_status") == "PASS"
    }
    criteria = load_json(root, "fit_criteria.json", [])
    concepts = load_json(root, "concepts.json", [])
    criteria_need_ids = {row.get("need_id") for row in criteria if isinstance(row, dict)}
    concept_need_ids = {row.get("need_id") for row in concepts if isinstance(row, dict)}
    incomplete_shape = sorted(
        need_id
        for need_id in passing_need_ids
        if need_id not in criteria_need_ids or need_id not in concept_need_ids
    )
    if incomplete_shape:
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="F",
            reason="At least one supported need passed the Concept Generation Gate and requires Fit Check shaping.",
            blockers=[f"Passing need lacks requirements or materially distinct mechanisms: {need_id}" for need_id in incomplete_shape],
        )

    outcome = load_json(root, "decision_outcome.json", {})
    if not isinstance(outcome, dict) or not outcome.get("status"):
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="G",
            reason=(
                "No need passed the Concept Generation Gate; return to the original decision without inventing concepts."
                if not passing_need_ids
                else "The evidence and any justified concept work are ready for a decision outcome."
            ),
            blockers=[],
            human_gate="The agent prepares decision-ready evidence; the human makes or authorizes the product decision.",
        )

    if manifest.get("study_status") != "COMPLETE":
        return result(
            current_phase=current_phase,
            state="READY",
            next_phase="H",
            reason="The decision is recorded; render and verify only the proportionate supported deliverables.",
            blockers=[],
            human_gate="Choose whether additional derived formats or a research-to-frame handoff are useful.",
        )

    return result(
        current_phase=current_phase,
        state="COMPLETE",
        next_phase=None,
        reason="The research study is complete. Its implications do not become accepted planning truth automatically.",
        blockers=[],
        human_gate="Accept, reject, or revise the proposed research-to-frame implications before invoking framing.",
        conditional_next_skill="framing-doc",
    )


def render_text(value: dict[str, Any]) -> str:
    blockers = value["blockers"] or ["None"]
    next_move = value["recommended_command"] or "None"
    if value.get("conditional_next_skill"):
        next_move = f"{next_move}; after explicit acceptance, {value['conditional_next_skill']}"
    lines = [
        f"Research status: {value['state']}",
        f"Current phase: {value['current_phase']}",
        f"Next recommended move: {next_move}",
        f"Why: {value['reason']}",
        "Required inputs or unresolved blockers:",
        *[f"- {item}" for item in blockers],
        f"Human gate: {value['human_gate']}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Path to the Lead User study workspace")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    try:
        value = recommend(Path(args.workspace))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(value, indent=2) if args.json else render_text(value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
