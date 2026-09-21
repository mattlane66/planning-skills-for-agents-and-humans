# Visual breadboard mixed-fidelity golden

A strong breadboard keeps the canonical behavior model authoritative while producing a deliberate spatial projection for human review.

Expected characteristics:

- The primary scenario is visually obvious and can be finger-traced from entry to observable consequence.
- Major places read as loose vertical stacks with visible affordances directly beneath their context.
- User-visible behavior is the dominant visual layer.
- Validation, persistence, APIs, stores, and background work sit on a secondary system rail when possible.
- Product-relevant branches leave near the decision that causes them and show their visible consequence locally.
- Whitespace and alignment are preferred over boxing every node.
- Wire crossings are minimized by rearranging the board or duplicating clearly labeled references.
- Targeted sketches are used only where spatial arrangement materially changes understanding.
- Each targeted sketch has a stable `SK#` identifier and maps to canonical `P/U/N/S` IDs.
- Fidelity is raised locally, not globally.
- No visual or sketch introduces behavior absent from the canonical tables.
- Mermaid may be used as a compact fallback, but automatic graph layout must not dictate the human reasoning surface.
