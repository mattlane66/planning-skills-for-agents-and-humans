# Planning Skills for Agents and Humans

Turn a fuzzy feature into a selected, testable, vertically sliced implementation packet—without letting the agent invent scope.

These skills help product and engineering teams preserve intent from raw evidence through implementation. They are most useful for strategically important feature work with a bounded appetite, usually a 2–6 week bet for a small launch team.

**New here? Start with the [10-minute guide](./docs/start-here.md).**

## When should I use these skills?

You do not have to begin your idea inside this repo.

Start wherever it is easiest to think: a conversation, whiteboard, document, Claude Design, Codex, rough prototype, or pile of notes. Explore freely while you are still discovering what the idea might be.

Use these skills when the idea becomes important enough that you do not want its meaning to live only inside a conversation or disappear between prompts. This repo is the bridge between **playing with an idea** and **building it deliberately**.

That usually happens when:

- there are several plausible ways to solve the problem
- a prototype looks promising, but you do not yet understand how it should behave
- an agent is about to modify a real codebase
- the work will take days or weeks rather than minutes
- several people or agents need to share the same understanding
- important requirements, boundaries, or decisions could easily be forgotten
- you need to hand the work from exploration into implementation
- implementation may be drifting away from the original intent

### It is a mode switch, not necessarily a tool switch

You can use the same agent for exploration, planning, and implementation. What changes is what you ask it to do:

- **Explore:** “Help me think through this idea. Show me possibilities.”
- **Plan:** “Stop proposing finished implementations. Clarify the problem, compare approaches, and record the decisions.”
- **Build:** “Implement only this selected slice. Preserve these requirements and verify it against the breadboard.”

A practical workflow is:

1. Play with the idea in whichever tool helps you think.
2. Stop when the work becomes consequential or ambiguous.
3. Use the smallest skill that resolves the current uncertainty.
4. Make the human decision about direction and scope.
5. Give the coding agent a bounded slice and compact context packet.
6. Check drift as implementation evolves.

For example, you might begin in Claude Design by generating and revising screens. Once something feels promising, bring the useful outputs—screens, notes, decisions, unanswered questions, and transcript—into framing, shaping, and breadboarding before asking Codex to build a selected slice.

You can also begin directly in Codex. For a small, obvious task, just make the change. For a larger or ambiguous task, tell Codex to use the relevant planning skill and stop before implementation or selection unless you explicitly authorize the next gate.

Do not add planning ceremony where it provides no value. A small copy change, contained bug fix, disposable experiment, low-risk script, or already-clear change may not need the full workflow.

> Use the smallest planning move that prevents an important misunderstanding.

### Use the skills in the repository where the product is being built

Install or reference these skills once, then open the product repository you are actually working on. The Planning Skills repository supplies the method and reusable instructions; project-specific frames, shaping decisions, breadboards, slices, and implementation packets should normally live beside the product code they govern.

Do not replace an existing project `AGENTS.md` with this repository's file. Prefer an installed plugin, point the agent at the relevant canonical `SKILL.md`, or selectively merge the planning rules that fit the project. Existing product-specific instructions remain authoritative for that codebase unless the team explicitly changes them.

See [Using Planning Skills in a product repository](./docs/using-in-a-product-repo.md) for the practical setup.

### Recommended project layout

A simple default is:

```text
planning/
  frame.md
  shaping.md
  appetite.md          # optional when the appetite needs its own decision record
  breadboard.md
  sketch-reconciliation.md
  statechart.md
  slices.md
  interface-contracts.md
  executable-breadboard.md
  dumplink.md
  kickoff.md
  context-packet.md
  spikes/
  runs/
```

This is a convention, not a requirement. Keep one clearly active artifact for each planning level unless the project intentionally versions them. Preserve rejected alternatives in the shaping artifact, keep tables authoritative over generated diagrams, and treat run logs as audit records rather than product truth.

### Choose the handoff artifact by its job

| Artifact | Use it for |
| --- | --- |
| **Appetite card** | The fixed time or scope budget, cut line, accepted uncertainty, and revisit conditions that shapes must fit. |
| **Kickoff document** | A durable, human-readable map of the shaped product territory. It is not the build sequence. |
| **Executable breadboard** | The behavioral and test contract for one selected slice. |
| **Dumplink plan** | Vertical task groups, risk, dependency order, sequence, and appetite-based cuts. |
| **Context packet** | The exact subset of planning material handed to the active implementation agent. |

A common path is: accepted criteria and appetite → selected shape and breadboard → optional kickoff reference → executable breadboard and/or Dumplink when needed → context packet → implementation. Not every project needs every artifact.

Set appetite before selecting a shape. Use the `Appetite` section in the [shaping template](./templates/shaping.md) for a compact decision or the standalone [appetite card](./templates/appetite-card.md) when ownership, rationale, and revisit conditions need their own record.

## The core workflow

```text
messy evidence
  -> frame the problem
  -> define criteria and set appetite
  -> compare solution shapes
  -> reconcile sketches or screenshots when they reveal missing detail
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
| [`shaping`](./shaping/SKILL.md) | You need requirements, appetite, alternative approaches, fit checks, and a selected direction. | A bounded shape with a cut line, tradeoffs, non-goals, and remaining unknowns. |
| [`breadboarding`](./breadboarding/SKILL.md) | A direction is selected and its behavior needs to become concrete. | Places, affordances, stores, wiring, branches, and slice candidates. |

Start there. Add the advanced moves only when the work needs them.

## Advanced workflow

| Skill | Add it when | Output |
| --- | --- | --- |
| [`sketch-reconciliation`](./sketch-reconciliation/SKILL.md) | A sketch, screenshot, wireframe, mockup, or whiteboard may clarify or contradict the active plan. | Visual observations mapped to stable IDs, explicit deltas, a human decision gate, and synchronized accepted updates. |
| [`statechart`](./statechart/SKILL.md) | A selected portion of an accepted breadboard has retries, timeouts, approvals, lifecycle stages, or other state complexity. | A derived state inventory, transition table, Mermaid statechart, and explicit gaps. |
| [`interface-contracts`](./interface-contracts/SKILL.md) | A selected slice crosses a meaningful data or system boundary. | Plain-language inputs, outputs, branches, errors, and open decisions. |
| [`executable-breadboards`](./executable-breadboards/SKILL.md) | A slice needs fixtures, example runs, edge cases, and acceptance tests before build handoff. | A buildable, testable slice contract. |
| [`dumplink`](./dumplink/SKILL.md) | Selected work needs vertical task groups, dependency-aware sequencing, risk states, or appetite-based cuts. | A bounded task-group plan and agent handoff packet. |
| [`feed-planning-context`](./feed-planning-context/SKILL.md) | An implementation agent needs the exact relevant subset of the planning stack. | A compact context packet with an execution contract and verification target. |
| [`breadboard-reflection`](./breadboard-reflection/SKILL.md) | Implementation exists and may differ from the intended behavior. | Synced reality, drift, design smells, and explicit correction options. |
| [`kickoff-doc`](./kickoff-doc/SKILL.md) | Builders need a durable reference organized by product territory. | A builder-facing kickoff document. |

See the [sketch reconciliation guide](./docs/sketch-reconciliation.md) for the visual-to-plan procedure and command examples.

## First useful prompt

```text
Use this repository's planning workflow.

First determine whether this work needs framing, shaping, sketch reconciliation, or breadboarding.
Do not implement code until an appetite, direction, and demoable slice are selected.
Keep requirements separate from mechanisms, preserve the cut line and explicit non-goals,
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

For work on this Planning Skills repository, open it directly so `GEMINI.md` imports the shared agent instructions. For real product work, copy or symlink the needed skill folders into the product repository, or use the MCP adapter. The repo-local TOML commands are adapter examples: if you copy them, update their `@{...}` includes to the installed skill and support-file paths. Keep the product repository's own instructions authoritative.

See [Gemini CLI usage](./docs/gemini-usage.md) and the [Gemini/MCP integration guide](./integrations/gemini/README.md).

### MCP server

```bash
cd mcp-server
npm ci
npm run check
npm start
```

See the [MCP server README](./mcp-server/README.md) for client configuration and exposed tools.

### Live Mermaid viewer

Watch the diagrams in one or more planning artifacts and refresh them in a local browser after every save:

```bash
bash scripts/watch-planning-diagrams.sh examples/simple-grocery-list/04-breadboard.md
```

The viewer uses a pinned local Mermaid package, binds to localhost, and uploads nothing. See [visual hot reload](./docs/visual-hot-reload.md).

## Examples

- [`simple-grocery-list`](./examples/simple-grocery-list/) is a deliberately small walkthrough of the foundational workflow.
- [`existing-codebase-drift`](./examples/existing-codebase-drift/) demonstrates how to surface differences between an intended breadboard and implementation reality.
- [`statechart-retry-workflow`](./examples/statechart-retry-workflow/) shows how to derive a traceable statechart when retries, cancellation, and timeouts make breadboard wiring harder to review.
- [`sketch-reconciliation`](./examples/sketch-reconciliation/) shows how a dropped visual becomes mapped observations and accepted planning deltas without silently overriding the selected shape.

These are teaching examples, not evidence of comparative model performance. A realistic codebase-scale case study remains a useful next addition.

## Repository integrity

The root skill folders are canonical. [`skill-inventory.txt`](./skill-inventory.txt) defines the complete set, and the `skills/` directory is generated packaging for plugin consumers.

After changing a canonical skill:

```bash
bash scripts/sync-packaged-skills.sh
bash scripts/check-repo-health.sh
```

The health check verifies packaged-skill parity, manifest and artifact references, version parity, command wrappers, generated plugin output, the visual hot-reload viewer, and the MCP build and tests. See [CI health](./docs/ci-health-workflow.md).

The fixtures under `evals/` are structural contract checks, not behavioral model benchmarks.

## License

Released under the [MIT License](./LICENSE).

## Optional lightweight demo

For a quick conversational feel before installing the repository, try the [Shape to Slice Assistant](https://chatgpt.com/g/g-699222e353288191afb01ea178db6da6-shape-to-slice-assistant).
