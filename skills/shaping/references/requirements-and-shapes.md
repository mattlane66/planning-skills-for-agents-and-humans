# Requirements and Shapes Reference

Load this reference when requirements are hard to separate from mechanisms, an existing system needs a baseline, or shape notation needs more detail.

## Requirement smell test

For each candidate requirement, ask:

1. Would this still need to be true if the solution used a completely different interface or architecture?
2. Does it name a UI, vendor, protocol, runtime, storage method, database, or framework?
3. Is it a need, outcome, or constraint—or merely one proposed way to satisfy one?
4. Can it be rewritten without prescribing the mechanism?

Examples:

- Avoid: `Use a modal for confirmation.`
- Prefer: `People must understand the consequence before committing an irreversible action.`

- Avoid: `Persist state in SQLite.`
- Prefer: `The selected state must survive process restarts.`

- Avoid: `Use a local LLM for commands.`
- Prefer: `People can change the active configuration through natural-language input.`

A requirement may contain a hard external constraint, such as compatibility with an existing API or legal rule. State the constraint directly and cite its source.

## Requirement structure

Use stable IDs:

- top level: `R0`, `R1`, `R2`
- grouped detail: `R3.1`, `R3.2`

Prefer fewer than nine top-level requirements. Group detail instead of creating an unscannable flat list.

Statuses:

- Core goal — the central result the bet exists to produce
- Must-have — failure makes a shape unacceptable
- Nice-to-have — valuable but cuttable within appetite
- Undecided — requires evidence or a human decision
- Out — explicitly excluded from this bet

## Mechanism parking lot

When a solution idea appears before criteria or appetite are accepted, preserve it without granting it authority.

```md
## Mechanism parking lot
- Possible bulk-edit surface suggested in interview 4; not yet evaluated.
- Existing webhook path may be reusable; confirm during shape exploration.
```

The parking lot prevents useful ideas from disappearing while keeping them from becoming hidden requirements.

## Shapes

Shapes are materially different solution directions. They may later be combined, but each should initially make a distinct tradeoff visible.

Use:

- `CURRENT` for the existing system baseline
- `A`, `B`, `C` for alternative directions
- `B1`, `B2`, `B3` for mechanisms inside a direction
- `B3-A`, `B3-B` for local alternatives inside one part

Good titles characterize the approach:

- `A: Guided single-path setup`
- `B: Progressive configuration with saved drafts`
- `C: Existing workflow plus automated validation`

Weak titles hide the distinction:

- `A: Option one`
- `B: Better workflow`

## CURRENT as baseline

When changing an existing product, model enough of `CURRENT` to make deltas legible. Capture only the behavior relevant to the decision.

Use `CURRENT` to show:

- what people do today
- which existing seams or constraints matter
- what remains unchanged
- where each candidate departs from reality

Current behavior is evidence, not automatically selected future intent.

## Shape parts

A shape part should state a concrete mechanism:

- `B1: Save draft configuration after each completed section.`
- `B2: Validate required fields before advancing.`
- `B3: Publish only after an explicit review step.`

Avoid wishes:

- `B1: Make setup easier.`
- `B2: Improve reliability.`

Extract shared mechanisms when multiple shapes repeat them. This keeps comparison focused on meaningful differences.

## Flagged unknowns

Mark a mechanism with `⚠️` when its purpose is clear but the implementation or feasibility is not understood enough to count as known.

```md
| Part | Mechanism | Flag |
|---|---|:---:|
| B1 | Save draft after each section | |
| B2 | Infer missing configuration from repository evidence | ⚠️ |
```

A flagged mechanism may be justified by a requirement but cannot pass the main fit check until the relevant uncertainty is accepted or resolved.

## When to create a spike

Create a focused spike only when an unknown blocks selection or makes appetite fit unknowable. The spike should return evidence for a named decision, not a broad report.

A useful spike states:

- decision it informs
- smallest experiment or investigation
- evidence expected
- time box
- stopping condition
