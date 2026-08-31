from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "lead-user-research"
MIRROR = ROOT / "skills" / "lead-user-research"


class LeadUserHybridSafeguardTests(unittest.TestCase):
    def test_web_need_solution_and_signal_boundary_are_explicit(self):
        phase = (CANONICAL / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        protocol = (CANONICAL / "PROTOCOL.md").read_text(encoding="utf-8")
        for value in ("WEB_NEED_SOLUTION", "DISCOVERY_SIGNAL", "search/post frequency"):
            self.assertIn(value, phase)
        self.assertIn("Discovery signals versus decision evidence", protocol)
        self.assertIn("do not by themselves establish LU1/LU2", protocol)

    def test_branch_independence_and_enabler_scan_are_explicit(self):
        phase = (CANONICAL / "prompts" / "phase-b-discover.md").read_text(encoding="utf-8")
        freeze = (CANONICAL / "prompts" / "phase-d-freeze.md").read_text(encoding="utf-8")
        contract = (CANONICAL / "references" / "state-contract.md").read_text(encoding="utf-8")
        self.assertIn("branch_independence", phase)
        self.assertIn("meaningfully independent discovery branches", freeze)
        self.assertIn("ENABLER_SCAN", phase)
        self.assertIn("NONHUMAN_CONTEXT", phase)
        self.assertIn("branch_independence", contract)

    def test_transferability_is_a_hard_concept_gate(self):
        phase = (CANONICAL / "prompts" / "phase-f-shape.md").read_text(encoding="utf-8")
        validator = (CANONICAL / "scripts" / "validate_study.py").read_text(encoding="utf-8")
        contract = (CANONICAL / "references" / "state-contract.md").read_text(encoding="utf-8")
        for text in (phase, validator, contract):
            self.assertIn("transferability_supported", text)
        self.assertIn("PASS requires transferability SUPPORTED or PLAUSIBLE", validator)

    def test_layer_preserving_rejection_is_explicit(self):
        phase = (CANONICAL / "prompts" / "phase-f-shape.md").read_text(encoding="utf-8")
        handoff = (CANONICAL / "study-templates" / "research-to-frame-handoff.md").read_text(encoding="utf-8")
        validator = (CANONICAL / "scripts" / "validate_study.py").read_text(encoding="utf-8")
        self.assertIn("reject mechanism ≠ reject requirement ≠ reject need", phase)
        self.assertIn("reject mechanism ≠ reject requirement ≠ reject need", handoff)
        self.assertIn("REJECTION_LAYER", validator)

    def test_packaged_mirror_matches_changed_canonical_files(self):
        for relative in (
            Path("README.md"),
            Path("SKILL.md"),
            Path("PROTOCOL.md"),
            Path("PORTABLE_PROMPT.md"),
            Path("prompts/phase-b-discover.md"),
            Path("prompts/phase-c-evidence.md"),
            Path("prompts/phase-d-freeze.md"),
            Path("prompts/phase-e-interpret.md"),
            Path("prompts/phase-f-shape.md"),
            Path("prompts/phase-g-decide.md"),
            Path("references/state-contract.md"),
            Path("scripts/validate_study.py"),
            Path("examples/reference-study/needs.json"),
            Path("study-templates/research-to-frame-handoff.md"),
        ):
            self.assertEqual(
                (CANONICAL / relative).read_bytes(),
                (MIRROR / relative).read_bytes(),
                f"packaged Lead User mirror drifted for {relative}",
            )


if __name__ == "__main__":
    unittest.main()
