#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

missing=0

require_text() {
  local file="$1"
  local text="$2"
  if grep -Fq "$text" "$file"; then
    echo "✓ $file contains $text"
  else
    echo "✗ $file missing $text" >&2
    missing=$((missing + 1))
  fi
}

forbid_text() {
  local file="$1"
  local text="$2"
  if grep -Fq "$text" "$file"; then
    echo "✗ $file unexpectedly contains $text" >&2
    missing=$((missing + 1))
  else
    echo "✓ $file excludes $text"
  fi
}

require_text templates/context-packet.md "## Execution contract"
require_text templates/wayfinding-map.md "## Not yet specified"
require_text templates/wayfinding-map.md "source_of_truth: false"
require_text templates/wayfinding-ticket.md "blocked_by"
require_text wayfinding/SKILL.md "coordination artifacts, never product truth"
require_text wayfinding/SKILL.md "never back to Wayfinding"
require_text wayfinding/SKILL.md "Dumplink decomposes a selected project into sequenced vertical task groups"
require_text templates/context-packet.md "Goal condition"
require_text templates/context-packet.md "Kickoff doc, for builder orientation only"
require_text templates/frame.md "## Current situation"
require_text framing-doc/SKILL.md "current approach, workaround"
require_text shaping/SKILL.md "Exploration is fluid. Commitment is gated."
require_text shaping/SKILL.md "### Start from S — shape first"
require_text shaping/SKILL.md "These are promotion gates, not navigation locks."
require_text shaping/SKILL.md "Do not dump or cluster implementation tasks, select committed slices, create a build sequence, or write production code inside shaping."
require_text shaping/SKILL.md "A candidate breadboard does not automatically become authoritative"
require_text shaping/SKILL.md "Identify the unknown before choosing the next move"
require_text shaping/SKILL.md "Promotion from candidate to Working to Accepted changes authority, not identity."
require_text shaping/SKILL.md "## Requirement coverage"
require_text shaping/references/fit-checks.md "Coverage is not realized fit"
forbid_text shaping/SKILL.md "## Kick-off: From selected shape to slices"
require_text breadboarding/SKILL.md "### Current-state mapping (descriptive)"
require_text breadboarding/SKILL.md "### Candidate-shape mapping (exploratory)"
require_text breadboarding/SKILL.md "### Selected-design mapping (normative)"
require_text breadboarding/SKILL.md "accepted requirements or appetite are **not prerequisites for exploratory candidate breadboarding**"
require_text breadboarding/SKILL.md "Only an accepted selected-design breadboard can feed slice selection"
require_text breadboarding/SKILL.md "requirement realization map"
require_text templates/breadboard.md "## Requirement realization map — selected-design mode"
require_text breadboarding/SKILL.md "Candidate-shape breadboarding is a shaping technique"
require_text breadboarding/SKILL.md "entry → control path → decision or branch → state/data effect → observable consequence"
require_text breadboarding/SKILL.md "reverse-trace each observable consequence"
require_text breadboarding/SKILL.md "## Affordance and seam test"
require_text breadboarding/references/behavior-tracing-and-verification.md "## Reverse-trace observable consequences"
require_text breadboarding/references/behavior-tracing-and-verification.md "## Verify graph integrity"
require_text breadboarding/references/notation-rendering-and-slicing.md "Mode: current-state | candidate-shape | selected-design"
require_text templates/breadboard.md 'Mode: `current-state`, `candidate-shape`, or `selected-design`'
require_text templates/breadboard.md "## Behavior traces"
require_text templates/breadboard.md "## Reverse-trace audit"
require_text evals/workflow-behavior-cases.json '"id": "current-state-code-fidelity"'
require_text evals/workflow-behavior-cases.json '"id": "breadboard-causal-integrity"'
require_text evals/workflow-behavior-cases.json '"id": "breadboard-reverse-reachability"'
require_text evals/workflow-behavior-cases.json '"id": "selected-design-granularity"'
require_text evals/workflow-behavior-cases.json '"id": "criterion-identity-survives-promotion"'
require_text evals/workflow-behavior-cases.json '"id": "selected-shape-exposes-uncovered-accepted-r"'
require_text evals/workflow-behavior-cases.json '"id": "implementation-conformance-is-not-realized-fit"'
require_text evals/workflow-behavior-cases.json '"id": "reality-can-contradict-a-correct-implementation"'
require_text evals/workflow-behavior-cases.json '"id": "realized-fit-supported-by-outcome-evidence"'
require_text docs/skill-behavior-evals.md 'protocol is `blind-command-v1`'
require_text scripts/run-skill-behavior-evals.py '"prompt": case["prompt"]'
require_text templates/dumplink.md "## Vertical task groups"
require_text templates/dumplink.md "## Scope cuts"
require_text templates/statechart.md "## Transition table"
require_text templates/statechart.md "breadboard tables remain authoritative"
require_text mcp-server/src/index.ts "templates/context-packet.md"
require_text mcp-server/src/index.ts "templates/dumplink.md"
require_text dumplink/SKILL.md "Vertical task groups"
require_text dumplink/SKILL.md "Scope cuts"
require_text dumplink/SKILL.md "The project is the discrete unit of work Dumplink ingests"
require_text dumplink/SKILL.md "Dumplink discovers the implementation slices"
require_text dumplink/SKILL.md "Stop for task-group approval"
require_text kickoff-doc/SKILL.md "Start with the accepted frame, selected shape, accepted breadboard, selected slice"
require_text statechart/SKILL.md "breadboard tables remain the source of truth"
require_text sketch-reconciliation/SKILL.md "observations before interpretations"
require_text sketch-reconciliation/SKILL.md "Stop at the reconciliation gate"
require_text breadboard-reflection/SKILL.md "explicit drift decision"
require_text breadboard-reflection/SKILL.md "Do not silently rewrite the accepted breadboard"
require_text breadboard-reflection/SKILL.md "Implementation conformance is not realized-fit evidence"
require_text templates/breadboard-reflection.md "## Realized fit"
require_text templates/context-packet.md "## Criterion bindings"
require_text docs/claude-design-workflow.md "## Entry path B — Start from S"
require_text docs/claude-design-workflow.md "A beautiful candidate prototype remains a candidate."
require_text docs/claude-design-workflow.md "## Hard promotion gate — select a shape"
require_text .agent-orchestration.yaml "collaborative:"
require_text .agent-orchestration.yaml "gated:"
require_text .agent-orchestration.yaml "hard_promotion_gates:"
require_text .claude/commands/spike.md "The spike gathers evidence"
require_text .gemini/commands/spike.toml "The spike gathers evidence"
require_text examples/solution-first-shaping/README.md "rough S"
require_text .github/workflows/repo-health.yml "set -o pipefail"
require_text scripts/build_claude_skills.py "removeprefix"
require_text scripts/build_claude_skills.py "skill-metadata.json"
forbid_text scripts/run-skill-behavior-evals.py "input=json.dumps(case)"
require_text mcp-server/src/index.ts "skill-metadata.json"
require_text tests/test_build_claude_skills.py "test_repo_root_is_never_a_valid_output_directory"
require_text visualizer/test/viewer.test.mjs "malformedVendorPath.status, 400"
require_text .claude/commands/check-drift.md "selected Dumplink task group"
require_text .gemini/commands/check-drift.toml "selected Dumplink task group"
require_text evals/golden/context-packet-execution-contract.md "Execution contract"
require_text evals/golden/dumplink-vertical-groups.md "cluster by judgeable"
require_text evals/golden/statechart-derived-authority.md "breadboard remains authoritative"
require_text evals/golden/sketch-reconciliation-authority.md "Record visible observations before interpretations"
require_text evals/golden/drift-check-strict-output.md "No planning drift found"

if [[ "$missing" -gt 0 ]]; then
  echo "Contract fixture checks failed with $missing missing item(s)." >&2
  exit 1
fi

echo "Contract fixture checks passed."
