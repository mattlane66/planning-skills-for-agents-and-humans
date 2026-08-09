# Execution Graphs

An execution graph is an optional, derived bridge between an approved planning decomposition and an implementation harness.

Use it when a runtime needs a machine-readable answer to questions such as:

- which approved task groups exist?
- which groups depend on which others?
- which groups are ready, blocked, active, done, or cut?
- what verification is bound to each group?
- when must execution stop and return to planning?

Do not use an execution graph to decide what the product should be, create new task groups, expand scope, or silently change dependencies.

## Authority

Dumplink answers:

> What are the vertical implementation groups, how do they depend on one another, and which should come first?

The execution graph answers:

> Given those already-approved decisions, what work is ready, blocked, active, complete, or required to return to planning?

The approved planning artifacts remain authoritative. The graph is compiled from them.

Changing the graph does not change the plan. If implementation reveals that a node, edge, boundary, cut, or acceptance condition is wrong, update the owning planning artifact through the appropriate human gate and regenerate the graph.

## When to compile one

Compile an execution graph only when an implementation harness benefits from explicit topology or runtime state. A single obvious slice being implemented by one agent usually does not need one.

Typical uses include:

- multi-step implementation where later groups depend on earlier groups
- long-running agent sessions that need explicit readiness and stop conditions
- coordination across multiple agents or workers
- runtimes that can traverse dependencies, persist node state, or resume interrupted work
- cases where verification failure must route to retry, blocking, or planning review

## Compilation rules

Start from an approved Dumplink task-group plan or another explicitly approved slice dependency structure.

Preserve exactly:

- stable task-group or slice IDs
- project boundary
- dependency edges
- cut state
- acceptance checks and verification targets
- human activation requirements
- return-to-planning conditions

Do not infer new product decisions while compiling.

If the graph would require a new task group, a changed dependency, a broader boundary, or a new acceptance condition, stop and return to the owning planning artifact instead.

## Execution policy

The default policy is conservative:

```yaml
max_active_groups: 1
require_human_activation: true
parallel_execution: explicit_only
```

Graph structure may reveal that two groups are independent. That does not authorize parallel execution. Parallel activation requires an explicit decision by the human or governing implementation harness policy.

## Node outcomes

A node should end in an explicit result rather than merely "the agent stopped."

Recommended outcomes are:

- `done` — the goal condition and required verification passed
- `retry_or_block` — execution failed without changing planning intent
- `return_to_planning` — implementation reality conflicts with an authoritative artifact
- `human_gate` — continuing would require a scope, dependency, or product decision
- `cut` — the approved plan intentionally removed the group

## Relationship to loops

The graph and the loop solve different problems.

The graph determines **where work may go next**. The execution contract and agent loop determine **how one active node keeps working until it reaches a verifiable outcome**.

A typical flow is:

```text
approved planning
  -> execution graph
  -> human-selected active group
  -> context packet
  -> execution contract
  -> agent loop
  -> verification
  -> graph state update
  -> next ready group, block, or return to planning
```

Use `templates/execution-graph.yaml` as the runtime-neutral starter artifact.
