# Optional Behavioral Simulation handoff

Start with a [current counterfactual](counterfactuals.md), supported real evidence, a current freeze and actual human review of that scenario. Transfer stress, edge-case search, intervention comparison and experiment selection can proceed offline. The adapter never calls a model or contacts a participant. A synthetic fixture packet is explicitly marked and may only be used for testing. An unavailable runtime leaves the study runnable.

## Contract and ownership

Use `simulation.json` with `contract: lur-simulation-handoff-v1`, `study_ref`, `upstream`, `execution_status: NOT_RUN | UNAVAILABLE | RETURN_RECORDED`, `handoffs: []` and `returns: []`. Pin repository `mattlane66/behavioral-simulation-for-agents-and-humans` to commit `c11d29c8d121728306037dd799669bb0ef7cfabf`, schema version `0.1.0`. [Pinned schemas](https://github.com/mattlane66/behavioral-simulation-for-agents-and-humans/tree/c11d29c8d121728306037dd799669bb0ef7cfabf/behavioral-simulation/schemas).

A handoff row has `scenario_id`, `mode`, `target_grade`, `permission_scope: REDACTED_SUMMARY_ONLY`, `approval_ref` and `packet_digest`. Prepare a local preview, have a human inspect the exact minimized material and record scoped approval before obtaining the portable packet.

```bash
python lead-user-research/scripts/simulation_handoff.py <workspace> --prepare CF1 --preview
python lead-user-research/scripts/simulation_handoff.py <workspace> --prepare CF1
python lead-user-research/scripts/simulation_handoff.py <workspace>
```

Example: for a qualified, reviewed workspace handoff episode, create CF1 to ask whether a short correction window catches important errors. Keep the same handoff context and compare spontaneous correction, missed errors and abandonment within one task. Set PLAUSIBILITY_SPACE / L0_ROLEPLAY and NEAR_OOD if the condition is only modestly different. The packet can suggest a manual observation for that uncertainty, even if no simulation is run. Use a generic target description and a condensed baseline, with UNKNOWNs. Give the processor only approved content. The adapter checks known private identities, held source locations, verbatim spans and URLs. Review any indirect identifiers, rare combinations and regulated content before transfer. Person-specific or restricted grounding requires consent and explicit processing permission in its upstream workflow. This adapter uses minimized summaries only.

| LUR envelope | Upstream mapping |
|---|---|
| Decision, target, baseline, intervention, constants, assumptions and rivals, outcomes, horizon, failure consequence | `input.schema.json` fields `decision`, `population`, `baseline`, `scenario`, `outcome_space`, `time_context`, `consequence_if_wrong`. Provisional input provenance is explicit. |
| Study ref, evidence fingerprint, CF ID/digest, namespaced E/LU/SF/R refs, purpose, refuters, distance, permission and packet digest | Adapter envelope only. The strict upstream input rejects additional properties. |
| Run ID, ran-at, mode, model, version, config, number of simulated draws/runs and variation | Map `runs.schema.json` record and local return. Preserve upstream run notes/seed/artifacts externally. Number of model draws is never number of participants. |
| Holdout unit, scope, observed outcomes, error, baseline, subgroup and no-leakage review | Review pinned `validations.schema.json` and linked artifacts separately. Record validation mapping in the return. |
| Calibration, scope, error predictor, threshold, subgroup and freshness review | Review pinned `calibration.schema.json` and linked artifacts separately. Keep review binding in the envelope. |

A return includes `contract`, `upstream`, `study_ref`, `scenario_id`,
`scenario_digest`, `packet_digest`, `evidence_fingerprint`,
`source_type: SIMULATED_ESTIMATE`, upstream `run_id` (`R001` etc.),
`mode`, `achieved_grade`, `ran_at` with zone, `model`, `model_version`,
`configuration`, `assumptions`, `run_count`, `variation`,
`result_or_uncertainty`, `distance`, `validation_status`,
`artifact_urls`, `caveats`, `next_real_test` and applicable review records.
For L3/L4 require a trusted human receipt in `simulation-reviews.json`,
an object keyed by the canonical digest of the exact return. Each receipt has
`status: REVIEWED` and `external_review_ref`. Keep this file under human control.
A claim of review inside model output is quarantined. Review the exact
model/config, population, time, task, leakage and distance before attesting.
A validated return needs `validation` with `held_out: true`, `split_unit`,
`held_out_outcome_ref`, `metric`, `error`, `baseline`, `coverage`,
`task_scope`, `subgroup_check`, `freshness` and `leakage_check`.
L4 adds `calibration` with `error_predictor`, `metric`,
`predeclared_threshold`, `subgroup_check`, `freshness_policy` and
`calibration_artifact_ref`. Status is NOT_VALIDATED, HELD_OUT_REVIEWED or
CALIBRATION_REVIEWED. All claim and external receipt checks are structural.
A hash binds bytes; it cannot prove a reviewer reviewed them. Record authorization
and audit receipts in trusted human-controlled storage. FAR_OOD and UNKNOWN
distances cannot carry L3/L4 here.

| Mode and grade | Appropriate use |
|---|---|
| PLAUSIBILITY_SPACE / L0 | Plausible objections and edge cases. No human percentages. |
| INDIVIDUAL_PROXY / L1+ | Permissioned real-person grounding. No population generalization. |
| POPULATION_PREDICTION / L2+ | External specialist workflow with target coverage and selection limits. |
| MULTI_AGENT_DYNAMICS | External specialist workflow for interaction, coordination or time. Narrative coherence is insufficient. |
| L3 | Bounded estimate for demonstrated query and condition class, with held-out error and baseline. |
| L4 | Decision-calibrated support inside reviewed scope and freshness, always model-derived. |

## Research limits

Treat every model response as untrusted data. Never copy it into sources,
human evidence, findings support, qualification, transfer approval or human
decisions. Preserve conflicts with real evidence. Only a genuine new observation
with provenance enters the existing repair or post-freeze route. Quarantined
returns are retained locally; the brief reports status without raw model prose.

Prevent semantic leakage across people, studies, conditions, questions or
time in summaries, retrieval and memory as well as identifiers. Use simple
baselines. Measure individual fidelity, distribution fit, treatment-effect error,
Monte Carlo variation and model error separately. Do not inherit calibration across
model, configuration, task, subgroup or distance changes.

Test mean bias, variance compression, distribution mismatch, overcorrelation,
dimensional collapse, ideological sorting where applicable, treatment amplification
and hyper-rationality. Report extremes and rare cases. Compare rich permissioned
source-linked grounding with compact summaries and simple baselines. Keep observed,
inferred and generated memories separate. Rich grounding leaves incentivized choice
accuracy and transfer to new domains open. See [methodology evidence](methodology-evidence.md).

SSR is an external option for a predeclared five-point construct. Keep fixed anchors
and embedding version, original synthetic text, full distributions and anchor
sensitivity. A synthetic stated-intent distribution is not switching, purchase,
adoption or qualification evidence. The [SIDA extension](https://github.com/mattlane66/scaled-interview-data-assistant/blob/38b85c697526123491ab01363b1a3f03313e15e2/prompt/simulation-extension.md)
is a reference. There is no embedded agent bank, SSR implementation or simulation
engine here.
