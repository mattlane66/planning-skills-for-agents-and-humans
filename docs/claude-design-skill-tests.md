# Claude Design skill test prompts

Use these prompts after uploading and enabling the Planning Skills in Claude. Run them with realistic but disposable source material. The goal is to verify skill selection and behavior, not the quality of a particular product idea.

For every positive test, confirm that Claude loads the intended skill, preserves human decision gates, and does not silently advance into implementation.

## `framing-doc`

```text
Use my framing-doc skill. I have interview notes, screenshots of the current workflow, and a stakeholder request. Create a frame covering the source, trigger, current approach, current result, current problem, desired outcome, boundaries, and criteria candidates. Do not propose UI yet.
```

Expected: a frame grounded in the supplied evidence, with the present approach/result explicit and interpretation separated from source material.

## `shaping`

```text
Use my shaping skill. Turn this accepted frame into criteria and appetite, then sketch materially different solution shapes. Stop before selecting a shape and show me the human decision required.
```

Expected: requirements separated from mechanisms, an explicit appetite, and alternatives rather than one polished answer.

## `sketch-reconciliation`

```text
Use my sketch-reconciliation skill. Compare this Claude Design canvas with the accepted frame and shaping artifact. Record only observable visual evidence, proposed planning deltas, and the decision gate. Do not silently overwrite the plan.
```

Expected: mapped observations and proposed deltas, not automatic acceptance of the visual.

## `breadboarding`

```text
Use my breadboarding skill on the selected shape. Model places, user affordances, system affordances, stores, consequences, and wiring. Keep the tables authoritative and identify candidate vertical slices.
```

Expected: a `selected-design` behavioral model rather than a set of polished screens, with the selected shape, appetite, and cut line cited.

```text
Use my breadboarding skill in current-state mode. Map how this existing workflow behaves from the supplied code, tests, screenshots, and logs. Cite evidence, mark unresolved observations, and do not turn current behavior into selected future intent or slice it for implementation.
```

Expected: a descriptive `current-state` map that does not require or invent a selected direction.

## `statechart`

```text
Use my statechart skill for this accepted slice, which includes retries, cancellation, timeout, and approval. Derive the states and transitions from the breadboard and identify any missing decisions.
```

Expected: a derived state inventory and transition model that does not replace the breadboard.

## `interface-contracts`

```text
Use my interface-contracts skill for the selected slice crossing the client, API, and external service. Define inputs, outputs, branches, errors, and unresolved field-level decisions without inventing an implementation.
```

Expected: plain-language boundary contracts and explicit open questions.

## `executable-breadboards`

```text
Use my executable-breadboards skill. Turn this selected slice into a testable contract with a normal fixture, difficult fixture, ambiguous fixture, expected outputs, edge cases, and acceptance scenarios.
```

Expected: a buildable behavioral test contract, not an expanded feature set.

## `dumplink`

```text
Use my dumplink skill. Inside this selected slice, group work into vertical tasks, sequence dependencies, mark risk states, and identify appetite-based cuts. Preserve the slice boundary, exclusions, and non-goals.
```

Expected: bounded task groups and cuts rather than a generic backlog.

```text
Use my dumplink skill, but no slice has been selected yet. Show candidate groups, risks, dependencies, and slice-selection questions only. Do not create a build sequence, active task group, acceptance plan, or agent handoff.
```

Expected: pre-slice exploration that stops at candidates and returns the decision to breadboarding and the human.

## `kickoff-doc`

```text
Use my kickoff-doc skill. Create a builder-facing reference from the accepted frame, shape, breadboard, and slice. Organize it by shaped product territory, not by implementation sequence.
```

Expected: a durable orientation document, not a task plan.

## `feed-planning-context`

```text
Use my feed-planning-context skill. Prepare the smallest context packet an implementation agent needs for this slice, including authority order, execution contract, non-goals, and verification target.
```

Expected: compact bounded context, with irrelevant planning history omitted.

## `breadboard-reflection`

```text
Use my breadboard-reflection skill. Compare this implemented prototype with the accepted breadboard and selected slice. Preserve intended and current behavior separately, identify planning drift and design smells, and stop for my correction decision.
```

Expected: a factual side-by-side comparison that changes neither implementation nor plan until the human chooses explicitly.

## Automatic-selection test

Do not name a skill:

```text
I have a transcript, three screenshots of the current workflow, and a stakeholder request. Before proposing any solution, turn the evidence into a clear statement of the trigger, current approach, current result, current problem, desired outcome, boundaries, and unresolved questions.
```

Expected: Claude selects `framing-doc` rather than jumping to shaping, breadboarding, or UI generation.

## Near-neighbor routing test

```text
We have already selected a slice. It sends a request from the client to an API and then to a payment provider. Clarify exactly what crosses each boundary, including required inputs, possible outputs, errors, and unresolved field decisions.
```

Expected: Claude selects `interface-contracts`, not general shaping or executable breadboarding.

## Command-wrapper distinction test

```text
Define criteria for this frame, but do not propose shapes yet. Use the relevant installed Planning Skill. Treat /criteria as a Claude Code shortcut, not as a separate uploaded skill.
```

Expected: Claude uses the `shaping` skill and stops after the criteria gate.

## Negative trigger test

```text
Rewrite this two-sentence meeting invitation so it sounds warmer and more concise.
```

Expected: no Planning Skill loads. The presence of broad words such as “plan,” “shape,” or “frame” in unrelated requests should not trigger the repository workflow.

## Cross-surface fallback test

```text
Use the most relevant Planning Skill for this request. If you cannot read or modify the authoritative product-repository artifacts from Claude Design, stop and tell me exactly which skill to run in Claude Code and which output to bring back here.
```

Expected: Claude does not pretend the canvas has repository authority or access it lacks.
