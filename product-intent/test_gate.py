import importlib.util
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location("gate",ROOT/"gate.py")
gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)

def pkg(confidence="confirmed", statement="save failure leaves original unchanged"):
    return {"product_intent":{"planning_records":[],
        "extension_records":[{"uid":"extension:INV-1","kind":"invariant",
                               "status":"accepted","statement":statement}],
        "bindings":[{"intent_id":"INV-1","paths":["src/profile.py"],
                     "confidence":confidence}]}}

MANIFEST={"schema_version":1,"scenarios":[{
    "id":"SC-1","adapter":"python_function","module":"src/profile.py",
    "function":"update_profile","intent_ids":["INV-1"],
    "cases":[{"id":"failed-save","args":[{"name":"Old"},{"name":"New"},False],
              "expected":{"name":"Old"}}]
}]}

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=pathlib.Path(self.tmp.name)
        (self.root/"src").mkdir()
        self.file=self.root/"src"/"profile.py"
        self.file.write_text("def update_profile(saved,draft,success):\n"
                             "    return draft if success else saved\n",encoding="utf-8")
    def check(self, head=None, base=None, paths=None):
        return gate.gate(head or pkg(),paths or ["src/profile.py"],
                         self.root,MANIFEST,base)
    def test_clean_behavior(self):
        self.assertEqual("PASS",self.check(base=pkg())["verdict"])
    def test_seeded_regression_detected(self):
        self.file.write_text("def update_profile(saved,draft,success):\n    return draft\n",encoding="utf-8")
        self.assertEqual("DRIFT",self.check(base=pkg())["verdict"])
    def test_mapping_uncertain(self):
        self.assertEqual("REVIEW",self.check(head=pkg("inferred"),base=pkg())["verdict"])
    def test_accepted_intent_changed(self):
        self.assertEqual("REVIEW",self.check(base=pkg(statement="old approved behavior"))["verdict"])
    def test_unknown_change(self):
        result=self.check(base=pkg(),paths=["src/unknown.py"])
        self.assertEqual("REVIEW",result["verdict"])
    def test_altered_bindings_need_review(self):
        altered=pkg()
        altered["product_intent"]["bindings"][0]["paths"]=["src/*.py"]
        self.assertEqual("REVIEW",self.check(head=altered,base=pkg())["verdict"])
    def test_altered_accepted_decision_metadata_needs_review(self):
        altered=pkg()
        altered["product_intent"]["extension_records"][0]["reopen_when"]="anytime"
        self.assertEqual("REVIEW",self.check(head=altered,base=pkg())["verdict"])
    def test_base_is_required(self):
        self.assertEqual("REVIEW",self.check()["verdict"])

if __name__=="__main__":unittest.main()
