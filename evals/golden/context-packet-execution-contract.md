# Golden eval: context packet execution contract

## Input

A selected slice is ready for implementation. The agent has a frame, shaping doc, breadboard, executable breadboard, and interface contracts.

## Expected qualities

A good context packet must include:

- `## Execution contract`
- goal condition
- required checks
- allowed files / areas
- out-of-scope changes
- return-to-planning conditions
- checkpoint cadence
- verification caveats

## Failure examples

Fail if the packet:

- jumps from current slice directly to verification target
- omits allowed files / areas
- omits return-to-planning conditions
- asks the agent to "finish the feature" without a concrete goal condition
