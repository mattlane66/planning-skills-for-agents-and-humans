import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("intent_mapper",ROOT/"mapping.py")
mapping=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mapping)

class WorkingProposalsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=pathlib.Path(self.tmp.name)
        (self.root/"src").mkdir()
        (self.root/"src"/"meaning-contract.ts").write_text(
            "export function compareMeaningContract(original, candidate) { return original === candidate; }\n",
            encoding="utf-8"
        )
        self.package={"product_intent":{"extension_records":[
            {"id":"INV-5","uid":"extension:INV-5","status":"working",
             "title":"Compare meaning contract","statement":"Compare meaning before committing"}
        ],"planning_records":[]}}

    def test_working_intent_not_implicitly_promoted(self):
        report=mapping.propose(self.package,self.root)
        self.assertEqual([],report["proposals"])
        self.assertEqual([],report["unmapped_intent_uids"])

    def test_opted_in_working_proposal_is_inferred(self):
        report=mapping.propose(self.package,self.root,include_working=True)
        matches=[p for p in report["proposals"] if p["intent_id"]=="INV-5"]
        self.assertTrue(matches,report)
        self.assertEqual({"working"},{p["intent_authority"] for p in matches})
        self.assertTrue(all(p["requires_review"] and p["confidence"]=="inferred" for p in matches))
        self.assertEqual("js_ts_declaration_regex",matches[0]["evidence"]["parser"])

    def test_rejected_is_never_mapped(self):
        self.package["product_intent"]["extension_records"][0]["status"]="rejected"
        self.assertEqual([],mapping.propose(self.package,self.root,include_working=True)["proposals"])

if __name__=="__main__":
    unittest.main()
