import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "publish_shaped_work.py"
EXAMPLE = ROOT / "examples" / "simple-grocery-list"

spec = importlib.util.spec_from_file_location("publish_shaped_work", SCRIPT)
publisher = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(publisher)


class PlanningPublisherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = publisher.build_package(EXAMPLE)

    def test_example_compiles_into_normalized_package(self):
        package = self.package
        self.assertEqual("PlanningPackage", package["kind"])
        self.assertEqual(1, package["schema_version"])
        self.assertEqual("Simple Grocery List", package["title"])
        self.assertEqual(6, len(package["shaping"]["requirements"]))
        self.assertEqual({"A", "B"}, {shape["id"] for shape in package["shaping"]["shapes"]})
        self.assertEqual("A", package["shaping"]["selected_shape"])
        self.assertEqual("selected-design", package["breadboard"]["mode"])
        self.assertEqual("V1", package["breadboard"]["active_slice"])
        self.assertEqual("Accepted", package["authority"]["requirements"])
        self.assertEqual("Selected", package["authority"]["shape"])

    def test_visual_is_derived_from_canonical_ids_and_self_contained(self):
        rendered = publisher.render_html(self.package)
        for planning_id in ("R0", "A1", "P1", "U1", "N1", "S1", "V1"):
            self.assertIn(f'data-plan-id="{planning_id}"', rendered)
        self.assertIn('type="application/json" id="planning-package"', rendered)
        self.assertIn("Composite shape board", rendered)
        self.assertIn("System rail", rendered)
        self.assertNotIn("<script src=", rendered)
        self.assertNotIn("<link rel=", rendered)

    def test_presentation_spec_cannot_invent_planning_truth(self):
        with self.assertRaisesRegex(publisher.PublisherError, "absent from canonical"):
            publisher.validate_presentation(
                self.package,
                {
                    "schema_version": 1,
                    "hero_place": "P999",
                    "annotations": [{"ref": "A999", "text": "invented"}],
                },
            )

    def test_cli_can_emit_html_and_machine_readable_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = pathlib.Path(temporary) / "shaped-work.html"
            data = pathlib.Path(temporary) / "planning-package.json"
            status = publisher.main(
                [
                    "--planning-dir",
                    str(EXAMPLE),
                    "--output",
                    str(out),
                    "--json-output",
                    str(data),
                ]
            )
            self.assertEqual(0, status)
            self.assertTrue(out.is_file())
            payload = json.loads(data.read_text(encoding="utf-8"))
            self.assertEqual("A", payload["shaping"]["selected_shape"])
            self.assertEqual("P1", payload["presentation"]["hero_place"])


if __name__ == "__main__":
    unittest.main()
