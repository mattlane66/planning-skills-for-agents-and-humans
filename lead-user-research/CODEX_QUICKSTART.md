# Lead User Research — Codex Quick Start

Use this when you want to run the Lead User Research system in Codex without managing the research files or Python scripts yourself.

## What you do

1. Open this repository in Codex.
2. Start a new Codex thread with the repository available.
3. Tell Codex to use `lead-user-research/SKILL.md` and create a new study under `research/[study-name]`.
4. Give it your research domain, what you want to understand, and the human decision the research should inform.
5. Add the target market or innovation altitude if you know them. If you do not, leave them unknown rather than guessing; Phase A may propose low-risk missing fields as **PROVISIONAL**.
6. When web or browser access is available, allow it so Codex can investigate real public sources, people, behavior, artifacts, communities, and advanced analogs.
7. Let Codex perform the **current valid phase**, persist the study state, run the repository's validation/controller checks when supported, and return the standard phase handoff.
8. If the handoff recommends another phase, say: **"Continue with the next valid phase."**
9. Repeat until the study reaches its decision or delivery stop.
10. Read the generated Decision Brief. You do not need to edit or interpret the JSON files yourself unless you want to audit the research record.

## Copy/paste starter

```text
Use the Lead User Research system in `lead-user-research/`.

Read `lead-user-research/SKILL.md` and follow it as the authoritative execution instructions.

Run a STANDARD study.

Research Domain / Problem Space:
[insert]

Target Market:
[insert, or leave unknown]

What do we want to understand?
[insert]

What human decision should this research help inform?
[insert]

Desired innovation altitude:
[insert, or leave unknown]

Create the study in `research/[study-name]`.

Use real public evidence and real people where available. Preserve links, citations,
evidence lineage, uncertainties, contradictions, and source-coverage limitations.

Run the current valid phase, persist the research state, validate it as required,
and end with the repository's standard phase handoff. Do not modify the Lead User
Research methodology itself.
```

## The important operating pattern

Codex is intentionally **phase-bounded** for this research system. Prefer:

> current phase → persist and validate → phase handoff → continue

over asking one long session to run the entire study from memory.

You do not need to run the Python commands yourself. They are infrastructure Codex can use to initialize the workspace, validate the persisted state, determine the next valid phase, and render the Decision Brief.

For the broader cross-platform workflow and mode definitions, see `QUICKSTART.md`. For the canonical methodology, see `PROTOCOL.md`.
