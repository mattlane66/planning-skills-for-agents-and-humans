# Phase A — Frame

Read:

- `../PROTOCOL.md`;
- current `manifest.json`;
- current `decision.json`;
- the user's current research request.

Do not perform broad Lead User discovery yet.

## Task

Preserve or define:

1. Research Domain / Problem Space;
2. Target Market;
3. What do we want to understand? — the learning objective;
4. What human decision should this research help inform?;
5. Desired innovation altitude;
6. Optional starting hypotheses;
7. optional discovery seeds;
8. optional candidate-profile hypotheses;
9. optional search constraints;
10. mode — SCOUT / STANDARD / FULL;
11. study boundary;
12. starting assumptions;
13. consequential unknowns;
14. evidence that could disconfirm the starting hypothesis;
15. questions this method will not answer;
16. likely discoverability biases in an AI-plus-search study;
17. actual study execution level — DESK_RESEARCH | FIELDWORK_ENRICHED | FULL_LEAD_USER_PROJECT — and its basis.

## Hypothesis challenge setup

For every starting hypothesis create or update H## in hypotheses.json. Before broad discovery, define when possible:

- observable predictions;
- strongest plausible refuter;
- rival explanations;
- targeted refutation searches.

Use status UNTESTED. Never use CONFIRMED.

## Observability map

Create O## records in observability.json for facts or variables that could materially change the decision. Record whether each appears TRACE_OBSERVABLE, PARTIALLY_OBSERVABLE, NOT_OBSERVABLE, or UNKNOWN. Do not recommend fieldwork merely because an item is unknown.

Do not silently collapse the learning objective into the decision. Preserve the user's wording for supplied fields. If a missing brief field can be drafted safely, label it PROVISIONAL; if it could materially change scope, leave it UNKNOWN or request clarification when appropriate.

Treat discovery seeds and candidate-profile hypotheses as starting directions, not qualification evidence or a closed search universe. Preserve explicit search constraints as hard boundaries. If a human supplies sources, people, communities, or candidate profiles without explicitly restricting the search to them, record them as seeds/hypotheses and allow Phase B to pyramid outward.

Default to DESK_RESEARCH. Set FIELDWORK_ENRICHED only when direct interviews, observation, or comparable fieldwork materially informs the study. Set FULL_LEAD_USER_PROJECT only when direct Lead User/expert participation supports both need/solution learning and collaborative concept development. FULL run mode alone does not justify that execution label.

## Proportionality check

Confirm that the selected mode is proportionate.

If FULL is unnecessary, recommend STANDARD or SCOUT.

Do not silently change a user-selected mode; record the recommendation.

## Write state

Update:

- `manifest.json`;
- `decision.json`;
- initial coverage.json;
- hypotheses.json;
- observability.json;
- change_log.json when modifying an existing study.

Write structured files before writing the human-readable phase summary.

If files are unavailable, emit a complete STATE PACKET.

## Exit gate

The phase is complete when another researcher can tell:

- what the study is trying to understand;
- what decision is being informed;
- what is in/out;
- what uncertainty matters most;
- what evidence could reverse the decision;
- what populations search may systematically miss;
- which discovery inputs are seeds/hypotheses versus hard search constraints;
- how each starting hypothesis could be falsified;
- which decision-critical unknowns are trace-observable versus likely to require targeted fieldwork.

Do not proceed by inventing missing scope. Mark consequential ambiguity.

## Phase handoff

After writing and validating this phase, follow
`references/phase-handoff.md`. For a file-backed study, derive the next move with
`scripts/next_research_move.py`; do not advance from invocation history alone.
