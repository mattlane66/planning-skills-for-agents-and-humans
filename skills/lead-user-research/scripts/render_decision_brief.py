#!/usr/bin/env python3
"""Render the canonical human-facing Decision Brief from structured Lead User state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(root: Path, name: str, default: Any) -> Any:
    path = root / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def bullets(values: list[Any], empty: str = "None recorded.") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(f"- {value}" for value in values)


def indexed(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {row.get(key): row for row in rows if isinstance(row, dict) and row.get(key)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    root = Path(args.workspace)
    manifest = load(root, "manifest.json", {})
    decision = load(root, "decision.json", {})
    outcome = load(root, "decision_outcome.json", {})
    coverage = load(root, "coverage.json", {})
    findings = load(root, "findings.json", [])
    episodes = load(root, "lu_episodes.json", [])
    needs = load(root, "needs.json", [])
    criteria = load(root, "fit_criteria.json", [])
    concepts = load(root, "concepts.json", [])

    finding_by_id = indexed(findings, "finding_id")
    lu_by_id = indexed(episodes, "lu_id")
    need_by_id = indexed(needs, "need_id")

    lines: list[str] = []
    lines += ["# Lead User Research — Decision Brief", ""]
    lines += ["## Decision", "", str(decision.get("decision") or "UNKNOWN"), ""]
    status = outcome.get("status") or "NOT_DECIDED"
    lines += [f"## Recommendation — {status}", "", str(outcome.get("recommendation") or "No recommendation recorded."), ""]
    lines += ["## Why", "", bullets(outcome.get("why", [])), ""]

    lines += ["## Decisive evidence", ""]
    decisive_rows: list[str] = []
    for ref in outcome.get("decisive_finding_refs", []):
        row = finding_by_id.get(ref, {})
        decisive_rows.append(f"**{ref}** — {row.get('claim', 'Missing finding text')}")
    for ref in outcome.get("decisive_lu_refs", []):
        row = lu_by_id.get(ref, {})
        decisive_rows.append(
            f"**{ref}** — {row.get('need_statement', 'Missing LU need statement')} "
            f"({row.get('user_entity') or row.get('user/entity') or 'entity not named'})"
        )
    lines += [bullets(decisive_rows, "No decisive evidence refs recorded."), ""]

    lines += ["## Critical uncertainty", "", bullets(outcome.get("critical_uncertainties", [])), ""]
    lines += ["## Action now", "", bullets(outcome.get("action_now", [])), ""]
    lines += ["## What would change this decision", "", bullets(outcome.get("change_conditions", [])), ""]

    lines += ["## What the evidence supports", "", bullets(outcome.get("what_evidence_supports", [])), ""]
    lines += ["## What the evidence does not support", "", bullets(outcome.get("what_evidence_does_not_support", [])), ""]
    lines += ["## What could make us wrong", "", bullets(outcome.get("contradictions", [])), ""]

    shaped = [n for n in needs if n.get("concept_gate_status") == "PASS"]
    if shaped or criteria or concepts:
        lines += ["## Opportunity shaping", ""]
        for need in shaped:
            nid = need.get("need_id")
            lines += [f"### {nid} — {need.get('statement', 'Need statement missing')}", ""]
            reqs = [r for r in criteria if r.get("need_id") == nid]
            mechs = [m for m in concepts if m.get("need_id") == nid]
            if reqs:
                lines += ["**Fitness conditions**", ""]
                lines += [bullets([f"{r.get('requirement_id')} — {r.get('requirement')}" for r in reqs]), ""]
            if mechs:
                lines += ["**Candidate mechanisms**", ""]
                lines += [bullets([f"{m.get('concept_id')} — {m.get('mechanism')}" for m in mechs]), ""]

    lines += ["## Discovery coverage", ""]
    lines += ["### Likely overrepresented", "", bullets(coverage.get("likely_overrepresented", [])), ""]
    lines += ["### Likely underrepresented", "", bullets(coverage.get("likely_underrepresented", [])), ""]
    lines += ["### Inaccessible / private areas", "", bullets(coverage.get("inaccessible_or_private", [])), ""]
    lines += ["### Corrective discovery", "", bullets(coverage.get("corrective_actions", [])), ""]

    lines += ["## Recommended next evidence", "", bullets(outcome.get("recommended_next_evidence", [])), ""]
    lines += ["## Priority human review", "", bullets(outcome.get("priority_human_review", [])), ""]

    lines += ["## Study execution", ""]
    lines += [
        f"- Execution level: {manifest.get('study_execution_level', 'UNKNOWN')}",
        f"- Basis: {', '.join(manifest.get('study_execution_basis', [])) or 'none recorded'}",
        "",
    ]

    lines += ["## Verification state", ""]
    lines += [
        f"- Human review: {manifest.get('human_review', 'UNKNOWN')}",
        f"- Deterministic validation: {manifest.get('deterministic_validation', 'UNKNOWN')}",
        f"- Interpretive status: {manifest.get('interpretive_status', 'UNKNOWN')}",
        f"- Model checklist: {manifest.get('model_check', 'UNKNOWN')}",
        "",
    ]

    rendered = "\n".join(lines).rstrip() + "\n"
    output = Path(args.output) if args.output else root / "outputs" / "decision-brief.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"Rendered Decision Brief to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
