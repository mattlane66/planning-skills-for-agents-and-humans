# The Work Should Get Clearer

A practical manifesto for teams using AI to build useful software.

This repo exists to help teams move from unclear intent to useful shipped work without losing the thread.

The work should get clearer as it moves from evidence and ideas into accepted intent, buildable behavior, working slices, and shipped learning.

That does **not** mean thinking has to happen in a fixed order.

> **Start where the useful thinking already is. Exploration is fluid. Commitment is gated.**

A team may begin from a real struggle, a set of requirements, a proposed solution, a sketch, a prototype, or a technical unknown. Good shaping lets those things inform one another without confusing any of them for accepted truth too early.

---

## Values

**Understanding the struggle without forbidding solution-first thinking.**  
A request or solution idea may be a clue to the real problem. Capture it, inspect it, and extract what it teaches you. Do not treat it as automatically correct.

**Keeping requirements and mechanisms separate.**  
Requirements state what must be true. Shapes state how it might be achieved. A mechanism can reveal a missing requirement, but it does not become a requirement merely because someone thought of it first.

**Letting R and S sharpen each other.**  
Requirements reveal bad shapes. Shapes reveal missing requirements. Fit checks, spikes, sketches, and breadboards make the relationship visible.

**Using process to support judgment, not replace it.**  
The process exists to help people think, decide, and collaborate. If it becomes theater or blocks useful inquiry, loosen it.

**Gating commitment, not curiosity.**  
Working ideas should be easy to explore. Accepted requirements, Appetite, selected direction, selected-design behavior, and build scope should be hard to change accidentally.

**Mapping behavior before polishing the screen.**  
Rough flows, sketches, fit checks, and breadboards reveal how the thing works faster than finished-looking mockups.

**Checking system reality before trusting the idea.**  
The data, code, permissions, edge cases, and legacy constraints are part of the design.

**Building end-to-end slices before handing work across functions.**  
“Backend done” or “design done” is not progress until useful behavior can be observed, tested, and demonstrated through the appropriate surface.

**Letting reality update the plan.**  
Plans are guesses. Real use teaches the team what the plan could not know.

**Using AI to preserve intent and execute bounded work.**  
AI should help carry context, structure working material, expose contradictions, spike unknowns, and execute selected slices. It should not silently invent strategy or promote exploration into commitment.

---

## The shaping loop

Collaborative shaping is not a conveyor belt.

```text
requirements (R) ↔ shapes (S) ↔ fit checks
      ↑                ↕             │
      └── discoveries ← spikes / candidate breadboards / sketches
```

You can enter the loop from any useful point:

- **R-first** — needs, constraints, outcomes, criteria
- **S-first** — a solution already in someone's head
- **evidence-first** — a prototype, sketch, workflow, or existing product behavior
- **uncertainty-first** — one question worth spiking or breadboarding

Working R and S may change as evidence appears.

The point of the loop is not to complete artifacts. It is to improve judgment.

---

## The commitment path

When the team is ready to promote exploration into accepted intent, the order becomes stricter:

```text
clear-enough problem boundary
→ accepted requirements
→ accepted Appetite + cut line
→ decision-ready candidate evidence
→ fit + reverse fit + Appetite implications
→ explicit human selection
→ selected-design reconciliation
→ accepted behavior
→ human-selected slice
→ bounded implementation
```

These are **promotion gates, not navigation locks**.

A team can explore Shape A before Appetite exists. It cannot honestly claim Shape A fits the bet until Appetite exists.

A candidate breadboard can reveal behavior before requirements are accepted. It cannot become selected-design intent until a human selects the direction and reconciles the evidence.

---

## Collaborative and gated modes

### Collaborative shaping

Use when humans are actively steering the work.

- provisional inputs are allowed
- R and S can arrive in either order
- working fit checks are useful
- focused spikes can happen whenever an unknown matters
- candidate breadboards can use Working R or Unset/Working Appetite
- accepted material changes only through an explicit decision

### Gated / orchestrated shaping

Use when a team, CI harness, policy, or multi-agent system needs deterministic prerequisites.

The controlled route may require accepted R and Appetite before comparative shape work or candidate breadboarding.

That is a valid operating profile. It is not the definition of shaping itself.

The machine-readable profile lives in `.agent-orchestration.yaml`.

---

## Principles

### 1. Start with the real material, not the ideal artifact.

If the user has research, start there.

If the user has requirements, start there.

If the user has a solution in their head, capture it as a candidate shape.

If the user has a prototype, inspect what it implies.

Do not make people translate useful thinking into the “correct” starting document before the work can begin.

### 2. A solution is valid evidence, not automatic strategy.

An S-first idea can be extremely useful because it exposes assumptions quickly.

Ask:

- What outcome is this mechanism trying to create?
- What constraint makes it seem necessary?
- Which part is a preference rather than a need?
- What would still need to be true if this mechanism disappeared?

Extract those answers into Working R.

### 3. Keep working and accepted material visibly different.

Use explicit authority when it matters:

- Requirements: Working | Accepted
- Appetite: Unset | Working | Accepted
- Shape: Candidate | Selected
- Fit check: Working | Decision-ready
- Breadboard: current-state | candidate-shape | selected-design

Visual polish, detail, or recency does not grant authority.

### 4. Use fit checks early, not only at the end.

A working fit check can expose:

- missing requirements
- bad mechanisms
- unjustified scope
- the next spike
- the next candidate breadboard

If the judging inputs are provisional, the result is provisional too.

### 5. Use spikes to learn, not decide.

A focused spike answers a technical or empirical question.

It should return explicit implications to R, S, fit, and Appetite where relevant.

The spike does not choose the product direction.

### 6. Breadboard the unknown, not everything.

Candidate-shape breadboarding exists to clarify one decision-relevant uncertainty.

In collaborative mode, it may use provisional judging inputs. It must say so.

Candidate evidence cannot select itself, create build scope, or automatically become accepted future behavior.

### 7. Set Appetite before selection.

You may explore solutions before Appetite is accepted.

You may not select a shape and then reverse-engineer the budget from the solution you already want.

Appetite is what the opportunity is worth, not an estimate that ratifies a favorite shape.

### 8. Compare paths before committing when real alternatives exist.

Do not manufacture alternatives for ceremony.

But when there are materially different ways to solve the problem, make the trade-offs visible before selection.

### 9. Human selection is a real gate.

Agents can summarize, compare, test, and recommend.

They do not infer commitment from enthusiasm, recency, visual polish, or exploratory depth.

### 10. Candidate evidence must be reconciled before promotion.

A selected candidate breadboard is still a candidate breadboard.

After selection:

- remove unselected mechanisms
- reconcile surviving behavior against accepted R, Appetite, cuts, and direction
- preserve unresolved gaps
- obtain acceptance

Only then does selected-design behavior become normative.

### 11. Shape a path, not a full spec.

A good shape gives firm boundaries and leaves room for local judgment.

It shows where the walls, pipes, and wires probably go. It does not choose every fixture.

### 12. Build small end-to-end slices.

A slice should produce an observable, testable, demonstrable result through the appropriate UI, API, CLI, job, event, or product surface.

Before asking an agent to build, feed only the authoritative context for the selected slice.

### 13. Protect the selected boundary.

New ideas are welcome.

They are not automatically part of the current version.

Keep clear buckets for blocker, fix, enhancement, later bet, and discard.

### 14. Treat drift as information.

When implementation no longer matches accepted intent, choose explicitly:

- update the code
- update the plan
- cut or split scope
- create a new bet

Silent drift is failure.

---

## When to use each skill

| Moment | Use |
|---|---|
| You do not know the smallest useful planning move | [`planning-router`](./planning-router/SKILL.md) |
| A bounded planning route needs dependent decisions coordinated across sessions | [`wayfinding`](./wayfinding/SKILL.md) |
| The problem, outcome, evidence, or boundary is genuinely unclear | [`framing-doc`](./framing-doc/SKILL.md) |
| R, S, Appetite, fit, focused spikes, or human selection need collaborative shaping | [`shaping`](./shaping/SKILL.md) |
| Current behavior, one candidate, or selected behavior needs a concrete map | [`breadboarding`](./breadboarding/SKILL.md) |
| A visual may change accepted intent | [`sketch-reconciliation`](./sketch-reconciliation/SKILL.md) |
| Selected stateful behavior needs a precise transition model | [`statechart`](./statechart/SKILL.md) |
| A selected slice crosses a meaningful boundary | [`interface-contracts`](./interface-contracts/SKILL.md) |
| A selected slice needs fixtures, examples, edge cases, and acceptance checks | [`executable-breadboards`](./executable-breadboards/SKILL.md) |
| A selected project needs vertical task groups, sequence, risk, or scope cuts | [`dumplink`](./dumplink/SKILL.md) |
| Builders need a durable orientation reference | [`kickoff-doc`](./kickoff-doc/SKILL.md) |
| An implementation agent needs the authoritative subset for one selected slice | [`feed-planning-context`](./feed-planning-context/SKILL.md) |
| Implementation reality needs to be compared with accepted intent | [`breadboard-reflection`](./breadboard-reflection/SKILL.md) |

Use the smallest skill that resolves the current uncertainty.

Do not use skills to add ceremony.

---

## Go / No-Go checks

### Selection Go

Can we clearly say:

- What problem boundary are we actually solving inside?
- Which requirements are Accepted?
- What Appetite and cut line are Accepted?
- What candidates are genuinely viable?
- What do the fit and reverse-fit checks say?
- What important unknowns remain?
- Which direction did the human explicitly select?

If not, keep shaping.

### Selected-design Go

Can we clearly say:

- Which mechanisms survived selection?
- Which candidate evidence was reconciled rather than promoted automatically?
- What are the accepted places, affordances, stores, consequences, and branches?
- What did we cut?
- What remains unresolved?

If not, do not slice.

### Build Go

Can we clearly say:

- What slice is selected?
- What is inside and outside it?
- What accepted behavior must be preserved?
- What counts as done?
- What verification target proves it?

If not, do not hand the work to an implementation agent as if the boundary were clear.

---

## Anti-patterns to refuse

Do not force R-first when S-first is the useful entry point.  
Do not treat S-first as permission to skip judging criteria before selection.  
Do not confuse a solution idea with an accepted strategy.  
Do not confuse Working R with Accepted R.  
Do not treat a Working fit check as decision-ready.  
Do not derive Appetite from a favorite shape.  
Do not let candidate breadboards select themselves.  
Do not let polished prototypes fake authority.  
Do not silently rewrite Accepted material when new evidence appears.  
Do not start implementation from candidate evidence.  
Do not let AI invent missing commitment.  
Do not let drift run silent.

---

## The Human Clause

This is not a machine for controlling people.

It is a way to help people do better work together.

Leave room for judgment.  
Let people start from the material that helps them think.  
Let designers explore.  
Let engineers push back.  
Let product people change the requirements when a shape reveals the real need.  
Let a spike kill a favorite mechanism.  
Let a prototype expose a missing constraint.  
Let good ideas wait.  
Let imperfect first versions ship when they solve the real problem.

If the process becomes theater, stop.  
If it becomes bureaucracy, cut it down.  
If it removes judgment, loosen it.  
If it hides authority, clarify it.  
If it hides reality, change it.

The right amount of process is the amount that helps the work get clearer.

No more.
