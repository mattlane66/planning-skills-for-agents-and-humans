# Synthetic v1.7 Reference Study

This is a complete, validator-ready demonstration of the Lead User Research v1.7
state contract and Decision Brief. The source corpus and every entity in it are
fictional. Nothing in this directory is empirical evidence about real AI users or
markets.

The example deliberately contains:

- one qualified Lead User episode;
- one derivative candidate that must not be counted independently;
- one counterexample;
- explicit falsification and observability ledgers;
- a terminated, attribute-specific synthetic pyramid;
- an embedded instruction in a source that is recorded and ignored;
- a passing Concept Generation Gate with two solution-independent requirements;
- one human-selected fictional prototype arm plus one unselected candidate, with production selection explicitly unsupported;
- a structured operational action;
- privacy-safe evidence drill-down.

Validate and regenerate it from the repository root:

```bash
python lead-user-research/scripts/validate_study.py \
  lead-user-research/examples/reference-study
python lead-user-research/scripts/render_decision_brief.py \
  lead-user-research/examples/reference-study
```
