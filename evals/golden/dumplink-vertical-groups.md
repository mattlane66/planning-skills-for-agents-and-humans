# Contract fixture: Dumplink vertical groups

## Input

A shaped feature has UI work, API work, persistence work, copy, QA, and launch notes.

## Expected qualities

A good Dumplink output must:

- ingest the selected project as the discrete unit of work
- preserve the shaped project boundary
- dump tasks before sequencing
- cluster by judgeable user/system behavior, not by discipline
- treat each task group as a vertical implementation slice created from the project
- use task IDs such as `T1`
- use task group IDs such as `TG1`
- mark each task group's risk state
- map causal dependencies between task groups
- sequence risk-unlocking and dependency-unlocking groups first
- name scope cuts before implementation begins
- stop for task-group plan approval and active-group selection
- end with one bounded handoff packet for the selected group

## Failure examples

Fail if the output clusters only as:

- Frontend
- Backend
- Design
- QA

Fail if it treats task count as progress while an important unknown remains unresolved.

Fail if it asks for a selected implementation slice before decomposing the project.
