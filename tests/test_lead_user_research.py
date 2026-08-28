import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAD = ROOT / "lead-user-research"


class LeadUserResearchTests(unittest.TestCase):
    def init_workspace(self, tmp, mode="standard"):
        workspace = pathlib.Path(tmp) / "study"
        subprocess.run(
            [
                sys.executable,
                str(LEAD / "scripts" / "init_study.py"),
                "--mode", mode,
                "--domain", "AI-assisted design workflows",
                "--target-market", "Professional designers",
                "--understand", "Which future-facing needs are advanced users already solving?",
                "--decision", "Should we fund a validation sprint?",
                "--innovation-altitude", "workflow",
                "--workspace", str(workspace),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        return workspace

    def validate(self, workspace):
        return subprocess.run(
            [sys.executable, str(LEAD / "scripts" / "validate_study.py"), str(workspace)],
            text=True,
            capture_output=True,
        )

    def write_json(self, workspace, name, value):
        (workspace / name).write_text(json.dumps(value), encoding="utf-8")

    def write_valid_evidence_core(self, workspace):
        self.write_json(
            workspace,
            "trends.json",
            [
                {
                    "trend_id": "T1",
                    "statement": "Workflows span more AI tools",
                    "direction": "increasing",
                    "evidence_refs": ["E1"],
                    "observable_indicators": ["Maintains cross-tool context artifacts"],
                    "importance": "Material to continuity of work",
                    "status": "VERIFIED",
                }
            ],
        )
        self.write_json(
            workspace,
            "sources.json",
            [
                {
                    "source_id": "SRC1",
                    "title": "Primary artifact",
                    "creator": "Example user",
                    "url": "https://example.com",
                    "source_type": "artifact",
                    "coverage": "FULL",
                    "coverage_note": "",
                    "access_date": "2026-08-28",
                }
            ],
        )
        self.write_json(
            workspace,
            "evidence.json",
            [
                {
                    "evidence_id": "E1",
                    "source_id": "SRC1",
                    "exact_location": "README",
                    "evidence_type": "behavior",
                    "verbatim_excerpt": "Maintains a persistent context system after repeated context loss",
                    "user_entity": "Example user",
                    "trend_id": "T1",
                    "lu_id": "LU1",
                    "caveat": "",
                }
            ],
        )
        episode = {
            "lu_id": "LU1",
            "user_entity": "Example user",
            "trend_id": "T1",
            "need_statement": "Recover context across tools",
            "context": "Multi-tool workflow",
            "status": "QUALIFIED",
            "lu1_evidence": ["E1"],
            "lu1_rationale": "The user is already operating across multiple AI tools and maintaining continuity infrastructure.",
            "advancement_indicator": "Persistent cross-tool context artifact maintained before it is mainstream behavior.",
            "lu2_evidence": ["E1"],
            "lu2_rationale": "Repeated context loss caused enough cost that the user built and maintained a workaround.",
            "benefit_signal": "Sustained effort to build and maintain the workaround after repeated loss.",
            "qualification_caveats": ["Exact time savings are unknown."],
            "baseline": "Manual reconstruction",
            "alternatives": [],
            "user_response": "Built a workaround",
            "desired_progress": "Resume work without reconstruction",
            "observed_result": "Workaround used",
            "trace": {
                "status": "SUFFICIENT",
                "initiating_condition": "Context was missing",
                "prior_approach": "Manual reconstruction",
                "switch_or_change_trigger": "Repeated loss",
                "expected_improvement": "Faster resumption",
                "sequence": [
                    {
                        "step_id": "S1",
                        "action": "Reconstruct context",
                        "context": "New session",
                        "result": "Repeated effort",
                        "evidence_refs": ["E1"],
                    }
                ],
                "fit_points": [
                    {
                        "step_ref": "S1",
                        "observed_behavior": "Manual reconstruction",
                        "compensating_behavior": "Persistent context artifact",
                        "stated_purpose": None,
                        "inferred_purpose": "Reduce repeated reconstruction",
                        "unknowns": ["Exact time cost"],
                        "evidence_refs": ["E1"],
                    }
                ],
                "actual_outcome": "Workaround used",
                "evidence_refs": ["E1"],
                "unknowns": [],
            },
            "unknowns": [],
        }
        self.write_json(workspace, "lu_episodes.json", [episode])
        self.write_json(
            workspace,
            "lineage.json",
            [
                {
                    "lineage_id": "L1",
                    "member_refs": ["SRC1", "LU1"],
                    "relationship": "INDEPENDENT_REDISCOVERY",
                    "independence": "INDEPENDENT",
                    "evidence_refs": ["E1"],
                    "rationale": "No upstream dependency or shared creator is evidenced.",
                }
            ],
        )
        self.write_json(
            workspace,
            "coverage.json",
            {
                "likely_overrepresented": ["Public English-language practitioners"],
                "likely_underrepresented": ["Private enterprise practitioners"],
                "inaccessible_or_private": ["Proprietary internal workflows"],
                "languages_or_regions_searched": ["English"],
                "corrective_actions": ["Interview private enterprise operators"],
                "fieldwork_referrals": [],
            },
        )
        return episode

    def freeze_valid(self, workspace):
        self.write_json(
            workspace,
            "sufficiency.json",
            {
                "status": "SUFFICIENT",
                "trend_support": "SUFFICIENT",
                "lu_qualification": "SUFFICIENT",
                "contradiction_search": "SUFFICIENT",
                "lineage_resolution": "SUFFICIENT",
                "pyramid_coverage": "SUFFICIENT",
                "marginal_value": "SUFFICIENT",
                "rationale": "The current corpus is sufficient for the stated decision; the next high-value branch is fieldwork.",
                "unresolved_actions": ["Interview private enterprise operators"],
            },
        )
        self.write_json(
            workspace,
            "freeze.json",
            {
                "status": "FROZEN",
                "frozen_at": "2026-08-28T18:00:00+00:00",
                "evidence_count": 1,
                "qualified_lu_count": 1,
                "independent_lineage_count": 1,
                "unresolved_gaps": ["Private enterprise coverage"],
                "post_freeze_evidence": [],
            },
        )

    def test_canonical_input_contract_is_visible_at_every_front_door(self):
        labels = [
            "Research Domain / Problem Space",
            "Target Market",
            "What do we want to understand?",
            "What human decision should this research help inform?",
            "Desired innovation altitude",
            "Optional hypotheses",
            "Optional discovery seeds",
            "Optional candidate-profile hypotheses",
            "Optional search constraints",
        ]
        for relative in ["SKILL.md", "QUICKSTART.md", "PORTABLE_PROMPT.md", "study-templates/research-input.md"]:
            body = (LEAD / relative).read_text(encoding="utf-8")
            for label in labels:
                self.assertIn(label, body, f"{relative} missing {label}")

    def test_initializer_preserves_full_research_brief_and_new_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "study"
            subprocess.run(
                [
                    sys.executable,
                    str(LEAD / "scripts" / "init_study.py"),
                    "--mode", "standard",
                    "--domain", "AI-assisted design workflows",
                    "--target-market", "Professional designers",
                    "--understand", "Which future-facing needs are advanced users already solving?",
                    "--decision", "Should we fund a validation sprint?",
                    "--innovation-altitude", "workflow",
                    "--hypothesis", "Context recovery has unusually high expected benefit",
                    "--hypothesis", "Cross-tool portability may matter",
                    "--discovery-seed", "GitHub repositories for persistent context systems",
                    "--discovery-seed", "AI workflow communities",
                    "--candidate-profile", "People maintaining elaborate cross-tool context workarounds",
                    "--search-constraint", "English-language sources only for this pass",
                    "--workspace", str(workspace),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            decision = json.loads((workspace / "decision.json").read_text(encoding="utf-8"))
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("AI-assisted design workflows", decision["domain"])
            self.assertEqual("Professional designers", decision["target_market"])
            self.assertEqual("Which future-facing needs are advanced users already solving?", decision["what_to_understand"])
            self.assertEqual("Should we fund a validation sprint?", decision["decision"])
            self.assertEqual("workflow", decision["innovation_altitude"])
            self.assertEqual(["Context recovery has unusually high expected benefit", "Cross-tool portability may matter"], decision["starting_hypotheses"])
            self.assertEqual(["GitHub repositories for persistent context systems", "AI workflow communities"], decision["discovery_seeds"])
            self.assertEqual(["People maintaining elaborate cross-tool context workarounds"], decision["candidate_profile_hypotheses"])
            self.assertEqual(["English-language sources only for this pass"], decision["search_constraints"])
            self.assertEqual("1.6", manifest["protocol_version"])
            self.assertEqual("DESK_RESEARCH", manifest["study_execution_level"])
            self.assertTrue((workspace / "sufficiency.json").exists())
            self.assertTrue((workspace / "decision_outcome.json").exists())

    def test_fresh_workspace_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("structural validation passed", result.stdout.lower())

    def test_discovery_inputs_do_not_prequalify_lead_users(self):
        protocol = (LEAD / "PROTOCOL.md").read_text(encoding="utf-8")
        phase_b = (LEAD / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        state = (LEAD / "references" / "state-contract.md").read_text(encoding="utf-8")
        self.assertIn("not qualification evidence", protocol)
        self.assertIn("not as Lead User qualification evidence", phase_b)
        self.assertIn("not a closed search universe", phase_b)
        self.assertIn("Search constraints are the only one", state)

    def test_episode_tracing_contract_is_explicit(self):
        protocol = (LEAD / "PROTOCOL.md").read_text(encoding="utf-8")
        phase_c = (LEAD / "prompts" / "phase-c-evidence.md").read_text(encoding="utf-8")
        phase_e = (LEAD / "prompts" / "phase-e-interpret.md").read_text(encoding="utf-8")
        state = (LEAD / "references" / "state-contract.md").read_text(encoding="utf-8")
        self.assertIn("Trace pivotal Lead User episodes", protocol)
        self.assertIn("Episode tracing", phase_c)
        self.assertIn("OBSERVED behavior", phase_c)
        self.assertIn("traced sequence", phase_e)
        self.assertIn("NOT_ASSESSED | PARTIAL | SUFFICIENT", state)

    def test_validator_requires_qualification_reasoning(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            episode = self.write_valid_evidence_core(workspace)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            episode.pop("benefit_signal")
            self.write_json(workspace, "lu_episodes.json", [episode])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("benefit_signal", result.stderr)

    def test_validator_checks_trace_evidence_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            episode = self.write_valid_evidence_core(workspace)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            episode["trace"]["fit_points"][0]["evidence_refs"] = ["E999"]
            self.write_json(workspace, "lu_episodes.json", [episode])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("E999", result.stderr)

    def test_validator_checks_trend_and_lineage_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            trends = json.loads((workspace / "trends.json").read_text(encoding="utf-8"))
            trends[0]["evidence_refs"] = ["E999"]
            self.write_json(workspace, "trends.json", trends)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("E999", result.stderr)

            self.write_valid_evidence_core(workspace)
            lineage = json.loads((workspace / "lineage.json").read_text(encoding="utf-8"))
            lineage[0]["member_refs"] = ["SRC999"]
            self.write_json(workspace, "lineage.json", lineage)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("SRC999", result.stderr)

    def test_freeze_requires_sufficiency_and_exact_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.freeze_valid(workspace)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            freeze = json.loads((workspace / "freeze.json").read_text(encoding="utf-8"))
            freeze["evidence_count"] = 99
            self.write_json(workspace, "freeze.json", freeze)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("does not match actual", result.stderr)

            self.freeze_valid(workspace)
            sufficiency = json.loads((workspace / "sufficiency.json").read_text(encoding="utf-8"))
            sufficiency["marginal_value"] = "INSUFFICIENT"
            self.write_json(workspace, "sufficiency.json", sufficiency)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("marginal_value", result.stderr)

    def test_fit_requirement_pass_requires_all_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.freeze_valid(workspace)
            self.write_json(
                workspace,
                "findings.json",
                [{"finding_id": "F1", "claim": "Context recovery is costly", "epistemic_label": "VERIFIED", "evidence_refs": ["E1"], "lu_refs": ["LU1"], "contradictions": [], "confidence_rationale": "Direct artifact"}],
            )
            self.write_json(
                workspace,
                "needs.json",
                [{"need_id": "N1", "statement": "Resume work with less reconstruction", "finding_ids": ["F1"], "relevant_trends": ["T1"], "propagation_status": "Plausible propagation", "contradictions": [], "concept_gate_status": "PASS", "concept_gate_rationale": "Supported"}],
            )
            criterion = {
                "requirement_id": "R1",
                "need_id": "N1",
                "requirement": "Resuming work must require materially less reconstruction.",
                "evidence_refs": ["E1"],
                "traceability": True,
                "implementation_independence": True,
                "solution_plurality": True,
                "causal_relevance": True,
                "altitude_check": True,
                "information_gain": True,
                "status": "PASS",
            }
            self.write_json(workspace, "fit_criteria.json", [criterion])
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            criterion["solution_plurality"] = False
            self.write_json(workspace, "fit_criteria.json", [criterion])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("solution_plurality", result.stderr)

    def test_full_lead_user_project_label_requires_direct_participation_basis(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp, mode="full")
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            manifest["study_execution_level"] = "FULL_LEAD_USER_PROJECT"
            manifest["study_execution_basis"] = []
            self.write_json(workspace, "manifest.json", manifest)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("direct_lead_user_participation", result.stderr)

    def test_execution_basis_rejects_non_string_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp, mode="full")
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            manifest["study_execution_level"] = "FULL_LEAD_USER_PROJECT"
            manifest["study_execution_basis"] = [{"unexpected": "object"}]
            self.write_json(workspace, "manifest.json", manifest)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("study_execution_basis[0]", result.stderr)

    def test_decision_outcome_is_validated_and_rendered_action_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.freeze_valid(workspace)
            self.write_json(
                workspace,
                "findings.json",
                [{"finding_id": "F1", "claim": "Advanced users incur repeated context-reconstruction cost.", "epistemic_label": "VERIFIED", "evidence_refs": ["E1"], "lu_refs": ["LU1"], "contradictions": [], "confidence_rationale": "Direct behavior"}],
            )
            self.write_json(
                workspace,
                "decision_outcome.json",
                {
                    "status": "TEST",
                    "recommendation": "Run a bounded private-enterprise validation sprint before committing to product development.",
                    "why": ["The need is supported in a qualified Lead User episode.", "Private-enterprise coverage remains weak."],
                    "decisive_finding_refs": ["F1"],
                    "decisive_lu_refs": ["LU1"],
                    "critical_uncertainties": ["Whether the behavior propagates beyond public advanced users."],
                    "action_now": ["Interview 5-8 referred private-enterprise operators and test the same need."],
                    "change_conditions": ["Move to ACT if direct fieldwork confirms the need across independent enterprise lineages."],
                    "what_evidence_supports": ["A future-facing need for lower-cost context recovery."],
                    "what_evidence_does_not_support": ["Population prevalence or willingness to pay."],
                    "contradictions": ["Public-source discoverability may overstate tool builders."],
                    "recommended_next_evidence": ["Direct enterprise interviews."],
                    "priority_human_review": ["Review LU1 qualification and propagation inference."],
                },
            )
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            subprocess.run(
                [sys.executable, str(LEAD / "scripts" / "render_decision_brief.py"), str(workspace)],
                check=True,
                text=True,
                capture_output=True,
            )
            brief = (workspace / "outputs" / "decision-brief.md").read_text(encoding="utf-8")
            self.assertLess(brief.index("## Recommendation"), brief.index("## Discovery coverage"))
            self.assertLess(brief.index("## Action now"), brief.index("## What the evidence supports"))
            self.assertIn("## What would change this decision", brief)
            self.assertIn("Execution level: DESK_RESEARCH", brief)

            outcome = json.loads((workspace / "decision_outcome.json").read_text(encoding="utf-8"))
            outcome["status"] = "STOP"
            self.write_json(workspace, "decision_outcome.json", outcome)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("invalid for mode STANDARD", result.stderr)


if __name__ == "__main__":
    unittest.main()
