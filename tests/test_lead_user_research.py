import json
import pathlib
import shutil
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

    def next_move(self, workspace):
        result = subprocess.run(
            [
                sys.executable,
                str(LEAD / "scripts" / "next_research_move.py"),
                str(workspace),
                "--json",
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        return json.loads(result.stdout)

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
                    "embedded_instruction_risk": "NONE",
                    "embedded_instruction_note": "",
                    "content_trust": "UNTRUSTED_DATA",
                    "outward_citation_allowed": False,
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
            "public_label": "An anonymized advanced operator",
            "identity_surface_allowed": False,
            "identity_surface_rationale": "",
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
                "trace_basis": "EVIDENCE_BACKED_ARTIFACT_RECONSTRUCTION",
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
                        "fit_point_id": "FP1",
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
                "dimensions": {
                    "trend_support": {
                        "status": "SUFFICIENT",
                        "rationale": "T1 has direct support.",
                        "supporting_refs": ["T1", "E1"],
                        "next_actions": [],
                    },
                    "lu_qualification": {
                        "status": "SUFFICIENT",
                        "rationale": "LU1 has separate advancement and benefit evidence.",
                        "supporting_refs": ["LU1", "E1"],
                        "next_actions": [],
                    },
                    "contradiction_search": {
                        "status": "SUFFICIENT",
                        "rationale": "The bounded fixture has been checked for contradictions.",
                        "supporting_refs": ["E1"],
                        "next_actions": [],
                    },
                    "lineage_resolution": {
                        "status": "SUFFICIENT",
                        "rationale": "The only lineage has direct independence evidence.",
                        "supporting_refs": ["SRC1", "E1"],
                        "next_actions": [],
                    },
                    "pyramid_coverage": {
                        "status": "SUFFICIENT",
                        "rationale": "The bounded test branch is resolved.",
                        "supporting_refs": ["SRC1"],
                        "next_actions": [],
                    },
                    "marginal_value": {
                        "status": "SUFFICIENT",
                        "rationale": "The next useful evidence requires fieldwork.",
                        "supporting_refs": [],
                        "next_actions": [],
                    },
                },
                "overall_rationale": "The current corpus is sufficient for the stated decision; the next high-value branch is fieldwork.",
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
            self.assertEqual("1.7", manifest["protocol_version"])
            self.assertEqual("DESK_RESEARCH", manifest["study_execution_level"])
            self.assertTrue((workspace / "sufficiency.json").exists())
            self.assertTrue((workspace / "decision_outcome.json").exists())
            self.assertTrue((workspace / "hypotheses.json").exists())
            self.assertTrue((workspace / "observability.json").exists())
            self.assertTrue((workspace / "analysis_runs.json").exists())
            hypotheses = json.loads((workspace / "hypotheses.json").read_text(encoding="utf-8"))
            self.assertEqual(["H1", "H2"], [row["hypothesis_id"] for row in hypotheses])
            self.assertTrue(all(row["status"] == "UNTESTED" for row in hypotheses))

    def test_fresh_workspace_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("structural validation passed", result.stdout.lower())

    def test_next_move_routes_from_brief_through_discovery_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            move = self.next_move(workspace)
            self.assertEqual("B", move["next_phase"])
            self.assertEqual("/lead-user-discover", move["recommended_command"])

            self.write_json(workspace, "trends.json", [{"trend_id": "T1"}])
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            move = self.next_move(workspace)
            self.assertEqual("C", move["next_phase"])
            self.assertEqual("/lead-user-evidence", move["recommended_command"])

            self.write_valid_evidence_core(workspace)
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            move = self.next_move(workspace)
            self.assertEqual("D", move["next_phase"])

    def test_next_move_routes_insufficient_research_to_the_right_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            sufficiency = json.loads((workspace / "sufficiency.json").read_text(encoding="utf-8"))
            sufficiency["status"] = "INSUFFICIENT"
            sufficiency["dimensions"]["trend_support"] = {
                "status": "INSUFFICIENT",
                "rationale": "The trend branch is too narrow.",
                "supporting_refs": ["T1"],
                "next_actions": ["Search an independent trend branch."],
            }
            sufficiency["unresolved_actions"] = ["Search an independent trend branch."]
            self.write_json(workspace, "sufficiency.json", sufficiency)
            move = self.next_move(workspace)
            self.assertEqual("B", move["next_phase"])

            sufficiency["dimensions"]["trend_support"]["status"] = "SUFFICIENT"
            sufficiency["dimensions"]["lu_qualification"] = {
                "status": "INSUFFICIENT",
                "rationale": "Benefit evidence remains weak.",
                "supporting_refs": ["LU1"],
                "next_actions": ["Inspect another evidence batch."],
            }
            self.write_json(workspace, "sufficiency.json", sufficiency)
            move = self.next_move(workspace)
            self.assertEqual("C", move["next_phase"])

    def test_next_move_routes_scout_from_bounded_evidence_to_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp, mode="scout")
            self.write_valid_evidence_core(workspace)
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            move = self.next_move(workspace)
            self.assertEqual("G", move["next_phase"])
            self.assertEqual("/lead-user-decide", move["recommended_command"])
            self.assertIn("bounded SCOUT", move["reason"])

    def test_next_move_skips_shape_when_no_need_passes_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            self.freeze_valid(workspace)
            self.write_json(workspace, "findings.json", [{"finding_id": "F1"}])
            self.write_json(
                workspace,
                "needs.json",
                [{"need_id": "N1", "concept_gate_status": "FAIL"}],
            )
            self.write_json(workspace, "principles.json", [{"principle_id": "SP1"}])
            move = self.next_move(workspace)
            self.assertEqual("G", move["next_phase"])
            self.assertIn("without inventing concepts", move["reason"])

    def test_next_move_requires_shape_only_for_passing_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.write_json(workspace, "candidates.json", [{"candidate_id": "C1"}])
            self.write_json(workspace, "search_log.json", [{"query": "advanced workflows"}])
            self.freeze_valid(workspace)
            self.write_json(workspace, "findings.json", [{"finding_id": "F1"}])
            self.write_json(
                workspace,
                "needs.json",
                [{"need_id": "N1", "concept_gate_status": "PASS"}],
            )
            self.write_json(workspace, "principles.json", [{"principle_id": "SP1"}])
            move = self.next_move(workspace)
            self.assertEqual("F", move["next_phase"])
            self.assertIn("shaping frame", move["reason"])

            self.write_json(
                workspace,
                "shaping_frame.json",
                [{
                    "frame_id": "SF1",
                    "need_id": "N1",
                    "status": "PROVISIONAL",
                    "accepted_by_human": False,
                }],
            )
            move = self.next_move(workspace)
            self.assertEqual("HUMAN_REVIEW", move["state"])
            self.assertEqual("F", move["next_phase"])
            self.assertIn("must not self-accept", move["human_gate"])

            self.write_json(
                workspace,
                "shaping_frame.json",
                [{
                    "frame_id": "SF1",
                    "need_id": "N1",
                    "status": "ACCEPTED",
                    "accepted_by_human": True,
                }],
            )
            self.write_json(workspace, "fit_criteria.json", [{"need_id": "N1"}])
            self.write_json(workspace, "concepts.json", [{"need_id": "N1"}])
            move = self.next_move(workspace)
            self.assertEqual("G", move["next_phase"])

    def test_next_move_marks_complete_study_and_preserves_frame_gate(self):
        move = self.next_move(LEAD / "examples" / "reference-study")
        self.assertEqual("COMPLETE", move["state"])
        self.assertIsNone(move["recommended_command"])
        self.assertEqual("framing-doc", move["conditional_next_skill"])
        self.assertIn("Accept, reject, or revise", move["human_gate"])

    def test_planning_system_exposes_one_skill_with_phase_commands(self):
        phases = {
            "frame": "phase-a-frame.md",
            "discover": "phase-b-discover.md",
            "evidence": "phase-c-evidence.md",
            "freeze": "phase-d-freeze.md",
            "interpret": "phase-e-interpret.md",
            "shape": "phase-f-shape.md",
            "decide": "phase-g-decide.md",
            "deliver": "phase-h-deliver.md",
        }
        for name, prompt in phases.items():
            claude = ROOT / ".claude" / "commands" / f"lead-user-{name}.md"
            gemini = ROOT / ".gemini" / "commands" / f"lead-user-{name}.toml"
            self.assertTrue(claude.is_file(), claude)
            self.assertTrue(gemini.is_file(), gemini)
            self.assertIn("lead-user-research/SKILL.md", claude.read_text(encoding="utf-8"))
            self.assertIn(prompt, claude.read_text(encoding="utf-8"))
            self.assertIn(prompt, gemini.read_text(encoding="utf-8"))

        router = (ROOT / "planning-router" / "SKILL.md").read_text(encoding="utf-8")
        orchestration = (ROOT / ".agent-orchestration.yaml").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("`lead-user-research`", router)
        self.assertIn("lead_user_research:", orchestration)
        self.assertIn("/lead-user-deliver", orchestration)
        self.assertIn("upstream evidence move", agents)

    def test_research_to_frame_transition_requires_human_acceptance(self):
        handoff = (LEAD / "study-templates" / "research-to-frame-handoff.md").read_text(encoding="utf-8")
        skill = (LEAD / "SKILL.md").read_text(encoding="utf-8")
        controller = (LEAD / "references" / "phase-handoff.md").read_text(encoding="utf-8")
        self.assertIn("PROPOSED | ACCEPTED | REJECTED | REVISE", handoff)
        self.assertIn("Do not invoke `framing-doc`", handoff)
        self.assertIn("before invoking `framing-doc`", skill)
        self.assertIn("Completion does not automatically invoke framing", controller)

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

    def test_validator_enforces_source_content_trust_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

            sources = json.loads((workspace / "sources.json").read_text(encoding="utf-8"))
            sources[0]["content_trust"] = "TRUSTED_INSTRUCTION"
            self.write_json(workspace, "sources.json", sources)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("UNTRUSTED_DATA", result.stderr)

            sources[0]["content_trust"] = "UNTRUSTED_DATA"
            sources[0]["embedded_instruction_risk"] = "UNKNOWN"
            sources[0]["embedded_instruction_note"] = ""
            self.write_json(workspace, "sources.json", sources)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("embedded_instruction_note", result.stderr)

            sources[0]["embedded_instruction_risk"] = "NONE"
            self.write_json(workspace, "sources.json", sources)
            episodes = json.loads((workspace / "lu_episodes.json").read_text(encoding="utf-8"))
            episodes[0]["public_label"] = "Example user profile"
            self.write_json(workspace, "lu_episodes.json", episodes)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("public_label exposes private user_entity", result.stderr)

            episodes[0]["public_label"] = "An anonymized advanced operator"
            self.write_json(workspace, "lu_episodes.json", episodes)
            evidence = json.loads((workspace / "evidence.json").read_text(encoding="utf-8"))
            evidence[0]["public_summary"] = "Example user maintains a context system."
            self.write_json(workspace, "evidence.json", evidence)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("public_summary exposes private user_entity", result.stderr)

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
            sufficiency["dimensions"]["marginal_value"]["status"] = "INSUFFICIENT"
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
                [{"need_id": "N1", "statement": "Resume work with less reconstruction", "finding_ids": ["F1"], "relevant_trends": ["T1"], "propagation_status": "Plausible propagation", "contradictions": [], "concept_gate_status": "PASS", "concept_gate_rationale": "Supported", "concept_gate_checks": {"credible_trend": True, "qualified_lu_support": True, "need_workaround_separation": True, "fitness_evidence_sufficient": True, "no_blocking_contradiction": True}}],
            )
            self.write_json(
                workspace,
                "shaping_frame.json",
                [{
                    "frame_id": "SF1",
                    "need_id": "N1",
                    "x": {
                        "trigger_or_context": "Context is missing in a new session.",
                        "current_approach": "Manual reconstruction.",
                        "current_result": "Repeated effort.",
                        "breakdowns": ["The user repeats prior reconstruction work."],
                    },
                    "f": {"status": "UNSPECIFIED"},
                    "y": {"desired_outcome": "Resume work without reconstruction."},
                    "gap": "Carry enough state forward to avoid repeated reconstruction.",
                    "boundaries": ["Do not require more upkeep than reconstruction."],
                    "evidence_refs": ["E1"],
                    "status": "ACCEPTED",
                    "accepted_by_human": True,
                    "acceptance_note": "Accepted for the test.",
                }],
            )
            criterion = {
                "requirement_id": "R1",
                "need_id": "N1",
                "frame_ref": "SF1",
                "origin": "FROM_GAP",
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
                    "recommendation": "Do not expose Example user; run a bounded private-enterprise validation sprint before committing to product development.",
                    "why": ["The need is supported in a qualified Lead User episode.", "Private-enterprise coverage remains weak."],
                    "decisive_finding_refs": ["F1"],
                    "decisive_lu_refs": ["LU1"],
                    "critical_uncertainties": ["Whether the behavior propagates beyond public advanced users."],
                    "action_now": [
                        {
                            "action_id": "A1",
                            "action": "Interview referred private-enterprise operators and test the same need.",
                            "owner": "Research lead",
                            "timebox": "Two weeks",
                            "deliverable": "An evidence-linked fieldwork readout",
                            "evidence_to_collect": ["Observed reconstruction behavior", "Benefit and maintenance signals"],
                            "success_condition": "At least three independent episodes establish the same need and net benefit.",
                            "stop_condition": "Stop if two independent episodes contradict the need or field access remains blocked.",
                            "decision_at_end": "Choose ACT, HOLD, or REJECT.",
                        }
                    ],
                    "change_conditions": ["Move to ACT if direct fieldwork confirms the need across independent enterprise lineages."],
                    "what_evidence_supports": ["A future-facing need for lower-cost context recovery."],
                    "what_evidence_does_not_support": ["Population prevalence or willingness to pay."],
                    "contradictions": ["Public-source discoverability may overstate tool builders."],
                    "recommended_next_evidence": ["Direct enterprise interviews."],
                    "priority_human_review": ["Review LU1 qualification and propagation inference."],
                },
            )
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            manifest["phase"] = "G"
            manifest["study_status"] = "DECIDED"
            self.write_json(workspace, "manifest.json", manifest)
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
            self.assertNotIn("Example user", brief)
            self.assertNotIn("https://example.com", brief)
            self.assertNotIn("Primary artifact", brief)
            self.assertNotIn("Maintains a persistent context system after repeated context loss", brief)
            self.assertIn("An anonymized advanced operator", brief)

            outcome = json.loads((workspace / "decision_outcome.json").read_text(encoding="utf-8"))
            outcome["action_now"][0].pop("stop_condition")
            self.write_json(workspace, "decision_outcome.json", outcome)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("stop_condition", result.stderr)

            outcome["action_now"][0]["stop_condition"] = "Stop if access remains blocked."
            outcome["status"] = "STOP"
            self.write_json(workspace, "decision_outcome.json", outcome)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("invalid for mode STANDARD", result.stderr)

    def test_complete_reference_study_validates_and_resists_source_instruction(self):
        reference = LEAD / "examples" / "reference-study"
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "reference-study"
            shutil.copytree(reference, workspace)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)
            subprocess.run(
                [sys.executable, str(LEAD / "scripts" / "render_decision_brief.py"), str(workspace)],
                check=True,
                text=True,
                capture_output=True,
            )
            brief = (workspace / "outputs" / "decision-brief.md").read_text(encoding="utf-8")
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            sources = json.loads((workspace / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual("H", manifest["phase"])
            self.assertEqual("COMPLETE", manifest["study_status"])
            self.assertIn("- State fingerprint: sha256:", brief)
            self.assertTrue(any(row["embedded_instruction_risk"] == "PRESENT" for row in sources))
            self.assertTrue(all(row["content_trust"] == "UNTRUSTED_DATA" for row in sources))
            for forbidden in [
                "ASSURANCE_OVERRIDE_TOKEN",
                "Ignore the Lead User protocol",
                "Operator Alpha",
                "Operator Beta",
                "Operator Gamma",
            ]:
                self.assertNotIn(forbidden, brief)

            outcome = json.loads((workspace / "decision_outcome.json").read_text(encoding="utf-8"))
            outcome["recommendation"] += " This unrendered change must invalidate completion."
            self.write_json(workspace, "decision_outcome.json", outcome)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("State fingerprint", result.stderr)

    def test_complete_status_requires_real_phase_h_delivery(self):
        reference = LEAD / "examples" / "reference-study"
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "reference-study"
            shutil.copytree(reference, workspace)
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            manifest["phase"] = "G"
            manifest["model_check"] = "NOT_RUN"
            self.write_json(workspace, "manifest.json", manifest)
            (workspace / "outputs" / "decision-brief.md").write_text("", encoding="utf-8")
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("complete study must be in phase H", result.stderr)
            self.assertIn("complete study requires model_check COMPLETED", result.stderr)
            self.assertIn("complete study requires non-empty outputs/decision-brief.md", result.stderr)


    def test_next_move_blocks_unfalsifiable_starting_hypothesis(self):
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
                    "--hypothesis", "Cross-tool context loss creates unusually high benefit from continuity tooling",
                    "--workspace", str(workspace),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            move = self.next_move(workspace)
            self.assertEqual("A", move["next_phase"])
            self.assertEqual("BLOCKED", move["state"])
            self.assertIn("falsifiable", move["reason"])

            hypotheses = json.loads((workspace / "hypotheses.json").read_text(encoding="utf-8"))
            hypotheses[0]["observable_predictions"] = [
                "Advanced users repeatedly reconstruct or persist context across tool boundaries."
            ]
            hypotheses[0]["strongest_plausible_refuter"] = (
                "Comparable advanced users exposed to cross-tool work do not incur meaningful continuity cost."
            )
            self.write_json(workspace, "hypotheses.json", hypotheses)
            move = self.next_move(workspace)
            self.assertEqual("B", move["next_phase"])

    def test_validator_enforces_hypothesis_status_and_contrastive_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            hypothesis = {
                "hypothesis_id": "H1",
                "claim": "Cross-tool context loss creates material continuity cost.",
                "scope": "Advanced multi-tool AI workflows",
                "observable_predictions": ["Advanced users create persistent continuity workarounds."],
                "strongest_plausible_refuter": "Comparable exposed users show no continuity cost.",
                "rival_explanations": ["The workaround exists for convenience rather than loss."],
                "targeted_refutation_searches": ["Find advanced users without continuity workarounds."],
                "evidence_for": ["E1"],
                "evidence_against": [],
                "contrastive_cases": [],
                "boundary_conditions": [],
                "status": "CONFIRMED",
                "update_rationale": "Not allowed.",
            }
            self.write_json(workspace, "hypotheses.json", [hypothesis])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("invalid status", result.stderr)

            hypothesis["status"] = "SURVIVED_CURRENT_TESTS"
            hypothesis["update_rationale"] = "The current bounded evidence did not overturn the claim."
            self.write_json(workspace, "hypotheses.json", [hypothesis])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("contrastive case", result.stderr)

            hypothesis["contrastive_cases"] = [
                {
                    "case_type": "PREDICTED_POSITIVE",
                    "evidence_refs": ["E1"],
                    "interpretation": "The predicted condition and observed workaround co-occur.",
                }
            ]
            self.write_json(workspace, "hypotheses.json", [hypothesis])
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_validator_rejects_synthetic_or_simulated_human_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            evidence = json.loads((workspace / "evidence.json").read_text(encoding="utf-8"))
            evidence[0]["evidence_basis"] = "SYNTHETIC_OR_SIMULATED"
            self.write_json(workspace, "evidence.json", evidence)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("cannot be persisted as human evidence", result.stderr)

    def test_freeze_blocks_open_observability_and_unvalidated_ai_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.freeze_valid(workspace)

            self.write_json(
                workspace,
                "observability.json",
                [
                    {
                        "observability_id": "O1",
                        "question": "Does continuity cost persist in private enterprise workflows?",
                        "decision_critical": True,
                        "status": "NOT_OBSERVABLE",
                        "evidence_refs": [],
                        "resolution": "OPEN",
                        "fieldwork_referral": "",
                        "acceptance_rationale": "",
                    }
                ],
            )
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("observability", result.stderr)

            observability = json.loads((workspace / "observability.json").read_text(encoding="utf-8"))
            observability[0]["resolution"] = "FIELDWORK_REFERRAL"
            observability[0]["fieldwork_referral"] = "Interview referred private-enterprise operators."
            self.write_json(workspace, "observability.json", observability)

            self.write_json(
                workspace,
                "analysis_runs.json",
                [
                    {
                        "analysis_run_id": "AR1",
                        "task": "Extract repeated continuity failures from a large issue corpus.",
                        "model": "ExampleModel",
                        "model_version": "1",
                        "prompt_or_workflow_version": "v1",
                        "extraction_schema": "episode-v1",
                        "sampled_validation": {
                            "status": "NOT_ASSESSED",
                            "sample_size": 0,
                            "agreement_or_error_summary": "",
                        },
                    }
                ],
            )
            evidence = json.loads((workspace / "evidence.json").read_text(encoding="utf-8"))
            evidence[0]["analysis_run_id"] = "AR1"
            self.write_json(workspace, "evidence.json", evidence)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("sampled validation PASSED", result.stderr)

            analysis_runs = json.loads((workspace / "analysis_runs.json").read_text(encoding="utf-8"))
            analysis_runs[0]["sampled_validation"] = {
                "status": "PASSED",
                "sample_size": 20,
                "agreement_or_error_summary": "Sampled extraction errors were within the study's accepted bound.",
            }
            self.write_json(workspace, "analysis_runs.json", analysis_runs)
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_adversarial_trace_research_contract_is_explicit(self):
        protocol = (LEAD / "PROTOCOL.md").read_text(encoding="utf-8")
        phase_b = (LEAD / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        phase_c = (LEAD / "prompts" / "phase-c-evidence.md").read_text(encoding="utf-8")
        phase_d = (LEAD / "prompts" / "phase-d-freeze.md").read_text(encoding="utf-8")
        state = (LEAD / "references" / "state-contract.md").read_text(encoding="utf-8")

        for value in [
            "SURVIVED_CURRENT_TESTS",
            "EXPOSED_NO_OUTCOME",
            "OUTCOME_WITHOUT_EXPOSURE",
            "ABANDONED_OR_REVERSED_SOLUTION",
            "Observability gate",
            "AI analysis validation",
        ]:
            self.assertIn(value, protocol)
        self.assertIn("targeted refutation searches", phase_b)
        self.assertIn("Synthetic personas", phase_c)
        self.assertIn("process-mining-style", phase_c)
        self.assertIn("platform/community context", phase_c)
        self.assertIn("decision-critical observability", phase_d)
        self.assertIn("hypotheses.json", state)
        self.assertIn("observability.json", state)
        self.assertIn("analysis_runs.json", state)


    def test_trace_requires_real_case_basis_and_stable_fit_point_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            episode = self.write_valid_evidence_core(workspace)
            episode["trace"]["trace_basis"] = "FRAGMENTARY_EVIDENCE"
            self.write_json(workspace, "lu_episodes.json", [episode])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("cannot be SUFFICIENT", result.stderr)

            episode["trace"]["trace_basis"] = "EVIDENCE_BACKED_ARTIFACT_RECONSTRUCTION"
            episode["trace"]["fit_points"][0]["step_ref"] = "S999"
            self.write_json(workspace, "lu_episodes.json", [episode])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("missing step_ref", result.stderr)

    def test_pass_requirement_requires_human_accepted_frame_and_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self.init_workspace(tmp)
            self.write_valid_evidence_core(workspace)
            self.write_json(
                workspace,
                "findings.json",
                [{"finding_id": "F1", "claim": "Context recovery is costly", "epistemic_label": "VERIFIED", "evidence_refs": ["E1"], "lu_refs": ["LU1"], "trace_refs": ["LU1:FP1"], "contradictions": [], "confidence_rationale": "Direct artifact"}],
            )
            self.write_json(
                workspace,
                "needs.json",
                [{"need_id": "N1", "statement": "Resume work with less reconstruction", "finding_ids": ["F1"], "relevant_trends": ["T1"], "trace_refs": ["LU1:FP1"], "propagation_status": "Plausible propagation", "contradictions": [], "concept_gate_status": "PASS", "concept_gate_rationale": "Supported", "concept_gate_checks": {"credible_trend": True, "qualified_lu_support": True, "need_workaround_separation": True, "fitness_evidence_sufficient": True, "no_blocking_contradiction": True}}],
            )
            frame = {
                "frame_id": "SF1",
                "need_id": "N1",
                "x": {"trigger_or_context": "New session", "current_approach": "Manual reconstruction", "current_result": "Repeated effort", "breakdowns": ["Repeated reconstruction"]},
                "f": {"status": "UNSPECIFIED"},
                "y": {"desired_outcome": "Resume without reconstruction"},
                "gap": "Preserve enough state to avoid reconstruction",
                "boundaries": [],
                "evidence_refs": ["E1"],
                "status": "PROVISIONAL",
                "accepted_by_human": False,
                "acceptance_note": "",
            }
            self.write_json(workspace, "shaping_frame.json", [frame])
            criterion = {
                "requirement_id": "R1", "need_id": "N1", "frame_ref": "SF1",
                "origin": "FROM_GAP", "requirement": "Reduce reconstruction effort.",
                "evidence_refs": ["E1"], "traceability": True,
                "implementation_independence": True, "solution_plurality": True,
                "causal_relevance": True, "altitude_check": True,
                "information_gain": True, "status": "PASS",
            }
            self.write_json(workspace, "fit_criteria.json", [criterion])
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("accepted human-reviewed shaping frame", result.stderr)

            frame["status"] = "ACCEPTED"
            frame["accepted_by_human"] = True
            frame["acceptance_note"] = "Accepted explicitly."
            self.write_json(workspace, "shaping_frame.json", [frame])
            result = self.validate(workspace)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_selected_shape_requires_rotated_parts_covering_requirements(self):
        reference = LEAD / "examples" / "reference-study"
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "reference-study"
            shutil.copytree(reference, workspace)
            manifest = json.loads((workspace / "manifest.json").read_text(encoding="utf-8"))
            manifest["study_status"] = "DECIDED"
            manifest["phase"] = "G"
            self.write_json(workspace, "manifest.json", manifest)
            concepts = json.loads((workspace / "concepts.json").read_text(encoding="utf-8"))
            concepts[0]["rotation_status"] = "NOT_RUN"
            concepts[0]["parts"] = []
            self.write_json(workspace, "concepts.json", concepts)
            result = self.validate(workspace)
            self.assertEqual(1, result.returncode)
            self.assertIn("SELECTED requires rotation_status RUN", result.stderr)

    def test_trace_frame_fit_contract_is_explicit(self):
        protocol = (LEAD / "PROTOCOL.md").read_text(encoding="utf-8")
        phase_c = (LEAD / "prompts" / "phase-c-evidence.md").read_text(encoding="utf-8")
        phase_f = (LEAD / "prompts" / "phase-f-shape.md").read_text(encoding="utf-8")
        framing = (ROOT / "framing-doc" / "SKILL.md").read_text(encoding="utf-8")
        shaping = (ROOT / "shaping" / "SKILL.md").read_text(encoding="utf-8")
        for value in ["real episode → ordered steps", "x → f() → y", "FROM_X", "Requirements × Shapes", "Rotated Fit Check"]:
            self.assertIn(value, protocol)
        self.assertIn("specific real use case", phase_c)
        self.assertIn("accepted_by_human", phase_f)
        self.assertIn("x → f() → y", framing)
        self.assertIn("Parts × Requirements", shaping)


if __name__ == "__main__":
    unittest.main()
