# Claude Design skill test prompts

Use these prompts after uploading and enabling the Planning Skills in Claude or Claude Design. Run them with realistic but disposable source material. The goal is to verify skill selection, collaborative fluidity, and promotion-gate behavior—not the quality of a particular product idea.

For every positive test, confirm that Claude loads the intended skill, distinguishes Working from Accepted material, preserves human promotion gates, and does not silently advance into implementation.

## `framing-doc`

```text
Use my framing-doc skill. I have interview notes, screenshots of the current workflow, and a stakeholder request, but no clear problem boundary. Create a source-grounded frame covering current approach/result, problem, desired outcome, boundaries, and criteria candidates. Do not propose UI yet.
```

Expected: a frame grounded in supplied evidence, with interpretation separated from source material.

## `shaping` — R-first collaborative

```text
Use my shaping skill in collaborative mode. Start from these needs and constraints as Working requirements, then let solution shapes emerge. Move back to R whenever fit checks, spikes, or candidate evidence expose a missing requirement. Stop before selecting a shape.
```

Expected: R and S can iterate rather than being treated as a one-way sequence; Working versus Accepted authority is visible.

## `shaping` — S-first collaborative

```text
Use my shaping skill in collaborative mode. I already have a rough solution in my head. Capture it as Shape A first, extract the provisional requirements it implies, separate needs from mechanisms, and help me move among R, S, fit checks, spikes, and candidate breadboards as useful. Do not select for me.
```

Expected: Shape A is preserved as a candidate, provisional R is extracted from it, and Claude does not force a completed frame/criteria sequence before useful shaping can continue.

## `shaping` — Working fit

```text
Use my shaping skill. Shape A and Working requirements exist, but Appetite is still unset. Run a fit and reverse-fit check now to expose missing R or unjustified S. Label the result Working and do not claim final Appetite fit or selection readiness.
```

Expected: the fit check is useful exploratory evidence but is not promoted to decision-ready evidence.

## `shaping` — focused spike

```text
Use my shaping skill for a focused spike. The current fit check exposed one unknown about persistence. Investigate only that question and return explicit implications for R, S, fit, and Appetite. Do not make the product decision.
```

Expected: bounded evidence and shaping implications, not a selected direction.

## `shaping` — gated profile

```text
Use my shaping skill in gated/orchestrated mode. Requirements are Working and Appetite is unset. I want to proceed to comparative candidate breadboarding anyway.
```

Expected: Claude enforces the stricter `.agent-orchestration.yaml` prerequisites instead of borrowing collaborative-mode flexibility.

## `sketch-reconciliation`

```text
Use my sketch-reconciliation skill. Compare this Claude Design canvas with accepted shaping artifacts. Record observable visual evidence, proposed planning deltas, and the human decision gate. Do not silently overwrite accepted intent.
```

Expected: mapped observations and proposed deltas, not automatic acceptance of the visual.

## `breadboarding` — selected-design

```text
Use my breadboarding skill on the explicitly selected shape. Requirements and Appetite are Accepted. Model places, user affordances, system affordances, stores, consequences, and wiring. Reconcile earlier candidate evidence rather than promoting it automatically.
```

Expected: a `selected-design` behavioral model with accepted inputs cited and no automatic candidate promotion.

## `breadboarding` — current-state

```text
Use my breadboarding skill in current-state mode. Map how this existing workflow behaves from supplied code, tests, screenshots, and logs. Cite evidence, mark unresolved observations, and do not turn current behavior into selected future intent or slice it for implementation.
```

Expected: a descriptive `current-state` map that does not require or invent a selected direction.

## `breadboarding` — candidate-shape with provisional inputs

```text
Use my breadboarding skill in candidate-shape mode. Shape A is named, requirements are Working, and Appetite is unset. Breadboard only the add-city interaction because that behavior is unclear. Return R/S/fit implications to shaping and keep all final fit/Appetite claims provisional.
```

Expected: candidate breadboarding proceeds in collaborative mode, explicitly labels input authority, and does not select, slice, or create build scope.

## `statechart`

```text
Use my statechart skill for this accepted slice, which includes retries, cancellation, timeout, and approval. Derive states and transitions from the accepted selected-design breadboard and identify any missing decisions.
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
Use my dumplink skill. Turn this selected, bounded project into vertical task groups, sequence dependencies, mark risk states, and identify Appetite-based cuts. Preserve the project outcome, boundary, exclusions, and non-goals. Stop for approval before selecting the active group.
```

Expected: the selected project is decomposed into bounded, judgeable vertical slices rather than a generic backlog.

```text
Use my dumplink skill, but no project has been selected or bounded yet. Create the task groups and build sequence anyway.
```

Expected: Dumplink stops without inventing task groups and returns the missing project decision to shaping or the human gate.

## `kickoff-doc`

```text
Use my kickoff-doc skill. Create a builder-facing reference from accepted frame/boundary, selected shape, accepted breadboard, and selected slice. Organize it by shaped product territory, not implementation sequence.
```

Expected: durable orientation, not new scope or a task plan.

## `feed-planning-context`

```text
Use my feed-planning-context skill. Prepare the smallest context packet an implementation agent needs for this selected slice, including authority order, execution contract, non-goals, and verification target. Exclude Working shapes and candidate breadboards as active build scope.
```

Expected: compact accepted context with exploratory history omitted from active scope.

## `breadboard-reflection`

```text
Use my breadboard-reflection skill. Compare this implemented prototype with the accepted breadboard and selected slice. Preserve intended and current behavior separately, identify planning drift and design smells, and stop for my correction decision.
```

Expected: a factual side-by-side comparison that changes neither implementation nor accepted plan until the human chooses explicitly.

## Automatic-selection test — unclear problem

Do not name a skill:

```text
I have a transcript, three screenshots of the current workflow, and a stakeholder request. There is no clear problem statement or useful solution yet. Choose the smallest planning move.
```

Expected: Claude selects `framing-doc` (possibly via the router) rather than jumping to implementation.

## Automatic-selection test — solution-first

Do not name a skill:

```text
I already know roughly what I want to build and can describe the mechanism, but I have not written requirements. Help me capture the solution and tease out what it actually needs to accomplish before we commit to it.
```

Expected: Claude selects `shaping`, preserving the solution as a candidate and extracting Working R rather than forcing the user back to framing by default.

## Near-neighbor routing test

```text
We have already selected a slice. It sends a request from the client to an API and then to a payment provider. Clarify exactly what crosses each boundary, including required inputs, possible outputs, errors, and unresolved field decisions.
```

Expected: Claude selects `interface-contracts`, not general shaping or executable breadboarding.

## Command-wrapper distinction tests

```text
For this move, define or revise requirements only. If an existing Shape A implies a missing requirement, extract it. Treat /criteria as a Claude Code shortcut, not a separate uploaded skill.
```

Expected: Claude uses `shaping`; the focused move does not imply that R had to precede S.

```text
For this move, spike one technical unknown and return its R/S/fit/Appetite implications. Treat /spike as a Claude Code shortcut inside shaping, not a separate uploaded skill.
```

Expected: Claude uses `shaping` rather than looking for a standalone spike skill.

## Negative trigger test

```text
Rewrite this two-sentence meeting invitation so it sounds warmer and more concise.
```

Expected: no Planning Skill loads. Broad words such as “plan,” “shape,” or “frame” in unrelated requests should not trigger the repository workflow.

## Cross-surface fallback test

```text
Use the most relevant Planning Skill for this request. If you cannot read or modify the authoritative product-repository artifacts from Claude Design, stop and tell me exactly which skill to run in Claude Code and which output to bring back here.
```

Expected: Claude does not pretend the canvas has repository authority or access it lacks.

## Shared activation corpus

Run the positive and negative cases in `evals/skill-activation-cases.json` and the behavior cases in `evals/workflow-behavior-cases.json` after changing descriptions, profile rules, or upload packaging. Claude Design should select the same canonical skills as other surfaces and preserve the same collaborative/gated distinction and hard promotion gates.
