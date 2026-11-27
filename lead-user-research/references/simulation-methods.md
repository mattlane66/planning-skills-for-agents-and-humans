# Simulation-assisted Lead User Research — operating methods

Status: proposed research extension, not a validated improvement to the Lead User Method.
Source review date: 2026-11-27. This document turns the simulation literature into
conditional research moves. It does not claim that every paper, supplement and
replication artifact has been read end to end. See the coverage ledger below.
Von Hippel remains the governing methodology. Behavioral Simulation remains the
owner of simulation modes, evidence grades, execution and validation. This local
reference owns how those methods are used in Lead User Research.

## 1. Route the unknown

For every material gap, name the decision, unresolved variable, current evidence
refs, observability and missing population/context coverage. Ask what different
answers would change. Search or observe directly where feasible; optionally use
simulation to develop new search routes, design observations or evaluate scenarios.
Keep data-processing permissions and hard search constraints intact. Never simulate
to satisfy a quota, confirm a favored concept, or fill a missing evidence field.

| Question | Method | Earliest permitted use | Return to Lead User Research |
|---|---|---|---|
| What contexts, behaviors, workarounds, refuters might we have missed? | PLAUSIBILITY_SPACE: scenario generation, branching, alternative continuations | A/B, L0 possible with no data | Proposed searches/contrasts only |
| What might this specific person do in another circumstance? | INDIVIDUAL_PROXY: rich self-report and behavioral grounding | B/C with consent and real person evidence | Person-specific hypotheses, tests, not observations |
| How might needs spread as the environment changes? | MULTI_AGENT_DYNAMICS: time, memory, network, feedback | B/E; actual parameters required for predictive claims | Conditional trajectories and mechanisms to investigate |
| How does a defined outcome vary across a population? | POPULATION_PREDICTION: empirical sample frame, outcome distributions | Separate quantitative study; not the purposive lead-user sample | Model-derived estimate with scope, uncertainty and validation |
| How to measure a generated ordinal attitude? | DLR/FLR/SSR comparison | Eligible simulation run, fixed construct | Measurement of generated text |
| Can real labels improve an estimate from many model predictions? | PPI/DSL rectification | Separate eligible survey design | Scoped model-assisted estimate |
| Is the result trustworthy enough for its intended use? | Held-out fidelity, distortion, robustness and error-prediction tests | Plan before generation; assess afterward | Validation report, no evidence promotion |

Run one mode per simulation study/run under the companion skill. Select only the
methods required. A material lack of real evidence must remain open after simulation.
If the question is trace-observable, follow the suggested routes to real records.
For each completed or aborted run, save the separate run ID and return packet.
Never turn generated personas into SRC/E/LU IDs, referral nodes, independent
pyramids, trend support, prevalence or fieldwork participation. After a freeze,
new real evidence goes through the existing change contract.

## 2. Explore breadth (Social Simulacra)

Source: Park et al., [UIST 2022, sections 3–7](https://arxiv.org/html/2208.04024v1).
The study evaluates social prototypes for plausibility and designer utility, not
calibrated population prediction.

Local procedure:
1. Encode the real or explicitly hypothetical environment: actors, goals, rules,
   constraints, artifacts, information access and allowed actions. Seed it with
   a small set of behaviorally distinct situations; mark which are grounded.
2. Expand across an explicit condition matrix (e.g. scale, expertise, tool access,
   resources, authority, dependency). Include extremes, ordinary cases, failure,
   refusal and abandonment. Do not equate diversity of generated prose with diversity
   of needs. Assign synthetic-only IDs; no real names or invented source links.
3. Generate an initiating episode and conditional responses in stages. Preserve
   roles, prior states, provenance and alternative continuations. Test whether a
   changed rule or constraint changes the response; vary one factor at a time
   when a contrast is useful.
4. Branch from one fixed state and generate alternative plausible futures, including
   adverse outcomes and no effect. Record seeds/config where supported. Do not
   assign frequencies to alternative paths without a validated sampling model.
5. Extract distinct mechanisms and convert them into a specific observable prediction,
   refuter and query or fieldwork plan. Search separately through target, advanced
   analog and attribute-specific paths. Do not count simulations as search results.

Local adaptation: a simulated missed case is a search lead, not a new qualified
lead user. Evaluate incremental real discoveries per unit of research effort.
A simulation that fails to generate a rare but real case is not evidence of absence.

## 3. Persistent agents and conditional frontier movement

Source: Park et al., [UIST 2023, sections 4–7](https://arxiv.org/html/2304.03442v2).
The memory/planning architecture supports temporal coherence; the evaluation of
believability and emergence does not validate real-market diffusion.

Local procedure:
- State explicit environmental affordances, social graph, heterogeneous initial
  conditions, simulation clock, horizon, events, and how people learn or change.
- Each agent has a bounded experience log; each memory has time and source
  (observed grounding vs simulated event). Retrieve using normalized recency,
  relevance and importance scores. Treat their weights and decay as parameters
  to test, not universal human properties.
- Make reflections cite prior memory IDs; retain reflection as model inference.
  Plan at a coarse horizon, refine to executable actions, react to new observations,
  update shared environment and record the consequences. No future information
  may leak into current state or private memory into another agent.
- Branch identical initial states across changes in cost, access, network topology,
  rules or skills. Repeat runs and preserve no-diffusion, stalled and reversed
  trajectories. Remove memory, reflection, planning or edges in ablations where
  the question depends on these mechanisms.
- Evaluate real system observables (time to spread, reached nodes, conditional
  transitions, bottlenecks, distributions of activity, failures). If ground truth
  is absent, report assumption-conditioned possibilities only. No timing forecast
  or propagation evidence is created by a convincing trajectory.

Lead User frontier map: use separately evidenced LU1/LU2 episodes to annotate the
current frontier. Simulated future positions use a separate overlay and never
change qualification or empirical propagation. Compare alternative constraint
scenarios, not a predetermined upward adoption curve.

## 4. Person grounding and measurement distortions

Source: Park et al., [arXiv:2411.10109v4](https://arxiv.org/abs/2411.10109v4),
revised 2026-11-16, main paper and SI section 9.13. The revision is titled
*AI Simulations Grounded in Rich Self-Reports Increase Accuracy and Reduce Distortion*.
Combined self-report grounding improved many attitude tasks, but did not improve
the incentivized economic games. Do not transplant its accuracy into a new domain.

Local procedure:
- Use permissioned interviews/traces and structured self-report about the actual
  person. Ask broad neutral questions before revealing the target evaluation.
  Preserve contradiction and uncertainty; do not generate missing biography.
- Contrast generic, minimal-profile, person-authored description, structured
  responses, interview-only and combined grounding; add a concise summary variant
  if data minimization is required. Don't assume richer is always better.
- Reserve genuinely unseen questions/outcomes for the same individual; separate
  repeated-item retest prediction from new-item generalization. For training or
  tuning, split at participant level and keep all their dependent records together.
  Check semantic duplicates, not just IDs. Compare same-person held-out outcomes
  and, when feasible, a human repeat measurement.
- Treat predicted behavior under changed conditions as hypothetical until tested
  in a relevant actual behavioral task; ask specifically whether incentives
  change behavior in ways the model misses.

Distortion audit (adaptation of v4 Table 1 and SI 9.13):
| Failure | Local diagnostic |
|---|---|
| Mean bias | absolute standardized mean gap with human reference SD |
| Variance compression | simulated/human SD ratio; handle zero SD explicitly |
| Distribution distortion | ordered earth mover distance or categorical TVD |
| Excess cross-item dependence | mean absolute Spearman correlation and matrix differences |
| Dimensionality collapse | first component share, same coding/scaling and missing-data policy |
| Sorting/stereotyping | compare predeclared group/attribute associations, avoid sensitive proxies unless necessary and permitted |
| Inflated intervention effects | compare estimated signs and magnitudes to held-out human contrasts |
| Hyper-rationality | compare to actual incentivized choices and a stated theoretical baseline |

Use paired unit-level resampling when applicable; report interval, sample sizes,
missingness and nonapplicable tests. Compare to generic and person-grounded
baselines and report deterioration too. A predictive claim on one outcome family
does not authorize another. Preserve test-retest as a reference, not a perfect
ceiling or automatic normalized score.

## 5. Population response modelling

Source: Kolluri et al., [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1530/);
[arXiv:2509.05830](https://arxiv.org/abs/2509.05830), sections on metrics,
generalization, prompting and subgroup results. The preprint and proceedings
abstracts report different relative gains; cite the exact version, not a merged value.

Local procedure:
- Define the estimand, target population, sampling frame, real covariates, stimulus,
  possible outcomes and horizon. Record who is missing from the frame.
- For an external dataset, normalize records by study, participant, condition,
  outcome and measurement scale; preserve original stimulus and response coding.
  Exclude leakage and ambiguous labels. Respect licensing and privacy.
- Compare direct prompting, permitted examples retrieved only from training data,
  and task-specific supervised adaptation when independently eligible. Never
  train on inference labels. Choose a method based on evidence, not brand.
- Separate holdouts by question/outcome, condition, participant and entire study,
  according to the claimed generalization. Report which dimension is actually
  unseen. Validate with the same unit and scale as the intended decision.
- For ordered outcomes compare normalized Wasserstein distance; for unordered
  categories use TVD. Report individual accuracy separately, groupwise error and
  human-only resampling/no-information baselines. Do not pool all groups until
  poor performance disappears. Estimate treatment effects only with an appropriate
  human experimental comparison.
- A purposive frontier sample is not a representative sample. More generated rows
  do not justify cluster counts, incidence, adoption or need prevalence.

## 6. Ordinal measurement (SSR, FLR, DLR)

Source: Maier et al., [arXiv:2510.08338v3](https://arxiv.org/html/2510.08338v3),
sections 3–5, Appendices A, C–E. Existing executable SSR:
[Scaled Interview Assistant](https://github.com/mattlane66/scaled-interview-data-assistant/blob/main/simulation/ssr.py).
Reuse it rather than fork code. It requires externally computed embeddings.

Local procedure:
- Only use for a fixed declared ordinal attitude: e.g. stated relevance of a
  hypothetical condition, not LU qualification or real revealed behavior.
- Compare direct rating (DLR), text then separately rated (FLR), and text embedded
  against anchor sets (SSR). Keep identical stimulus and eligible population.
- Create construct-specific ordered anchors before outcomes are seen. For each
  set, cosine similarity to the generated response, subtract the minimum,
  optionally add epsilon and apply temperature power, normalize to a PMF.
  Aggregate across preregistered anchor sets; retain per-set sensitivity.
  Reject degenerate embeddings. Keep verbatim text as simulated text.
- Compare PMFs with real human held-out response distributions (KS similarity for
  ordered categories, TVD), and across-concept mean correlations. If replicating
  correlation attainment, use repeated equal-sized human split-half cohorts,
  compare corresponding synthetic samples and divide mean cross-source
  correlation by mean human split-half correlation; undefined for zero denominator.
  This is a relative ranking statistic, not individual accuracy or purchase probability.
- Include naive/direct and alternate measurement baselines, stimulus format
  sensitivity and grounding ablations. Do not choose anchors on test data.

## 7. Scarce labels: synthesis and statistical rectification

Source: Krsteski et al., [ACL 2026](https://aclanthology.org/2026.acl-long.498/),
[preprint v2](https://arxiv.org/html/2510.11408v2), sections 3–6, Appendix B.
The paper compares profile prompts, persona/history-based prompting, domain and
external distribution fine-tuning, and model-assisted correction. Multi-turn
elicitation can increase acquiescence; reserve real responses for correction
rather than spend them all on adaptation.

Local procedure:
- Only on a separate defined population estimand and eligible real sampling
  design, with a large real covariate frame and smaller paired human labels.
  Predeclare numeric mapping (ordinal scale, binary indicator, scalar unit).
  Separate fitting/tuning/correction and final validation roles. No generated
  covariates as substitutes for real population units; no convenience sample
  pretending to be representative. Do not apply to a missing episode.
- With independent i.i.d. labeled and unlabeled samples from the same population,
  frozen predictor independent of inference samples, and fixed lambda in [0,1],
  estimate mean = lambda * mean(pred_U) + mean(y_H - lambda*pred_H).
  Estimated variance = lambda^2 * var(pred_U)/N + var(y_H-lambda*pred_H)/n.
  Lambda=0 is human-only, lambda=1 full correction. Compare precision and real
  coverage against human-only and raw simulation; don't assume improvement.
- For PPI++ power tuning or quantile/regression estimating equations, route to a
  validated statistical implementation and document the theorem/sampling design.
  The preprint appendix power-tuning description is inconsistent with main
  equation conventions; use main equation (1) for the mean and verify the
  original PPI++ methodology before implementing adaptive tuning. No informal
  tuning on inference outcomes, naive binomial CIs on generated respondents,
  or claiming observed sample size increased.
- Report n human, N real covariate units, model draws separately; estimator,
  interval method, bias, variance, coverage, subgroup errors and actual effective
  sample size comparison if supported. Fixed-weight implementation is in the
  companion [draft PR #3](https://github.com/mattlane66/behavioral-simulation-for-agents-and-humans/pull/3);
  not an automatic Lead User workspace operation.

## 8. Conditional fidelity, model risk and calibrated error

Sources: Bisbee et al., [Political Analysis 2024](https://doi.org/10.1017/pan.2024.5),
sections 2–3; Bommasani et al., [Foundation Models v3](https://arxiv.org/html/2108.07258v3),
especially sections 4.4, 4.6–4.8 and 5; Simile, [Building confidence](https://www.simile.com/blog/confidence)
and [What-If Machine](https://www.simile.com/blog/what-if-machine). Simile is
public product methodology, not an independently replicated result.

- Compare conditional regression relationships with real data, not only mean
  alignment. Use same coding, specification and units; preserve coefficient
  magnitude, sign, uncertainty and variance gaps. Test prompt paraphrase, option
  order, model/version, temperature and time sensitivity; use human variance/effect
  estimates for planning human sample size. Do not power an experiment from
  synthetic variance.
- Treat the foundation model as part of the measurement instrument. Record
  access/model/config/data lineage; compare independent baselines, evaluate
  robustness, group fairness, privacy, security, cost and suitability. Shared
  base-model outputs are dependent; never present independent draws as humans.
- For material predictive decisions, define decision-quality threshold in advance.
  Obtain independent real outcomes, compute observed error (e.g. TVD), train a
  separate error predictor on prior labeled questions, evaluate on unseen query
  families with groupwise/nested splits. Compare simple distribution features,
  question embeddings and, only if actually accessible, model representations
  or a tuned error-prediction model. Report RMSE, discrimination (AUROC for
  threshold) and correlation as separate diagnostics; examine calibration and
  coverage of accepted decisions. No generic product threshold imports.
- Recheck drift, freshness, counterfactual distance, subgroup error and changes in
  model/configuration. Decline predictive use if outside validated scope. Record
  whether each metric was computed or remains NOT_ASSESSED.

## 9. Return packet and benchmark

Use the [run worksheet](simulation-discovery-worksheet.md) for every material
simulation. It is an optional companion record, not a new required canonical
workspace registry. Do not insert simulation output in evidence tables.
For a real test of the integrated method, preregister equal resource budgets and
blind independent source corpora, randomize order/assignment where possible,
and compare search-only vs simulation-assisted discovery. Primary outcome:
new independent human-evidenced qualified LU episodes per budget. Secondary:
unique supported needs, counterexamples, coverage across independent branches,
precision of proposed searches, false positives, effort and missed real cases.
Use independent human adjudicators and retained sources. Report uncertainty,
disagreement, failed runs, and no-improvement cases. Never confuse a successful
fixture validation with scientific validation.

## Source coverage ledger

All eight sources identified; original source records checked on 2026-11-27.
The following is a transparent **partial primary-source extraction**, not a
full-paper reading certificate. Each source link is versioned where available.

| Source | Examined in this pass | Outstanding before comprehensive sign-off |
|---|---|---|
| Social Simulacra v1 | HTML introduction, method headings, persona expansion and branching excerpts, evaluation context | Read all remaining sections, examples and limitations in full |
| Generative Agents v2 | Original abstract and HTML memory/retrieval excerpts | Full architecture, implementation, experiment and ablation details |
| Rich Self-Reports v4 | Abstract, main results, evaluation figure and SI 9.13 excerpts | Remaining 123-page paper/SI, exact distortion formulas and training splits |
| SocSci210 | Proceedings abstract, preprint metrics/baselines and subgroup excerpts | Full proceedings PDF timed out; reconcile version differences and appendices |
| Foundation Models v3 | Abstract and evaluation sections/excerpts | Full report, including application/security/fairness sections |
| SSR v3 | HTML methods/results, metrics, anchor appendix excerpts | Remaining appendix/code audit and paper reproduction |
| Valid Survey Simulations | Proceedings abstract, PDF equation page, preprint methodology/appendix/ablation excerpts | All remaining pages and appendices, replication code, original PPI++ convention verification |
| Synthetic Replacements | Publisher article mean/variance/regression excerpts | Remaining article, sensitivity analysis, supplements and replication |
| Simile | Public confidence and What-If pages, error-model and metrics excerpts | Remaining text/claims; private architecture not available |

No full-text reproduction is included. Local procedures are original adaptations,
not claims that the source authors validated Lead User Research. Maintain this
ledger as later full-paper reviews are completed.
