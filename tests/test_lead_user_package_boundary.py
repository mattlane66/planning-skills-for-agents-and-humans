import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "lead-user-research"
PACKAGED = ROOT / "skills" / "lead-user-research"


class LeadUserPackageBoundaryTests(unittest.TestCase):
    def read(self, relative: str, packaged: bool = False) -> str:
        base = PACKAGED if packaged else CANONICAL
        return (base / relative).read_text(encoding="utf-8")

    def test_boundary_document_is_packaged_byte_identically(self):
        canonical = self.read("PACKAGE_BOUNDARY.md")
        packaged = self.read("PACKAGE_BOUNDARY.md", packaged=True)
        self.assertEqual(canonical, packaged)
        self.assertIn("research-local concept probes", canonical)
        self.assertIn("research-to-planning-v1", canonical)
        self.assertIn("LUR:<workspace>:R3", canonical)
        self.assertIn("Phase F material", canonical)

    def test_phase_f_states_do_not_claim_planning_authority(self):
        prompt = self.read("prompts/phase-f-shape.md")
        packaged = self.read("prompts/phase-f-shape.md", packaged=True)
        self.assertEqual(prompt, packaged)
        self.assertIn("research-local concept-shaping exercise", prompt)
        self.assertIn("not an accepted planning frame", prompt)
        self.assertIn("not a selected project shape", prompt)
        self.assertIn("do not automatically own the project's `R##` namespace", prompt)
        self.assertIn("does not authorize a project shape or implementation", prompt)

    def test_phase_handoff_reuses_phase_f_without_bypassing_gates(self):
        handoff = self.read("references/phase-handoff.md")
        packaged = self.read("references/phase-handoff.md", packaged=True)
        self.assertEqual(handoff, packaged)
        self.assertIn("E-only evidence normally routes to `framing-doc`", handoff)
        self.assertIn("Phase F material normally routes directly to collaborative `shaping`", handoff)
        self.assertIn("as **Working**", handoff)
        self.assertIn("Do not ask the human to recreate or reselect Phase F material", handoff)

    def test_research_to_planning_handoff_preserves_namespaced_lineage(self):
        template = self.read("study-templates/research-to-frame-handoff.md")
        packaged = self.read("study-templates/research-to-frame-handoff.md", packaged=True)
        self.assertEqual(template, packaged)
        self.assertIn("Contract: `research-to-planning-v1`", template)
        self.assertIn("`LUR:<workspace>:R##`", template)
        self.assertIn("existing project R## / new Working R## / do not carry", template)
        self.assertIn("Phase F material = PRESENT and useful", template)
        self.assertIn("invoke `shaping` in collaborative mode", template)

    def test_decision_prompt_labels_phase_f_state_as_research_local(self):
        prompt = self.read("prompts/phase-g-decide.md")
        packaged = self.read("prompts/phase-g-decide.md", packaged=True)
        self.assertEqual(prompt, packaged)
        self.assertIn("human research-selection provenance", prompt)
        self.assertIn("states are research-local under `PACKAGE_BOUNDARY.md`", prompt)
        self.assertIn("not accepted product requirements", prompt)
        self.assertIn("not a selected project shape", prompt)


if __name__ == "__main__":
    unittest.main()
