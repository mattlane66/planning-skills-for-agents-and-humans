# Prospective evaluation of the revised method

Status: protocol proposed. Fixture assurance is available now. Prospective human
outcomes have yet to be collected. Start from the [benchmark manifest](empirical-benchmark.json).

| Arm | Method |
|---|---|
| A | Conventional human-led Lead User Method with comparable resources and access |
| B | Baseline AI-assisted skill at the pinned pre-revision commit |
| C | Revised evidence-first method with no synthetic respondent generation |
| D | C plus optional Behavioral Simulation, restricted to a predeclared eligible subset |

Preregister decisions, tasks, domains, participants, labels, graders, budget,
exclusions, thresholds, primary measures and analysis before seeing outcomes.
Use paired tasks, randomize or counterbalance order, hold access and budget constant
where possible, and document discrepancies and time/cost tradeoffs. Separate
exploration from confirmation, freeze source cutoff and arm instructions, and
prevent leakage between arms, reviewers and model inputs. For historical cases
hold out the solution, use obscure or recent tasks and track training leakage.
Include prospective real research. Retrospective retrieval alone cannot show
whether a method helps make successful innovations.

Use independent domain reviewers who see the same source access and adjudicate
qualification, supported needs and alternative explanations blind to arm
where practical. Retain disagreements and methods for adjudication. Bounded recall
uses only adjudicated episodes in a named accessible corpus. Report additional
valid discoveries separately. Unobservable recall stays unknown.

## Scoring rubric

| Measure | Unit and scoring rule |
|---|---|
| Episode precision and bounded recall | One unit per adjudicated user–trend–need–benefit episode with independent provenance. Precision = valid retrieved / retrieved claims. Bounded recall = valid retrieved in adjudicated set / eligible adjudicated episodes. Undefined denominators stay UNKNOWN. |
| Overlooked supported needs | Count distinct decision-relevant needs with accessible support and adjudicated novelty to the team. Merge paraphrases and preserve constraint differences. |
| Attribution and entailment | Score atom, source and context independently. Count correctly attributed and entailed pivotal claims over those asserted. Mark unavailable source UNKNOWN and report its rate. |
| Mechanism alternatives | Count distinct viable operating mechanisms under the same accepted criteria. Report separate blind novelty and applicability ratings, duplicates and boundary violations. |
| Test discrimination and decision value | Blind graders score 0 (no divergent observation), 1 (observable contrast with unresolved feasibility or decision consequence), 2 (feasible contrast separates live rivals and changes decision under predeclared outcomes). Compare with subsequent measured decision effect and cost. |
| Time and cost | Record human time, compute, cash, delay and source access per task and arm. Report unsuccessful or abstaining runs. |

Predeclare which outcomes are primary. Secondary measures are search coverage,
contradictions and negative cases, false qualification, transfer errors,
contamination, researcher burden and actual follow-up human behavior. Analyze
within-task differences, uncertainty, distributions and heterogeneity by domain
and researcher. For C vs D, preregister eligibility before generation. Assess test
selection against observed outcomes. If D includes predictions, separately assess
held-out direction/effect, baseline error and, where relevant, individual,
distributional and calibration performance. Track model, prompt/config,
grounding, cost, grade, subgroup and freshness. Human or model preference cannot
establish commercialization.

Before outcomes, set rollback rules for reduced discovery diversity, increased
false qualification or costs without useful learning. Publish uncertainty,
exclusions, failures, disagreement and positive/negative results. Treat the
revised method as experimental until prospective evidence supports stronger claims.
