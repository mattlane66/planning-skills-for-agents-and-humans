# Gemini CLI usage

When maintaining this repository, Gemini CLI should use `GEMINI.md` as its project context file.

This repo includes a root `GEMINI.md` that imports `AGENTS.md`, so Gemini gets the same tool-neutral planning instructions as Claude Code, Codex, and other agents.

For product work, prefer Gemini CLI's native skill management. Install from Git with `gemini skills install https://github.com/mattlane66/planning-skills-for-agents-and-humans`, or link a local checkout with `gemini skills link /path/to/planning-skills-for-agents-and-humans`. Use `gemini skills list`, `enable`, `disable`, and `/skills reload` to inspect or refresh discovery. Copying folders or using the MCP adapter remains a fallback. Preserve the product repository's own `GEMINI.md`, `AGENTS.md`, and other local instructions instead of replacing them with this repository's files.

## Default shaping behavior

For interactive human-guided planning, default to **collaborative shaping**:

> **Start where the useful thinking already is. Exploration is fluid. Commitment is gated.**

Gemini may begin from requirements, a proposed solution, a prototype, current-system evidence, a fit question, or a focused unknown. Requirements (R), shapes (S), fit checks, spikes, sketches, and candidate breadboards may iterate in any useful order while they remain Working.

Use the **gated/orchestrated profile** only when the user or automation explicitly asks for strict prerequisites.

Hard promotion gates remain universal: accepted R + accepted Appetite before final selection, explicit human selection, explicit candidate-to-selected reconciliation, accepted selected-design behavior before slicing, and human-selected scope before build.

## Native skill installation

Gemini Agent Skills load the canonical `SKILL.md` instructions and bundled resources on demand. The `.gemini/commands/` files are focused aliases for explicit moves; they do not replace native skill discovery or create a second method.

## Project commands

Gemini CLI discovers project-local custom commands from:

```text
.gemini/commands/
```

This repo includes Gemini-native wrappers for both fluid shaping moves and downstream gates:

| Command | Purpose |
|---|---|
| `/plan` | Choose the smallest next planning move without forcing a fixed exploration order. |
| `/wayfind` | Chart or advance a bounded multi-session planning effort through one shared map and frontier. |
| `/shape` | Main collaborative shaping surface; start R-first, S-first, evidence-first, or uncertainty-first. |
| `/criteria` | Work on R for the current move; may extract requirements from an existing shape or prototype. |
| `/appetite` | Set, revise, or accept the fixed time/scope budget and cut line. |
| `/sketch-shapes` | Work on S for the current move; valid as an S-first entry point. |
| `/fit-check` | Run Working or decision-ready fit and reverse-fit checks. |
| `/spike` | Resolve one focused technical or empirical shaping unknown. |
| `/breadboard` | Map current behavior, candidate behavior, or selected-design behavior in the declared mode. |
| `/select-shape` | Record a human shape-selection decision after the hard selection gate is satisfied. |
| `/reconcile-sketch` | Map a visual to planning IDs, surface proposed deltas, and apply only accepted changes. |
| `/statechart` | Derive a transition table and Mermaid projection for selected stateful behavior. |
| `/dumplink` | Turn a selected project into vertical task groups with dependency order, risk states, and scope cuts. |
| `/check-drift` | Check implementation direction against selected planning artifacts and stop if drift is found. |

These commands use Gemini's TOML command format and inject the files named by their `@{...}` includes. In this repository those paths are already correct; in a product repository, verify or adapt them before use.

## Collaborative usage examples

### Start from a solution

```text
/shape "I already have a rough solution idea. Capture it as Shape A, extract the provisional requirements it implies, and move among R, S, fit, spikes, and candidate breadboarding as useful. Do not select for me."
```

### Start from requirements

```text
/shape planning/notes.md "Start R-first from these needs and constraints, then let shapes emerge. Return to R whenever fit, spikes, or candidate evidence expose a missing requirement."
```

### Focus only on R now

```text
/criteria planning/shaping.md
```

This constrains the current move; it does not imply that criteria had to come before S.

### Focus only on S now

```text
/sketch-shapes planning/shaping.md
```

If R or Appetite is still provisional, keep those implications provisional.

### Working fit check

```text
/fit-check planning/shaping.md
```

When R or Appetite is not yet accepted, the command should label the result `Working fit check` and avoid treating it as final selection evidence.

### Focused spike

```text
/spike planning/shaping.md "Can the existing persistence layer support the proposed restore behavior without a new store?"
```

The spike returns explicit R/S/fit/Appetite implications and does not choose the product direction.

### Candidate breadboard with provisional inputs

```text
/breadboard planning/shaping.md "mode: candidate-shape; candidate: A; question: how does the restore flow behave? requirements: Working; Appetite: Unset"
```

In collaborative mode this is valid. The artifact must label its judging inputs and cannot claim final fit, slicing, or build scope.

### Human selection

```text
/select-shape planning/shaping.md "Choose B"
```

The command should verify accepted requirements, accepted Appetite, and decision-ready fit evidence before recording selection.

## Gated / orchestrated usage

Use natural language or `/shape` to switch profiles:

```text
/shape "Use the gated/orchestrated profile. Enforce .agent-orchestration.yaml prerequisites and stop at every human promotion gate."
```

The controlled path is:

```text
accepted frame
→ accepted requirements
→ accepted Appetite
→ candidate shapes
↔ candidate breadboards / focused spikes
→ decision-ready fit
→ human selection
→ selected-design breadboard
→ selected slice
→ bounded build
```

## Visual reconciliation

```text
/reconcile-sketch planning/shaping.md planning/breadboard.md /path/to/sketch.png
```

You can instead attach or paste the image when Gemini CLI supports image input.

## Statechart

```text
/statechart planning/breadboard.md "Scope: V2 retry and cancellation"
```

## Dumplink

```text
/dumplink planning/shaping.md planning/breadboard.md "Selected project: onboarding; Appetite: 4 weeks"
```

## Drift check

```text
/check-drift planning/context-packet.md src/features/onboarding/
```

It should return only one of:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## Reloading commands

After adding or changing command files, reload Gemini commands:

```text
/commands reload
```

To inspect available commands:

```text
/commands list
```

## Design principle

Gemini commands remain thin wrappers around the canonical repo method.

Keep the workflow details in:

```text
AGENTS.md
.agent-orchestration.yaml
planning-router/SKILL.md
shaping/SKILL.md
breadboarding/SKILL.md
docs/human-decision-gates.md
templates/shaping.md
templates/spike.md
```

Update Gemini command files only when invocation behavior, stopping point, or user-facing command name changes.
