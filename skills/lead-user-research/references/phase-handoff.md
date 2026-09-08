# Phase handoff contract

Use this contract after every Lead User research phase and whenever the user asks
what to do next.

For file-backed studies, run `scripts/next_research_move.py` against the study
workspace after writing and validating the current phase artifacts. Do not infer
readiness from prose, invocation history, or source count alone.

For Phase F planning authority and package ownership, read
`../PACKAGE_BOUNDARY.md`.

Return:

```text
Research status: READY | BLOCKED | HUMAN_REVIEW | COMPLETE
Completed phase: A | B | C | D | E | F | G | H
Next recommended move: command, canonical skill + phase, or None
Why: decision-relevant reason
Required inputs or unresolved blockers:
- exact blocker or None
Human gate: exact decision required or None
```

Rules:

- Recommend one next move, not the rest of the pipeline.
- A Phase D insufficiency result returns to the smallest relevant discovery or
  evidence move with `sufficiency.repair_status = REQUIRED`. Phase B/C marks the
  bounded repair COMPLETED; the controller then returns to Phase D for reassessment
  instead of repeating the repair phase indefinitely.
- Phase C records `manifest.evidence_completion = COMPLETED` after the bounded pass,
  including an honest empty result. Empty arrays alone do not prove Phase C ran.
- Do not enter Phase E before decision-relative sufficiency and Evidence Freeze.
- Phase E records `manifest.interpretation_completion = COMPLETED` after considering
  the full frozen corpus, including when the supported result is an explicitly empty
  negative interpretation. Empty output arrays alone do not prove Phase E ran.
- Do not enter Phase F unless at least one need passes every Concept Generation
  Gate check.
- Phase F first constructs a PROVISIONAL `x → f() → y` **research concept-evaluation
  frame**. Stop with HUMAN_REVIEW until a human accepts or revises it; do not derive
  PASS research-local fit criteria or evaluate candidate mechanisms against a
  provisional frame.
- `SF## ACCEPTED`, research `R##`, and `M## SELECTED` are research-local states.
  They do not satisfy planning frame acceptance, project requirement acceptance,
  Appetite, selected project shape, selected-design reconciliation, active scope,
  or build authorization.
- If no need passes, proceed to Phase G without generating concepts merely to
  complete the sequence.
- Phase G prepares decision-ready evidence; it does not make the human's product
  decision unless the human explicitly authorizes that decision.
- A mechanism may be SELECTED inside the research study only with
  `selected_by_human = true` and a non-empty provenance note. Output must label
  that as research-local selection and distinguish it from project shape selection.
- Phase H is proportionate. Do not create PDF, HTML, or other formats merely
  because they exist.
- Every mode completes Phase H's final validation and canonical Decision Brief;
  proportionality controls only the extra derived formats.
- Completion does not automatically invoke framing or shaping. Propose a research-to-planning
  handoff and stop for explicit human acceptance.
- After an accepted handoff, choose the smallest planning move rather than restarting
  the workflow mechanically: E-only evidence normally routes to `framing-doc`; useful
  Phase F material normally routes directly to collaborative `shaping` as **Working**
  planning material with research provenance preserved.
- Do not ask the human to recreate or reselect Phase F material solely because the
  package boundary was crossed. Revisit a frame or mechanism decision only when a
  planning promotion gate remains unmet or a consequential planning input differs,
  such as project requirements, Appetite/cut line, project boundary, material
  evidence, or viable alternatives.

Cross-platform invocation:

- Claude Code and Gemini CLI: name the corresponding `/lead-user-*` command.
- Codex and skill-capable agents: name `lead-user-research`, the next phase, and
  the workspace.
- Plain chat: name the phase and provide the portable prompt continuation.
