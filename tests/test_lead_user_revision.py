"""Structural regressions for optional refinements, using fictional study data."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1] / "lead-user-research"
REFERENCE = PACKAGE / "examples/reference-study"


class RevisionStudyTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.study = Path(workspace.name) / "study"
        shutil.copytree(REFERENCE, self.study)

    def read(self, name):
        return json.loads((self.study / name).read_text())

    def write(self, name, value):
        (self.study / name).write_text(json.dumps(value), encoding="utf-8")

    def script(self, name, *args):
        return subprocess.run(
            [sys.executable, str(PACKAGE / "scripts" / name), str(self.study), *args],
            capture_output=True, text=True, check=False,
        )

    def start_evidence_repair(self):
        manifest = self.read("manifest.json")
        manifest.update(phase="C", study_status="IN_PROGRESS", evidence_completion="NOT_STARTED",
                        interpretation_completion="NOT_STARTED")
        self.write("manifest.json", manifest)
        freeze = self.read("freeze.json")
        freeze.update(status="NOT_FROZEN", frozen_at=None, evidence_fingerprint=None,
                      evidence_count=None, qualified_lu_count=None, independent_lineage_count=None)
        self.write("freeze.json", freeze)
        for name in ("findings", "needs", "principles", "shaping_frame", "fit_criteria", "concepts"):
            self.write(name + ".json", [])
        self.write("decision_outcome.json", {})

    def test_rare_search_records_under_ranked_original_with_access_caveats(self):
        self.start_evidence_repair()
        log = self.read("search_log.json")
        log[0]["rare_signal_check"] = {
            "channel": "Fictional docs index and offline referral",
            "access_limits": "Private operators omitted",
            "likely_missing": "Quiet failures in non-English teams",
            "batch_bound": "Four records; inspect an abandonment case below the popular thread",
            "signals": ["Abandoned high-effort handoff amid popular workflow mentions"],
            "methods": ["keyword search", "low-ranked originals"],
            "inspected_original_refs": ["SRC1", "SRC2", "SRC4"],
            "low_rank_sample_refs": ["SRC4"],
        }
        self.write("search_log.json", log)
        result = self.script("validate_study.py")
        self.assertNotIn("rare_signal_check", result.stderr)
        log[0]["rare_signal_check"]["low_rank_sample_refs"] = ["SRC3", "SRC999"]
        self.write("search_log.json", log)
        errors = self.script("validate_study.py").stderr
        self.assertIn("missing", errors)
        self.assertIn("must reference inspected originals", errors)

    def test_observed_analog_requires_evidence_and_limits(self):
        self.start_evidence_repair()
        candidates = self.read("candidates.json")
        candidates[0]["discovery_path"] = "ADVANCED_ANALOG"
        mapping = {
            "context": "Fictional handoff",
            "relationship": "State retention reduces reconstruction",
            "bottleneck": "Lost decisions",
            "constraints": "Short transitions",
            "desired_outcome": "Safe restart",
            "hypothesized_mechanism": "Snapshot only high-impact state",
            "analog_domain": "Incident rotation",
            "correspondence": "An incoming operator needs the last decisions",
            "disanalogy": "Rotations have dedicated preparation time",
            "potential_principle": "Reduce the number of facts to transfer",
            "break_condition": "Breaks if context decays before the next shift",
            "status": "SPECULATIVE",
            "evidence_refs": [],
        }
        candidates[0]["structural_analog"] = mapping
        self.write("candidates.json", candidates)
        self.assertNotIn("structural_analog", self.script("validate_study.py").stderr)
        mapping["status"] = "OBSERVED_ANALOG"
        mapping["disanalogy"] = ""
        self.write("candidates.json", candidates)
        errors = self.script("validate_study.py").stderr
        self.assertIn("requires non-empty disanalogy", errors)
        self.assertIn("evidence_refs", errors)

    def test_nested_rival_requires_distinct_predictions_and_refuter(self):
        self.start_evidence_repair()
        rows = self.read("hypotheses.json")
        contrast = {"kind": "NULL", "alternative": "Old need is newly visible",
                    "primary_predictions": ["More actual handoffs"],
                    "observable_predictions": ["No change in handoffs at equal logging"],
                    "discriminating_observation": "Handoffs before and after logging",
                    "refuter": "Actual handoff rate changed at equal visibility",
                    "evidence_for_alternative": ["E5"], "evidence_against_alternative": []}
        rows[0]["contrast"] = contrast
        self.write("hypotheses.json", rows)
        self.assertNotIn("contrast", self.script("validate_study.py").stderr)
        contrast["observable_predictions"] = contrast["primary_predictions"]
        del contrast["refuter"]
        self.write("hypotheses.json", rows)
        errors = self.script("validate_study.py").stderr
        self.assertIn("different predictions", errors)
        self.assertIn("requires non-empty refuter", errors)
        rows[0]["contrast"] = {"kind": "NOT_APPLICABLE"}
        self.write("hypotheses.json", rows)
        self.assertIn("requires non-empty rationale", self.script("validate_study.py").stderr)

    def test_unresolved_pivotal_claim_blocks_qualification_and_freeze_and_routes_repair(self):
        self.start_evidence_repair()
        manifest = self.read("manifest.json")
        manifest["evidence_completion"] = "COMPLETED"
        self.write("manifest.json", manifest)
        evidence = self.read("evidence.json")
        claim = next(row for row in evidence if row["evidence_id"] == "E2")
        claim["claim_audit"] = {"decision_use": "PIVOTAL", "human_review": "NOT_REVIEWED", "checks": {
            key: {"status": "PASS", "rationale": "Fictional audit record", "refs": [claim["source_id"]]}
            for key in ("access", "attribution", "context", "claim_type", "entailment",
                        "independent_support", "contradictions")
        }}
        for dim, status in (("attribution", "FAIL"), ("entailment", "FAIL"), ("contradictions", "UNKNOWN")):
            claim["claim_audit"]["checks"][dim]["status"] = status
        self.write("evidence.json", evidence)
        errors = self.script("validate_study.py").stderr
        self.assertIn("qualification uses unresolved", errors)
        self.assertIn("requires repair of pivotal claim E2", errors)
        self.assertIn("repair pivotal claims", self.script("freeze_evidence.py").stderr)
        result = json.loads(self.script("next_research_move.py", "--json").stdout)
        self.assertEqual(result["next_phase"], "C")
        self.assertIn("Unresolved pivotal claim: E2", result["blockers"])
        claim["claim_audit"]["checks"]["access"]["refs"] = ["SRC999"]
        self.write("evidence.json", evidence)
        self.assertIn("requires the accessible underlying source", self.script("validate_study.py").stderr)

    def test_unresolved_transfer_and_synthetic_refs_cannot_support_existing_gate(self):
        needs = self.read("needs.json")
        contrast = {"dimension": "expertise", "lead_user_situation": "Dedicated expert",
                    "target_situation": "Novice rotation", "load_bearing": True, "status": "UNKNOWN",
                    "evidence_refs": [], "refuter": "Novices maintain the transfer with equal effort"}
        needs[0]["transferability_assessment"]["contrasts"] = [contrast]
        self.write("needs.json", needs)
        self.assertIn("unresolved load-bearing contrast", self.script("validate_study.py").stderr)
        contrast.update(status="SUPPORTED", evidence_refs=["SIMULATED_ESTIMATE:RUN1"])
        self.write("needs.json", needs)
        errors = self.script("validate_study.py").stderr
        self.assertIn("unresolved load-bearing contrast", errors)
        self.assertIn("missing transfer evidence", errors)
        contrast.update(evidence_refs=["E3"])
        self.write("needs.json", needs)
        self.assertNotIn("contrasts", self.script("validate_study.py").stderr)

    def test_mechanism_remains_proposed_with_conflicting_cases(self):
        principles = self.read("principles.json")
        principles[0]["conditional_mechanism"] = {
            "status": "PROPOSED", "condition": "When recovery costs exceed maintenance",
            "behavioral_relation": "Operators may sustain a handoff practice",
            "supporting_episodes": ["LU1"], "conflicting_episodes": ["LU3"],
            "unassessed_episodes": [], "rival_hypothesis_refs": ["H1"],
            "discriminating_observation": "Compare work with equal continuity but different upkeep",
        }
        self.write("principles.json", principles)
        self.assertNotIn("conditional_mechanism", self.script("validate_study.py").stderr)
        principles[0]["conditional_mechanism"]["status"] = "CAUSALLY_IDENTIFIED"
        self.write("principles.json", principles)
        self.assertIn("PROPOSED interpretation", self.script("validate_study.py").stderr)

    def test_candidates_deduplicate_and_hold_frame_criteria_fixed(self):
        script_dir = PACKAGE / "scripts"
        sys.path.insert(0, str(script_dir))
        self.addCleanup(sys.path.remove, str(script_dir))
        from study_fingerprint import shaping_basis_digest

        frames = self.read("shaping_frame.json")
        criteria = self.read("fit_criteria.json")
        concepts = self.read("concepts.json")
        digest = shaping_basis_digest(frames[0], criteria)
        for concept, functional_key in zip(concepts, ("capture", "incremental-ledger")):
            concept["generation"] = {
                "branch": functional_key, "functional_key": functional_key, "frame_ref": "SF1",
                "boundary_status": "PASS", "predicted_behavior": "Less recovery effort",
                "distinctness_rationale": "Different trigger and update path",
                "collapsed_alternatives": [], "basis_digest": digest,
            }
        self.write("concepts.json", concepts)
        self.assertNotIn("generation", self.script("validate_study.py").stderr)
        concepts[1]["generation"].update(functional_key="CAPTURE", boundary_status="FAIL")
        self.write("concepts.json", concepts)
        errors = self.script("validate_study.py").stderr
        self.assertIn("duplicates a functional mechanism", errors)
        self.assertIn("boundary violation", errors)
        criteria[0]["requirement"] += " Materially different requirement."
        self.write("fit_criteria.json", criteria)
        self.assertIn("comparison basis is stale", self.script("validate_study.py").stderr)
