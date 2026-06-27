# Golden eval: Dumplink vertical groups

## Input

A shaped feature has UI work, API work, persistence work, copy, QA, and launch notes.

## Expected qualities

A good Dumplink output must:

- preserve the shaped project boundary
- dump tasks before sequencing
- cluster by judgeable user/system behavior, not by discipline
- use task IDs such as `T1`
- use task group IDs such as `TG1`
- mark each task group's risk state
- map causal dependencies between task groups
- sequence risk-unlocking and dependency-unlocking groups first
- name scope cuts before implementation begins
- end with one bounded agent handoff packet

## Failure examples

Fail if the output clusters only as:

- Frontend
- Backend
- Design
- QA

Fail if it treats task count as progress while an important unknown remains unresolved.
