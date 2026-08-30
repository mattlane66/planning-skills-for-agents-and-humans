# Lead User Research — Project / Files Quick Start

Use this when you want to run the Lead User Research system in a ChatGPT Project, Claude Project, or another chat workspace that can keep files available across turns but cannot run the repository's Python scripts.

## What you do

1. Create a new Project or persistent chat workspace.
2. Add `lead-user-research/SKILL.md` and `lead-user-research/PROTOCOL.md`.
3. Add the prompt for the phase you are starting with: `lead-user-research/prompts/phase-a-frame.md`.
4. Start a new conversation inside that Project.
5. Give the AI your research domain, what you want to understand, and the human decision the research should inform.
6. Tell it to create and maintain the structured study state as files in the Project. If the platform cannot create files directly, have it return the complete updated file contents so you can save or replace them.
7. When web or browser research is available, allow it so the AI can investigate real public sources, people, behavior, artifacts, communities, and advanced analogs.
8. At the end of the phase, make sure the updated study files remain available in the Project.
9. Before the next phase, add or reference that phase's prompt and tell the AI to **re-read the saved study files first**. Do not let conversational memory become the source of truth.
10. Repeat until the study reaches its decision or delivery stop, then read the generated Decision Brief.

## Copy/paste starter

```text
Use the Lead User Research system from the files in this Project.

Read `SKILL.md`, `PROTOCOL.md`, and the Phase A prompt before beginning.
Treat the saved study files in this Project as authoritative state.

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

Use real public evidence and real people where available. Preserve links, citations,
evidence lineage, uncertainties, contradictions, and source-coverage limitations.

For this turn, perform only the current valid phase. Create or update the structured
study files before writing narrative synthesis. End with the repository's standard
phase handoff and name the next valid phase.

You do not have shell access, so do not claim that deterministic Python validation
ran unless this platform actually supports it.
```

## What files should stay in the Project

At minimum, keep:

- `SKILL.md`
- `PROTOCOL.md`
- the prompt for the phase you are running
- the study JSON/state files created during the research
- the generated Decision Brief or other final outputs

You do **not** need to upload every file in the repository at once.

## Moving to the next phase

When the phase handoff says to continue, add or reference the next prompt from `prompts/` and say:

```text
Re-read all authoritative study files in this Project first.

Then run the next valid Lead User Research phase using the attached/referenced phase
prompt. Update the structured study state before narrative synthesis and end with
the standard phase handoff.
```

The relevant prompts are:

- Phase A — `prompts/phase-a-frame.md`
- Phase B — `prompts/phase-b-discover.md`
- Phase C — `prompts/phase-c-evidence.md`
- Phase D — `prompts/phase-d-freeze.md`
- Phase E — `prompts/phase-e-interpret.md`
- Phase F — `prompts/phase-f-shape.md` only when the Concept Generation Gate passes
- Phase G — `prompts/phase-g-decide.md`
- Phase H — `prompts/phase-h-deliver.md` when the selected mode requires delivery

## The important operating pattern

For a Project/files workflow, prefer:

> saved files → re-read state → current phase → update files → phase handoff → continue

The saved files are the research memory. The conversation is not.

Unlike the Codex/repository path, this setup may not be able to run `validate_study.py` or `next_research_move.py`. The AI should be explicit about that limitation rather than claiming deterministic validation it did not perform.

For an ordinary chat with no persistent files, use `PORTABLE_PROMPT.md` instead. For the full repository-backed Codex path, use `CODEX_QUICKSTART.md`. For the broader cross-platform workflow and mode definitions, see `QUICKSTART.md`.
