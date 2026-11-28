# Simulation benchmark and replay results

Discovery runs began on 2026-11-27 and blinded adjudication finished on 2026-11-28. This is a one-domain retrospective pilot against public historical documents. The source documents describe actual events. The three searchers and two blinded reviewers were separate model sessions.

## Historical discovery pilot

The question was which actors and equipment adaptations were ahead of the emerging need for durable, controllable off-road bicycles in Northern California during 1973–82. Each arm started with the same nine-record catalog and one planning pass. The limit was four source opens, 4,700 indexed words, four nominated episodes and two refutations. Source opens were logged. Reasoning time and compute were not matched. The protocol and corpus manifest were fixed before the runs. Reviewers saw pseudonymized claims, a list of what each arm opened, and the corpus. Claims passed only when both reviewers found documentary support for both LU criteria. A refutation had to contradict a specific claim.

| Arm | Source IDs opened | Words | Nominated | Accepted | Accepted per source | Refutations accepted | Reviewer disagreements |
|---|---|---:|---:|---:|---:|---:|---:|
| Conventional discovery | D01, D04, D03, D02 | 4,253 | 3 | 2 | 0.50 | 2 | 0 |
| Generic AI brainstorming | D01, D04, D03, D02 | 4,253 | 3 | 2 | 0.50 | 2 | 0 |
| Structured plausibility scenarios | D01, D02, D04, D05 | 4,045 | 2 | 1 | 0.25 | 2 | 0 |

All three arms qualified Joe Breeze’s purpose-built frame. The two comparison arms also qualified the collective Repack rider-builders’ earlier reinforcement adaptations. All three proposed Tom Ritchey, but the sources they opened did not connect his frame-building investment to unusually strong own-use benefit. The structured arm alone opened the Lawwill biography and used it to rule out attributing his later rear-suspension application to the early Pro Cruiser. Each arm refuted the claim that a standard cruiser brake was adequate for repeated steep descents. Both reviewers agreed on all 14 dispositions. The structured arm surfaced a useful different refutation and yielded fewer qualified episodes in this run.

This small, curator-selected corpus is influenced by source overlap and model memory of a well-known case. It supplies no independent inventory of all historically eligible episodes and no estimate of discovery uplift, population validity or causal effect. Evaluating effectiveness requires multiple domains, repeated runs, prospective source and outcome holdouts, and independent human adjudication. This pilot carries no instance-specific behavioral predictions.

### Corpus inventory

Hashes identify the exact normalized text inspected on 2026-11-27. The extraction selected the main article, removed navigation and non-content nodes, normalized whitespace, deduplicated text blocks and kept headings, paragraphs, captions and list items. One candidate returned no usable article and was excluded before opening the arms. Corpus article bodies are not redistributed.

| ID | Document | Words | Text SHA-256 |
|---|---|---:|---|
| D01 | [Repack downhill history](https://mmbhof.org/mtn-bike-hall-of-fame/history/repack-history/) | 1128 | `0b4228e80998e617bfca0516c3efbf679f1f0345b0482442815b0ff0e09eeee1` |
| D02 | [A public history of early rugged bicycles](https://www.smithsonianmag.com/innovation/before-mountain-biking-became-popular-recreational-sports-adventurous-souls-american-west-invent-rugged-bike-180989645/) | 890 | `60cfd7a1465785e423992dcaf0d4082425942b5933d6b741562d40a53efe875d` |
| D03 | [A museum collection record](https://americanhistory.si.edu/collections/object/nmah_1419571) | 566 | `85a08c237592aba2e5ad392c29aec087a3449da8a7f00366796571362b2f189f` |
| D04 | [An earlier Northern California rider](https://mmbhof.org/mtn-bike-hall-of-fame/history/john-finley-scott/) | 1669 | `2052b181c1fab3bf8c62bd7adeba23c970ed47cd891c6312f0012aa3fed856a8` |
| D05 | [A Northern California racing biography](https://mmbhof.org/mountain-bike-hall-of-fame/mert-lawwill/) | 358 | `acc374128905cc5ea922ec449abd2c749c29c917fa875b26af3dfcbee42aa335` |
| D06 | [A Marin race organizer biography](https://mmbhof.org/mountain-bike-hall-of-fame/1988/charlie-kelly/) | 267 | `63bf514566f12975349c8e2de9544b88fe98878748344f20649d7c0ae3ee67ab` |
| D07 | [A museum exhibition artifact gallery](https://www.sfomuseum.org/exhibitions/repack-rwanda-origins-evolution-and-global-reach-mountain-bike/gallery) | 2402 | `721dab2a36e32c9d7db5b14ae7eb9c47d367c039be4171030718e26a72fba3e7` |
| D08 | [An archival photograph series](https://mmbhof.org/mtn-bike-hall-of-fame/history/cragg_galleries/repack-photos-preparation-in-fairfax/) | 72 | `621753fd0723e75bd4250c9a2bd1256c0a38f71c40e56cc7f2381d1f96bbe1e0` |
| D10 | [A museum exhibition overview](https://www.sfomuseum.org/exhibitions/repack-rwanda-origins-evolution-and-global-reach-mountain-bike) | 704 | `88987be3ed2f9b43ee256eeab0510e5d4ce2ae22038ee7051efdedf02d7fe720` |

## Archived survey arithmetic replay

A separate descriptive check uses the public ATP1 human answers and Qwen fine-tuned outputs from the pinned [survey-simulations release](https://github.com/skrsteski/survey-simulations/tree/d0926093b57b373760679c4b6d7ef01d4447c387/datasets/atp1). All 690 identifiers joined one-to-one. The 630 response pairs scorable under the released A–E to 4–0 coding are the fixed evaluation frame. Its archived human mean was 1.9968. These are finite-frame repeated splits of known records. No confidence interval, sampling-design attestation or new model prediction was produced.

Use the checked-in `evals/replay-survey-point-estimates.py` with the released `data/human_test.csv` and `outputs/simulated_data/qwen/ft.csv`. The script repeats 500 splits with seed 2192. A total of 200 labels is available in each split. The tuned variant spends half on a disjoint pilot and half on correction. Human-only and full correction use all 200 labels. Raw predictions use the 430 unlabelled rows. RMSE and MAE are in the 0–4 response scale.

| Method | Mean signed error | MAE | RMSE |
|---|---:|---:|---:|
| Human-only, 200 labels | 0.0018 | 0.0671 | 0.0835 |
| Raw archived prediction | 0.4225 | 0.4225 | 0.4231 |
| Full correction, 200 labels | -0.0025 | 0.0768 | 0.0965 |
| Separate pilot, 100 + 100 labels | 0.0033 | 0.1011 | 0.1259 |

Mean pilot weight was 0.2996. Both corrections reduced mean bias relative to raw predictions. Human-only had the smallest error at the same total label budget in this archived case. Results depend on the chosen sample, model, target and label budget. They supply neither a calibrated prediction nor evidence that correction improves precision in a live Lead User study.

## Packaged workflow assurance

The first blind replay independently constructed the study, passed the packaged validator, and reached Phase H. The initial scorer accepted 14 of 16 checks. It missed a valid SHA-256 suffix on the source locator. The runtime missed a bounded referral path as a PY row. The scorer now verifies the checksum in both observed locator formats. Re-scoring the unchanged first artifacts passed 15 of 16. The missing referral record remains a first-run failure.

The first replay exposed two workflow instructions that conflicted with the verification contract. Blind runs on this fictional corpus must declare the synthetic fixture type and build their own study. Bookkeeping in the fingerprinted hypotheses and change log must be recorded through the existing post-freeze change command with an accurate reason. The renderer now links the decisive findings and qualification criteria to their evidence rows and includes recorded discovery-branch independence.

A fresh Codex Work session used the corrected packaged instructions and renderer on 2026-11-28. It independently built a Phase H study with four sources, 13 synthetic evidence rows, one qualified fictional episode, a document-backed terminated referral path and a bounded `TEST` decision. The packaged validator passed. The final scorer passed all 16 checks on the unchanged second artifacts after recognizing its hash fragment spelling. The suite checks that a wrong digest fails. This demonstrates workflow execution on the fictional corpus in Codex Work. The human-review field was `NOT_REVIEWED`. Runtime and adapter packaging checks have separate coverage.

## Candidate for prospective validation

The JupyterLab and Jupyter Collaboration public trackers provide an active stream of dated notebook continuity reports. The starting question is which operators have already invested in restoring a usable notebook after a disconnect, a server restart or an out-of-band edit, and under what conditions the workaround is worth the cost. The starting records below were open as of 2026-11-28. The hash covers the issue body returned by GitHub, encoded as UTF-8 with line endings normalized to LF. These records are seeds. The initial review has yet to establish an eligible lead-user episode or independent deployment lineage for each.

| Record | Last update in snapshot (UTC) | Role in the candidate corpus | Body SHA-256 |
|---|---|---|---|
| [Jupyter Collaboration #594](https://github.com/jupyterlab/jupyter-collaboration/issues/594) | 2026-08-12 | Controlled reproduction after restart with persistence removed. Check whether the report connects to a distinct own-use episode. | `42a0ef1e569c60f637c8a78223fac64a48845304aaf13762a48f195b5653d6ea` |
| [Jupyter Collaboration #621](https://github.com/jupyterlab/jupyter-collaboration/issues/621) | 2026-10-20 | First-person report from a long-running deployment with unreliable connections. Keep the related #594 mechanism in the lineage review. | `cae466c2c51fcc95413a41d6bb694254fa4fa91f307f605a5f1f05e877e28b91` |
| [Jupyter Collaboration #627](https://github.com/jupyterlab/jupyter-collaboration/issues/627) | 2026-09-22 | Deployment report with missing outputs and a first-person workaround. Check the cost and whether the workaround persists. | `4837f465d0640ad29c78bdd9a3b8dda84a7e0c89eb29084be42f67be5fb0825f` |
| [JupyterLab #18699](https://github.com/jupyterlab/jupyterlab/issues/18699) | 2026-10-12 | Adjacent file-change problem with a manual reload workaround. Use it to test the boundary between reconnect and other causes of stale notebook state. | `735a5288d483f532da1dfd8a201abf923b2052c907434c9a04f362833aece864` |

Before the search arms run, freeze the issue bodies, pre-cutoff comments and allowed linked records, with timestamps, a sampling rule, eligibility criteria and source/time limits. Give all arms the same index and restrict searches to those immutable snapshots. Use conventional discovery, generic model brainstorming and structured simulation under the same documented budget. Hash nominations, predictions and refutations before examining post-lock events. Independent reviewers should score arm-blind packets for ahead-of-trend behavior, unusually strong own-use benefit, provenance, counterexamples and duplicate episodes. For follow-up, use a proposed 60-day observation window from the prediction lock. Record separately whether a different deployment reports corroboration, whether there is documented sustained workaround use, and whether a linked fix ships with a relevant reproduction or regression test. A label, vote or issue closure alone supports none of those outcomes. Record insufficient visibility as unknown and report it alongside the eligible denominators. Report discovery yield and outcome follow-up separately. The public tracker offers dated artifacts and no general population sampling frame or permission for private telemetry.

Potential external reviewers are [Adam Rule](https://adamrule.com/), who led a published study of collaborative notebook reuse with lab and field evaluation, and [Lorena Barba](https://ospo.gwu.edu/lorena-barba), who works on computational reproducibility and has documented Jupyter expertise. Confirm availability and any involvement in the sampled issues before assigning review. The prospective comparison has no locked predictions, outcome observations or human ratings yet.

Goeldner, Kruse and Herstatt's [Indonesia flood-resilience study](https://www.econstor.eu/bitstream/10419/172256/1/1007199059.pdf) is a public precedent for independent human review. Five experts rated 85 concept descriptions without knowing the collection method. The appendices include selected concepts and the two fieldwork arms used different resources. The complete concept packets and individual ratings were unavailable in the public paper, so this study supplies a design precedent for review, not a replay dataset for testing simulation.
