# Compare interventions over the same evidence

After supported Phase E interpretation, use a counterfactual to identify what to learn about a transfer condition, a failure mode or a test choice. Compare candidate interventions after the Phase F gate and explicit frame acceptance, over the same frozen PASS requirements. Keep a status quo option where useful. Keep the same decision, x/y, target, observed baseline, selected episode, evidence, other held conditions, time horizon and outcomes. Specify each changed condition when changing multiple variables. Comparisons guide a test. Estimating causal effects requires a study design that identifies them.

Use one optional `counterfactuals.json` beside the study registries with `contract: lur-counterfactuals-v1`, `study_ref: LUR:<study_id>` and `scenarios: []`. New workspaces receive a local random study ID. To adopt this optional format in an old study, assign a fresh lowercase 32-hex ID in its manifest and render a new brief. Preserve all frozen records and the original evidence fingerprint. Use the same ID when moving a workspace and a new ID when branching to a different study.

Each scenario records:

| Field | Contents |
|---|---|
| Identity | `scenario_id` (CF##), `comparison_id` shared by proposed alternatives, `purpose` (TRANSFER_STRESS, INTERVENTION_COMPARE, EDGE_CASE or TEST_PRIORITY) |
| Binding | Current `evidence_fingerprint` and `scenario_digest` computed by `scenario_digest(study_ref, fingerprint, scenario)` from the documented script |
| Basis | `need_ref`, `episode_ref`, `evidence_refs`, `decision`, `owner`, `consequence_if_wrong`, `target`, `baseline` (including UNKNOWN if needed), `unknowns`, `held_constant`, `time_horizon`, `outcome_space` |
| Shaping basis | Within basis, `frame_ref`, `frame_digest`, `requirement_refs`. Use null, null, [] for the E-only route. Supply local `candidate_ref` and its `candidate_digest` for a candidate intervention. The standard-library script exposes both hash functions. |
| Hypothesis | `provenance: ANALYST_HYPOTHESIS`, `intervention` or STATUS_QUO, `changed_conditions` (empty for STATUS_QUO), `critical_assumption`, `predicted_behavior`, `rival_explanation`, `refuter`, `if_disproved`, `smallest_test`, `counterfactual_distance` |
| Review | `human_review: NOT_REVIEWED` for drafts. For REVIEWED, record actual `review_ref` and `review_digest` equal to the scenario digest. |

Copy one basis literally to compare alternatives. Use study-local IDs in the sidecar. Start with the LU1 and LU2 evidence for the selected qualified episode and add only relevant scoped evidence. Use namespaced references when handing off externally. Record the actual baseline and its limits. Do not substitute the expected effect for an observed result.

```bash
python lead-user-research/scripts/counterfactuals.py <workspace> --basis SF1
python lead-user-research/scripts/counterfactuals.py <workspace>
```

The check reports current, stale, noncomparable and invalid records. A changed evidence, frame, criterion or candidate basis requires a new scenario and review before reuse. Use a new CF## and retain the original as history. A stale or noncomparable comparison cannot be used for simulation. Existing study phases operate with or without the sidecar.
