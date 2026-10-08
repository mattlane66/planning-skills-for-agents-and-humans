"""Integrated publisher, binding discovery, and behavioral regression tests."""
import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

publisher = load("product_intent_publisher", ROOT/"scripts"/"publish_shaped_work.py")
mapping = load("product_intent_mapper", ROOT/"product-intent"/"mapping.py")
behaviors = load("product_intent_behaviors", ROOT/"product-intent"/"behaviors.py")

def overlay(refs=("R0","U1"), bindings=None):
    return {
        "schema_version": 1, "product": "Grocery List", "records": [
            {"id": "INV-1", "kind": "invariant", "title": "Preserve saved list",
             "status": "accepted", "statement": "Editing an item does not erase the saved list",
             "approved_by": "Human reviewer", "approved_at": "2026-10-07",
             "refs": list(refs), "evidence": ["Accepted selected-design behavior"],
             "verification": ["An edit leaves saved entries unchanged"]},
            {"id":"DEC-1", "kind":"decision", "title":"Use explicit saves",
             "status":"accepted", "statement":"Use explicit persistence rather than silent replacement.",
             "approved_by":"Human reviewer", "approved_at":"2026-10-07",
             "refs":["INV-1"], "evidence":["Human tradeoff review"],
             "alternatives":[
                 {"name":"Automatic overwrites", "disposition":"rejected", "reason":"Could erase unsaved work"},
                 {"name":"Explicit save", "disposition":"chosen", "reason":"Preserves user control"}
             ]}
        ],
        "bindings": bindings or [
            {"intent_id":"INV-1","paths":["src/grocery/**"],
             "symbols":["edit_grocery_item"], "tests":["tests/test_grocery.py"],
             "confidence":"inferred","evidence":["Code identifier match"]}
        ]
    }

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = pathlib.Path(self.tmp.name)/"planning"
        shutil.copytree(ROOT/"examples"/"simple-grocery-list", self.directory)
        self.file = self.directory/"product-intent.json"
        self.write_overlay(overlay())

    def write_overlay(self, value):
        self.file.write_text(json.dumps(value, indent=2), encoding="utf-8")

    def test_publisher_embeds_typed_and_linked_model(self):
        package = publisher.build_package(self.directory)
        model = package["product_intent"]
        self.assertEqual("ProductIntentModel", model["kind"])
        self.assertEqual("INV-1", model["extension_records"][0]["id"])
        self.assertIn("requirement:R0", model["extension_records"][0]["resolved_refs"])
        self.assertIn("affordance:U1", model["extension_records"][0]["resolved_refs"])
        self.assertEqual("extension:INV-1", model["bindings"][0]["resolved_intent_uid"])
        self.assertEqual(64, len(model["content_sha256"]))
        self.assertIn("product_intent", publisher.render_html(package))

    def test_missing_or_working_intent_cannot_be_accepted(self):
        value = overlay(refs=("R999",))
        self.write_overlay(value)
        with self.assertRaisesRegex(publisher.PublisherError, "unknown intent ref"):
            publisher.build_package(self.directory)
        value = overlay(refs=("shape:B",))
        self.write_overlay(value)
        with self.assertRaisesRegex(publisher.PublisherError, "unaccepted"):
            publisher.build_package(self.directory)

    def test_bare_unknown_binding_is_rejected(self):
        value = overlay(bindings=[{"intent_id":"requirement:R999", "paths":["src/**"],
                                   "confidence":"inferred"}])
        self.write_overlay(value)
        with self.assertRaisesRegex(publisher.PublisherError, "missing or ambiguous"):
            publisher.build_package(self.directory)

    def test_typed_canonical_binding_resolves(self):
        value = overlay(bindings=[{"intent_id":"requirement:R0", "paths":["src/**"],
                                   "confidence":"inferred"}])
        self.write_overlay(value)
        package = publisher.build_package(self.directory)
        self.assertEqual("requirement:R0",package["product_intent"]["bindings"][0]["resolved_intent_uid"])

    def test_model_without_extension_remains_backward_compatible(self):
        self.file.unlink()
        self.assertNotIn("product_intent", publisher.build_package(self.directory))

    def test_binding_proposals_have_symbol_evidence_only(self):
        root = pathlib.Path(self.tmp.name)/"code"
        (root/"src"/"grocery").mkdir(parents=True)
        (root/"src"/"grocery"/"items.py").write_text(
            "def preserve_saved_list(item):\n    return item\n", encoding="utf-8")
        package = publisher.build_package(self.directory)
        report = mapping.propose(package, root)
        proposals = [p for p in report["proposals"] if p["intent_id"]=="INV-1"]
        self.assertTrue(proposals, report)
        self.assertTrue(all(p["requires_review"] and p["confidence"]=="inferred" for p in proposals))
        self.assertEqual("python_ast", proposals[0]["evidence"]["parser"])

class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.app = self.root/"profile.py"
        self.app.write_text(
            "def update_profile(saved, draft, save_succeeded):\n"
            "    return draft if save_succeeded else saved\n",
            encoding="utf-8")
        self.manifest = {
            "schema_version":1,"scenarios":[
                {"id":"SC-1","adapter":"python_function","module":"profile.py",
                 "function":"update_profile","intent_ids":["INV-1"],
                 "cases":[
                     {"id":"failed-save","args":[{"name":"Old"},{"name":"New"},False],
                      "expected":{"name":"Old"}},
                     {"id":"successful-save","args":[{"name":"Old"},{"name":"New"},True],
                      "expected":{"name":"New"}}
                 ]}
            ]
        }

    def test_real_product_behavior_passes(self):
        result=behaviors.verify(self.manifest,self.root,["INV-1"])
        self.assertEqual("PASS",result["verdict"])
        self.assertEqual(["PASS","PASS"],[r["status"] for r in result["results"]])

    def test_deliberate_behavior_regression_detected(self):
        self.app.write_text(
            "def update_profile(saved, draft, save_succeeded):\n"
            "    return draft\n", encoding="utf-8")
        result=behaviors.verify(self.manifest,self.root,["INV-1"])
        self.assertEqual("DRIFT",result["verdict"])
        self.assertEqual("DRIFT",result["results"][0]["status"])

    def test_incomplete_coverage_needs_review(self):
        result=behaviors.verify(self.manifest,self.root,["INV-1","INV-2"])
        self.assertEqual("REVIEW",result["verdict"])
        self.assertEqual(["INV-2"],result["uncovered_intent_ids"])

    def test_untrusted_path_is_rejected(self):
        manifest=copy.deepcopy(self.manifest)
        manifest["scenarios"][0]["module"]="../outside.py"
        with self.assertRaisesRegex(ValueError,"escapes code root"):
            behaviors.verify(manifest,self.root)

    def test_empty_manifest_is_rejected(self):
        with self.assertRaises(ValueError):
            behaviors.verify({"schema_version":1,"scenarios":[]},self.root)

if __name__=="__main__":
    unittest.main()
