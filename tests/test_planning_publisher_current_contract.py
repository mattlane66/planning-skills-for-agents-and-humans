import pathlib
import tempfile
import unittest

from scripts import publish_shaped_work as publisher


FRAME = """---
planning: true
shaping: true
artifact_type: frame
status: accepted
source_of_truth: true
---

# Current Contract — Frame

## Transformation frame (x → f() → y)
- x — trigger/context: user has work to do
- x — current approach: manual
- x — current result: slow
- f() — current transformation or breakdown: repeated handling
- y — desired outcome: quick completion
- Gap between x and y: remove repeated handling
- Boundaries that constrain a valid transformation: one small surface

## Problem
- Repeated handling makes the task slow.

## Outcome
- The task completes quickly.

## Boundaries

### Less about
- broad automation

### More about
- one clear flow
"""

SHAPING = """---
planning: true
shaping: true
artifact_type: shaping
status: accepted
source_of_truth: true
---

# Current Contract — Shaping

## Frame reference
- Transformation frame: x → f() → y
- Frame artifact: 01-frame.md
- Frame authority: Accepted
- Outcome: quick completion
- Non-goals: broad automation

## Requirements

| ID | Requirement | Status | Authority | Origin | Evidence refs | Notes |
|---|---|---|---|---|---|---|
| R0 | User can complete the task from one place. | Core goal | Accepted | FROM_GAP | frame | — |
| R1 | User sees the result immediately. | Must-have | Accepted | FROM_Y | frame | — |

## Appetite
- Authority: Accepted
- Time budget: a few focused days
- Team shape: one builder
- Review point: working demo
- Cut line: no accounts
- Accepted uncertainty: polish can remain rough
- Must-resolve unknowns: none
- Revisit conditions: if the main path cannot be completed

## Shapes

### CURRENT: Existing baseline

| Part | Mechanism | Flag |
|---|---|:---:|
| CURRENT1 | Manual multi-step flow | |

### A: Single-surface flow

| Part | Mechanism | Flag |
|---|---|:---:|
| A1 | One main screen | |
| A2 | Inline completion | |

### B: Wizard flow

| Part | Mechanism | Flag |
|---|---|:---:|
| B1 | Multi-step wizard | |

## Fit check
- Authority: Decision-ready

| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | User can complete the task from one place. | Core goal | ❌ | ✅ | ❌ |
| R1 | User sees the result immediately. | Must-have | ❌ | ✅ | ✅ |

## Reverse fit check

| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| A1 | One main screen | R0 | ✅ |
| A2 | Inline completion | R1 | ✅ |

## Appetite fit

| Shape | Evidence quality | Fits Appetite? | Required cuts | Uncertainty / spike |
|---|---|:---:|---|---|
| A | decision-ready | ✅ | none | none |
| B | decision-ready | ❌ | wizard complexity | none |

## Decision
- Status: selected
- Chosen direction: A
- Why: smallest shape that fits the accepted requirements
- Rejected directions: CURRENT, B
- Cuts / non-goals: no accounts
- Remaining unknowns: none
- Candidate evidence to reconcile: none
"""

BREADBOARD = """---
planning: true
shaping: true
artifact_type: breadboard
status: accepted
source_of_truth: true
---

# Current Contract — Breadboard

## Mode and authority
- Mode: selected-design
- Authority: accepted normative intent
- Requirements authority: Accepted
- Appetite authority: Accepted

## Places

| ID | Authority | Shape part | Place | Description |
|---|---|---|---|---|
| P1 | selected | A1 | Main screen | User completes the task here |
| P2 | selected | A2 | Result state | Immediate result is shown here |

## UI affordances

| ID | Place | Authority | Shape part | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|---|---|
| U1 | P1 | selected | A1 | form | task input | type | -> N1 | — |
| U2 | P1 | selected | A2 | form | complete button | click | -> N1 | — |
| U3 | P2 | selected | A2 | result | completion result | display | — | <- N1 |

## Non-UI affordances

| ID | Place | Authority | Shape part | Component | Affordance | Control | Wires Out | Returns To |
|---|---|---|---|---|---|---|---|---|
| N1 | P1 | selected | A2 | action | complete task | call | -> S1 | -> U3 |

## Stores

| ID | Place | Authority | Shape part | Store | Description |
|---|---|---|---|---|---|
| S1 | P1 | selected | A2 | result | completion result |

## Behavior traces

| Scenario | Entry | Control path | Decision / branch | State / data effect | Observable consequence | Evidence or status |
|---|---|---|---|---|---|---|
| Complete task | U1, U2 | U2 -> N1 | — | N1 -> S1 | N1 -> U3 | supported |

## Reverse-trace audit

| Observable consequence | Direct incoming sources | Upstream entries / writers | Unresolved predecessors | Status |
|---|---|---|---|---|
| U3 | N1 | U2 | none | supported |

## Targeted sketches

| Sketch | Elaborates | Question resolved | States / controls shown | Status |
|---|---|---|---|---|
| SK1 | P1 / U1 / U2 | Input and action hierarchy | input, action | resolved |

## Slice candidates

| Slice | Affordances / stores included | Demo | Produces | Unknowns |
|---|---|---|---|---|
| V1 | P1, P2, U1, U2, U3, N1, S1 | Complete one task and see result | end-to-end completion | none |
"""


class CurrentCanonicalContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        (self.root / "01-frame.md").write_text(FRAME, encoding="utf-8")
        (self.root / "02-shaping.md").write_text(SHAPING, encoding="utf-8")
        (self.root / "03-breadboard.md").write_text(BREADBOARD, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_publisher_accepts_current_frame_and_shaping_contract(self):
        package = publisher.build_package(self.root)
        self.assertEqual(["broad automation"], package["frame"]["less_about"])
        self.assertEqual(["one clear flow"], package["frame"]["more_about"])
        self.assertEqual(["R0", "R1"], [row["ID"] for row in package["shaping"]["requirements"]])
        self.assertEqual("Accepted", package["authority"]["requirements"])
        self.assertEqual("Accepted", package["authority"]["appetite"])
        self.assertEqual("A", package["shaping"]["selected_shape"])
        self.assertEqual("Selected", package["authority"]["shape"])

    def test_publisher_accepts_current_breadboard_authority_slice_and_sketch_tables(self):
        package = publisher.build_package(self.root)
        self.assertEqual("selected-design", package["breadboard"]["mode"])
        self.assertEqual("Accepted selected-design", package["authority"]["breadboard"])
        self.assertEqual(["V1"], [row["id"] for row in package["breadboard"]["slices"]])
        self.assertEqual(["SK1"], [row["id"] for row in package["breadboard"]["targeted_sketches"]])
        rendered = publisher.render_html(package)
        self.assertIn('data-plan-id="V1"', rendered)
        self.assertIn('data-plan-id="SK1"', rendered)

    def test_current_contract_still_emits_a_useful_visual_model_without_presentation_json(self):
        package = publisher.build_package(self.root)
        self.assertEqual("P1", package["presentation"]["hero_place"])
        self.assertEqual("P1", package["visual_model"]["places"][0]["id"])
        self.assertTrue(package["visual_model"]["journey"])
        self.assertTrue(package["visual_model"]["slices"])
        self.assertTrue(package["visual_model"]["sketches"])


if __name__ == "__main__":
    unittest.main()
