# Lead User Research revision ledger

## Baseline

| Item | Observed baseline |
|---|---|
| Planning main | Commit `8f6f2884ac40a7513946123549d3cf90f4fc67b0`, tree `20d4dad3bba6aac108492e0e0d124c5216c7ea2b`. The brief mislabeled the commit as the tree. |
| Implementation base | `5cb4ba9bda112d0157592f8b8b5cd90d5944bba2` ([PR #189](https://github.com/mattlane66/planning-skills-for-agents-and-humans/pull/189)), three commits ahead of main. It already implements preliminary empirical enhancements and open need–solution discovery. The revision is stacked to preserve that work and keep review scope legible. |
| Checkout | Isolated byte-verified connector snapshot, initially clean. Direct GitHub git transport unavailable. The generated standalone portal (`site/index.html`, unrelated) exceeds connector download limits. Remote commits use the original server tree as base. |
| Runtime versions | Python 3.12.14, Git 2.56.1, Node 24.22.3. |
| Study and packaging | Protocol/state 1.7, assurance reports schema 1, A–H and SCOUT/STANDARD/FULL, portable state packet fallback. Canonical `lead-user-research/` mirrors `skills/lead-user-research/`; existing release tools build runtime packages from those files. The documentation portal also embeds the canonical skill and its references. |
| Presentation | Standalone HTML `lead-user-research-interactive-v10.html`, 1,545,476 bytes, SHA-256 `92800c538cb87a75aedad1829b46384537163d269180a36473501581f06f5c5b`. Its inline data, styles and script are editable in-place. Its prior links follow PR #189. The reviewed update preserves the same file, replaces relevant notes inside A–H, and targets the revision branch. Browser coverage at 1440×900 and 390×844. No site deployment. |
| External contracts | Behavioral Simulation commit `c11d29c8d121728306037dd799669bb0ef7cfabf`, upstream schemas 0.1.0. SIDA reference commit `38b85c697526123491ab01363b1a3f03313e15e2`. Both read-only. |

Existing registries cover search and lineage, contrastive hypotheses, observability, verification dimensions, transfer assessment, the six-check Phase F gate, frozen criteria, and action records. Extend those records. Keep optional comparison/return data outside the evidence freeze. The research purpose, participant access and product approval remain human decisions.

## Implementation progress

| Slice | Change and verification |
|---|---|
| S0 | Baseline lead-user regression 80 passed. Structural reference validation passed. Controller returned COMPLETE (H). Fixture assurance passed 1/1 cases and 15/15 checks. Source-by-source limits are in the methodology ledger. |
| S1 | Rare search and bounded structural analog records. 82 lead-user tests passed, including under-ranked source and unsupported analog checks. |
| S2 | Consequential contrast and pivotal audit, including qualification, freeze repair, decisive review and host validation. 84 lead-user tests passed. |
| S3 | Conditional M, target contrasts and distinct branches with a fixed frame and PASS requirements. Host digest covers the validator imports. 87 lead-user tests passed. |
| S4 | Optional evidence-first CF sidecar with study identity, stable fingerprints, shared comparison basis and stale status. 89 lead-user tests passed. |
| S5 | Pinned offline simulation handoff and isolated, grade-aware return quarantine. 91 lead-user tests passed. |
| S6 | Bounded learning, neutral fieldwork, discriminating A## actions and prospective benchmark manifest/rubric. 94 lead-user tests passed. |
| S7 | Decision-first report plus conditional comparison/simulation, portable and runtime entry points, release mirrors, and the revised presentation. 97 lead-user tests passed before audit corrections. |
| Final review | Independent audit reproduced and retested claim, freeze, privacy, provenance, and report bypasses. 104 lead-user tests passed after fixes. The final optional fixture compares two mechanisms and status quo. |

## Requirements and verification

| ID | Requirement | Test target | Status |
|---|---|---|---|
| R01 | Rare-signal discovery | `test_bounded_sample_finds_rare_original_among_popular_derivatives`, rare search registry and existing lineage regressions | PASS in a bounded ranked-list fixture |
| R02 | Structural analog | `test_observed_analog_requires_evidence_and_limits` and unresolved transfer guard | PASS |
| R03 | Falsifiable rival or null | `test_nested_rival_requires_distinct_predictions_and_refuter`, existing contrast and negative-interpretation fixtures | PASS |
| R04 | Pivotal claim audit | `test_unresolved_pivotal_claim_blocks_qualification_and_freeze_and_routes_repair`, `test_excluded_trend_claim_cannot_support_qualification_or_sufficiency` | PASS for recorded audit states |
| R05 | Conditional mechanisms | `test_mechanism_remains_proposed_with_conflicting_cases` and separate candidate generation records | PASS |
| R06 | Transfer assumption guard | `test_unresolved_transfer_and_synthetic_refs_cannot_support_existing_gate`, invalid transfer flag return quarantine | PASS |
| R07 | Distinct shape mechanisms | `test_candidates_deduplicate_and_hold_frame_criteria_fixed`, existing acceptance/selection/rotation regressions | PASS |
| R08 | Evidence-first counterfactual | `test_evidence_first_comparison_validates_offline_and_flags_mismatch`, foreign/tampered state, E-only, two mechanisms plus baseline | PASS |
| R09 | Simulation boundary | `test_handoff_is_minimized_review_bound_and_offline`, invalid freeze/gate and short-text privacy checks | PASS for exact binding and receipt structure |
| R10 | Grade-aware return | `test_simulated_return_stays_isolated_and_wrong_binding_or_grade_is_quarantined`, separate review receipts and optional assurance | PASS for tested packet/return states |
| R11 | Empirical next action | `test_test_design_is_falsifiable_and_preserves_ambiguity`, participant attribution, prospective manifest and existing observability tests | PASS for artifact acceptance |
| R12 | Distribution and compatibility | Original v1.7 validation and Phase H, fresh install, canonical byte parity, unchanged old fingerprint, optional report tampering, distinct short-source redaction, browser walkthrough | PASS |

## Running the checkpoints

Run `python -m unittest discover -s tests -p 'test_lead_user*.py'` after each slice after synchronizing the mirror. Full run commands and results are recorded at the final checkpoint. Deterministic validation checks artifact structure and invariants. The human reviewer checks whether evidence entails the claims. Prospective evaluation uses observed outcomes.


## Final verification

| Command or check | Result |
|---|---|
| `python -m unittest discover -s tests -p 'test_lead_user*.py'` | 104 passed |
| `python -m unittest discover -s tests -p 'test_*.py'` | 278 passed |
| Legacy validator and controller example | Structural validation passed; Phase H COMPLETE |
| `scripts/run-lead-user-assurance-evals.py --adapter fixture` | Ordinary case passed 15 checks. Optional cases file passed 2 cases with 16 checks each. |
| `scripts/build_claude_skills.py` and `scripts/check-release-install.py` after release build | 15 validated upload ZIPs and fresh install checks passed |
| Local links, frontmatter, actionlint, mirror comparison, `git diff --check` | Passed |
| Portal `npm run check`, Shaping Board test and Chromium smoke | Passed. Integrity check traversed 168 routes, including the added references. |
| Standalone presentation | Chromium at 1440×900 and 390×844. Eight phases, expanded protocol notes, optional simulation disclosure, completed Decision Brief download, no page errors. |
| `bash scripts/check-repo-health.sh` | Two failures in dependency audits for the existing portal and MCP server lockfiles. Their functional checks passed. The same failures appeared at baseline. This revision leaves those lockfiles intact. |

Fixture assurance exercises artifacts and constraints. Blind command-adapter
runs and prospective human evaluation are NOT_RUN. A human still determines
source entailment, consent, comparator validity and calibration scope. Documented
redaction catches known identifiers and source spans. Review indirect identifiers
and newly entered free text before sharing.

## Migration and rollback

Existing protocol 1.7 study files, freeze fingerprints and no-simulation routes
continue to work. New study IDs namespace optional scenario artifacts. To add
them to an old study, add only the manifest study ID and optional files, keep
the original frozen records, and rerender the Decision Brief. When content or
permission changes, create a new scenario/receipt and retain the prior history.
The source ledger lists publications with abstract-only or blocked access.

To roll back, revert the revision commits without rewriting research workspaces.
Keep optional sidecars and receipts as read-only research history. The old
renderer ignores these files. Rerender its view if returning to the previous
workflow. Retain the earlier version of the standalone walkthrough.

## Review material

- [Independent audit and retest](lead-user-research-independent-audit.md)
- [Methodology evidence ledger](../../lead-user-research/references/methodology-evidence.md)
- [Prospective benchmark and rubric](../../lead-user-research/references/empirical-evaluation.md)
- Updated fictional presentation: `lead-user-research-interactive-v10.html`
