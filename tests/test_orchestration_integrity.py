import copy
import pathlib
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from orchestration_integrity import (  # noqa: E402
    load_yaml_unique,
    validate_execution_graph,
    validate_gate_definitions,
    validate_id_contract,
    validate_manifest_references,
    validate_repository,
)


class OrchestrationIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orchestration = load_yaml_unique(ROOT / ".agent-orchestration.yaml")
        cls.contract = load_yaml_unique(ROOT / "contracts" / "planning-integrity.yaml")
        cls.graph = load_yaml_unique(ROOT / "templates" / "execution-graph.yaml")
        cls.stable_ids = (ROOT / "docs" / "stable-ids.md").read_text(encoding="utf-8")

    def test_repository_contract_passes(self) -> None:
        self.assertEqual([], validate_repository(ROOT))

    def test_duplicate_yaml_mapping_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "duplicate.yaml"
            path.write_text("nodes:\n  TG1: {}\n  TG1: {}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate YAML mapping key"):
                load_yaml_unique(path)

    def test_every_hard_promotion_gate_token_must_be_defined(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["gate_definitions"].pop("explicit_human_selection")
        errors = validate_gate_definitions(self.orchestration, contract)
        self.assertTrue(
            any("explicit_human_selection" in error and "missing definitions" in error for error in errors),
            errors,
        )

    def test_id_collisions_must_match_the_declared_namespaces(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["id_namespaces"]["lead_user_study"]["collisions_with_planning"].remove("N")
        errors = validate_id_contract(contract, self.stable_ids)
        self.assertTrue(any("collision declaration mismatch" in error for error in errors), errors)

    def test_human_readable_planning_id_table_must_match_contract(self) -> None:
        changed_docs = self.stable_ids.replace(
            "| `TG` | task group | `TG2` |",
            "| `TG` | task batch | `TG2` |",
        )
        errors = validate_id_contract(self.contract, changed_docs)
        self.assertIn(
            "docs/stable-ids.md planning defaults do not match the machine-readable ID contract",
            errors,
        )

    def test_orchestration_artifact_references_must_exist(self) -> None:
        orchestration = copy.deepcopy(self.orchestration)
        orchestration["artifacts"]["execution_graph"] = "templates/does-not-exist.yaml"
        errors = validate_manifest_references(ROOT, orchestration, self.contract)
        self.assertTrue(any("templates/does-not-exist.yaml" in error for error in errors), errors)

    def test_execution_graph_rejects_missing_dependency_reference(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["nodes"]["TG2"]["depends_on"] = ["TG404"]
        errors = validate_execution_graph(graph, self.contract)
        self.assertTrue(any("depends on missing node 'TG404'" in error for error in errors), errors)

    def test_execution_graph_rejects_dependency_cycles(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["nodes"]["TG1"]["depends_on"] = ["TG2"]
        graph["edges"].append({"from": "TG2", "to": "TG1", "reason": None})
        errors = validate_execution_graph(graph, self.contract)
        self.assertTrue(any("dependency cycle" in error for error in errors), errors)

    def test_execution_graph_dependencies_and_edges_must_agree(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["edges"] = []
        errors = validate_execution_graph(graph, self.contract)
        self.assertTrue(any("edges do not match" in error for error in errors), errors)

    def test_runtime_state_is_disjoint_and_bounded(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["runtime_state"]["active"] = ["TG1", "TG2"]
        graph["runtime_state"]["ready"] = ["TG1"]
        errors = validate_execution_graph(graph, self.contract)
        self.assertTrue(any("appears in both active and ready" in error for error in errors), errors)
        self.assertTrue(any("max_active_groups is 1" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
