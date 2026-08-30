# Phase handoff contract

Use this contract after every Lead User research phase and whenever the user asks
what to do next.

For file-backed studies, run `scripts/next_research_move.py` against the study
workspace after writing and validating the current phase artifacts. Do not infer
readiness from prose, invocation history, or source count alone.

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
- Do not enter Phase E before decision-relative sufficiency and Evidence Freeze.
- Phase E records `manifest.interpretation_completion = COMPLETED` after considering
  the full frozen corpus, including when the supported result is an explicitly empty
  negative interpretation. Empty output arrays alone do not prove Phase E ran.
- Do not enter Phase F unless at least one need passes every Concept Generation
  Gate check.
- Phase F first constructs a PROVISIONAL `x → f() → y` shaping frame. Stop with
  HUMAN_REVIEW until a human accepts or revises it; do not derive PASS requirements
  or evaluate candidate shapes against a provisional frame.
- If no need passes, proceed to Phase G without generating concepts merely to
  complete the sequence.
- Phase G prepares decision-ready evidence; it does not make the human's product
  decision unless the human explicitly authorizes that decision.
- A mechanism may be SELECTED only with `selected_by_human = true` and a non-empty
  provenance note. Output must distinguish selected mechanisms from candidates.
- Phase H is proportionate. Do not create PDF, HTML, or other formats merely
  because they exist.
- Completion does not automatically invoke framing. Propose a research-to-frame
  handoff and stop for explicit human acceptance.

Cross-platform invocation:

- Claude Code and Gemini CLI: name the corresponding `/lead-user-*` command.
- Codex and skill-capable agents: name `lead-user-research`, the next phase, and
  the workspace.
- Plain chat: name the phase and provide the portable prompt continuation.
