# Contract fixtures

These are lightweight structural checks for the planning method.

They are not behavioral model evaluations or benchmarks. They make a few required contracts explicit enough to catch documentation and packaging drift. Claims about model-output quality require separate scenario-based evaluations.

Run:

```bash
bash scripts/check-golden-evals.sh
```

## What they cover

- context packets include execution contracts
- Dumplink clusters vertically instead of by discipline
- Statechart output stays traceable to and subordinate to the accepted breadboard
- sketch reconciliation separates observations from interpretations and keeps visuals subordinate to accepted planning decisions
- drift checks use the strict output format
