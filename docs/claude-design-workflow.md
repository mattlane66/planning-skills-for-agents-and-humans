# Using Claude Design with the Planning Skills Repository

Use Claude Code to invoke the planning skills, create authoritative artifacts, preserve stable IDs, and carry accepted decisions into implementation. Use Claude Design when the work benefits from a visual, spatial, or interactive surface.

## Before you begin

Direct invocation in Claude Design requires the relevant Planning Skills to be uploaded and enabled in Claude, with code execution and file creation available. See [Install Planning Skills in Claude and Claude Design](./claude-skills-installation.md).

When an enabled skill is available in Claude Design, invoke it there explicitly or ask Claude to use it. A slash command is not guaranteed to appear for every custom skill in every Claude surface. When the skill is unavailable, or the work requires reading or updating the product repository, invoke it in Claude Code and bring the resulting artifact into Claude Design.

In every case, project planning files in the product repository remain authoritative. Write accepted discoveries from Claude Design back through Claude Code.

## 1. Load context → `/framing-doc`

**What you likely have:**  
Research notes, screenshots, stakeholder requests, an existing product, a rough idea, or a problem someone has asked you to solve.

**Use:**  
**Claude Code first; Claude Design optionally.**

**How to use it:**  
Use Claude Code to invoke `/framing-doc`, read the source material, and create the authoritative framing document in the product repository.

When `framing-doc` is enabled in Claude Design, you may invoke it there to inspect screenshots, journeys, environments, or relationships visually. Otherwise, bring the Claude Code framing artifact and relevant source material into Claude Design. Use its chat to correct Claude’s interpretation before generating interfaces.

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

## 3. Define success → `/criteria`

**What you likely have:**  
A broad sense of what should improve, plus stakeholder expectations, technical limitations, business needs, and user concerns.

**Use:**  
**Claude Code for defining and maintaining criteria; Claude Design for keeping them visible during exploration.**

**How to use it:**  
Invoke `/criteria` in Claude Code to convert that material into explicit criteria. Give each requirement, constraint, non-goal, and unknown a stable ID.

If the shaping skill is enabled in Claude Design, it may help inspect or challenge the criteria there, but write all accepted changes back into the authoritative shaping artifact through Claude Code.

Keep the resulting criteria visible beside the territory map in Claude Design. Remove proposed features disguised as requirements and restate them as observable outcomes or necessary conditions.

**Result:**  
A stable basis for judging proposed designs rather than relying on preference or polish.

---

## 4. Explore alternatives → `/sketch-shapes` and lightweight `/breadboard`

**What you likely have:**  
One obvious solution in mind, an existing interface that people expect you to improve, or several loosely formed ideas.

**Use:**  
**Both. Claude Code structures the alternatives; Claude Design makes them visible and interactive.**

**How to use it:**  
Invoke `/sketch-shapes` in Claude Code to generate three structurally different approaches—not three visual treatments of the same interface.

For each shape, use a lightweight `/breadboard` pass to show:

- places the user can be
- actions available to the user
- actions performed by the system
- important stored objects
- major state changes
- how actions lead to consequences

When the relevant skills are enabled in Claude Design, you may perform these passes directly there. Otherwise, generate the structured artifacts in Claude Code and place all three on the Claude Design canvas. Run the same representative scenario through each.

Use Claude Code to preserve the shape definitions, IDs, and behavioral differences in version-controlled planning files.

**Result:**  
Three comparable models of how the product could work before committing to one.

---

## 5. Evaluate and select → `/fit-check`

**What you likely have:**  
Several plausible shapes, each solving some parts of the problem while introducing different tradeoffs.

**Use:**  
**Both. Claude Code performs the structured comparison; Claude Design supports visual inspection and discussion.**

**How to use it:**  
Invoke `/fit-check` in Claude Code to compare each shape against the approved requirements and constraints. If shaping is enabled in Claude Design, you may run the comparison there as well, but the recorded decision belongs in the repository.

Use Claude Design to make the comparison inspectable. Each judgment should point to something visible in the sketch or breadboard.

Identify:

- strong fits
- partial fits
- fatal or correctable misfits
- tradeoffs
- unresolved risks
- evidence that could reverse the decision

Select the shape yourself and preserve the rationale on the canvas. Record the final decision and rationale in the planning repository through Claude Code.

**Result:**  
A traceable choice based on contextual fit rather than aesthetic preference.

---

## 6. Develop the selected shape → `/breadboard` and `executable-breadboards/SKILL.md`

**What you likely have:**  
A selected product shape whose overall logic appears promising but whose detailed behavior remains unresolved.

**Use:**  
**Claude Code for the behavioral specification and implementation-ready artifact; Claude Design for prototyping and interaction testing.**

**How to use it:**  
Invoke `/breadboard` in Claude Code to fully model the selected shape:

- places
- user and system affordances
- stores
- state
- permissions
- inputs and outputs
- wiring between actions and consequences

Then identify the assumption whose failure would most undermine the shape.

Use `executable-breadboards/SKILL.md` in Claude Code to define the smallest interactive slice that tests that uncertainty. Use realistic data and include a normal case, a difficult case, and an ambiguous case.

When these skills are enabled in Claude Design, they may be invoked there to help render and interact with the slice. Use Claude Code whenever the slice needs repository access, real code, data behavior, tests, or integration with the existing product.

**Result:**  
A coherent behavioral model and a focused prototype that tests the design’s most important uncertainty.

---

## 7. Validate and reconcile → `/check-drift`

**What you likely have:**  
An interactive prototype that has accumulated design decisions, discoveries, shortcuts, and behavior not present in the original plan.

**Use:**  
**Both. Claude Design exposes visual and interaction discrepancies; Claude Code compares and reconciles the authoritative artifacts and implementation.**

**How to use it:**  
Use the executable breadboard to test important states, failures, interruptions, recovery paths, and acceptance scenarios.

Then invoke `/check-drift` in Claude Code to compare the prototype with:

- the original frame
- the requirements
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

If the relevant reflection skill is enabled in Claude Design, it may help surface discrepancies there. Decide whether to correct the prototype, update the implementation, or revise the planning artifacts. Use Claude Code to make and preserve the accepted changes.

**Result:**  
A reconciled prototype whose behavior, requirements, implementation, and underlying rationale remain aligned.

---

## The roles of Claude Design and Claude Code

The repository supplies the planning methods and artifact structures.

### Claude Code is the primary environment for

- invoking the repository’s skills with full repository context
- reading the product repository
- creating authoritative planning artifacts
- maintaining stable IDs and traceability
- comparing plans with implementation
- writing accepted discoveries back into version control
- moving from planning into working code

### Claude Design is the working surface where you

- bring visual source material together
- invoke enabled skills when available
- visualize the territory
- place alternatives side by side
- inspect behavioral breadboards
- annotate specific misfits
- interact with risky slices
- expose states and failures
- compare the prototype with the original intent

The skills structure the reasoning. Claude Code preserves and executes it. Claude Design makes it visible, editable, and testable.
