---
description: Start or resume one valid phase of a Lead User research study from persisted state.
argument-hint:
- research brief
- study workspace
- or continuation request
disable-model-invocation: true
---

Read `lead-user-research/SKILL.md` and
`lead-user-research/references/phase-handoff.md` first.

User request and source context:

$ARGUMENTS

If no study exists, begin Phase A and create a proportionate research brief. If a
file-backed study exists, run its deterministic next-move controller and perform
only the recommended phase. Do not advance by invocation history or source count.

Use real sources when conducting actual research. Preserve exact source locations,
coverage, instruction-risk, lineage, evidence references, privacy controls, and
outward-citation eligibility. Never substitute the synthetic assurance fixture for
real research.

End with the standardized phase handoff and exactly one next move or stop condition.
