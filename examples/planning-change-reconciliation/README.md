# Planning changes after kickoff

This fictional example demonstrates a **decision**, a **suggestion**, and a **human-readable proposal** without inventing project authority.

Current accepted plan: [accepted-shaping.md](./accepted-shaping.md).
Meeting notes: [meeting-notes.md](./meeting-notes.md).
Private proposed revision: [private-shaping-v2.md](./private-shaping-v2.md).
Proposed delta inventory: [change-review.json](./change-review.json).

The meeting suggests batch export, but does not decide it. D1 remains `pending` even though the suggested mechanism appears in the proposed draft. The exact change to existing R1 is also pending until an authorized reviewer accepts it. D2 is merely editorial; no new product scope is implied.

Generate a human-readable *read-only* diff (run from repository root):

```sh
python3 scripts/publish-shaped-work.py \
  --review-base examples/planning-change-reconciliation/accepted-shaping.md \
  --review-proposal examples/planning-change-reconciliation/private-shaping-v2.md \
  --review-record examples/planning-change-reconciliation/change-review.json \
  --review-output /tmp/planning-change-review.html
```

Review and decide. Only after acceptance should the relevant canonical files, dependent breadboards, slices, and derived views be updated. The review command never merges them.
