#!/usr/bin/env python3
"""Render a privacy-safe, evidence-linked Lead User Decision Brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from study_fingerprint import study_fingerprint


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


def ref_link(ref: str) -> str:
    return f"[{ref}](#{ref.lower()})"


def public_lu_label(row: dict[str, Any]) -> str:
    label = row.get("public_label")
    if isinstance(label, str) and label.strip():
        return label.strip()
    return "Anonymized Lead User episode"


def source_citation(source: dict[str, Any]) -> str:
    title = str(source.get("title") or source.get("source_id") or "Source")
    url = source.get("url")
    if source.get("outward_citation_allowed") is True and isinstance(url, str) and url:
        return f"[{title}]({url})"
    return f"{source.get('source_id', 'Source')} (citation withheld)"


def render_action(action: dict[str, Any]) -> list[str]:
    action_id = action.get("action_id", "A?")
    lines = [f"### {action_id} — {action.get('action', 'Action missing')}", ""]
    lines += [
        f"- **Owner:** {action.get('owner', 'UNKNOWN')}",
        f"- **Timebox:** {action.get('timebox', 'UNKNOWN')}",
        f"- **Deliverable:** {action.get('deliverable', 'UNKNOWN')}",
        f"- **Success condition:** {action.get('success_condition', 'UNKNOWN')}",
        f"- **Stop condition:** {action.get('stop_condition', 'UNKNOWN')}",
        f"- **Decision at end:** {action.get('decision_at_end', 'UNKNOWN')}",
        "",
        "**Evidence to collect**",
        "",
        bullets(action.get("evidence_to_collect", [])),
        "",
    ]
    return lines


def redact_private_entities(rendered: str, episodes: list[dict[str, Any]]) -> str:
    """Prevent an exact internal identity from leaking through free-text fields."""
    for row in episodes:
        if row.get("identity_surface_allowed") is True:
            continue
        internal = row.get("user_entity")
        if not isinstance(internal, str) or not internal.strip():
            continue
        rendered = re.sub(
            re.escape(internal.strip()),
            lambda _match: public_lu_label(row),
            rendered,
            flags=re.IGNORECASE,
        )
    return rendered


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
    evidence = load(root, "evidence.json", [])
    sources = load(root, "sources.json", [])
    needs = load(root, "needs.json", [])
    criteria = load(root, "fit_criteria.json", [])
    concepts = load(root, "concepts.json", [])
    hypotheses = load(root, "hypotheses.json", [])
    observability = load(root, "observability.json", [])
    analysis_runs = load(root, "analysis_runs.json", [])

    finding_by_id = indexed(findings, "finding_id")
    lu_by_id = indexed(episodes, "lu_id")
    evidence_by_id = indexed(evidence, "evidence_id")
    source_by_id = indexed(sources, "source_id")

    lines: list[str] = ["# Lead User Research — Decision Brief", ""]
    lines += ["## Decision", "", str(decision.get("decision") or "UNKNOWN"), ""]
    status = outcome.get("status") or "NOT_DECIDED"
    lines += [
        f"## Recommendation — {status}",
        "",
        str(outcome.get("recommendation") or "No recommendation recorded."),
        "",
    ]
    lines += ["## Why", "", bullets(outcome.get("why", [])), ""]

    lines += ["## Decisive evidence", ""]
    decisive_rows: list[str] = []
    for ref in outcome.get("decisive_finding_refs", []):
        row = finding_by_id.get(ref, {})
        decisive_rows.append(
            f"**{ref_link(ref)} — {row.get('epistemic_label', 'UNKNOWN')}** — "
            f"{row.get('claim', 'Missing finding text')}"
        )
    for ref in outcome.get("decisive_lu_refs", []):
        row = lu_by_id.get(ref, {})
        decisive_rows.append(
            f"**{ref_link(ref)} — {row.get('status', 'UNKNOWN')}** — "
            f"{row.get('need_statement', 'Missing LU need statement')} "
            f"({public_lu_label(row)})"
        )
    lines += [bullets(decisive_rows, "No decisive evidence refs recorded."), ""]

    lines += ["## Critical uncertainty", "", bullets(outcome.get("critical_uncertainties", [])), ""]
    lines += ["## Action now", ""]
    actions = outcome.get("action_now", [])
    if actions:
        for action in actions:
            if isinstance(action, dict):
                lines += render_action(action)
    else:
        lines += ["- No operational action recorded.", ""]
    lines += ["## What would change this decision", "", bullets(outcome.get("change_conditions", [])), ""]

    lines += ["## What the evidence supports", "", bullets(outcome.get("what_evidence_supports", [])), ""]
    lines += ["## What the evidence does not support", "", bullets(outcome.get("what_evidence_does_not_support", [])), ""]
    lines += ["## What could make us wrong", "", bullets(outcome.get("contradictions", [])), ""]

    if hypotheses:
        lines += ["## Hypothesis challenge", ""]
        lines += [
            bullets(
                [
                    f"{row.get('hypothesis_id', 'H?')} — {row.get('status', 'UNTESTED')} — "
                    f"{row.get('claim', 'Missing hypothesis')}"
                    + (
                        f" — {row.get('update_rationale')}"
                        if row.get("update_rationale")
                        else ""
                    )
                    for row in hypotheses
                    if isinstance(row, dict)
                ]
            ),
            "",
        ]

    critical_observability = [
        row for row in observability
        if isinstance(row, dict) and row.get("decision_critical") is True
    ]
    if critical_observability:
        lines += ["## Observability / fieldwork gate", ""]
        lines += [
            bullets(
                [
                    f"{row.get('observability_id', 'O?')} — {row.get('status', 'UNKNOWN')} — "
                    f"{row.get('question', 'Missing question')}"
                    + (
                        f" — Fieldwork: {row.get('fieldwork_referral')}"
                        if row.get("fieldwork_referral")
                        else ""
                    )
                    for row in critical_observability
                ]
            ),
            "",
        ]

    if analysis_runs:
        lines += ["## AI analysis validation", ""]
        lines += [
            bullets(
                [
                    f"{row.get('analysis_run_id', 'AR?')} — "
                    f"{row.get('model', 'UNKNOWN')} {row.get('model_version', '')}".strip()
                    + f" — sampled validation: "
                    f"{(row.get('sampled_validation') or {}).get('status', 'NOT_ASSESSED')}"
                    for row in analysis_runs
                    if isinstance(row, dict)
                ]
            ),
            "",
        ]

    shaped = [need for need in needs if need.get("concept_gate_status") == "PASS"]
    if shaped or criteria or concepts:
        lines += ["## Opportunity shaping", ""]
        for need in shaped:
            need_id = need.get("need_id")
            lines += [f"### {need_id} — {need.get('statement', 'Need statement missing')}", ""]
            reqs = [row for row in criteria if row.get("need_id") == need_id]
            mechanisms = [row for row in concepts if row.get("need_id") == need_id]
            passing_reqs = [row for row in reqs if row.get("status") == "PASS"]
            nonpassing_reqs = [row for row in reqs if row.get("status") != "PASS"]
            lines += ["**Passing fitness conditions**", ""]
            lines += [
                bullets(
                    [
                        f"{row.get('requirement_id')} — {row.get('requirement')}"
                        for row in passing_reqs
                    ],
                    "No PASS fitness conditions recorded.",
                ),
                "",
            ]
            if nonpassing_reqs:
                lines += ["**Provisional or failed criteria**", ""]
                lines += [
                    bullets(
                        [
                            f"{row.get('requirement_id')} — {row.get('status')} — "
                            f"{row.get('requirement')}"
                            for row in nonpassing_reqs
                        ]
                    ),
                    "",
                ]
            if mechanisms:
                lines += ["**Candidate mechanisms — not selected solutions**", ""]
                for mechanism in mechanisms:
                    lines += [
                        f"#### {mechanism.get('concept_id')} — {mechanism.get('mechanism')}",
                        "",
                        f"- Requirements: {', '.join(mechanism.get('requirement_ids', [])) or 'none'}",
                        f"- Assumptions: {'; '.join(mechanism.get('assumptions', [])) or 'none recorded'}",
                        f"- Risks: {'; '.join(mechanism.get('risks', [])) or 'none recorded'}",
                        f"- Evidence needed next: {'; '.join(mechanism.get('evidence_needed_next', [])) or 'none recorded'}",
                        "",
                    ]

    lines += ["## Discovery coverage", ""]
    lines += ["### Likely overrepresented", "", bullets(coverage.get("likely_overrepresented", [])), ""]
    lines += ["### Likely underrepresented", "", bullets(coverage.get("likely_underrepresented", [])), ""]
    lines += ["### Inaccessible / private areas", "", bullets(coverage.get("inaccessible_or_private", [])), ""]
    lines += ["### Corrective discovery", "", bullets(coverage.get("corrective_actions", [])), ""]
    lines += ["### Fieldwork referrals", "", bullets(coverage.get("fieldwork_referrals", [])), ""]

    lines += ["## Recommended next evidence", "", bullets(outcome.get("recommended_next_evidence", [])), ""]
    lines += ["## Priority human review", "", bullets(outcome.get("priority_human_review", [])), ""]

    lines += ["## Study execution", ""]
    lines += [
        f"- Run mode: {manifest.get('mode', 'UNKNOWN')}",
        f"- Current phase: {manifest.get('phase', 'UNKNOWN')}",
        f"- Study status: {manifest.get('study_status', 'UNKNOWN')}",
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
        f"- State fingerprint: {study_fingerprint(root)}",
        "",
    ]

    lines += ["## Evidence drill-down", ""]
    drill_evidence_refs: list[str] = []
    for ref in outcome.get("decisive_finding_refs", []):
        row = finding_by_id.get(ref, {})
        lines += [f"### {ref}", ""]
        lines += [
            f"- Epistemic label: {row.get('epistemic_label', 'UNKNOWN')}",
            f"- Claim: {row.get('claim', 'Missing finding text')}",
            f"- Confidence rationale: {row.get('confidence_rationale', 'None recorded')}",
            f"- LU refs: {', '.join(row.get('lu_refs', [])) or 'none'}",
            f"- Contradictions: {'; '.join(row.get('contradictions', [])) or 'none recorded'}",
            "",
        ]
        drill_evidence_refs.extend(row.get("evidence_refs", []))

    for ref in outcome.get("decisive_lu_refs", []):
        row = lu_by_id.get(ref, {})
        lines += [f"### {ref}", ""]
        lines += [
            f"- Public label: {public_lu_label(row)}",
            f"- Status: {row.get('status', 'UNKNOWN')}",
            f"- Trend: {row.get('trend_id', 'UNKNOWN')}",
            f"- Emerging need: {row.get('need_statement', 'UNKNOWN')}",
            f"- Advancement indicator: {row.get('advancement_indicator', 'UNKNOWN')}",
            f"- LU1 rationale: {row.get('lu1_rationale', 'UNKNOWN')}",
            f"- Benefit signal: {row.get('benefit_signal', 'UNKNOWN')}",
            f"- LU2 rationale: {row.get('lu2_rationale', 'UNKNOWN')}",
            f"- Qualification caveats: {'; '.join(row.get('qualification_caveats', [])) or 'none recorded'}",
            "",
        ]
        drill_evidence_refs.extend(row.get("lu1_evidence", []))
        drill_evidence_refs.extend(row.get("lu2_evidence", []))

    seen: set[str] = set()
    for ref in drill_evidence_refs:
        if ref in seen:
            continue
        seen.add(ref)
        row = evidence_by_id.get(ref, {})
        source = source_by_id.get(row.get("source_id"), {})
        lines += [f"#### {ref}", ""]
        lines += [
            f"- Public summary: {row.get('public_summary') or 'See the structured evidence record; raw source content is not reproduced outwardly.'}",
            f"- Evidence type: {row.get('evidence_type', 'UNKNOWN')}",
            f"- Source: {source_citation(source)}",
            f"- Source coverage: {source.get('coverage', 'UNKNOWN')}",
            f"- Source ref: {row.get('source_id', 'UNKNOWN')}",
            "",
        ]

    rendered = "\n".join(lines).rstrip() + "\n"
    rendered = redact_private_entities(rendered, episodes)
    output = Path(args.output) if args.output else root / "outputs" / "decision-brief.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"Rendered Decision Brief to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
