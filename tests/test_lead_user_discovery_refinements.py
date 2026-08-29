from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "lead-user-research"
MIRROR = ROOT / "skills" / "lead-user-research"


class LeadUserDiscoveryRefinementTests(unittest.TestCase):
    def test_phase_b_requires_all_three_discovery_paths(self):
        text = (CANONICAL / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        for value in ("TARGET_MARKET", "ADVANCED_ANALOG", "ATTRIBUTE_SPECIFIC"):
            self.assertIn(value, text)
        self.assertIn("specific important attribute", text)
        self.assertIn("not merely another whole-problem analogy", text)

    def test_pyramiding_contract_is_attribute_specific_and_auditable(self):
        phase = (CANONICAL / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        contract = (CANONICAL / "references" / "state-contract.md").read_text(encoding="utf-8")
        required = (
            "pyramid_id",
            "target_attribute",
            "starting_node",
            "referral_rationale",
            "next_node",
            "advancement_rationale",
            "network_visibility",
            "termination_criterion",
            "termination_reason",
        )
        for value in required:
            self.assertIn(value, phase)
            self.assertIn(value, contract)
        self.assertIn("better information about who does", phase)
        self.assertIn("never a qualification criterion", phase)

    def test_candidate_enrichment_cannot_substitute_for_lu_qualification(self):
        phase = (CANONICAL / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        contract = (CANONICAL / "references" / "state-contract.md").read_text(encoding="utf-8")
        for value in ("technical_expertise", "community_resources"):
            self.assertIn(value, phase)
            self.assertIn(value, contract)
        self.assertIn("do not establish LU1 or LU2", phase)
        self.assertIn("must never compensate for missing LU1/LU2 evidence", phase)
        self.assertIn("does not establish LU1", contract)
        self.assertIn("does not establish LU2", contract)

    def test_packaged_mirror_matches_changed_canonical_files(self):
        for relative in (
            Path("prompts/phase-b-discover.md"),
            Path("references/state-contract.md"),
        ):
            self.assertEqual(
                (CANONICAL / relative).read_bytes(),
                (MIRROR / relative).read_bytes(),
                f"packaged Lead User mirror drifted for {relative}",
            )


if __name__ == "__main__":
    unittest.main()
