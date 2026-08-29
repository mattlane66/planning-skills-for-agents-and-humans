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
  evidence move.
- Do not enter Phase E before decision-relative sufficiency and Evidence Freeze.
- Do not enter Phase F unless at least one need passes every Concept Generation
  Gate check.
- If no need passes, proceed to Phase G without generating concepts merely to
  complete the sequence.
- Phase G prepares decision-ready evidence; it does not make the human's product
  decision unless the human explicitly authorizes that decision.
- Phase H is proportionate. Do not create PDF, HTML, or other formats merely
  because they exist.
- Completion does not automatically invoke framing. Propose a research-to-frame
  handoff and stop for explicit human acceptance.

Cross-platform invocation:

- Claude Code and Gemini CLI: name the corresponding `/lead-user-*` command.
- Codex and skill-capable agents: name `lead-user-research`, the next phase, and
  the workspace.
- Plain chat: name the phase and provide the portable prompt continuation.
