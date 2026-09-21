import copy
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
        self.assertEqual(2, package["schema_version"])
        self.assertEqual("Simple Grocery List", package["title"])
        self.assertEqual(6, len(package["shaping"]["requirements"]))
        self.assertEqual({"A", "B"}, {shape["id"] for shape in package["shaping"]["shapes"]})
        self.assertEqual("A", package["shaping"]["selected_shape"])
        self.assertEqual("selected-design", package["breadboard"]["mode"])
        self.assertEqual("V1", package["breadboard"]["active_slice"])
        self.assertEqual("Accepted", package["authority"]["requirements"])
        self.assertEqual("Selected", package["authority"]["shape"])
        self.assertEqual("01-frame.md", package["sources"]["frame"])
        self.assertEqual("02-shaping.md", package["sources"]["shaping"])
        self.assertEqual("03-breadboard.md", package["sources"]["breadboard"])
        self.assertEqual(2, package["presentation"]["schema_version"])
        self.assertIn("visual_hints", package["presentation"])
        self.assertIn("slice_scopes", package["presentation"])
        self.assertIn("P1", package["presentation"]["visual_hints"])
        self.assertIn("V1", package["presentation"]["slice_scopes"])

    def test_visual_is_derived_from_canonical_ids_and_self_contained(self):
        rendered = publisher.render_html(self.package)
        for planning_id in ("R0", "A1", "P1", "U1", "N1", "S1", "V1"):
            self.assertIn(f'data-plan-id="{planning_id}"', rendered)
        self.assertIn('type="application/json" id="planning-package"', rendered)
        self.assertIn("Composite shape board", rendered)
        self.assertIn("System rail", rendered)
        self.assertIn("Slice views", rendered)
        self.assertIn("Selected build scope", rendered)
        self.assertIn("Unselected candidate · collapsed by default", rendered)
        self.assertIn("Accepted selected-design", rendered)
        self.assertIn('data-scope="V1"', rendered)
        self.assertNotIn("<script src=", rendered)
        self.assertNotIn("<link rel=", rendered)

    def test_working_material_is_not_visually_promoted(self):
        package = copy.deepcopy(self.package)
        package["shaping"]["selected_shape"] = ""
        for shape in package["shaping"]["shapes"]:
            shape["selected"] = False
        package["breadboard"]["mode"] = "candidate-shape"
        package["presentation"] = publisher.default_presentation(package)
        self.assertEqual([], package["presentation"]["annotations"])
        rendered = publisher.render_html(package)
        self.assertIn("No human-selected shape", rendered)
        self.assertIn("candidate-shape", rendered)
        self.assertNotIn("Shape A · Selected", rendered)

    def test_presentation_spec_cannot_invent_planning_truth(self):
        with self.assertRaisesRegex(publisher.PublisherError, "absent from canonical"):
            publisher.validate_presentation(
                self.package,
                {
                    "schema_version": 2,
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
            self.assertEqual(2, payload["schema_version"])

    def test_cli_can_emit_svg_overview_and_slice_boards(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = pathlib.Path(temporary) / "shaped-work.html"
            svg_dir = pathlib.Path(temporary) / "boards"
            status = publisher.main(
                [
                    "--planning-dir",
                    str(EXAMPLE),
                    "--output",
                    str(out),
                    "--svg-dir",
                    str(svg_dir),
                ]
            )
            self.assertEqual(0, status)
            self.assertTrue((svg_dir / "shape-overview.svg").is_file())
            slices = sorted(svg_dir.glob("V*.svg"))
            self.assertGreaterEqual(len(slices), 1)
            overview = (svg_dir / "shape-overview.svg").read_text(encoding="utf-8")
            self.assertIn("<svg", overview)
            self.assertIn("P1", overview)

    def test_optional_downstream_artifacts_are_ingested_without_becoming_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary)
            for name in ("01-frame.md", "02-shaping.md", "03-breadboard.md", "presentation.json"):
                (target / name).write_text((EXAMPLE / name).read_text(encoding="utf-8"), encoding="utf-8")
            (target / "04-statechart.md").write_text(
                "# Grocery — Statechart\n\n## State inventory\n\n"
                "| State ID | Source breadboard IDs | State | Parent state | Meaning | Status |\n"
                "|---|---|---|---|---|---|\n"
                "| ST1 | S1 | Needed | — | Item is needed | explicit |\n\n"
                "## Transition table\n\n"
                "| Transition ID | From | Trigger type | Event | Guard | Effect | To | Source wiring | Status |\n"
                "|---|---|---|---|---|---|---|---|---|\n"
                "| TR1 | ST1 | user | buy | — | mark bought | ST1 | U3 -> N4 | explicit |\n",
                encoding="utf-8",
            )
            package = publisher.build_package(target)
            self.assertIn("statechart", package["artifacts"])
            self.assertEqual("04-statechart.md", package["sources"]["optional"]["statechart"])
            self.assertEqual("Accepted selected-design", package["authority"]["breadboard"])
            rendered = publisher.render_html(package)
            self.assertIn("Supporting artifacts", rendered)
            self.assertIn("Grocery — Statechart", rendered)


if __name__ == "__main__":
    unittest.main()
