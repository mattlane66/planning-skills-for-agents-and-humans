# Simulation-assisted Lead User Research — operating methods

Research extension under review. See the [source-coverage ledger](simulation-source-coverage.md)
for exact versions and open coverage, and the [traceability matrix](simulation-traceability.md)
for methods, dispositions and verification. Von Hippel governs Lead User Research.
Behavioral Simulation owns execution and grade validation. Scaled Interview owns
run-bound ordinal measurement. This reference specifies when those methods help
the Lead User workflow and what can return to it.

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

| Research move | Smallest useful contribution | Empirical follow-through |
|---|---|---|
| A/B Discovery | Generate gaps in the search matrix, abandoned attempts and rival analogs | Search independently via target, advanced-analog and attribute-specific paths. |
| C Qualification | Branch on a suspected confound. Write an observable advancement indicator for LU1, a benefit signal for LU2 and a refuter for each. A permissioned proxy can help design a follow-up. | Compare actual timing and behavior to the relevant trend and comparator. Obtain a real trace or first-person evidence of unusually high benefit. |
| B/C/D Evidence-gap repair | Compare observations that would distinguish explanations. Prioritize the real test that could change the sufficiency decision. | Rerun B/C, then reassess D. Keep the unresolved dimension open if the required evidence is still missing. |
| E Interpretation | Hold frozen facts constant and generate mechanisms with different observable implications. | Check each against counterexamples and contrasts in the frozen record. Apply the change contract to new evidence. |
| E Propagation | Compare transmission, independent reinvention, incentives and selection under a varied network or constraint. | Seek dated receipts, independent origins and use-after-receipt. Keep reach, adoption, continued use and abandonment distinct. |
| F/G Counterfactual | Hold baseline and outcome fixed, vary one named intervention or use a declared factorial design. Include null, downside, non-use and substitution. | Use the existing gates. Test a named intervention, observable outcome and rival on actual people or systems. |

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
   when a contrast is useful. Distinguish whole-environment generation, a local
   WhatIf intervention on fixed history (including responder substitution), and
   Multiverse branches from a specific event. Declare turn limits, stopping
   rules, participant eligibility and context truncation; these are simulation
   design choices, not estimates of real conversational frequencies.
4. Branch from one fixed state and generate alternative plausible futures, including
   adverse outcomes and no effect. Record seeds/config where supported. Do not
   assign frequencies to alternative paths without a validated sampling model.
   For a second scope of Multiverse, hold the design fixed and regenerate an entire
   community using another composition of seed personas. Compare what changed
   with what persisted across compositions. Keep simulated norm guidance soft
   where users can violate it, and validate actual hard action constraints separately.
   In the original system each reply is conditioned on the ancestry of the
   selected branch, with an explicitly selected speaker and an option to end.
   When testing interventions, distinguish replacing the utterance (a changed
   input) from keeping it and drawing another continuation (sampling variation).
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
  to test. The paper (§4.1) uses 0.995 raised to elapsed sandbox hours since access,
  model-assigned importance on a 1–10 scale, cosine relevance, per-component
  min–max normalization and equal weights. The public Smallville code uses a
  different recency function over ascending last-access rank, default decay 0.99
  (older entries get higher raw recency), a default top-30 rank cutoff and
  explicit weights 0.5 recency, 3 relevance and 2 importance before per-agent
  multipliers. Declare which variant ran. Log retrieved records and scores,
  handle constant components as ties, and compare with simpler retrieval.
- Make reflections cite prior memory IDs; retain reflection as model inference.
  Plan at a coarse horizon, refine to executable actions, react to new observations,
  update shared environment and record the consequences. Keep a spatial or
  workflow-affordance graph distinct from the social graph. Store relevant
  relationships as cited inferences. If activities can collide, preserve the
  schedule, conflict resolution and state update order in the event log. No future information
  may leak into current state or private memory into another agent. The original
  example triggers reflection at accumulated importance 150, forms questions from
  recent memories, retrieves relevant records and derives insights with citations.
  Plans refine from day to hour to short actions; unexpected observations may
  trigger replanning. Preserve observation/action boundaries and validate actions
  against environmental constraints rather than accepting narrated outcomes.
- Branch identical initial states across changes in cost, access, network topology,
  rules or skills. Repeat runs and preserve no-diffusion, stalled and reversed
  trajectories. Remove memory, reflection, planning or edges in ablations where
  the question depends on these mechanisms. Distinguish fixed-history capability
  probes (self-knowledge, retrieval, planning, reaction, reflection) from full-run
  trajectory ablations: their estimands differ. Evaluate both where appropriate.
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
  repeated-item retest prediction from new-item generalization. Mask related item
  families (the source masks whole Big Five traits) and have a person check
  interview–outcome overlaps. Label any inferred answer trace as direct
  statement, supported inference or missing. Test the contribution of grounding
  with summaries and controlled removal of relevant versus arbitrary facts. For training or
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
| Ideological sorting (or a declared domain-specific analogue) | mean absolute correlation of responses with the specified organizing variable; group stereotyping is a separate audit |
| Inflated intervention effects | compare estimated signs and magnitudes to held-out human contrasts |
| Hyper-rationality | compare to actual incentivized choices and a stated theoretical baseline |

Use paired unit-level resampling when applicable; report interval, sample sizes,
missingness and nonapplicable tests. Compare to generic and person-grounded
baselines and report deterioration too. A predictive claim on one outcome family
does not authorize another. Preserve test-retest as a reference, not a perfect
ceiling or automatic normalized score. Test individuation (improvement over a
shared generic model) separately from demographic stereotyping and subgroup
representation. Where probabilistic predictions are available, compare Brier
skill against a predeclared empirical base-rate baseline and report calibration
and resolution separately. Check joint distributions and dependence after
marginal reweighting when appropriate; agreement on marginals alone is insufficient.
Exclude constant items consistently and report exclusions. Distinguish repeat
measurements from generalization to genuinely novel questions.

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
- Compare direct prompts, reasoning prompts, nearest-stimulus few-shot examples
  retrieved only from training data, and task-specific adaptation if eligible.
  Record the base model, checkpoint split, and inference prompt. In DPO the
  prompt stays fixed to the focal person. The comparison answer comes from a
  different person under the same stimulus and must actually differ.
  The paper compares supervised fine-tuning, supervised tuning augmented with
  answer-conditioned reasoning traces, and contrastive preference tuning (DPO).
  For the latter, construct contrast pairs within a common stimulus/condition and
  outcome, varying the participant and preferring their actual response. Keep
  answer-conditioned traces strictly in training: they are synthetic rationales,
  not observed reasoning or valid inputs at prediction time. Never train on
  inference labels. Select individual versus population objectives separately;
  improvement on one need not imply improvement on the other. Inspect extracted
  stimulus/outcome coding against sampled original studies; successfully executed
  parsing code does not establish semantic accuracy.
- Separate holdouts by question/outcome, condition, participant and entire study,
  according to the claimed generalization. Report which dimension is actually
  unseen. Validate with the same unit and scale as the intended decision.
- For ordered outcomes compare normalized Wasserstein distance; for unordered
  categories use TVD as a local extension. For SocSci210-style individual
  accuracy subtract mean normalized absolute error from one. Normalize by the
  scale width within each condition/outcome pair, then aggregate by study and
  across studies. The proceedings formula displays absolute-value bars.
  Verify the authors’ exact evaluator before claiming replication. Report exact
  match separately when useful. Declare the scale bounds and report zero-width
  cases. Compare groupwise error and human-only resampling/no-information baselines. Normalize ordered distances by
  response scale range where applicable. Aggregate within condition/outcome then
  across studies with an explicit weighting rule; preserve subgroup error gaps. Do not pool all groups until
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
  set, cosine similarity to the generated response, subtract the minimum and
  normalize to a PMF. Aggregate across preregistered anchor sets and repeated
  draws within the same unit; retain per-set sensitivity. Reject degenerate
  embeddings. Keep verbatim text as simulated text.
- For nonzero epsilon use the explicit `MAIER_V3_SINGLE_MINIMUM` transform in
  [Scaled Interview draft PR #25](https://github.com/mattlane66/scaled-interview-data-assistant/pull/25)
  or the [authors' library](https://github.com/pymc-labs/semantic-similarity-rating/blob/main/semantic_similarity_rating/compute.py).
  Convert epsilon for the authors' rescaled cosine. Released Scaled Interview
  and the compatibility entry point in Behavioral Simulation use uniform epsilon.
  Both agree at epsilon zero for nondegenerate scores. Record the transform and
  keep provider temperature distinct from PMF temperature.
- Compare PMFs with real human held-out response distributions (KS similarity for
  ordered categories, TVD), and across-concept mean correlations. If replicating
  correlation attainment, use repeated equal-sized human split-half cohorts,
  compare corresponding synthetic samples and divide mean cross-source
  correlation by mean human split-half correlation; undefined for zero denominator.
  This is a relative ranking statistic, not individual accuracy or purchase probability.
- Include naive/direct and alternate measurement baselines, stimulus format
  sensitivity and grounding ablations. For ordered KS similarity use one minus
  the largest absolute CDF difference; unlike unordered cosine similarity it
  respects rating order. Compare against a human-trained predictive baseline
  if labels and design permit. Do not choose anchors on test data.

## 7. Scarce labels: synthesis and statistical rectification

Source: Krsteski et al., [ACL 2026](https://aclanthology.org/2026.acl-long.498/),
[preprint v2](https://arxiv.org/html/2510.11408v2), sections 3–6, Appendix B.
The paper compares profile prompts, persona/history-based prompting, domain and
external distribution fine-tuning, and model-assisted correction. Multi-turn
elicitation can increase acquiescence; reserve real responses for correction
rather than spend them all on adaptation.

Compare demographics-only prompting, historical-response/persona grounding,
domain adaptation trained on permitted past responses, and external population
distribution adaptation where the external data are relevant and authorized.
These are alternatives. In panels hold out the target wave and control for
question overlap. Domain fine-tuning uses historical question/covariate/response
triplets. SubPOP aligns first-token multiple-choice probabilities to subgroup
distributions by KL divergence. It is a population objective; free-text outcomes
need a predefined coding rule applied symmetrically to human and generated text.
Keep label mapping and person dependence across waves explicit.

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
  Lambda=0 is human-only. Lambda=1 is full correction, the DSL-named special
  case in this survey paper. Broader design-based DSL requires its own design
  and variance procedure. Compare precision and real
  coverage against human-only and raw simulation; don't assume improvement.
  Pilot the budget allocation between training and correction with independent
  data; assess effective sample size gains only at adequate interval coverage.
  Global correction need not reduce errors in every subgroup. Relative bias
  is undefined if the reference mean is zero.
- For PPI++ power tuning or quantile/regression estimating equations, route to a
  validated statistical implementation and document the theorem/sampling design.
  The survey paper's appendix power-tuning description is inconsistent with main
  equation conventions; use main equation (1) for the mean. The original
  [PPI++ section 6](https://arxiv.org/html/2311.01453v2) confirms weighting the
  prediction contribution on both samples. See the measurement reference for
  the scalar optimal weight and conditions on tuning. No informal
  tuning on inference outcomes, naive binomial CIs on generated respondents,
  or claiming observed sample size increased.
- Report n human, N real covariate units, model draws separately; estimator,
  interval method, bias, variance, coverage, subgroup errors and actual effective
  sample size comparison if supported. Use the fixed-weight or disjoint-pilot mean implementation in
  [Behavioral Simulation draft PR #3](https://github.com/mattlane66/behavioral-simulation-for-agents-and-humans/pull/3).
  Its variance formula targets independent samples from a common distribution.
  Reproduction of a fixed finite panel or a weighted survey requires design-aware
  inference. Keep the model-assisted estimate outside the Lead User workspace.

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
  synthetic variance. Test one-question versus jointly elicited answers, first
  versus second person, inconsistent or invalid replies, outcome type, and
  retraining/version effects where these could alter the decision. Keep
  self-reported confidence, variation across draws and predictive uncertainty
  against human outcomes separate.
- Treat the foundation model as part of the measurement instrument. Record
  access/model/config/data lineage; compare independent baselines, evaluate
  robustness, group fairness, privacy, security, cost and suitability. Shared
  base-model outputs are dependent; never present independent draws as humans.
- For material predictive decisions, define decision-quality threshold in advance.
  Obtain independent real outcomes, compute observed error (e.g. TVD), train a
  separate error predictor on prior labeled questions, evaluate on unseen query
  families with groupwise/nested splits. Compare simple distribution features,
  question embeddings and, only if actually accessible, model representations
  or a tuned error-prediction model. Simile compares basic feature regression,
  generic embeddings, nested layer selection for ridge probes, continued
  fine-tuning with an error head, and the same training from the stock model.
  Use accessible baselines. Preserve real question-family and experimental-sample
  grouping. Match population, date, action space and stimulus in the actual
  benchmark, and disclose ground-truth sampling uncertainty. Report RMSE, Pearson
  correlation, and threshold AUROC separately. Agree with decision owners on
  consequences, tolerable error and the decision itself. Check calibration and
  coverage of accepted cases. Report calibration in the intended deployment
  distribution before using a confidence label.
- Recheck drift, freshness, counterfactual distance, subgroup error and changes in
  model/configuration. Decline predictive use if outside validated scope. Record
  whether each metric was computed or remains NOT_ASSESSED.

Read [Simulation measurement and evaluation](simulation-measurement-evaluation.md) for precise evaluation definitions, leakage controls, SSR conformance fixtures, rectification and the local execution checklist. Do not select metrics after inspecting their results.

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
