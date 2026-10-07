import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "simple-grocery-list"

spec = importlib.util.spec_from_file_location("product_intent", ROOT / "scripts" / "product_intent.py")
product_intent = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(product_intent)

drift_spec = importlib.util.spec_from_file_location("check_intent_drift", ROOT / "scripts" / "check_intent_drift.py")
check_intent_drift = importlib.util.module_from_spec(drift_spec)
assert drift_spec.loader is not None
drift_spec.loader.exec_module(check_intent_drift)


class ProductIntentTests(unittest.TestCase):
    def test_existing_example_compiles(self):
        model = product_intent.compile_model(EXAMPLE)
        self.assertEqual("ProductIntentModel", model["kind"])
        self.assertEqual(1, model["schema_version"])
        self.assertEqual("A", model["selected_design"]["shape"])
        self.assertEqual(6, len(model["requirements"]))
        self.assertEqual("DEC1", model["decisions"][0]["id"])
        self.assertIn("B", model["decisions"][0]["rejected"])
        self.assertEqual([], model["invariants"])
        self.assertEqual([], model["implementation_bindings"])

    def test_invariants_and_bindings_join_through_stable_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary)
            for source in EXAMPLE.iterdir():
                if source.is_file():
                    shutil.copy2(source, target / source.name)

            breadboard = target / "03-breadboard.md"
            text = breadboard.read_text(encoding="utf-8")
            marker = "## Places"
            invariant = (
                "## Product invariants — selected-design mode\n\n"
                "| ID | Invariant | Severity | Protects | Reopen when | Verification |\n"
                "|---|---|---|---|---|---|\n"
                "| INV1 | Saved items survive reload. | must | R3, S1 | Product intentionally becomes session-only. | RUN1 |\n\n"
            )
            breadboard.write_text(text.replace(marker, invariant + marker), encoding="utf-8")

            (target / "implementation-bindings.json").write_text(
                json.dumps({
                    "schema_version": 1,
                    "bindings": [{
                        "id": "BIND1",
                        "intent_refs": ["R3", "S1", "INV1"],
                        "paths": ["src/items/**"],
                        "symbols": ["itemsStore"],
                        "tests": ["tests/items.spec.ts"],
                        "notes": "Persistence path"
                    }]
                }),
                encoding="utf-8",
            )

            model = product_intent.compile_model(target)
            self.assertEqual("INV1", model["invariants"][0]["id"])
            self.assertEqual(["R3", "S1"], model["invariants"][0]["protects"])
            self.assertEqual("BIND1", model["implementation_bindings"][0]["id"])
            self.assertIn("INV1", model["implementation_bindings"][0]["intent_refs"])

    def test_unknown_binding_ref_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary)
            for source in EXAMPLE.iterdir():
                if source.is_file():
                    shutil.copy2(source, target / source.name)
            (target / "implementation-bindings.json").write_text(
                json.dumps({
                    "schema_version": 1,
                    "bindings": [{
                        "id": "BIND1",
                        "intent_refs": ["R999"],
                        "paths": ["src/**"]
                    }]
                }),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(product_intent.ProductIntentError, "unknown intent refs"):
                product_intent.compile_model(target)

    def test_path_binding_supports_globs(self):
        self.assertTrue(check_intent_drift.matches("src/profile/EditForm.tsx", "src/profile/**"))
        self.assertTrue(check_intent_drift.matches("src/profile/EditForm.tsx", "src/profile/EditForm.tsx"))
        self.assertFalse(check_intent_drift.matches("src/cart/Cart.tsx", "src/profile/**"))

    def test_schema_is_valid_json_and_names_model(self):
        payload = json.loads((ROOT / "product-intent" / "schema.json").read_text(encoding="utf-8"))
        self.assertEqual("ProductIntentModel", payload["title"])
        self.assertEqual("ProductIntentModel", payload["properties"]["kind"]["const"])


if __name__ == "__main__":
    unittest.main()
