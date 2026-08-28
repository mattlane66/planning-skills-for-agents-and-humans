# Phase A — Frame

Read:

- `../PROTOCOL.md`;
- current `manifest.json`;
- current `decision.json`;
- the user's current research request.

Do not perform broad Lead User discovery yet.

## Task

Define:

1. the exact decision this research should inform;
2. domain and target market;
3. mode — SCOUT / STANDARD / FULL;
4. study boundary;
5. desired innovation altitude;
6. starting assumptions;
7. consequential unknowns;
8. evidence that could disconfirm the starting hypothesis;
9. questions this method will not answer;
10. likely discoverability biases in an AI-plus-search study.

## Proportionality check

Confirm that the selected mode is proportionate.

If FULL is unnecessary, recommend STANDARD or SCOUT.

Do not silently change a user-selected mode; record the recommendation.

## Write state

Update:

- `manifest.json`;
- `decision.json`;
- initial `coverage.json`;
- `change_log.json` when modifying an existing study.

Write structured files before writing the human-readable phase summary.

If files are unavailable, emit a complete STATE PACKET.

## Exit gate

The phase is complete when another researcher can tell:

- what decision is being informed;
- what is in/out;
- what uncertainty matters most;
- what evidence could reverse the decision;
- what populations search may systematically miss.

Do not proceed by inventing missing scope. Mark consequential ambiguity.
