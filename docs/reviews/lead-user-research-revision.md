# Lead User Research revision ledger

## Baseline

| Item | Observed baseline |
|---|---|
| Planning main | Commit `8f6f2884ac40a7513946123549d3cf90f4fc67b0`, tree `20d4dad3bba6aac108492e0e0d124c5216c7ea2b`. The brief mislabeled the commit as the tree. |
| Implementation base | `5cb4ba9bda112d0157592f8b8b5cd90d5944bba2` ([PR #189](https://github.com/mattlane66/planning-skills-for-agents-and-humans/pull/189)), three commits ahead of main. It already implements preliminary empirical enhancements and open need–solution discovery. The revision is stacked to preserve that work and keep review scope legible. |
| Checkout | Isolated byte-verified connector snapshot, initially clean. Direct GitHub git transport unavailable. The generated standalone portal (`site/index.html`, unrelated) exceeds connector download limits. Remote commits use the original server tree as base. |
| Runtime versions | Python 3.12.14, Git 2.56.1, Node 24.22.3. |
| Study and packaging | Protocol/state 1.7, assurance reports schema 1, A–H and SCOUT/STANDARD/FULL, portable state packet fallback. Canonical `lead-user-research/` mirrors `skills/lead-user-research/`; existing release tools build runtime packages from those files. |
| Presentation | Standalone HTML `lead-user-research-interactive-v10.html`, 1,545,476 bytes, SHA-256 `92800c538cb87a75aedad1829b46384537163d269180a36473501581f06f5c5b`. Its inline data, styles and script are editable in-place. Its links and content follow PR #189. No site deployment. |
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

| S5 | Pinned offline simulation handoff and isolated, grade-aware return quarantine. |

## Requirements and verification

| ID | Requirement | Test target | Status |
|---|---|---|---|
| R01 | Rare-signal discovery | Under-ranked case, distractors, access limits and derivative lineage | Pending |
| R02 | Structural analog | Observed vs speculative, correspondence and disanalogy | Pending |
| R03 | Falsifiable rival or null | Observable implications, justified N/A and negative outcome | Pending |
| R04 | Pivotal claim audit | Trace/attribution, entailment, access, contradictions and bounded repair | Pending |
| R05 | Conditional mechanisms | Evidence-linked contrast and independent candidate effect | Pending |
| R06 | Transfer assumption guard | Load-bearing uncertainty closes concept gate, including with favorable simulated return | Pending |
| R07 | Distinct shape mechanisms | Shared accepted basis, functional deduplication, human selection | Pending |
| R08 | Evidence-first counterfactual | Same basis, differences, stale/foreign inputs, offline | Pending |
| R09 | Simulation boundary | Explicit permission, minimized packet, upstream version, offline status | Pending |
| R10 | Grade-aware return | Wrong hash, forged calibration, model-only hypotheses | Pending |
| R11 | Empirical next action | Rivals, outcomes and effort, neutral human observation | Pending |
| R12 | Distribution and compatibility | Prior freeze/report digests, no-tool path, mirror, rendered privacy | Pending |

## Running the checkpoints

Run `python -m unittest discover -s tests -p 'test_lead_user*.py'` after each slice after synchronizing the mirror. Full run commands and results are recorded at the final checkpoint. Deterministic validation checks artifact structure and invariants. The human reviewer checks whether evidence entails the claims. Prospective evaluation uses observed outcomes.
