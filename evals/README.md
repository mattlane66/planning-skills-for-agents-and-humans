# Golden evals

These are lightweight quality checks for the planning method.

They are not model benchmarks. They are small fixtures that make the repo's expected agent behavior explicit enough to guard against documentation drift.

Run:

```bash
bash scripts/check-golden-evals.sh
```

## What they cover

- context packets include execution contracts
- Dumplink clusters vertically instead of by discipline
- drift checks use the strict output format
