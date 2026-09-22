import contextlib
import importlib.util
import io
import pathlib
import shutil
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "publish_shaped_work.py"
FIXTURE = ROOT / "tests" / "fixtures" / "planning-publisher-current-contract"

spec = importlib.util.spec_from_file_location("publish_shaped_work_contracts", SCRIPT)
publisher = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(publisher)


class PlanningPublisherCanonicalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = publisher.build_package(FIXTURE)

    def test_current_contract_compiles_without_legacy_headings(self):
        package = self.package
        self.assertEqual(["R0", "R1", "R2"], [row["ID"] for row in package["shaping"]["requirements"]])
        self.assertEqual("Accepted", package["authority"]["requirements"])
        self.assertEqual("Accepted", package["authority"]["appetite"])
        self.assertEqual("A", package["shaping"]["selected_shape"])
        self.assertEqual("Selected", package["authority"]["shape"])
        self.assertEqual("selected-design", package["breadboard"]["mode"])
        self.assertEqual("Accepted selected-design", package["authority"]["breadboard"])
        self.assertEqual(["V1", "V2"], [row["id"] for row in package["breadboard"]["slices"]])
        self.assertEqual("V1", package["breadboard"]["active_slice"])
        self.assertEqual("Selected build scope", package["authority"]["slice"])
        self.assertEqual(["SK1"], [row["id"] for row in package["breadboard"]["targeted_sketches"]])
        self.assertEqual(
            "intentionally unspecified",
            package["frame"]["transformation"]["f() — solution / shape variable"],
        )
        self.assertIn("Relevant operating conditions", package["frame"]["operating_model"])
        self.assertEqual("Accepted", package["shaping"]["operating_model"]["Authority"])
        self.assertEqual("FROM_M", package["shaping"]["requirements"][2]["Origin"])

    def test_nested_frame_boundaries_survive_normalization(self):
        self.assertEqual(
            ["replacing the account system", "redesigning inventory"],
            self.package["frame"]["less_about"],
        )
        self.assertEqual(
            ["one clear checkout path", "visible completion state"],
            self.package["frame"]["more_about"],
        )

    def test_discovery_prefers_artifact_metadata_over_filenames(self):
        self.assertEqual("alpha.md", self.package["sources"]["frame"])
        self.assertEqual("beta.md", self.package["sources"]["shaping"])
        self.assertEqual("gamma.md", self.package["sources"]["breadboard"])
        self.assertEqual("delta.md", self.package["sources"]["slices"])
        self.assertEqual("epsilon.md", self.package["sources"]["optional"]["statechart"])

    def test_visual_model_preserves_explicit_slice_scopes_and_sketches(self):
        model = self.package["visual_model"]
        self.assertEqual("P1", model["places"][0]["id"])
        self.assertTrue(model["places"][0]["hero"])
        slices = {item["id"]: item for item in model["slices"]}
        self.assertEqual(
            ["N1", "P1", "S1", "U1", "U2", "U3"],
            sorted(slices["V1"]["scope"]),
        )
        self.assertEqual("selected-build-scope", slices["V1"]["authority"])
        self.assertEqual("deferred-accepted", slices["V2"]["authority"])
        self.assertEqual(["SK1"], [item["id"] for item in model["sketches"]])
        self.assertTrue(
            self.package["presentation"]["embedded_sketch_assets"]["SK1"].startswith(
                "data:image/svg+xml;base64,"
            )
        )
        self.assertGreaterEqual(len(model["journey"]), 2)

    def test_current_contract_renders_human_and_svg_views(self):
        rendered = publisher.render_html(self.package)
        for planning_id in ("R0", "A1", "P1", "U1", "N1", "S1", "V1", "SK1"):
            self.assertIn(f'data-plan-id="{planning_id}"', rendered)
        self.assertIn('data-scope="V1"', rendered)
        self.assertIn("Accepted selected-design", rendered)
        self.assertIn("Unselected candidate · collapsed by default", rendered)
        self.assertIn("data:image/svg+xml;base64,", rendered)
        self.assertIn("Operating model", rendered)
        self.assertIn("existing downstream system", rendered)
        with tempfile.TemporaryDirectory() as temporary:
            svg_dir = pathlib.Path(temporary)
            paths = publisher.write_svg_assets(self.package, svg_dir)
            self.assertEqual(3, len(paths))
            self.assertTrue((svg_dir / "shape-overview.svg").is_file())
            self.assertTrue(any(path.name.startswith("V1-") for path in paths))

    def test_default_presentation_is_useful_without_presentation_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary)
            for source in FIXTURE.iterdir():
                if source.name == "presentation.json":
                    continue
                if source.is_file():
                    shutil.copy2(source, target / source.name)
            package = publisher.build_package(target)
            self.assertEqual("P1", package["presentation"]["hero_place"])
            self.assertTrue(package["visual_model"]["journey"])
            self.assertTrue(package["visual_model"]["slices"])
            self.assertTrue(package["visual_model"]["sketches"])

    def test_check_fails_closed_when_current_contract_loses_accepted_requirements(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary)
            for source in FIXTURE.iterdir():
                if source.is_file():
                    shutil.copy2(source, target / source.name)
            shaping = target / "beta.md"
            text = shaping.read_text(encoding="utf-8")
            text = text.replace("## Requirements", "## Missing requirements")
            shaping.write_text(text, encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                status = publisher.main(["--planning-dir", str(target), "--check"])
            self.assertEqual(2, status)
            self.assertIn("selected shaping has no parsed requirements", stderr.getvalue())

    def test_check_succeeds_for_current_contract(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            status = publisher.main(["--planning-dir", str(FIXTURE), "--check"])
        self.assertEqual(0, status)
        self.assertIn("3 requirements", stdout.getvalue())
        self.assertIn("2 slices", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
