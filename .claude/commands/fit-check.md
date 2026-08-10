---
description: Run working or decision-ready fit checks across existing shapes without selecting a direction.
argument-hint:
- shaping file
- criteria
- shapes
- notes
- or selected comparison set
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
disable-model-invocation: true
---

Read `shaping/SKILL.md` first and follow it as the primary instruction for this command.

Use this focused command whenever a fit check would clarify the current shaping uncertainty. Fit checks may happen repeatedly; they are not reserved for the end of shaping.

Also read `docs/human-decision-gates.md`.

User request and source context:

$ARGUMENTS

Produce or update the Fit Check and Reverse Fit Check sections of a shaping artifact.

In collaborative mode:

- requirements may be Working or Accepted
- Appetite may be Unset, Working, or Accepted
- if judging inputs are provisional, label the result `Working fit check`
- a working fit check may reveal missing requirements or unjustified mechanisms, but cannot support final shape selection until the required judging inputs are accepted
- when Appetite is missing, omit final Appetite-fit claims and state what cannot yet be judged

In gated/orchestrated mode, enforce the stricter prerequisites in `.agent-orchestration.yaml`.

Fit check rules:

- compare the available requirements against the available shapes
- use full requirement text
- use binary `✅` or `❌` for requirement satisfaction; unknown is not a pass
- put explanations below the table
- use candidate breadboards and spikes as subordinate evidence
- identify any requirement that the comparison itself reveals should be added or revised

Reverse fit rules:

- check whether every shape part serves at least one requirement
- mark unjustified mechanisms as `❌`, Cut, or Needs requirement
- when a genuine missing need is exposed, propose it as Working R rather than silently accepting it

Do not select a direction unless the user explicitly gives the selection and the hard selection gate is satisfied. Do not promote candidate evidence or write production code.

End with the smallest next useful move: revise R, revise S, spike, candidate breadboard, set/revisit Appetite, rerun fit, or prepare selection.
