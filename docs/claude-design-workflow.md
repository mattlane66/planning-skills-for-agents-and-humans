# Using Claude Design with the Planning Skills Repository

Use Claude Code to create and preserve authoritative planning artifacts. Use Claude Design when the work benefits from a visual, spatial, or interactive surface.

## Before you begin

Direct invocation in Claude or Claude Design requires the relevant Planning Skills ZIPs to be uploaded and enabled. See [Install Planning Skills in Claude and Claude Design](./claude-skills-installation.md).

When a skill is available in Claude Design, invoke it by its canonical skill name or by an explicit natural-language request. If it is unavailable—or if the work requires reading or modifying the product repository—run it in Claude Code and bring the resulting artifact into Claude Design.

## Skill names versus command wrappers

The uploadable canonical skills are:

- `planning-router`
- `framing-doc`
- `shaping`
- `sketch-reconciliation`
- `breadboarding`
- `statechart`
- `interface-contracts`
- `executable-breadboards`
- `dumplink`
- `kickoff-doc`
- `feed-planning-context`
- `breadboard-reflection`

Claude Code also provides shorter command wrappers such as `/plan`, `/frame`, `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/select-shape`, `/breadboard`, and `/check-drift`. These wrappers expose gates or focused operations within the canonical skills; they are not separate uploaded Claude skills.

Command names in this guide are Claude Code shorthand. A plugin installation may namespace them. In Claude Design, request the corresponding canonical skill and mode in plain language.

## 1. Load context → `framing-doc` (`/frame` in Claude Code)

**What you likely have:**

Research notes, screenshots, stakeholder requests, an existing product, a rough idea, or a problem someone has asked you to solve.

**Use:**

**Claude Code first; Claude Design optionally.**

**How to use it:**

Use Claude Code to invoke framing, read the source material, and create the authoritative framing document in the product repository.

Use Claude Design when screenshots, journeys, environments, or relationships benefit from visual inspection. Correct Claude’s interpretation before generating interfaces.

**Result:**

A shared account of the current situation and why it is worth investigating.

---

## 2. Model the territory → refine the framing canvas

**What you likely have:**

The framing document, but the situation may still be difficult to understand as a whole.

**Use:**

**Claude Design, with Claude Code preserving the source of truth.**

**How to use it:**

Ask Claude Design to turn the frame into a low-fidelity territory map showing:

- the trigger and desired outcome
- the current approach
- people, tools, systems, and environments involved
- major activities and transitions
- breakdowns, compromises, and unresolved questions

Do not design the future product yet. Write accepted discoveries back into the framing document through Claude Code.

**Result:**

A visible model of the living context into which any new design must fit.

---

## 3. Define success → `shaping` criteria gate (`/criteria`)

**What you likely have:**

A broad sense of what should improve, plus stakeholder expectations, technical limitations, business needs, and user concerns.

**Use:**

**Claude Code for criteria; Claude Design for keeping them visible.**

**How to use it:**

Use shaping’s criteria gate to convert the material into explicit requirements, constraints, non-goals, and unknowns with stable IDs.

Keep the criteria visible beside the territory map. Remove proposed features disguised as requirements and restate them as outcomes or necessary conditions.

**Result:**

A stable basis for judging proposed designs rather than relying on preference or polish.

---

## 4. Set the appetite → `shaping` appetite gate (`/appetite`)

**What you likely have:**

Accepted criteria, but no explicit decision about how much time, scope, or uncertainty the work deserves.

**Use:**

**Claude Code for the authoritative Appetite decision; Claude Design for keeping the cut line visible.**

**How to use it:**

Record the fixed budget, team shape, review point, cut line, accepted uncertainty, and any unknown requiring a spike before selection.

Keep Appetite beside the criteria. Existing ideas may stay in a parking lot, but do not select a shape until Appetite is explicit.

**Result:**

A bounded bet that candidate shapes must fit rather than an estimate derived from a preferred design.

---

## 5. Explore alternatives → `shaping` plus candidate-shape breadboarding as needed

**What you likely have:**

One obvious solution, an existing interface people expect you to improve, or several loosely formed ideas.

**Use:**

**Both. Claude Code structures and preserves alternatives; Claude Design makes them visible and interactive.**

**How to use it:**

Use shaping’s shape-sketch gate to generate structurally different approaches—not visual treatments of the same mechanism.

Begin with the cheapest representation that makes each candidate understandable. For a straightforward candidate, a mechanism table or rough sketch may be enough.

When one named candidate cannot be judged without understanding its behavior, invoke `breadboarding` in `candidate-shape` mode. Name the candidate, accepted requirements, Appetite, cut line, and the single uncertainty to resolve. Map only enough to show:

- places the user can be
- actions available to the user
- important system actions
- stored objects and state
- major branches
- how actions lead to consequences
- rabbit holes and Appetite risks
- implications for the shaping fit check

Place candidates side by side and run representative scenarios through them. Candidate breadboards may differ in depth because they exist to resolve uncertainty, not to create symmetrical documentation.

They are candidate-shape breadboards; **they are not accepted breadboards** for selected-design authority, slicing, or implementation. They remain subordinate to shaping and cannot select themselves.

Use Claude Code to preserve the candidate shape IDs, breadboard mode, source shape parts, and fit implications in version-controlled planning files.

**Result:**

Comparable models of how the product could work before committing to one.

---

## 6. Evaluate and select → `shaping` fit and selection gates

**What you likely have:**

Several plausible shapes, with candidate evidence only where needed.

**Use:**

**Both. Claude Code performs the structured comparison; Claude Design supports inspection and discussion.**

**How to use it:**

Use shaping’s fit-check gate to compare each shape against requirements and Appetite. Candidate breadboards and spikes may support a judgment, but they do not choose a winner.

Identify:

- strong fits
- failed or correctable misfits
- unjustified mechanisms
- required cuts
- unresolved risks
- evidence that could reverse the decision

Do not allow visual polish or greater exploratory detail to imply selection. Select the shape yourself, preserve the rationale, and record the decision through Claude Code.

**Result:**

A traceable human choice based on contextual fit rather than aesthetic preference.

---

## 7. Reconcile and develop the selected shape → `breadboarding`

**What you likely have:**

A selected product shape, perhaps with a candidate breadboard whose exploratory rows need review.

**Use:**

**Claude Code for authoritative behavioral specification; Claude Design for prototyping and interaction testing.**

**How to use it:**

Invoke `breadboarding` in `selected-design` mode.

Do not automatically promote the candidate breadboard. Instead:

1. confirm the selected shape parts, Appetite, cuts, and remaining unknowns
2. remove candidate mechanisms that were not selected
3. reconcile surviving places, affordances, stores, branches, and wires against accepted intent
4. revise or replace rows whose meaning changed
5. preserve unresolved gaps explicitly
6. obtain human acceptance

If detailed behavior exposes a consequential conflict with a requirement, the cut line, or the selected shape, stop and return to shaping. Decide whether to revise the shape, cut behavior, run a focused spike, reopen selection, or stop the bet.

Only after acceptance should the selected-design breadboard produce candidate slices.

**Result:**

A coherent normative behavioral model tied explicitly to the selected direction.

---

## 8. Select and exercise a vertical slice → `breadboarding` and `executable-breadboards`

**What you likely have:**

An accepted selected-design breadboard.

**Use:**

**Claude Code for the selected slice and test contract; Claude Design for interactive exercise.**

**How to use it:**

Select the smallest vertical slice that produces an observable result and tests consequential uncertainty. Record its boundary, demo path, exclusions, `Produces` line, and verification target.

Use `executable-breadboards` only after the slice is selected. Add realistic data, normal cases, difficult cases, ambiguous cases, expected outputs, and acceptance tests without expanding scope.

Build or render that slice in Claude Design and interact with it rather than judging it as a static composition. Use Claude Code when the slice needs real code, data behavior, tests, or integration.

**Result:**

An accepted slice and focused prototype grounded in selected-design intent.

---

## 9. Validate and reconcile → executable tests and drift review

**What you likely have:**

An interactive prototype that has accumulated discoveries, shortcuts, or behavior not present in the plan.

**Use:**

**Both. Claude Design exposes discrepancies; Claude Code compares authoritative artifacts and implementation.**

**How to use it:**

Use the executable breadboard to test states, failures, interruptions, recovery paths, and acceptance scenarios.

Then run `/check-drift`, or use `breadboard-reflection` for a fuller comparison against:

- the frame
- requirements and Appetite
- selected shape
- accepted selected-design breadboard
- intended slice

Make preserved intent, deliberate changes, accidental drift, missing behavior, invented behavior, and discoveries visible. Decide whether to correct implementation or revise planning; use Claude Code to preserve the accepted decision.

**Result:**

A reconciled prototype whose behavior, requirements, implementation, and rationale remain aligned.

---

## The roles of Claude Design and Claude Code

### Claude Code is the primary environment for

- invoking repository-aware skills and command wrappers
- reading the product repository
- creating authoritative planning artifacts
- maintaining stable IDs and traceability
- recording candidate versus selected-design authority
- comparing plans with implementation
- writing accepted discoveries back into version control
- moving from planning into working code

### Claude Design is the working surface where you

- bring visual source material together
- visualize the territory
- place candidate shapes side by side
- inspect candidate and selected-design breadboards
- annotate specific misfits
- interact with risky slices
- expose states and failures
- compare the prototype with accepted intent

The skills structure the reasoning. Claude Code preserves and executes it. Claude Design makes it visible, editable, and testable.