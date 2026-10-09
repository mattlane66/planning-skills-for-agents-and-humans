import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ontology_view', HERE / 'ontology_view.py')
view = importlib.util.module_from_spec(spec)
spec.loader.exec_module(view)

BASE = {
    'kind': 'PlanningPackage', 'title': 'Example <script>alert(1)</script>',
    'authority': {'requirements': 'Accepted'},
    'shaping': {'selected_shape': 'A', 'requirements': [{'ID': 'R1', 'Requirement': 'Keep items after refresh'}]},
    'breadboard': {'active_slice': 'V1'}, 'sources': {'shaping': 'shaping.md'},
}


class OntologyViewTest(unittest.TestCase):
    def test_fallback_never_invents_intent_or_checks(self):
        data = view.project_package(BASE)
        self.assertFalse(data['has_intent_model'])
        self.assertEqual('accepted', data['records'][0]['status'])
        self.assertEqual([], data['bindings'])
        rendered = view.render_html(BASE)
        self.assertNotIn('<script>alert(1)</script>', rendered)
        self.assertIn(r'\u003cscript\u003e', rendered)
        self.assertIn('Result not provided', rendered)

    def test_opt_in_overlay_preserves_authority_and_mappings(self):
        model = {**BASE, 'product_intent': {
            'kind': 'ProductIntentModel',
            'planning_records': [{'uid': 'requirement:R1', 'id': 'R1', 'kind': 'requirement',
                                  'status': 'accepted', 'data': {'Requirement': 'Keep items after refresh'},
                                  'source': '02-shaping.md'}],
            'extension_records': [
                {'uid': 'extension:INV-1', 'id': 'INV-1', 'kind': 'invariant',
                 'status': 'working', 'title': 'Remember items', 'statement': 'Items survive reload',
                 'refs': ['R1'], 'verification': ['refresh-test'], 'source': 'product-intent.json'},
                {'uid': 'extension:DEC-1', 'id': 'DEC-1', 'kind': 'decision',
                 'status': 'accepted', 'title': 'Use local storage', 'statement': 'Persist locally',
                 'refs': ['INV-1'], 'evidence': ['Review'],
                 'alternatives': [{'name': 'server', 'disposition': 'rejected', 'reason': 'Needs account'}]},
            ],
            'bindings': [{'intent_id': 'INV-1', 'paths': ['src/store.ts'], 'confidence': 'inferred'}],
            'unlinked_accepted_requirements': ['requirement:R1'],
        }}
        data = view.project_package(model)
        self.assertTrue(data['has_intent_model'])
        self.assertEqual('working', next(x for x in data['records'] if x['id'] == 'INV-1')['status'])
        self.assertEqual('inferred', data['bindings'][0]['confidence'])
        self.assertEqual(['requirement:R1'], data['unlinked_accepted_requirements'])
        self.assertIn('Implementation status unknown', view.render_html(model))

    def test_fail_closed_on_inconsistent_model(self):
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            view.project_package({**BASE, 'product_intent': {'records': []}})
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            view.project_package({**BASE, 'shaping': {'requirements': [{'ID': 'R1'}, {'ID': 'R1'}]}})

    def test_cli_writes_standalone_html(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source = base / 'package.json'
            target = base / 'ontology.html'
            source.write_text(json.dumps(BASE))
            process = subprocess.run(
                [sys.executable, str(HERE / 'ontology_view.py'), '--package', str(source),
                 '--output', str(target)], capture_output=True, text=True)
            self.assertEqual(0, process.returncode, process.stderr)
            output = target.read_text()
            self.assertIn('id="ontology-data"', output)
            self.assertNotIn('__ONTOLOGY_JSON_PAYLOAD__', output)
            self.assertNotIn('src="http', output)


if __name__ == '__main__':
    unittest.main()
