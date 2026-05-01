# Codex plugin support

This repository can be installed as a Codex plugin. The plugin packages the existing planning skills under `skills/` and exposes them through the Codex plugin manifest at `.codex-plugin/plugin.json`.

## What is included

The Codex plugin includes these skills:

- `framing-doc`
- `shaping`
- `breadboarding`
- `breadboard-reflection`
- `kickoff-doc`
- `feed-planning-context`

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

## Use

Example prompts:

```text
Use Planning Skills for Agents and Humans to frame this feature before implementation.
```

```text
Use the shaping skill to compare possible solution directions before choosing one.
```

```text
Use the breadboarding skill to map places, affordances, stores, state, and wiring for this feature.
```

```text
Use the feed-planning-context skill to package the active planning artifacts for an implementation agent.
```

## Maintenance

Keep the root skill folders and the `skills/` copies aligned:

```text
framing-doc/                  -> skills/framing-doc/
shaping/                      -> skills/shaping/
breadboarding/                -> skills/breadboarding/
breadboard-reflection/        -> skills/breadboard-reflection/
kickoff-doc/                  -> skills/kickoff-doc/
feed-planning-context/        -> skills/feed-planning-context/
```

The root folders are useful for humans and other agent tools. The `skills/` folder is the plugin-packaged form Codex reads through `.codex-plugin/plugin.json`.
