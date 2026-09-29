# Agent Run Records

Agent run records are lightweight audit trails for meaningful agent work.

They are not a replacement for commits, pull requests, tests, or planning artifacts. They explain what happened during a run so a human or later agent can recover intent, authority, decisions, drift checks, and verification.

Use [`templates/agent-run-log.md`](../templates/agent-run-log.md) as the starter template.

## When to create one

Create an agent run log when an agent:

- changes implementation files
- changes planning artifacts
- runs a long implementation or refactor session
- uses a compact context packet
- performs a drift check that finds a planning conflict
- makes or records a decision that future agents may otherwise miss
- hands off work to another agent or human

You do not need a run log for tiny read-only exploration or a one-message answer.

## Where to put them

Recommended project-local paths:

```text
planning/runs/YYYY-MM-DD-short-task.md
.agent-runs/YYYY-MM-DD-short-task.md
```

Use whichever convention fits the implementation repository. This skills repo provides the template and protocol, not a required storage system.

## Minimum useful record

A useful run log should include:

- task, mode, source artifacts, authority order, and selected slice
- the Execution Appetite that bounded the run
- result and verification status
- realized human attention and delay
- runtime-specific resource evidence only when reliably measurable
- where work went: figuring it out versus executing down
- necessary discovery versus avoidable rediscovery
- files inspected and changed
- decisions, drift checks, and planning updates needed
- the next decision: continue, reshape, new bet, or stop
- handoff notes

## Relationship to planning artifacts

Do not use a run log to replace shaped artifacts.

If the run discovers a planning issue, update or request updates to the relevant artifact:

- frame
- shaping doc
- selected direction
- breadboard
- slice plan
- interface contract
- executable breadboard
- context packet
- reflection

The run log should point to the artifact that needs updating; it should not silently become the new source of truth.

## Relationship to reflection

Use a run log during or immediately after a run.

Use breadboard reflection when implementation exists and needs to be compared back to the breadboard.

A good run log can make reflection and future shaping easier by recording:

- where implementation diverged
- what the agent checked and verified
- how much human attention the run required
- what optional scope was cut
- where the run spent effort
- which uncertainty was necessary and which was avoidable rediscovery
- what still needs human review

Do not establish universal token, dollar, turn, session, or uphill/downhill thresholds from theory alone. Calibrate from comparable real runs.

See [Agent Execution Appetite](./agent-execution-appetite.md) for the runtime-neutral policy that the run log observes.
