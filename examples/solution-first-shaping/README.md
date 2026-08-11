# Solution-first shaping example

This example shows the collaborative shaping profile when the useful starting point is a solution already in someone's head.

The purpose is not to prove that solution-first work is better than requirements-first work. It demonstrates the repository's governing rule:

> **Exploration is fluid. Commitment is gated.**

## Starting point

A human says:

> I want a small terminal time-zone app. I should be able to keep a short list of cities, see their current local times, move between them with the keyboard, and quickly add or remove a city. I have this rough interaction in my head, but I have not written requirements yet.

Instead of forcing the idea through a completed frame and criteria document first, capture the idea as **Shape A**.

## 1. Capture the rough solution as Working S

### A: Keyboard-first city list

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | TUI shows a vertically selectable list of saved cities with current local time beside each city. | |
| A2 | Arrow keys move the active row; Enter opens a lightweight add-city interaction. | ⚠️ |
| A3 | A remove key deletes the active city after a small confirmation step. | |
| A4 | Saved cities persist between launches. | ⚠️ |

Nothing in this table is selected merely because it came from the human first.

## 2. Extract provisional requirements from the shape

Ask what needs or constraints make those mechanisms seem useful.

| ID | Requirement | Status | Authority |
|---|---|---|---|
| R0 | A person can compare the current time in a small set of personally relevant locations at a glance. | Core goal | Working |
| R1 | Common navigation should be fast without requiring a mouse. | Must-have | Working |
| R2 | The chosen locations should still be there the next time the app opens. | Must-have | Working |
| R3 | Adding or removing a location should not make the main comparison view feel cumbersome. | Nice-to-have | Working |

Notice that `R2` is not “use a JSON file.” Persistence is the need; storage format belongs in S.

## 3. Run a Working fit check early

The fit check is useful before the requirements are accepted because it can expose missing thinking.

| Req | Requirement | A |
|---|---|:---:|
| R0 | Compare relevant current times at a glance | ✅ |
| R1 | Fast keyboard navigation | ✅ |
| R2 | Locations survive relaunch | ❌ |
| R3 | Add/remove does not burden the main view | ❌ |

Why the failures?

- A4 says persistence exists but is still a flagged unknown, so it cannot honestly pass R2 yet.
- A2 does not explain the add interaction well enough to know whether R3 is satisfied.

The result is a **Working fit check**, not a selection decision.

## 4. Spike the technical unknown

Run a focused spike on A4:

**Question:** What is the smallest reliable persistence mechanism for a local TUI that keeps a short ordered city list across launches?

The spike returns evidence, not a product decision. Suppose it finds that a small user-scoped config file is already supported cleanly by the chosen runtime.

Implications:

- R2 stays unchanged.
- A4 becomes concrete: “read/write the ordered city list in the runtime's user config directory.”
- R2 can now be rerun in the fit check.
- Appetite impact appears small, but no final Appetite-fit claim is made until Appetite is accepted.

## 5. Candidate-breadboard the behavioral unknown

A2 is still hard to judge from prose. Run `breadboarding` in `candidate-shape` mode for one question:

**Candidate:** A  
**Question:** Can adding a city remain lightweight without turning the main list into a form-heavy interface?  
**Requirements:** Working  
**Appetite:** Unset

Map only enough places and affordances to answer that question.

The breadboard reveals that a blocking add-city prompt interrupts quick comparison more than expected. That leads to a revised A2 and a sharper R3.

### Revised Working R3

| ID | Requirement | Status | Authority |
|---|---|---|---|
| R3 | Adding or removing a location should require a deliberate action without turning the main comparison view into a data-entry screen. | Must-have | Working |

### Revised A2

| Part | Mechanism | Flag |
|---|---|:---:|
| A2 | Press `a` to open a focused city search overlay; choose a result and return immediately to the list. | |

The candidate breadboard did not become accepted future intent. It supplied evidence that improved Working R and S.

## 6. Set and accept Appetite

The human decides the opportunity is worth:

- one week
- one engineer
- local-only operation
- no accounts, sync, map view, or automatic location discovery

Now Appetite becomes **Accepted** and can constrain the decision.

## 7. Accept the judging requirements

After review, R0–R3 become **Accepted**. A second materially different shape may be introduced if there is a real alternative worth comparing—for example, a command-palette-first design instead of a persistent visible list.

Do not manufacture alternatives merely to satisfy process.

## 8. Run decision-ready fit and reverse fit

Now rerun fit against the accepted R and Appetite. Check that every surviving mechanism serves an accepted requirement and that the shape fits the cut line.

Only now can the comparison become **Decision-ready**.

## 9. Human selection

The human explicitly chooses Shape A.

That choice—not the fact that A came first, received more detail, or looked good in a prototype—makes it selected.

## 10. Reconcile into selected-design behavior

If the earlier candidate breadboard is useful, reconcile it rather than promoting it automatically:

1. remove exploratory rows that did not survive selection
2. align surviving places and affordances with accepted R, Appetite, and cuts
3. preserve unresolved gaps explicitly
4. declare `mode: selected-design`
5. obtain human acceptance before slicing

## What this example demonstrates

```text
rough S
→ provisional R
→ Working fit
→ spike
→ candidate breadboard
→ revise R + S
→ accept Appetite + R
→ decision-ready fit
→ explicit human selection
→ selected-design reconciliation
```

The path is intentionally non-linear during shaping. The promotion gates remain strict where commitment begins.
