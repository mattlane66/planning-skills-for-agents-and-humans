# Sketch Reconciliation Example

This example shows how a dropped visual can reveal missing detail without silently overriding a selected shape.

## Files

- [`01-shaping-before.md`](./01-shaping-before.md) - the accepted requirements and Shape A before visual review
- [`02-availability-sketch.svg`](./02-availability-sketch.svg) - a rough visual with an always-visible date label
- [`03-reconciliation.md`](./03-reconciliation.md) - observations, mapping, accepted delta, fit impact, and ripple status
- [`04-shaping-after.md`](./04-shaping-after.md) - the accepted shaping update

## Prompt

```text
Use sketch-reconciliation/SKILL.md.
Reconcile 02-availability-sketch.svg with 01-shaping-before.md.
The selected date must always be clear while natural-language commands change the view.
Update the shaping artifact after showing the proposed delta.
```

The explicit sentence authorizes the behavioral change. The image supplies supporting visual evidence; it does not independently prove how date changes work.
