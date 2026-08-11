# Planning eval fixtures

These files provide lightweight structural contracts plus scenario corpora for testing routing and workflow behavior.

They are not universal model benchmarks. Structural checks catch repository drift; scenario cases describe expected skill selection and authority behavior that can be exercised in a specific runtime or model harness.

Run the deterministic structural checks with:

```bash
bash scripts/check-golden-evals.sh
```

## What the structural fixtures cover

- collaborative shaping is allowed to start from S as well as R
- promotion gates remain explicit even when exploration is fluid
- candidate breadboards stay exploratory and selected-design authority stays gated
- breadboards preserve causal integrity from entry through observable consequence
- current-state maps stay grounded in concrete evidence and selected designs omit low-value plumbing
- context packets include execution contracts
- Dumplink clusters vertically instead of by discipline
- Statechart output stays traceable to and subordinate to the accepted breadboard
- sketch reconciliation separates observations from interpretations and keeps visuals subordinate to accepted planning decisions
- drift checks use the strict output format

## Scenario corpora

`skill-activation-cases.json` tests near-neighbor routing, including:

- solution-first work routes to `shaping`, not automatically back to framing
- focused spike requests stay inside `shaping`
- candidate behavioral questions route to `breadboarding`

`workflow-behavior-cases.json` tests method behavior, including:

- S-first shaping extracts Working R without selecting the shape
- Working fit checks can improve R/S before Appetite is accepted
- collaborative candidate breadboarding may use provisional judging inputs while keeping final claims provisional
- current-state breadboards cite actual code evidence instead of inventing generic architecture
- breadboards detect dangling wires, source-less displays, and branches without consequences
- selected-design breadboards include product-relevant seams while omitting wrappers and forwarding-only calls
- focused spikes return explicit R/S/fit/Appetite implications without deciding the product direction
- the gated/orchestrated profile still enforces deterministic prerequisites
- final shape selection still requires Accepted R, Accepted Appetite, decision-ready evidence, and explicit human choice

When changing canonical descriptions, profile behavior, command wrappers, or packaging, update these corpora in the same change and rerun the relevant runtime-specific activation tests.
