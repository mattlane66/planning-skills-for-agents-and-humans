#!/usr/bin/env python3
"""Render a privacy-safe, evidence-linked Lead User Decision Brief."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from report_safety import identity_pattern, markdown_escape, safe_outward_url
from study_fingerprint import study_fingerprint


def load(root: Path, name: str, default: Any) -> Any:
    path = root / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def bullets(
    values: list[Any],
    empty: str = "None recorded.",
    *,
    trusted_markdown: bool = False,
) -> str:
    if not values:
        return f"- {markdown_escape(empty)}"
    return "\n".join(
        f"- {value if trusted_markdown else markdown_escape(value)}"
        for value in values
    )


def safe_join(values: Any, separator: str = ", ", empty: str = "none") -> str:
    if not isinstance(values, list) or not values:
        return markdown_escape(empty)
    return separator.join(markdown_escape(value) for value in values)


def safe_token(value: object) -> str:
    token = str(value)
    if re.fullmatch(r"[A-Za-z0-9_-]+", token):
        return token
    return markdown_escape(token)


def indexed(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {
        row[key]: row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get(key), str) and row.get(key)
    }


def ref_link(ref: str) -> str:
    anchor = re.sub(r"[^a-z0-9_-]", "", ref.lower()) or "record"
    return f"[{markdown_escape(ref)}](#{anchor})"


def public_lu_label(row: dict[str, Any]) -> str:
    label = row.get("public_label")
    if isinstance(label, str) and label.strip():
        return label.strip()
    return "Anonymized Lead User episode"


def source_citation(source: dict[str, Any]) -> str:
    title = str(source.get("title") or source.get("source_id") or "Source")
    url = safe_outward_url(source.get("url"))
    if source.get("outward_citation_allowed") is True and url:
        return f"[{markdown_escape(title)}]({url})"
    return f"{markdown_escape(source.get('source_id', 'Source'))} (citation withheld)"


def render_action(action: dict[str, Any]) -> list[str]:
    action_id = markdown_escape(action.get("action_id", "A?"))
    lines = [f"### {action_id} — {markdown_escape(action.get('action', 'Action missing'))}", ""]
    lines += [
        f"- **Owner:** {markdown_escape(action.get('owner', 'UNKNOWN'))}",
        f"- **Timebox:** {markdown_escape(action.get('timebox', 'UNKNOWN'))}",
        f"- **Deliverable:** {markdown_escape(action.get('deliverable', 'UNKNOWN'))}",
        f"- **Success condition:** {markdown_escape(action.get('success_condition', 'UNKNOWN'))}",
        f"- **Stop condition:** {markdown_escape(action.get('stop_condition', 'UNKNOWN'))}",
        f"- **Decision at end:** {markdown_escape(action.get('decision_at_end', 'UNKNOWN'))}",
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
        replacement = markdown_escape(public_lu_label(row))
        rendered = identity_pattern(internal).sub(lambda _match: replacement, rendered)
        escaped_internal = markdown_escape(internal)
        if escaped_internal != internal:
            rendered = identity_pattern(escaped_internal).sub(
                lambda _match: replacement,
                rendered,
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
    shaping_frames = load(root, "shaping_frame.json", [])
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
    if manifest.get("fixture_type") == "SYNTHETIC_REFERENCE":
        lines += [
            "> **Synthetic reference fixture — not empirical human or market evidence.**",
            "",
        ]
    lines += ["## Decision", "", markdown_escape(decision.get("decision") or "UNKNOWN"), ""]
    status = outcome.get("status") or "NOT_DECIDED"
    lines += [
        f"## Recommendation — {safe_token(status)}",
        "",
        markdown_escape(outcome.get("recommendation") or "No recommendation recorded."),
        "",
    ]
    lines += ["## Why", "", bullets(outcome.get("why", [])), ""]

    lines += ["## Decisive evidence", ""]
    decisive_rows: list[str] = []
    for ref in outcome.get("decisive_finding_refs", []):
        row = finding_by_id.get(ref, {})
        decisive_rows.append(
            f"**{ref_link(ref)} — {markdown_escape(row.get('epistemic_label', 'UNKNOWN'))}** — "
            f"{markdown_escape(row.get('claim', 'Missing finding text'))}"
        )
    for ref in outcome.get("decisive_lu_refs", []):
        row = lu_by_id.get(ref, {})
        decisive_rows.append(
            f"**{ref_link(ref)} — {markdown_escape(row.get('status', 'UNKNOWN'))}** — "
            f"{markdown_escape(row.get('need_statement', 'Missing LU need statement'))} "
            f"({markdown_escape(public_lu_label(row))})"
        )
    lines += [
        bullets(
            decisive_rows,
            "No decisive evidence refs recorded.",
            trusted_markdown=True,
        ),
        "",
    ]

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
                    f"{safe_token(row.get('hypothesis_id', 'H?'))} — {safe_token(row.get('status', 'UNTESTED'))} — "
                    f"{markdown_escape(row.get('claim', 'Missing hypothesis'))}"
                    + (
                        f" — {markdown_escape(row.get('update_rationale'))}"
                        if row.get("update_rationale")
                        else ""
                    )
                    for row in hypotheses
                    if isinstance(row, dict)
                ],
                trusted_markdown=True,
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
                    f"{safe_token(row.get('observability_id', 'O?'))} — {safe_token(row.get('status', 'UNKNOWN'))} — "
                    f"{markdown_escape(row.get('question', 'Missing question'))}"
                    + (
                        f" — Fieldwork: {markdown_escape(row.get('fieldwork_referral'))}"
                        if row.get("fieldwork_referral")
                        else ""
                    )
                    for row in critical_observability
                ],
                trusted_markdown=True,
            ),
            "",
        ]

    if analysis_runs:
        lines += ["## AI analysis validation", ""]
        lines += [
            bullets(
                [
                    f"{safe_token(row.get('analysis_run_id', 'AR?'))} — "
                    f"{markdown_escape(row.get('model', 'UNKNOWN'))} {markdown_escape(row.get('model_version', ''))}".strip()
                    + f" — sampled validation: "
                    f"{safe_token((row.get('sampled_validation') or {}).get('status', 'NOT_ASSESSED'))}"
                    for row in analysis_runs
                    if isinstance(row, dict)
                    and isinstance(row.get("sampled_validation") or {}, dict)
                ],
                trusted_markdown=True,
            ),
            "",
        ]

    shaped = [
        need
        for need in needs
        if isinstance(need, dict) and need.get("concept_gate_status") == "PASS"
    ]
    if shaped or criteria or concepts:
        lines += ["## Opportunity shaping", ""]
        for need in shaped:
            need_id = need.get("need_id")
            lines += [
                f"### {safe_token(need_id)} — {markdown_escape(need.get('statement', 'Need statement missing'))}",
                "",
            ]
            frames = [
                row
                for row in shaping_frames
                if isinstance(row, dict) and row.get("need_id") == need_id
            ]
            reqs = [
                row
                for row in criteria
                if isinstance(row, dict) and row.get("need_id") == need_id
            ]
            mechanisms = [
                row
                for row in concepts
                if isinstance(row, dict) and row.get("need_id") == need_id
            ]
            passing_reqs = [row for row in reqs if row.get("status") == "PASS"]
            nonpassing_reqs = [row for row in reqs if row.get("status") != "PASS"]
            if frames:
                lines += ["**Shaping frame (x → f() → y)**", ""]
                for frame in frames:
                    x = frame.get("x") if isinstance(frame.get("x"), dict) else {}
                    f_value = frame.get("f") if isinstance(frame.get("f"), dict) else {}
                    y = frame.get("y") if isinstance(frame.get("y"), dict) else {}
                    lines += [
                        f"- Frame: {safe_token(frame.get('frame_id', 'SF?'))} — {safe_token(frame.get('status', 'UNKNOWN'))}",
                        f"- x — trigger/context: {markdown_escape(x.get('trigger_or_context', 'UNKNOWN'))}",
                        f"- x — current approach: {markdown_escape(x.get('current_approach', 'UNKNOWN'))}",
                        f"- x — current result: {markdown_escape(x.get('current_result', 'UNKNOWN'))}",
                        f"- x — breakdowns: {safe_join(x.get('breakdowns', []), '; ', 'none recorded')}",
                        f"- f(): {safe_token(f_value.get('status', 'UNKNOWN'))}",
                        f"- y — desired outcome: {markdown_escape(y.get('desired_outcome', 'UNKNOWN'))}",
                        f"- Gap: {markdown_escape(frame.get('gap', 'UNKNOWN'))}",
                        f"- Boundaries: {safe_join(frame.get('boundaries', []), '; ', 'none recorded')}",
                        f"- Human acceptance: {safe_token(frame.get('accepted_by_human', False))}",
                        f"- Acceptance note: {markdown_escape(frame.get('acceptance_note') or 'none recorded')}",
                        "",
                    ]
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
                lines += ["**Candidate and selected mechanisms**", ""]
                for mechanism in mechanisms:
                    lines += [
                        f"#### {safe_token(mechanism.get('concept_id', 'M?'))} — {markdown_escape(mechanism.get('mechanism'))}",
                        "",
                        f"- Selection status: {safe_token(mechanism.get('selection_status', 'UNKNOWN'))}",
                        f"- Selected by human: {safe_token(mechanism.get('selected_by_human', False))}",
                        f"- Selection note: {markdown_escape(mechanism.get('selection_note') or 'none recorded')}",
                        f"- Rotation status: {safe_token(mechanism.get('rotation_status', 'UNKNOWN'))}",
                        f"- Requirements: {safe_join(mechanism.get('requirement_ids', []))}",
                        f"- Assumptions: {safe_join(mechanism.get('assumptions', []), '; ', 'none recorded')}",
                        f"- Risks: {safe_join(mechanism.get('risks', []), '; ', 'none recorded')}",
                        f"- Evidence needed next: {safe_join(mechanism.get('evidence_needed_next', []), '; ', 'none recorded')}",
                        "",
                    ]
                    parts = mechanism.get("parts", [])
                    if isinstance(parts, list) and parts:
                        lines += ["**Rotated parts × requirements**", ""]
                        lines += [
                            bullets(
                                [
                                    f"{part.get('part_id', 'P?')} — {part.get('mechanism', 'Missing mechanism')} — requirements: {', '.join(part.get('requirement_ids', [])) or 'none'}"
                                    for part in parts
                                    if isinstance(part, dict)
                                ]
                            ),
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
        f"- Fixture type: {safe_token(manifest.get('fixture_type', 'UNKNOWN'))}",
        f"- Run mode: {safe_token(manifest.get('mode', 'UNKNOWN'))}",
        f"- Current phase: {safe_token(manifest.get('phase', 'UNKNOWN'))}",
        f"- Study status: {safe_token(manifest.get('study_status', 'UNKNOWN'))}",
        f"- Execution level: {safe_token(manifest.get('study_execution_level', 'UNKNOWN'))}",
        f"- Basis: {safe_join(manifest.get('study_execution_basis', []), ', ', 'none recorded')}",
        "",
    ]

    lines += ["## Verification state", ""]
    lines += [
        f"- Human review: {safe_token(manifest.get('human_review', 'UNKNOWN'))}",
        f"- Deterministic validation: {safe_token(manifest.get('deterministic_validation', 'UNKNOWN'))}",
        f"- Interpretation completion: {safe_token(manifest.get('interpretation_completion', 'UNKNOWN'))}",
        f"- Interpretive status: {safe_token(manifest.get('interpretive_status', 'UNKNOWN'))}",
        f"- Model checklist: {safe_token(manifest.get('model_check', 'UNKNOWN'))}",
        f"- State fingerprint: {study_fingerprint(root)}",
        "",
    ]

    lines += ["## Evidence drill-down", ""]
    drill_evidence_refs: list[str] = []
    for ref in outcome.get("decisive_finding_refs", []):
        row = finding_by_id.get(ref, {})
        lines += [f"### {safe_token(ref)}", ""]
        lines += [
            f"- Epistemic label: {markdown_escape(row.get('epistemic_label', 'UNKNOWN'))}",
            f"- Claim: {markdown_escape(row.get('claim', 'Missing finding text'))}",
            f"- Confidence rationale: {markdown_escape(row.get('confidence_rationale', 'None recorded'))}",
            f"- LU refs: {safe_join(row.get('lu_refs', []))}",
            f"- Contradictions: {safe_join(row.get('contradictions', []), '; ', 'none recorded')}",
            "",
        ]
        drill_evidence_refs.extend(row.get("evidence_refs", []))

    for ref in outcome.get("decisive_lu_refs", []):
        row = lu_by_id.get(ref, {})
        lines += [f"### {safe_token(ref)}", ""]
        lines += [
            f"- Public label: {markdown_escape(public_lu_label(row))}",
            f"- Status: {markdown_escape(row.get('status', 'UNKNOWN'))}",
            f"- Trend: {markdown_escape(row.get('trend_id', 'UNKNOWN'))}",
            f"- Emerging need: {markdown_escape(row.get('need_statement', 'UNKNOWN'))}",
            f"- Advancement indicator: {markdown_escape(row.get('advancement_indicator', 'UNKNOWN'))}",
            f"- LU1 rationale: {markdown_escape(row.get('lu1_rationale', 'UNKNOWN'))}",
            f"- Benefit signal: {markdown_escape(row.get('benefit_signal', 'UNKNOWN'))}",
            f"- LU2 rationale: {markdown_escape(row.get('lu2_rationale', 'UNKNOWN'))}",
            f"- Qualification caveats: {safe_join(row.get('qualification_caveats', []), '; ', 'none recorded')}",
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
        lines += [f"#### {safe_token(ref)}", ""]
        lines += [
            f"- Public summary: {markdown_escape(row.get('public_summary') or 'See the structured evidence record; raw source content is not reproduced outwardly.')}",
            f"- Evidence type: {markdown_escape(row.get('evidence_type', 'UNKNOWN'))}",
            f"- Evidence basis: {safe_token(row.get('evidence_basis', 'UNKNOWN'))}",
            f"- Source: {source_citation(source)}",
            f"- Source coverage: {markdown_escape(source.get('coverage', 'UNKNOWN'))}",
            f"- Source ref: {markdown_escape(row.get('source_id', 'UNKNOWN'))}",
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
