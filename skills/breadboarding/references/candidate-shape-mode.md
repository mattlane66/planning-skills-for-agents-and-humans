# Candidate-shape breadboarding

Use candidate-shape mode when a proposed shape cannot be judged honestly from a mechanism list or sketch alone. Its purpose is to resolve a specific shaping uncertainty by making enough places, affordances, stores, consequences, and wiring visible to compare or revise the candidate.

Candidate-shape breadboarding is an exploratory technique inside shaping. It is not accepted future intent and it cannot feed slicing or implementation.

## Collaborative versus gated inputs

The **minimum** inputs in collaborative shaping are:

- one named candidate shape and its shape-part IDs
- the uncertainty this breadboard should resolve
- whatever requirements currently exist, labeled `Working` or `Accepted`
- Appetite and cut line when they exist, labeled `Unset`, `Working`, or `Accepted`
- relevant current-state evidence, when the candidate must connect to an existing system

Accepted requirements and accepted Appetite are not prerequisites merely to explore a candidate in collaborative mode. If either judging input is provisional or missing:

- state that explicitly
- treat fit implications as provisional
- do not claim final Appetite fit
- do not claim the candidate is decision-ready solely from this breadboard

When the **gated/orchestrated profile** is active, enforce the stricter prerequisites in `.agent-orchestration.yaml`, including accepted requirements and Appetite before candidate breadboarding.

## Output

Declare `mode: candidate-shape` and include only the detail needed to answer the named uncertainty:

- candidate shape and shape-part references
- requirement authority and Appetite authority used for the investigation
- partial places, UI affordances, non-UI affordances, stores, consequences, and wiring
- supported mechanisms
- missing or contradictory mechanisms
- rabbit holes and Appetite risks when Appetite is known
- focused spike candidates
- implications for R, S, requirement fit, reverse fit, and Appetite fit where supportable
- unresolved questions

The artifact may be partial. Do not add detail merely to make competing candidates look symmetrical.

## Authority

A candidate breadboard is subordinate to its candidate shape and to the shaping document. It is evidence used to improve or compare a shape, not a selected-design artifact.

It must not:

- select its own candidate
- turn observed current behavior into future intent
- become build scope
- produce committed slices, contracts, task groups, or implementation handoffs
- claim final fit from provisional judging inputs
- silently change accepted requirements, Appetite, or a selected direction

When it exposes a useful change to **working** R or S, return that proposal to shaping and update the working material visibly. When it would change **accepted** material, show the delta and stop for the applicable human gate.

## Promotion after selection

A candidate breadboard does not automatically become the selected-design breadboard.

After a human selects the shape:

1. confirm the accepted requirements, shape parts, Appetite, cuts, and remaining unknowns
2. remove exploratory mechanisms that were not selected
3. reconcile the surviving rows with the selected shape
4. resolve or explicitly preserve gaps
5. declare the resulting artifact `mode: selected-design`
6. obtain acceptance before slicing or downstream build preparation

Stable IDs may be retained when the meaning is unchanged. Create new IDs when selection materially changes an element.

## Completion criterion

Candidate-shape breadboarding is complete when the named uncertainty is resolved or bounded, its R/S/fit implications are returned to shaping with judging-input authority made explicit, and no candidate has been promoted without a human selection.
