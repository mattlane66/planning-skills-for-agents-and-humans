# Simulation measurement and evaluation

Companion to [operating methods](simulation-methods.md). Local operational adaptation; not evidence that these methods improve Lead User Research. Read only the sections triggered by the decision. The Behavioral Simulation companion remains the owner of model execution; this reference specifies acceptance and interpretation. None of the following upgrades a synthetic record to empirical evidence.

## 1. Before running: define the unit and the test

Record population and sampling frame (if any), unit, question/construct, coding, conditions, outcome family, time horizon, comparator, estimand, split, acceptable error, and what decision changes. Separate person, episode, survey item, concept, study, social network and repeated draw. Never treat draws, paraphrases, simulated agents, or multiple reports of one event as new independent human units. Freeze the model and measurement rules before test labels are accessed. If parameters or prompts are selected using evaluation data, that data is development data, not a held-out test.

Use source disjointness and semantic deduplication, not merely different row IDs. For paired people, their approved grounding can be visible, but their outcome labels cannot. For prediction of new people, keep all their records out of training. For a new condition, withhold that condition; for a new study, withhold the entire study. Hold out future time for claims about drift. Cluster resampling and intervals at the sampling/assignment unit. For uncertainty over concept rankings, resample concepts as well as respondents when the design permits. Record missingness and outcome-specific exclusions.

Compare the smallest useful baseline: no simulation, generic response, empirical modal/base-rate, human-only estimator, straightforward prompt or simple supervised model where feasible. Report both absolute scores and relative gains; do not divide by zero. No universal acceptable score follows from these papers.

## 2. Breadth and social dynamics: measure the mechanism, not the story

Social Simulacra ([Park et al. 2022](https://arxiv.org/html/2208.04024v1), generation/intervention/evaluation sections): for a Lead User discovery benchmark, compare equal-budget search-only, search plus simple generic model, and search plus structured persona/condition branching. Hide condition identity from independent judges; score actionable search queries, novel source-backed episodes and refuters separately from perceived plausibility. Use small seed sets deliberately covering distinct situations, not a quota of generated personas. Include negative or non-use cases; a new narrative is valuable only if it yields a distinct test. Keep generated content private and never masquerade as real participants.

Generative Agents ([Park et al. 2023](https://arxiv.org/html/2304.03442v2), §§4–8, Appendices A/B): maintain the distinction between private observation log, retrieved context, reflection and action. Reflection may summarize other reflections but must retain a path to underlying records; a remembered event is not evidence it happened in the real world. Probe fixed-history recall, self-description, planning, reaction and synthesis using the same snapshots across ablations. Separately test whole trajectories under changed architecture with identical initial states and multiple seeds. A fixed-history ranking is not a causal estimate of what architecture does to long-run network behavior.

Local log-checkable outcomes:
- Information diffusion: fraction of eligible simulated nodes with a recorded receipt by time t; verify receipt against logged events rather than accepting narrated recall.
- Network change: define an edge before running; for mutual acquaintance in an undirected network, density = 2m/[v(v-1)] for v >= 2. Do not confuse directionality with mutual edges.
- Coordination: count eligible actors who perform the declared action at the specified time/location; distinguish invitation, stated intent, attempted action and completed action.
- Failure diagnostics: contradictory memories, unsupported relationship claims, invalid actions, norm/constraint violations, missing refusals, excessive agreement and plans that never execute. Retain both false positives and false negatives.

All are simulated system diagnostics until independently matched to a real system. Source evaluation ranks perceived believability under fixed histories and observes a short sandbox deployment, not a validation of market adoption. A lead-user study uses these outputs to search for real handoffs, dependency bottlenecks, diffusion conditions and failures.

## 3. Individual prediction versus population fidelity

Use the revised [Rich Self-Reports paper v4](https://arxiv.org/abs/2411.10109v4), main Table 1 and supplementary distortion/evaluation tables, and [SocSci210](https://arxiv.org/html/2509.05830v1), §3, §5, appendices. The measures below are local explicit diagnostics, not a claim to exactly reproduce every paper aggregation.

Let human outcomes Y and simulated predictions S be observed on the declared matched evaluation design. Aggregate repeated model draws at their intended unit before uncertainty analysis. For ordered items, retain ordering and scale; nominal category labels have no numerical order.

| Diagnostic | Local definition / procedure | Failure exposed |
|---|---|---|
| Individual agreement | proportion exactly matching on categorical paired items; absolute error on scalar outcomes; compare to the same person's retest where available | Wrong individual even with a correct aggregate |
| Standardized mean discrepancy | abs(mean(S)-mean(Y))/sd(Y); undefined if human SD=0 | Average response shifted |
| Spread ratio | sd(S)/sd(Y); use sample SD and report both; undefined at zero human SD | Compression or exaggeration |
| Ordered distribution distance | W1 = sum over adjacent ordered categories of abs(CDF_S-CDF_Y) times category spacing; divide by scale range only if normalization declared | Misplaced distribution mass |
| Nominal distribution distance | TVD = 0.5 * sum(abs(p_S-p_Y)) on the same categories | Wrong category proportions |
| Cross-item dependence | compare off-diagonal Spearman matrices and mean absolute correlation, excluding declared constant items | Excessively coherent or stereotyped profiles |
| Dimensionality | share of variance in first principal component on identically coded/scaled item matrices, same missingness policy | Collapse of multiple independent dimensions |
| Sorting | mean absolute association of answers with a preregistered organizing variable; compare with real associations | Overly predictable ideological/role alignment |
| Intervention effects | compare signs, standardized and raw magnitudes and intervals against actual randomized contrasts; ratios undefined near zero | Inflated/incorrect effects |
| Hyper-rationality | compare incentivized choices to observed behavior and specified maximizing reference; inspect direction toward that reference rather than declaring rationality from prose | Say/do and incentive mismatch |

For effect-size ratios, declare the aggregation and treatment/control SD convention (e.g. pooled SD for Cohen's d); retain near-null cases as such and report absolute gaps rather than unstable ratios. For hyper-rationality use a task-specific distance with sign toward the declared maximizing behavior; if no behavioral outcome/reference exists, mark NOT_ASSESSED.

Additional tests: compare individual prediction to generic no-profile baseline, compare demographic-only to consented richer grounding, report differences by adequately sampled groups, and check joint categorical TVD before/after matching marginals if supported. For probabilistic predictions use Brier loss mean(sum_k (p_k - onehot_k)^2) and skill = 1 - model_loss / baseline_loss, with baseline fixed without test outcomes. If the denominator is zero, mark undefined. Check reliability (observed frequency versus predicted probability in predeclared bins), sharpness and resolution separately. Do not assume individual accuracy proves representativeness, or that a sharper distribution is better calibrated.

The revised self-report study uses multiple grounding and supervised comparisons. For a local test, compare generic, demographics/minimal profile if authorized, self-description, structured questionnaire, interview, combined, and summary variants. Compare real retest, simple supervised response/embedding baseline, and independently adapted model if justified. Do not use answers from the same held-out items for grounding. Inspect new-item and same-item performance separately; assess incentivized behavior independently. Many source analyses are exploratory. Do not quote the study's aggregate improvement as expected accuracy for another domain.

For cross-study prediction preserve original question wording, stimulus, assignment, outcome options and respondent identifiers (deidentified). Check extracted study reconstruction against raw records. Use the same holdout for prompting, retrieval, supervised training and contrastive training comparisons. Reasoning traces conditioned on known labels are synthetic training augmentation only. Model preferences optimizing individual match and population alignment are different objectives. Keep distinct result tables rather than a combined accuracy score.

## 4. Ordinal elicitation and SSR equation conformance

[Maier et al. v3](https://arxiv.org/html/2510.08338v3), Appendix A.4 and C/D; [authors' compute.py](https://github.com/pymc-labs/semantic-similarity-rating/blob/main/semantic_similarity_rating/compute.py). This measures stated intent, not action. Use actual response text, frozen embedding model and anchor version, five ordered anchor statements per set for the paper's five-point design. For novel constructs, establish anchor meaning with humans; keep calibration concepts separate from held-out concepts. The paper's chosen anchors were developed in its study setting; do not transfer the reported performance as out-of-domain validation.

DLR requests the number directly. FLR elicits free text, then maps it to a number in a separate call. SSR elicits free text, embeds it with the anchors, transforms similarities to an ordinal PMF, and averages PMFs across anchor sets within response. Preserve anchor sensitivity and raw text; aggregate at declared unit. If reporting correlations across concepts, use matched-size human split-half and synthetic cohorts over the same concepts; correlation attainment is a ratio to human-human correlation, not an individual success percentage. Also report ordered KS similarity = 1 - max(abs(CDF_S-CDF_Y)), distribution distance and human sampling variability.

Paper Eq. 8/9: for similarities c_i, choose a single minimum index j (fix a tie rule), let w_i = c_i - c_j + epsilon * I(i=j), normalize, and for T > 0 normalize the powers p_i^(1/T). For zero total mass, zero embedding or nonfinite input, report NOT_ASSESSED rather than invent a uniform PMF. An explicit positive epsilon may resolve a tied degenerate vector mechanically, but that is not useful measurement without anchor separation. T=0 is an implementation limit requiring an explicit tie policy, not the paper's evaluated setting.

Conformance fixtures (hand-computable, not empirical):
- Raw cosine [0.1, 0.2, 0.3, 0.4, 0.5], epsilon=0, T=1 gives [0,0.1,0.2,0.3,0.4].
- Same inputs, epsilon=0.1, T=1: weights [0.1,0.1,0.2,0.3,0.4], sum 1.1. Existing Scaled Interview uniform-epsilon variant yields [0.1,0.2,0.3,0.4,0.5]/1.5, not Eq. 8.
- Authors' implementation uses gamma=(1+cos)/2, so the equivalent epsilon for that second example is 0.05. At epsilon=0, scale cancels.
- All similarities identical, epsilon=0: undefined. Do not silently score.
- With epsilon=0, T=0.5, powers of [0,0.1,0.2,0.3,0.4] give [0,1,4,9,16]/30.

Until companion code supports a tested explicit paper-conformant transform, use epsilon=0 and T=1 or declare an implementation variant. Do not overwrite another repo's legacy results. A conformance pass does not establish human predictive validity.

## 5. Statistical rectification

[Krsteski et al. preprint v2](https://arxiv.org/html/2510.11408v2), Eq. 1–3, Appendix B; [PPI++](https://arxiv.org/html/2311.01453v2), §6, Proposition 2. This is inference for a *declared population estimand*, not correction of a generated interview or qualification of a lead user.

Given independent real labeled sample H of n units with observed y and predictions f(x), and a disjoint real unlabeled covariate sample U of N units from the same population, with a predictor fixed independently of inference:
- Corrected mean theta(lambda) = mean(y_H) + lambda * (mean(f_U) - mean(f_H)).
- Estimated variance V(lambda) = var(y_H - lambda*f_H)/n + lambda^2*var(f_U)/N. Use sample variances, n,N >= 2; retain paired residuals. For fixed lambda the mean is unbiased under these assumptions. Wald intervals are asymptotic, not guaranteed at tiny n.
- Derived scalar variance-minimizing weight = Cov(Y,f) / [(1+n/N) Var(f)] under the stated common-distribution design. If using a separate tuning set, estimate covariance and variance there, using the *inference* n/N; freeze weight before inference. A local bounded variant clamps to [0,1], uses lambda=0 for undefined/zero variance or inadequate tuning, and compares precision with human-only. PPI++ itself supplies adaptive asymptotic inference under its conditions; do not generalize a naive same-data tuning interval.
- Compare human-only (lambda=0), model-only (uncorrected, no inferential claim), full correction (lambda=1), and tuned correction on an independent evaluation design. Preserve negatives: full correction can increase variance. Estimate equivalent human-only n_eff = human variance / V(lambda) only for comparable estimand/design and defensible interval coverage. Ratio or gain is not a count of additional humans.
- For binary outcome define indicator before fitting. For quantiles, regression or other parameters, use a validated PPI++/design-based method for the appropriate estimating equation and sandwich covariance; do not plug means into nonlinear parameters. For clustered, weighted, panel or nonprobability samples, use matching design-aware inference or do not make population claims.

Toy fixture: y_H=[1,3], f_H=[2,4], f_U=[4,6], lambda=0.5. Human mean=2, prediction difference=2, corrected mean=3, residuals=[0,1], V=0.5/2+0.25*2/2=0.5; human-only V=2/2=1. These numbers verify arithmetic, not coverage. Existing companion fixed-weight implementation is a subset of this method; adaptive tuning is not implemented by this local reference. Preserve human budget for correction and final validation; test allocation rather than choosing an optimum from the paper's dataset. Never count the same unit in multiple independent sample roles.

## 6. Reliability of the decision

[Bisbee et al.](https://doi.org/10.1017/pan.2024.5): test conditional relationships as well as means. Compare matched regression specifications, coefficient sign and magnitude, distribution and spread. Re-run approved prompt paraphrases, answer order, model configurations and dates. Distinguish reproducibility of individual draws from stability of the distribution and of the proposed decision. Do not power human fieldwork using compressed synthetic variance.

[Foundation Models report](https://arxiv.org/abs/2108.07258v3): treat model adaptation, prompts and data lineage as part of the instrument. Evaluate task validity, subgroup performance, robustness to distribution shift, resources and potential harms separately. Do not mistake model consensus for independent corroboration. Report the cost and actual sources used; protect sensitive inputs and forbid synthetic records passing as people.

[Simile public confidence method](https://www.simile.com/blog/confidence): estimate *error* on actual question-level holdouts, not linguistic confidence. Keep training, calibration and final test question families disjoint. Choose an acceptable error threshold from the decision cost before final testing. Compare predicted error to actual error using RMSE and rank association, classification discrimination if using a threshold, and calibration/coverage-risk curves: among accepted questions, what fraction failed the threshold? Report rejected and out-of-scope questions; no probability claim without held-out calibration. The published product threshold is not a Lead User Research standard. Re-evaluate after model, prompt, population or domain shifts.

## 7. Return gate and worked research move

Use the worksheet. Report each metric as computed, undefined, NOT_ASSESSED or NOT_APPLICABLE with reason. A material predictive claim lacking its required validation remains a hypothesis. Distinguish a tested method implementation, a successful simulation run and a scientifically validated prediction.

Example (fictional): a developer tool team has real reports of conflicting code changes from experienced multi-agent users, but no evidence about one particular coordination condition. Use an L0 condition matrix varying repository ownership and shared-state visibility. Generate rival mechanisms, including ordinary tooling failures and cases where agents are not the cause. Turn each into a specific search or observation, including analogous workflow handoffs outside AI. Independently locate real traces; qualify people only through the governing LU1/LU2 gates. If real traces are unavailable, leave that gap open. A population claim about willingness to switch would require separate representative research, grounded simulation and relevant held-out tests; SSR and rectification cannot turn these purposive cases into a population estimate.

No empirical comparison between this extension and conventional Lead User Research has been run. The [assurance cases](assurance-evals.md) and benchmark in the operating methods are the required next verification boundary, not results.
