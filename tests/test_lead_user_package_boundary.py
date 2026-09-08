import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "lead-user-research"
PACKAGED = ROOT / "skills" / "lead-user-research"


class LeadUserPackageBoundaryTests(unittest.TestCase):
    def read(self, relative: str, packaged: bool = False) -> str:
        base = PACKAGED if packaged else CANONICAL
        return (base / relative).read_text(encoding="utf-8")

    def assert_mirrored(self, relative: str) -> str:
        canonical = self.read(relative)
        packaged = self.read(relative, packaged=True)
        self.assertEqual(canonical, packaged)
        return canonical

    def test_boundary_document_is_packaged_byte_identically(self):
        canonical = self.assert_mirrored("PACKAGE_BOUNDARY.md")
        self.assertIn("research-local concept probes", canonical)
        self.assertIn("research-to-planning-v1", canonical)
        self.assertIn("LUR:<workspace>:R3", canonical)
        self.assertIn("Phase F material", canonical)

    def test_phase_f_states_do_not_claim_planning_authority(self):
        prompt = self.assert_mirrored("prompts/phase-f-shape.md")
        self.assertIn("research-local concept-shaping exercise", prompt)
        self.assertIn("not an accepted planning frame", prompt)
        self.assertIn("not a selected project shape", prompt)
        self.assertIn("do not automatically own the project's `R##` namespace", prompt)
        self.assertIn("does not authorize a project shape or implementation", prompt)

    def test_phase_handoff_reuses_phase_f_without_bypassing_gates(self):
        handoff = self.assert_mirrored("references/phase-handoff.md")
        self.assertIn("E-only evidence normally routes to `framing-doc`", handoff)
        self.assertIn("Phase F material normally routes directly to collaborative `shaping`", handoff)
        self.assertIn("as **Working**", handoff)
        self.assertIn("Do not ask the human to recreate or reselect Phase F material", handoff)

    def test_research_to_planning_handoff_preserves_namespaced_lineage(self):
        template = self.assert_mirrored("study-templates/research-to-frame-handoff.md")
        self.assertIn("Contract: `research-to-planning-v1`", template)
        self.assertIn("`LUR:<workspace>:R##`", template)
        self.assertIn("existing project R## / new Working R## / do not carry", template)
        self.assertIn("Phase F material = PRESENT and useful", template)
        self.assertIn("invoke `shaping` in collaborative mode", template)

    def test_decision_prompt_labels_phase_f_state_as_research_local(self):
        prompt = self.assert_mirrored("prompts/phase-g-decide.md")
        self.assertIn("human research-selection provenance", prompt)
        self.assertIn("states are research-local under `PACKAGE_BOUNDARY.md`", prompt)
        self.assertIn("not accepted product requirements", prompt)
        self.assertIn("not a selected project shape", prompt)

    def test_canonical_skill_routes_phase_f_handoff_to_working_shaping(self):
        skill = self.assert_mirrored("SKILL.md")
        self.assertIn("Read [PACKAGE_BOUNDARY.md](PACKAGE_BOUNDARY.md)", skill)
        self.assertIn("Phase F is research-local concept shaping", skill)
        self.assertIn("route directly to collaborative `shaping`", skill)
        self.assertIn("**Working** planning material", skill)
        self.assertIn("An accepted research concept-evaluation frame precedes PASS research-local fit criteria", skill)

    def test_human_readme_explains_conditional_downstream_route(self):
        readme = self.assert_mirrored("README.md")
        self.assertIn("research-to-planning handoff", readme)
        self.assertIn("if Phase F did not produce useful planning material", readme)
        self.assertIn("route directly to collaborative `shaping`", readme)
        self.assertIn("namespaced research provenance", readme)


if __name__ == "__main__":
    unittest.main()
