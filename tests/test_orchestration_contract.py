import pathlib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


class OrchestrationScopeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = yaml.safe_load(
            (ROOT / ".agent-orchestration.yaml").read_text(encoding="utf-8")
        )

    def test_active_scope_has_two_explicit_sources(self) -> None:
        active_scope = self.manifest["scope_contract"]["active_scope"]
        self.assertEqual(
            ["selected_slice", "selected_dumplink_task_group"],
            active_scope["valid_sources"],
        )
        self.assertIn("explicit_human_selection_required", active_scope["rules"])
        self.assertIn("exactly_one_active_scope", active_scope["rules"])

    def test_build_and_supporting_modes_use_the_canonical_scope_name(self) -> None:
        self.assertEqual(
            ["active_scope", "context_packet", "execution_contract"],
            self.manifest["hard_promotion_gates"]["build"],
        )
        for mode in ("interface_contract", "executable_breadboard", "kickoff", "feed_context", "build"):
            self.assertIn("active_scope", self.manifest["modes"][mode]["requires"], mode)
            self.assertNotIn("selected_slice", self.manifest["modes"][mode]["requires"], mode)

    def test_authority_order_names_active_scope_once(self) -> None:
        authority_order = self.manifest["authority_order"]
        self.assertEqual(1, authority_order.count("active_scope"))
        self.assertNotIn("selected_slice", authority_order)
        self.assertNotIn("selected_dumplink_task_group", authority_order)


if __name__ == "__main__":
    unittest.main()
