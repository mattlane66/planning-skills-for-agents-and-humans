# AI Workspace for Shaping Board

**Shape in the browser. Use your existing coding agent. Review what comes back.**

The [Shaping Board](./) now includes **AI Workspace** and **Product map** tabs. These are local-first tools for making Planning Skills useful across Codex, Claude Code, Gemini CLI, and other agents **without building a new AI service**.

## Three-minute workflow

1. Open the [hosted Shaping Board](https://mattlane66.github.io/planning-skills-for-agents-and-humans/shaping-board/) (or its standalone HTML), and create a project or import a `.board.json` from an existing planning project.
2. Go to **AI Workspace** and choose your agent and what you want to do: Explore, Shape, Plan a slice, Prepare a build, or Review. Inspect the generated instruction.
3. Click **Download AI-ready workspace ZIP**. It contains working planning Markdown, `planning/shaping.board.json`, `planning/AI-START-HERE.md`, and `README-SHAPING-WORKSPACE.md`.
4. Extract the ZIP into the **product repository you are building**, not this methods repository. **Review and merge deliberately** if the repo already has accepted planning artifacts. The ZIP must not overwrite accepted Markdown automatically.
5. Enable Planning Skills in Codex, Claude Code, or Gemini CLI using [install and use](../../docs/install-and-use.md). Open the product repository in that agent. Give it `planning/AI-START-HERE.md` and have it inspect the existing code, planning context and repo instructions.
6. Let the agent propose a changed `planning/shaping.board.json`, preserving the Board `project_id`. In **AI Workspace → Review AI proposal**, import the `.board.json`. Inspect each section and apply only the changes you choose.
7. Review changed planning artifacts, accept decisions through existing human gates, and run real code/tests in your coding environment. Export a fresh workspace when the Board changes again.

You can also **Copy instruction** directly (or download it as text). The generated instruction includes the Board's current preference, appetite, cut line, named slice, and decision blockers. The ZIP includes the actual planning files and diagrams.

## What is working now?

| Feature | Implemented behavior |
| --- | --- |
| Agent-aware instruction | A task-specific prompt that points to canonical skills and respects current human gates |
| Portable AI handoff | ZIP of working planning files, Board snapshot, starter prompt, and provider setup guide |
| Proposal review | Import same-project v3 Board JSON, preview before/after by section, selectively apply as Working |
| Product map | Inspect Board requirements, their selected-shape part references, candidate diagrams and product nouns; show trusted Product Intent status when present |
| Offline use | The original standalone Board HTML continues to bundle these features without API calls or installation |

This is **not** chat, account connection, one-click plugin installation, GitHub sync, execution of an agent or code, an authoritative Product Ontology compiler, automatic Markdown round-tripping, or a verified test result. A separate agent runtime and repository access remain necessary for actual software construction.

## Authority and security

- **An AI proposal is untrusted data.** The Board displays supported changes and does not silently accept them. Imports require matching `project_id` and schema version; proposals are not sent to any service.
- Applying any proposed section sets selection authority back to **Working**. Modified requirements become Working; frame/appetite authority also reverts to Working when those fields change. Stale imported Product Intent evidence is discarded after applying a proposal.
- Proposal comparisons cover six bounded sections: framing, appetite, design/requirements/stories/fit, things, preferred direction/next slice, and proposed slices. Agent-supplied verification and release statuses, authority claims and arbitrary extra fields are never promoted through proposal application.
- The Board's project map is a **working projection**. It is not the [compiled Product Ontology](../../product-intent/README.md), and linked elements are not evidence of runtime correctness.
- The existing ZIP exporter is an **editing copy**, not a lossless updater for accepted Markdown. Existing repositories require a human-reviewed merge. Follow the [Shaping Board guide](./GUIDE.txt) for distinctions.
- The Board does not request or store model API keys, logins, personal access tokens, or code access. Keep private product data in private repositories and share workspace ZIPs only with trusted agents.
- The agent must respect existing project instructions and obtain explicit approval before implementation. Shape selection, reconciled behavior, slice selection and run-level appetite are distinct gates.

## Why this direction?

The missing capability was not a new coding agent. It was a **portable, inspectable bridge between shaping and the agents people already use**. The Board now has that first complete handoff/review loop.

The remaining vision is optional and incremental: more precise file diffs against accepted Markdown, a compiled project-ontology ingestion layer, better diagrams for code-to-intent evidence, and eventually a local agent runtime. Those are **not** claimed as shipped.

## Where to change it

- `site/shaping-board/index.html` — standalone Board, AI Workspace, Product map and proposal review.
- `site/shaping-board/test-board.mjs` — browser-model and regression checks.
- `site/shaping-board/GUIDE.txt` — instructions, limitations and governance.
- `scripts/build_shaping_board_data.py` — existing read-only adapter from authoritative Markdown to Board JSON.
- `mcp-server/` — existing read-only canonical Planning Skills tools; the Board does not connect to MCP directly.

Use `node site/shaping-board/test-board.mjs` after `cd site && npm ci --ignore-scripts`, then the repository's existing health/CI suite.
