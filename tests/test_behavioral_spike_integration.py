"""Contract checks for optional Behavioral Simulation spikes in shaping.

These verify the integration boundaries, not the predictive validity of a simulation.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BehavioralSpikeIntegrationTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_packaged_mirrors_remain_identical(self):
        for path in (
            "shaping/SKILL.md",
            "shaping/references/fit-checks.md",
            "planning-router/SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.read(path), self.read("skills/" + path))

    def test_shaping_spike_is_optional_and_subordinate(self):
        shaping = self.read("shaping/SKILL.md")
        for required in (
            "### Optional behavioral spikes",
            "value and usability",
            "not a required stage",
            "PLAUSIBILITY_SPACE / L0_ROLEPLAY",
            "OBSERVED_HUMAN",
            "SIMULATED_ESTIMATE",
            "No simulated result automatically converts",
            "human selection gates remain unchanged",
        ):
            with self.subTest(required=required):
                self.assertIn(required, shaping)

    def test_router_chooses_existing_spike_without_mandating_simulation(self):
        router = self.read("planning-router/SKILL.md")
        for required in (
            "optional behavioral focused spike",
            "single optional shaping spike",
            "real-world observation/testing",
            "Do not force a behavioral spike",
        ):
            self.assertIn(required, router)

    def test_fit_check_does_not_promote_simulation_to_pass(self):
        fit = self.read("shaping/references/fit-checks.md")
        for required in (
            "Behavioral simulation is not a Fit Check",
            "not population predictions",
            "SIMULATED_ESTIMATE",
            "OBSERVED_HUMAN",
            "cannot independently convert an unknown",
            "human selection",
        ):
            self.assertIn(required, fit)

    def test_templates_preserve_evidence_type_and_next_test(self):
        spike = self.read("templates/spike.md")
        shaping = self.read("templates/shaping.md")
        self.assertIn("Behavioral simulation (optional)", spike)
        for tag in ("OBSERVED_HUMAN", "ASSUMPTION", "SIMULATED_ESTIMATE"):
            self.assertIn(tag, spike)
        self.assertIn("Smallest real-world test", spike)
        self.assertIn("SIMULATED_ESTIMATE", shaping)

    def test_example_does_not_pretend_to_have_results(self):
        example = self.read("examples/behavioral-spike/README.md")
        self.assertIn("not a completed simulation", example)
        self.assertIn("NOT simulation results", example)
        self.assertIn("Discriminating real-world observation", example)


if __name__ == "__main__":
    unittest.main()
