# Ticket routing

Load this reference when charting a ticket or selecting the leaf move that resolves an active ticket.

## Routing table

| Ticket question | Route |
|---|---|
| Problem, outcome, evidence, or boundary is unclear | `framing-doc` |
| Requirements, Appetite, alternative shapes, fit, or human selection | `shaping` |
| A visual may clarify or contradict accepted planning | `sketch-reconciliation` |
| Current behavior, one named candidate, or selected behavior needs a map | `breadboarding` in the applicable mode |
| Accepted selected behavior has state complexity | `statechart` |
| A selected slice crosses an ambiguous boundary | `interface-contracts` |
| A selected slice needs fixtures, examples, edge cases, or acceptance tests | `executable-breadboards` |
| Builders need a durable orientation reference | `kickoff-doc` |
| An implementation agent needs bounded authoritative context | `feed-planning-context` |
| Implementation reality may differ from accepted intent | `breadboard-reflection` |
| Code, documentation, primary sources, or data must be inspected | evidence move using available host tools |
| A candidate needs higher-fidelity behavioral evidence | `breadboarding` in `candidate-shape` mode |
| A technical uncertainty blocks honest comparison | focused spike recorded with `templates/spike.md` and returned to `shaping` |
| Selected implementation work needs grouping, sequence, risks, or cuts | end or narrow the map, then hand off to `dumplink` |

## Rules

1. Route from the active ticket's precise question and current artifact state, not from the whole map.
2. Choose exactly one leaf route. A leaf skill may return an upstream conflict, but the ticket does not run an entire workflow.
3. Never route an active Wayfinding ticket back to `wayfinding`. This prevents recursive maps.
4. Use only skills packaged with this repository or ordinary capabilities available in the host. Do not fetch or invoke another skills repository.
5. Preserve the selected product repository's instructions and terminology.
6. Do not use an evidence move to make a product decision. Return findings to the owning planning skill or human gate.
7. Do not use a prototype as selected intent. Reconcile accepted implications through shaping or selected-design breadboarding.
8. Do not put implementation task sequencing in a Wayfinding ticket when a selected project already makes Dumplink the appropriate owner.

## Human gates

Before resolving a ticket, identify whether it changes:

- the accepted frame
- requirement status
- Appetite or cut line
- selected direction
- candidate-to-selected authority
- accepted selected-design behavior
- selected slice
- drift disposition

If so, prepare the decision and stop for the human gate. Record the ticket as resolved only after the decision is explicit and the canonical artifact is updated.
