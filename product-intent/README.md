# Product Intent

This directory contains the formal contract for the Product Intent layer.

- `schema.json` defines `ProductIntentModel`.
- `implementation-bindings.example.json` shows how stable intent IDs connect to current code.
- `SKILL.md` defines the agent workflow for compiling intent, bootstrapping existing code, checking drift, and changing intent deliberately.

The normal project output is generated in the product repository:

```text
planning/product-intent.json
```

Do not hand-edit that generated file. Accepted planning artifacts are the human-authored authority; the model is their deterministic machine-readable projection.

See [the full product-intent guide](../docs/product-intent-layer.md).
