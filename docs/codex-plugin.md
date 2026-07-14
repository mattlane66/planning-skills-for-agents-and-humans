# Codex plugin support

This repository can be installed as a Codex plugin. The plugin packages the existing planning skills under `skills/` and exposes them through the Codex plugin manifest at `.codex-plugin/plugin.json`.

## What is included

The Codex plugin includes these skills:

- `framing-doc`
- `shaping`
- `sketch-reconciliation`
- `breadboarding`
- `statechart`
- `interface-contracts`
- `executable-breadboards`
- `dumplink`
- `breadboard-reflection`
- `kickoff-doc`
- `feed-planning-context`

The repo also includes tool-neutral orchestration and harnessing docs:

- `.agent-orchestration.yaml`
- `docs/codex-usage.md`
- `docs/agent-workflow.md`
- `docs/loop-prompting.md`
- `docs/agent-run-records.md`
- `docs/lifecycle-hooks.md`

## Repo-local marketplace

The repo includes a local marketplace file at:

```text
.agents/plugins/marketplace.json
```

That marketplace points Codex at this repository as a local plugin source.

## Install from GitHub

After cloning or referencing the repository, add it as a Codex plugin marketplace source:

```bash
codex plugin marketplace add mattlane66/planning-skills-for-agents-and-humans --ref main
```

Then open Codex and inspect available plugins:

```bash
codex
/plugins
```

Look for:

```text
Planning Skills for Agents and Humans
```

Open the product repository where the planning artifacts and implementation live, then invoke the installed skills there. Preserve that repository's existing `AGENTS.md`; do not copy this repository's root instructions over product-specific build, test, security, or architecture rules.

## Use

Example prompts:

```text
Use Planning Skills for Agents and Humans to frame this feature before implementation.
```

```text
Use the shaping skill to compare possible solution directions before choosing one.
```

```text
Use the shaping skill to set a bounded appetite and cut line before selecting a direction.
```

```text
Use the breadboarding skill to map places, affordances, stores, state, and wiring for this feature.
```

```text
Use the statechart skill to derive transitions for a selected stateful portion of an accepted breadboard without replacing the breadboard as source of truth.
```

```text
Use the interface-contracts skill to define the plain-language boundary contracts for this selected slice.
```

```text
Use the executable-breadboards skill to create examples, fixtures, expected outputs, edge cases, and acceptance tests before implementation.
```

```text
Use the dumplink skill to create vertical task groups, dependency-aware sequence, risk states, and scope cuts for this selected work.
```

```text
Use the feed-planning-context skill to package the active planning artifacts for an implementation agent.
```

```text
Use docs/loop-prompting.md and templates/drift-check.md to check whether implementation has drifted from the selected planning artifacts.
```

## Maintenance

Keep the root skill folders and the `skills/` copies aligned:

```text
framing-doc/                  -> skills/framing-doc/
shaping/                      -> skills/shaping/
sketch-reconciliation/        -> skills/sketch-reconciliation/
breadboarding/                -> skills/breadboarding/
statechart/                   -> skills/statechart/
interface-contracts/          -> skills/interface-contracts/
executable-breadboards/       -> skills/executable-breadboards/
dumplink/                     -> skills/dumplink/
breadboard-reflection/        -> skills/breadboard-reflection/
kickoff-doc/                  -> skills/kickoff-doc/
feed-planning-context/        -> skills/feed-planning-context/
```

The root folders are canonical. `skill-inventory.txt` defines the complete packaged set, and the `skills/` folder is the generated form Codex reads through `.codex-plugin/plugin.json`.

After changing a canonical skill, run:

```bash
bash scripts/sync-packaged-skills.sh
bash scripts/check-repo-health.sh
```
