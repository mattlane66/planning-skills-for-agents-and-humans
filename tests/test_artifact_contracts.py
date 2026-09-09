import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_planning_artifact import (  # noqa: E402
    load_contracts,
    validate_artifact_text,
    validate_contract_definitions,
)


class ArtifactContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contracts = load_contracts(ROOT / "contracts" / "artifact-contracts.yaml")

    def test_contract_definitions_match_repository_templates(self) -> None:
        self.assertEqual([], validate_contract_definitions(self.contracts, ROOT))

    def test_context_packet_requires_filled_execution_contract(self) -> None:
        template = (ROOT / "templates" / "context-packet.md").read_text(encoding="utf-8")
        errors = validate_artifact_text("context_packet", template, self.contracts)
        self.assertTrue(any("Goal condition" in error for error in errors), errors)
        self.assertTrue(any("Required checks" in error for error in errors), errors)

        completed = template
        replacements = {
            "- Goal condition:": "- Goal condition: selected slice behaves as accepted",
            "- Required checks:": "- Required checks: unit and integration tests",
            "- Allowed files / areas:": "- Allowed files / areas: src/checkout and tests/checkout",
            "- Out-of-scope changes:": "- Out-of-scope changes: authentication and billing",
            "- Return-to-planning conditions:": "- Return-to-planning conditions: accepted behavior is missing or contradicted",
        }
        for source, target in replacements.items():
            completed = completed.replace(source, target)
        self.assertEqual([], validate_artifact_text("context_packet", completed, self.contracts))

    def test_selected_design_breadboard_requires_accepted_authority(self) -> None:
        template = (ROOT / "templates" / "breadboard.md").read_text(encoding="utf-8")
        errors = validate_artifact_text("selected_design_breadboard", template, self.contracts)
        self.assertTrue(any("mode must be selected-design" in error for error in errors), errors)
        self.assertTrue(any("Requirements authority must be Accepted" in error for error in errors), errors)

        completed = template.replace("source_of_truth: false", "source_of_truth: true")
        completed = completed.replace(
            "- Mode: `current-state`, `candidate-shape`, or `selected-design`",
            "- Mode: `selected-design`",
        )
        completed = completed.replace(
            "- Requirements authority: `Working` | `Accepted` | `Not applicable`",
            "- Requirements authority: `Accepted`",
        )
        completed = completed.replace(
            "- Appetite authority: `Unset` | `Working` | `Accepted` | `Not applicable`",
            "- Appetite authority: `Accepted`",
        )
        completed = completed.replace(
            "- Candidate or selected shape:", "- Candidate or selected shape: Shape B"
        )
        completed = completed.replace(
            "- Reconciliation status for selected-design mode:",
            "- Reconciliation status for selected-design mode: accepted",
        )
        self.assertEqual(
            [], validate_artifact_text("selected_design_breadboard", completed, self.contracts)
        )

    def test_selected_shaping_requires_recorded_selection(self) -> None:
        template = (ROOT / "templates" / "shaping.md").read_text(encoding="utf-8")
        errors = validate_artifact_text("selected_shaping", template, self.contracts)
        self.assertTrue(any("Decision status must be selected" in error for error in errors), errors)

        completed = template.replace(
            "- Authority: Unset | Working | Accepted", "- Authority: Accepted"
        )
        completed = completed.replace(
            "- Status: exploring | decision-ready | selected | stopped", "- Status: selected"
        )
        completed = completed.replace("- Chosen direction:", "- Chosen direction: Shape B")
        self.assertEqual([], validate_artifact_text("selected_shaping", completed, self.contracts))

    def test_dumplink_requires_boundary_and_task_group(self) -> None:
        template = (ROOT / "templates" / "dumplink.md").read_text(encoding="utf-8")
        errors = validate_artifact_text("dumplink", template, self.contracts)
        self.assertTrue(any("Selected project" in error for error in errors), errors)
        self.assertTrue(any("TG##" in error for error in errors), errors)

        completed = template.replace("- Selected project:", "- Selected project: Checkout retry")
        completed = completed.replace("- Appetite:", "- Appetite: 2 weeks")
        completed = completed.replace(
            "- Project boundary:", "- Project boundary: retry failed checkout submission only"
        )
        completed = completed.replace(
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| --- | --- | --- | --- | --- | --- | --- |\n| TG1 | Retry path | T1, T2 | Failed checkout can be retried | known | no | — |",
            1,
        )
        self.assertEqual([], validate_artifact_text("dumplink", completed, self.contracts))

    def test_unknown_artifact_type_fails_closed(self) -> None:
        self.assertEqual(
            ["unknown artifact type: imaginary"],
            validate_artifact_text("imaginary", "# anything", self.contracts),
        )


if __name__ == "__main__":
    unittest.main()
