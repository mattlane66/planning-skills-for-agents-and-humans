---
description: Run fit checks and reverse fit checks across existing shapes without selecting a direction.
argument-hint:
- shaping file
- criteria
- shapes
- notes
- or selected comparison set
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this slash command when the user has criteria and candidate shapes and wants to see which shape actually fits before choosing.

Also read `docs/human-decision-gates.md`. Confirm Gate 2A: Appetite set, and stop before Gate 3: Shape selected.

User request and source context:

$ARGUMENTS

Produce or update the Fit Check and Reverse Fit Check sections of a shaping artifact.

Before checking, verify that the artifact has:

- requirements / criteria stated independently of any one mechanism
- an accepted appetite and cut line
- at least one candidate shape, plus `CURRENT` when applicable
- shape parts concrete enough to judge, or clearly marked with `⚠️`

If criteria are missing, recommend `/criteria`.
If appetite is missing, recommend `/appetite`.
If shapes are missing, recommend `/sketch-shapes`.

Fit check rules:

- compare requirements against the available shapes
- use full requirement text in the table
- use binary values only: `✅` or `❌`
- treat unknown or flagged mechanisms as not yet passing
- put explanations below the table, not inside shape cells
- add an appetite-fit comparison that names required cuts and unresolved spikes for each viable shape

Reverse fit check rules:

- check whether every selected or candidate shape part serves at least one requirement
- mark unjustified mechanisms as `❌`, Cut, or Needs requirement
- do not let implementation convenience create untracked scope

Do not select a direction unless the user explicitly gives the selection.
Do not breadboard.
Do not write production code.

End with a decision-readiness note:

- strongest passing shape, if any
- whether each viable shape fits the accepted appetite and cut line
- failed or undecided requirement rows
- unjustified shape parts
- flagged unknowns or spikes needed before selection
- whether the human can now use `/select-shape`
