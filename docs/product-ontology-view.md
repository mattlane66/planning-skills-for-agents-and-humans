# Product ontology view

A **read-only interface** for the existing [Product Intent Layer](../product-intent/README.md). It is not a second product engine or an independent source of truth.

The view answers three practical questions:

- **What must stay true?** Accepted requirements, rules and interactions, with Working items clearly distinguished.
- **What did we decide?** Selected shape and recorded choices, including rejected alternatives when recorded.
- **What is checked?** Declared verification targets and confirmed/inferred code mappings. No behavioral result is invented.

## Generate it

From this repository, with a product's accepted planning artifacts under `planning/`:

```bash
python3 scripts/publish-shaped-work.py \
  --planning-dir planning \
  --output planning/shaped-work.html \
  --json-output planning/planning-package.json \
  --ontology-output planning/product-ontology.html
```

Open `planning/product-ontology.html` in any browser. The output is self-contained, works offline and does not require an account or local server. This flag is optional and leaves existing publishing behavior unchanged. For an existing compiled package:

```bash
python3 product-intent/ontology_view.py \
  --package planning/planning-package.json \
  --output planning/product-ontology.html
```

Without `planning/product-intent.json`, the view still shows planning requirements but explicitly says the intent overlay is missing. With the overlay, it uses the publisher's compiled, source-tagged ontology; inferred links remain inferred.

**Authority:** Human-approved Markdown planning remains authoritative. The view never accepts requirements, selects a shape, changes a selected slice, or confirms mappings. Its 'Copy builder brief' action copies accepted context only, not proof of correctness.

**Verification:** This interface does **not** claim a product is correct, monitor a running app, connect to GitHub, or deliver notifications. The existing `product-intent/gate.py` and trusted behavioral checks determine scoped PASS / REVIEW / DRIFT. A future GitHub adapter should present their commit-specific results in the interface without recomputing or softening them.

**Safety:** Compiled planning text is embedded as escaped JSON, and the viewer uses text nodes rather than HTML injection for artifact content. Only open generated artifacts from projects you trust.
