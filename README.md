# Planning Skills for Agents and Humans

Turn a fuzzy feature into a selected, testable, vertically sliced implementation packet—without letting the agent invent scope.

These skills help product and engineering teams preserve intent from raw evidence through implementation. They are most useful for strategically important feature work with a bounded appetite, usually a 2–6 week bet for a small launch team.

**New here? Start with the [10-minute guide](./docs/start-here.md).**

## The core workflow

```text
messy evidence
  -> frame the problem
  -> compare solution shapes
  -> select a direction
  -> breadboard the behavior
  -> optionally model complex state
  -> select a demoable slice
  -> give the build agent bounded context
  -> check drift while building
```

The three core moves are:

| Move | Use it when | Output |
| --- | --- | --- |
| [`framing-doc`](./framing-doc/SKILL.md) | You have notes, transcripts, requests, or an unclear problem. | Source, problem, desired outcome, boundaries, and criteria candidates. |
| [`shaping`](./shaping/SKILL.md) | You need requirements, alternative approaches, fit checks, and a selected direction. | A bounded shape with tradeoffs, non-goals, and remaining unknowns. |
| [`breadboarding`](./breadboarding/SKILL.md) | A direction is selected and its behavior needs to become concrete. | Places, affordances, stores, wiring, branches, and slice candidates. |

Start there. Add the advanced moves only when the work needs them.

## Advanced workflow

| Skill | Add it when | Output |
| --- | --- | --- |
| [`statechart`](./statechart/SKILL.md) | A selected portion of an accepted breadboard has retries, timeouts, approvals, lifecycle stages, or other state complexity. | A derived state inventory, transition table, Mermaid statechart, and explicit gaps. |
| [`interface-contracts`](./interface-contracts/SKILL.md) | A selected slice crosses a meaningful data or system boundary. | Plain-language inputs, outputs, branches, errors, and open decisions. |
| [`executable-breadboards`](./executable-breadboards/SKILL.md) | A slice needs fixtures, example runs, edge cases, and acceptance tests before build handoff. | A buildable, testable slice contract. |
| [`dumplink`](./dumplink/SKILL.md) | Selected work needs vertical task groups, dependency-aware sequencing, risk states, or appetite-based cuts. | A bounded task-group plan and agent handoff packet. |
| [`feed-planning-context`](./feed-planning-context/SKILL.md) | An implementation agent needs the exact relevant subset of the planning stack. | A compact context packet with an execution contract and verification target. |
| [`breadboard-reflection`](./breadboard-reflection/SKILL.md) | Implementation exists and may differ from the intended behavior. | Synced reality, drift, design smells, and explicit correction options. |
| [`kickoff-doc`](./kickoff-doc/SKILL.md) | Builders need a durable reference organized by product territory. | A builder-facing kickoff document. |

## First useful prompt

```text
Use this repository's planning workflow.

First determine whether this work needs framing, shaping, or breadboarding.
Do not implement code until a direction and demoable slice are selected.
Keep requirements separate from mechanisms, preserve explicit non-goals,
and stop at human decisions about scope, appetite, or direction.

Source material:
[paste notes, transcript, request, or links here]
```

The tool-neutral operating rules live in [`AGENTS.md`](./AGENTS.md). The machine-readable modes, gates, allowed outputs, forbidden moves, artifacts, and hooks live in [`.agent-orchestration.yaml`](./.agent-orchestration.yaml).

## Why this exists

AI coding tools can one-shot simple applications. Larger bets fail differently: the agent fills missing product decisions, requirements collapse into mechanisms, rejected ideas return as scope, or implementation silently drifts from the selected direction.

This repository makes the planning stack explicit enough for humans and agents to share:

- what problem is being solved
- which requirements judge fitness
- which shape was selected and which were rejected
- how the behavior and state fit together
- what the current slice includes and excludes
- what the implementation agent must preserve
- what proves the slice is complete
- when reality requires the plan to change

The operating philosophy is in [The Work Should Get Clearer](./MANIFESTO.md).

## Planning Skills, Spec Kit, and implementation harnesses

These tools address different layers:

| Layer | Primary question |
| --- | --- |
| **Planning Skills** | What should we build, which path fits, and what intent must survive implementation? |
| **Spec Kit** | How should the selected slice become an implementation-specific plan, task structure, and technical specification? |
| **Implementation harnesses** | How should agents execute, test, review, and recover reliably inside a real codebase? |

Planning Skills is the upstream planning and alignment layer, not a replacement for either downstream category.

## Use across agent tools

The method is tool-agnostic. Invocation differs by environment:

| Environment | Recommended surface |
| --- | --- |
| Claude Code | Plugin skills plus `.claude/commands/` wrappers |
| Codex | Codex plugin, `AGENTS.md`, and prompt recipes |
| Gemini CLI | `GEMINI.md` plus `.gemini/commands/` wrappers |
| MCP-compatible clients | The optional server under `mcp-server/` |
| Cursor and other agents | `AGENTS.md`, canonical `SKILL.md` files, and templates |

See the [invocation matrix](./docs/agent-invocation-matrix.md) for exact mappings.

### Claude Code

Clone the repository, build the complete plugin layout, and use the generated bundle:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans
cd ~/.local/share/planning-skills-for-agents-and-humans
bash scripts/build-claude-plugin.sh
claude --plugin-dir dist/claude-code-plugin
```

Plugin entries are namespaced, for example `/planning-skills:frame` and `/planning-skills:statechart`.

See [Claude Code plugin guidance](./docs/claude-code-plugin.md) and [slash commands](./docs/claude-slash-commands.md).

### Codex

Use the packaged skills through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json), with `AGENTS.md` as the repo-level instruction surface.

See [Codex plugin installation](./docs/codex-plugin.md) and [Codex prompt recipes](./docs/codex-usage.md).

### Gemini CLI

Open the repository in Gemini CLI so `GEMINI.md` imports the shared agent instructions and `.gemini/commands/` exposes the project commands.

See [Gemini CLI usage](./docs/gemini-usage.md).

### MCP server

```bash
cd mcp-server
npm ci
npm run check
npm start
```

See the [MCP server README](./mcp-server/README.md) for client configuration and exposed tools.

## Examples

- [`simple-grocery-list`](./examples/simple-grocery-list/) is a deliberately small walkthrough of the foundational workflow.
- [`existing-codebase-drift`](./examples/existing-codebase-drift/) demonstrates how to surface differences between an intended breadboard and implementation reality.
- [`statechart-retry-workflow`](./examples/statechart-retry-workflow/) shows how to derive a traceable statechart when retries, cancellation, and timeouts make breadboard wiring harder to review.

These are teaching examples, not evidence of comparative model performance. A realistic codebase-scale case study remains a useful next addition.

## Repository integrity

The root skill folders are canonical. [`skill-inventory.txt`](./skill-inventory.txt) defines the complete set, and the `skills/` directory is generated packaging for plugin consumers.

After changing a canonical skill:

```bash
bash scripts/sync-packaged-skills.sh
bash scripts/check-repo-health.sh
```

The health check verifies packaged-skill parity, manifest and artifact references, version parity, command wrappers, generated plugin output, and the MCP build and tests. See [CI health](./docs/ci-health-workflow.md).

The fixtures under `evals/` are structural contract checks, not behavioral model benchmarks.

## License

Released under the [MIT License](./LICENSE).

## Optional lightweight demo

For a quick conversational feel before installing the repository, try the [Shape to Slice Assistant](https://chatgpt.com/g/g-699222e353288191afb01ea178db6da6-shape-to-slice-assistant).
