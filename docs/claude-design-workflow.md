# Using Claude Design with the Planning Skills Repository

Use Claude Code to create and preserve authoritative planning artifacts. Use Claude Design when the work benefits from a visual, spatial, or interactive surface.

## Before you begin

Direct invocation in Claude or Claude Design requires the relevant Planning Skills ZIPs to be uploaded and enabled. See [Install Planning Skills in Claude and Claude Design](./claude-skills-installation.md).

When a skill is available in Claude Design, invoke it by its canonical skill name or by an explicit natural-language request. If it is unavailable—or if the work requires reading or modifying the product repository—run it in Claude Code and bring the resulting artifact into Claude Design.

## Skill names versus command wrappers

The uploadable canonical skills are:

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

Claude Code also provides shorter command wrappers such as `/frame`, `/criteria`, `/appetite`, `/sketch-shapes`, `/fit-check`, `/select-shape`, `/breadboard`, and `/check-drift`. These wrappers expose gates or focused operations within the canonical skills; they are not separate uploaded Claude skills.

Command names in this guide are Claude Code shorthand. A plugin installation may namespace them, for example `/planning-skills:criteria`. In Claude Design, request the corresponding canonical skill and gate in plain language—for example, “Use the shaping skill to define criteria only.”

## 1. Load context → `framing-doc` (`/frame` in Claude Code)

**What you likely have:**  
Research notes, screenshots, stakeholder requests, an existing product, a rough idea, or a problem someone has asked you to solve.

**Use:**  
**Claude Code first; Claude Design optionally.**

**How to use it:**  
Use Claude Code to invoke the framing skill, read the source material, and create the authoritative framing document in the product repository.

Use Claude Design when screenshots, journeys, environments, or relationships would benefit from visual inspection. Upload the relevant material and use its chat to correct Claude’s interpretation before generating interfaces.

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

Use chat for structural changes, inline comments for factual corrections, and direct canvas editing for spatial clarity.

Do not design the future product yet.

Use Claude Code to write accepted discoveries or corrections back into the framing document.

**Result:**  
A visible model of the living context into which any new design must fit.

---

## 3. Define success → `shaping` criteria gate (`/criteria`)

**What you likely have:**  
A broad sense of what should improve, plus stakeholder expectations, technical limitations, business needs, and user concerns.

**Use:**  
**Claude Code for defining and maintaining criteria; Claude Design for keeping them visible during exploration.**

**How to use it:**  
Use the shaping skill’s criteria gate to convert that material into explicit criteria. Give each requirement, constraint, non-goal, and unknown a stable ID.

Keep the resulting criteria visible beside the territory map in Claude Design. Remove proposed features disguised as requirements and restate them as observable outcomes or necessary conditions.

Write all accepted changes back into the authoritative shaping artifact through Claude Code.

**Result:**  
A stable basis for judging proposed designs rather than relying on preference or polish.

---

## 4. Explore alternatives → `shaping` shape-sketch gate and lightweight `breadboarding`

**What you likely have:**  
One obvious solution in mind, an existing interface that people expect you to improve, or several loosely formed ideas.

**Use:**  
**Both. Claude Code structures the alternatives; Claude Design makes them visible and interactive.**

**How to use it:**  
Use the shaping skill’s shape-sketch gate (`/sketch-shapes` in Claude Code) to generate three structurally different approaches—not three visual treatments of the same interface.

For each shape, use a lightweight breadboarding pass to show:

- places the user can be
- actions available to the user
- actions performed by the system
- important stored objects
- major state changes
- how actions lead to consequences

Place all three on the Claude Design canvas and run the same representative scenario through each.

Use Claude Code to preserve the shape definitions, IDs, and behavioral differences in version-controlled planning files.

**Result:**  
Three comparable models of how the product could work before committing to one.

---

## 5. Evaluate and select → `shaping` fit and selection gates

**What you likely have:**  
Several plausible shapes, each solving some parts of the problem while introducing different tradeoffs.

**Use:**  
**Both. Claude Code performs the structured comparison; Claude Design supports visual inspection and discussion.**

**How to use it:**  
Use the shaping skill’s fit-check gate (`/fit-check` in Claude Code) to compare each shape against the approved requirements, appetite, and constraints.

Use Claude Design to make the comparison inspectable. Each judgment should point to something visible in the sketch or breadboard.

Identify:

- strong fits
- partial fits
- fatal or correctable misfits
- tradeoffs
- unresolved risks
- evidence that could reverse the decision

Select the shape yourself. Preserve the rationale on the canvas, then record the final decision in the planning repository through Claude Code. Use `/select-shape` only after the human decision is explicit.

**Result:**  
A traceable choice based on contextual fit rather than aesthetic preference.

---

## 6. Develop the selected shape → `breadboarding` and `executable-breadboards`

**What you likely have:**  
A selected product shape whose overall logic appears promising but whose detailed behavior remains unresolved.

**Use:**  
**Claude Code for the behavioral specification and implementation-ready artifact; Claude Design for prototyping and interaction testing.**

**How to use it:**  
Use `breadboarding` (`/breadboard` in Claude Code) to fully model the selected shape:

- places
- user and system affordances
- stores
- state
- permissions
- inputs and outputs
- wiring between actions and consequences

Then identify the assumption whose failure would most undermine the shape.

Use `executable-breadboards` in Claude Code to define the smallest interactive slice that tests that uncertainty. Use realistic data and include a normal case, a difficult case, and an ambiguous case.

Build or render that slice in Claude Design and interact with it rather than judging it only as a static composition.

Use Claude Code when the slice needs real code, data behavior, tests, or integration with the existing product.

**Result:**  
A coherent behavioral model and a focused prototype that tests the design’s most important uncertainty.

---

## 7. Validate and reconcile → executable tests and drift review

**What you likely have:**  
An interactive prototype that has accumulated design decisions, discoveries, shortcuts, and behavior not present in the original plan.

**Use:**  
**Both. Claude Design exposes visual and interaction discrepancies; Claude Code compares and reconciles authoritative artifacts and implementation.**

**How to use it:**  
Use the executable breadboard to test important states, failures, interruptions, recovery paths, and acceptance scenarios.

Then run `/check-drift` in Claude Code, or use `breadboard-reflection` when implementation exists and a fuller comparison is needed. Compare the prototype with:

- the original frame
- the requirements and appetite
- the selected shape
- the breadboard
- the intended slice

Use Claude Design to make discrepancies visible:

- preserved intent
- deliberate changes
- accidental drift
- missing behavior
- invented behavior
- discoveries that should update the plan

Decide whether to correct the prototype, update the implementation, or revise the planning artifacts. Use Claude Code to make and preserve the accepted changes.

**Result:**  
A reconciled prototype whose behavior, requirements, implementation, and underlying rationale remain aligned.

---

## The roles of Claude Design and Claude Code

The repository supplies the planning methods and artifact structures.

### Claude Code is the primary environment for

- invoking repository-aware skills and command wrappers
- reading the product repository
- creating authoritative planning artifacts
- maintaining stable IDs and traceability
- comparing plans with implementation
- writing accepted discoveries back into version control
- moving from planning into working code

### Claude Design is the working surface where you

- bring visual source material together
- visualize the territory
- place alternatives side by side
- inspect behavioral breadboards
- annotate specific misfits
- interact with risky slices
- expose states and failures
- compare the prototype with the original intent

The skills structure the reasoning. Claude Code preserves and executes it. Claude Design makes it visible, editable, and testable.
