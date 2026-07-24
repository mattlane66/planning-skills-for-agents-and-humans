# Candidate-shape breadboarding

Use candidate-shape mode when a proposed shape cannot be judged honestly from a mechanism list or sketch alone. Its purpose is to resolve a specific shaping uncertainty by making enough places, affordances, stores, consequences, and wiring visible to compare the candidate.

Candidate-shape breadboarding is an exploratory technique inside shaping. It is not accepted future intent and it cannot feed slicing or implementation.

## Required inputs

- accepted requirements
- accepted appetite and cut line
- one named candidate shape and its shape-part IDs
- the uncertainty this breadboard should resolve
- relevant current-state evidence, when the candidate must connect to an existing system

## Output

Declare `mode: candidate-shape` and include only the detail needed to answer the named uncertainty:

- candidate shape and shape-part references
- partial places, UI affordances, non-UI affordances, stores, consequences, and wiring
- supported mechanisms
- missing or contradictory mechanisms
- rabbit holes and appetite risks
- focused spike candidates
- implications for requirement fit, reverse fit, and appetite fit
- unresolved questions

The artifact may be partial. Do not add detail merely to make competing candidates look symmetrical.

## Authority

A candidate breadboard is subordinate to its candidate shape and to the shaping document. It is evidence used to improve or compare a shape, not a selected-design artifact.

It must not:

- select its own candidate
- turn observed current behavior into future intent
- become build scope
- produce committed slices, contracts, task groups, or implementation handoffs
- silently change accepted requirements or appetite

When it exposes a conflict, return the finding to shaping as an explicit proposed update.

## Promotion after selection

A candidate breadboard does not automatically become the selected-design breadboard.

After a human selects the shape:

1. confirm the accepted shape parts, appetite, cuts, and remaining unknowns
2. remove exploratory mechanisms that were not selected
3. reconcile the surviving rows with the selected shape
4. resolve or explicitly preserve gaps
5. declare the resulting artifact `mode: selected-design`
6. obtain acceptance before slicing or downstream build preparation

Stable IDs may be retained when the meaning is unchanged. Create new IDs when selection materially changes an element.

## Completion criterion

Candidate-shape breadboarding is complete when the named uncertainty is resolved or made decision-ready, its fit implications are returned to shaping, and no candidate has been promoted without a human selection.