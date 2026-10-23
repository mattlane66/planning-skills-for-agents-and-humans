# Shaping Board: fixed breadboard language v1

**Live proposal loop:** The optional local companion (documented in [AI-WORKSPACE.md](./AI-WORKSPACE.md)) invokes a signed-in Codex CLI to return a typed BreadboardPatch directly to the Board. The human sees the old and proposed diagrams plus record-level differences before applying. Accepted planning Markdown is never automatically rewritten.


This is a **versioned, validated semantic model**, not an agent prompt convention. Agents may propose product behaviors but cannot silently invent node types, relationships or SVG geometry.

## Authority

A breadboard/v1 candidate's text model is the semantic source within that **working candidate**. The visual and exported candidate Markdown are projections, not competing definitions. **Accepted selected-design Markdown and human gates remain authoritative for build scope**, until a human reconciles and explicitly accepts the new behavior. The exporter is not a lossless update to existing Markdown.

Older diagrams (no version header) remain readable with the legacy renderer. No automatic migration: ambiguous action/question nodes, implicit UI controls and custom paths cannot reliably be mapped to typed components.

## Syntax

The first non-comment line must be exactly: version: breadboard/v1

Nodes use five pipe-separated fields: ID | kind | title | detail | system. UI nodes add a sixth: in=P1.

| ID prefix | Kind | Meaning |
| --- | --- | --- |
| P1 | place | Interaction context |
| U1 | ui | User-visible affordance; must have an in=P# parent |
| N1 | nonui | Hidden but consequential mechanism |
| Q1 | decision | Branch in control flow |
| S1 | store | Meaningful retained state |

Stable IDs may include dot-number suffixes. Node fields have no pipes or embedded line breaks. Typed wires use FROM -> TO : kind, where kind is one of control, navigate, read, write, return, yes, no, show. Yes/no can originate only from Q decisions.

Example:

    version: breadboard/v1
    P1 | place | Request form | Enter a request | app
    U1 | ui | Submit | Click send | app | in=P1
    N1 | nonui | Validate | Reject incomplete requests | backend
    Q1 | decision | Valid? | Continue or error | backend
    S1 | store | Requests | Save accepted requests | db
    U2 | ui | Status | Show result | app | in=P1
    U1 -> N1 : control
    N1 -> Q1 : control
    Q1 -> S1 : yes
    Q1 -> U2 : no
    S1 -> U2 : return

The compiler rejects unknown kinds, dangling wires/parents, malformed IDs, duplicates, freeform SVG path directives and unsupported syntax. Layout is reproducible from semantic components without agent-specified coordinates. Browser typography may still vary.

## Revision protocol

Use Shaping Board > AI Workspace, export the project, and ask the agent for a BreadboardPatch JSON file based on the exact candidate model.

    {
      "kind": "BreadboardPatch",
      "schema_version": 1,
      "project_id": "REPLACE_WITH_EXPORTED_PROJECT_ID",
      "option_id": "A",
      "base_dsl": "version: breadboard/v1\nP1 | place | Request form | Enter a request | app\n",
      "operations": [
        {"op":"add_node","node":{"id":"U1","kind":"ui","title":"Submit","detail":"Send request","system":"app","parent":"P1"}},
        {"op":"add_edge","from":"P1","to":"U1","kind":"control"}
      ]
    }

The base_dsl must be the **complete canonical baseline** with its trailing newline. The importer compares full canonical text and rejects stale proposals. Available operations: add_node; update_node (id and set containing title, detail, system or parent); remove_node (after removing incident edges and child references); add_edge; remove_edge (from, to, kind). An ID or kind change requires explicit remove/add and wire reconciliation.

The Board previews complete per-ID **before/after semantic diffs** and proposed model text. A human can apply the whole patch **as Working** or discard it. Application is atomic: dependent node and wire edits cannot safely be split arbitrarily. To accept fewer changes, request a smaller patch against the updated baseline.

Patch application returns the candidate's fit and scenario ratings to unknown and discards stale read-only Product Intent status. It does NOT accept requirements, select a solution, authorize implementation, prove runtime behavior or update accepted Markdown. Other project changes still use the existing full .board.json proposal review.

## Language extensions

Compose existing primitives first. If they cannot express meaningful behavior, propose a **compiler/language version change** in normal repository review. New node or wire types require human approval, validation, rendering, tests, documentation and compatibility handling. A BreadboardPatch cannot introduce a new primitive.

## Implementation

- Canonical compiler: site/shaping-board/breadboard-core.cjs
- Offline Board: site/shaping-board/index.html (same compiler source inlined)
- Sync: python3 scripts/inline_shaping_board_core.py
- Tests: node site/shaping-board/test-breadboard-core.mjs and cd site && node shaping-board/test-board.mjs
- The existing DWC Requests example remains deliberately on the old notation until a human reconciles its meaning.
