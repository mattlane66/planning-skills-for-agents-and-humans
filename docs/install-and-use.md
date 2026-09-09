# Install Planning Skills, then use them in your product repo

Planning Skills has two layers:

1. **Make the method available to your agent once.** Install, link, upload, or otherwise expose the skills.
2. **Do the actual planning in the product repository.** Open the repository you are building, invoke the smallest useful skill there, and save project-specific artifacts beside the code, usually under `planning/`.

Do **not** paste this entire repository into every prompt and do not replace a product repository's existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or other local instructions. The Planning Skills repository supplies reusable method instructions; the product repository remains authoritative for its own build, test, security, and architecture rules.

## Fastest path by environment

| Environment | Make Planning Skills available | Invoke it in the product repo |
| --- | --- | --- |
| **Claude Code** | Clone this repo, run `bash scripts/build-claude-plugin.sh`, then start Claude Code with `--plugin-dir /path/to/planning-skills-for-agents-and-humans/dist/claude-code-plugin`. | Run `/planning-skills:plan`, `/planning-skills:shape`, and the other namespaced commands. |
| **Codex CLI** | `codex plugin marketplace add mattlane66/planning-skills-for-agents-and-humans --ref main`, then `codex plugin add planning-skills-for-agents-and-humans@planning-skills-marketplace`. Start a new Codex task after installation. | Ask for the named skill in natural language, for example: `Use the planning-router skill on what I have and recommend the smallest useful next move.` |
| **Codex app / managed workspace** | A workspace admin can import this GitHub repository as a plugin marketplace from **Workspace settings → Plugins → Add → Import marketplace**. The repo exposes `.agents/plugins/marketplace.json`. | In a supported Codex task view, open **Sources → Use plugins**, select the installed plugin, then ask for the named skill. |
| **Gemini CLI** | `gemini skills install https://github.com/mattlane66/planning-skills-for-agents-and-humans` or link a local checkout with `gemini skills link /path/to/planning-skills-for-agents-and-humans`, then run `/skills reload`. | Ask for the named skill in natural language. Native skill installation does **not** install this repo's `.gemini/commands/` wrappers into an unrelated product repo. |
| **Claude / Claude Design** | Run `python3 scripts/build_claude_skills.py`, then upload the generated ZIPs from `dist/claude-skills/` under **Customize → Skills** and enable them. | Ask Claude to use the named skill. Uploaded skills do not depend on Claude Code slash commands. |
| **Cursor or another agent** | Point the agent at the relevant canonical `SKILL.md`, or make the skill folders available through that tool's skill mechanism. | Ask for the named skill and profile explicitly. |
| **MCP-compatible client** | Run the optional server under `mcp-server/` and connect it using the client's MCP configuration. | Invoke the exposed planning tools/resources from the client. |

The exact installation surface can change as agent products evolve. The canonical method lives in the root `SKILL.md` files and `.agent-orchestration.yaml`; runtime wrappers are adapters around that method.

## Claude Code

For a local, self-contained plugin bundle:

```bash
git clone https://github.com/mattlane66/planning-skills-for-agents-and-humans.git ~/.local/share/planning-skills-for-agents-and-humans
cd ~/.local/share/planning-skills-for-agents-and-humans
bash scripts/build-claude-plugin.sh
```

Then, from the **product repository** you want to plan or build:

```bash
claude --plugin-dir ~/.local/share/planning-skills-for-agents-and-humans/dist/claude-code-plugin
```

Start with:

```text
/planning-skills:plan
```

The plugin bundle carries the canonical skills, command wrappers, templates, orchestration rules, hooks, examples, and support docs. See [`docs/claude-code-plugin.md`](./claude-code-plugin.md).

## Codex

### Personal / CLI use

Add this repository as a Codex marketplace source and install the plugin:

```bash
codex plugin marketplace add mattlane66/planning-skills-for-agents-and-humans --ref main
codex plugin add planning-skills-for-agents-and-humans@planning-skills-marketplace
```

Then start a new Codex task in the product repository. Codex uses the packaged skill inventory and prompt invocation rather than Claude-style slash commands.

Example:

```text
Use the planning-router skill on the notes, prototype, and relevant code in this repository. Recommend exactly one smallest useful next move, including no planning skill if appropriate.
```

### Managed workspace / Plugin Directory

OpenAI workspaces can import GitHub plugin marketplaces. An eligible admin can import this repository from **Workspace settings → Plugins → Add → Import marketplace**. Leave the marketplace path blank because `.agents/plugins/marketplace.json` is at the repository root. After the plugin is installed for the relevant user or role, select it in **Sources → Use plugins** in a supported Codex task view.

See [`docs/codex-plugin.md`](./codex-plugin.md) and [`docs/codex-usage.md`](./codex-usage.md).

## Gemini CLI

Gemini CLI's native Agent Skills manager recursively discovers valid skills in this repository, so a single install can make the canonical skill set available:

```bash
gemini skills install https://github.com/mattlane66/planning-skills-for-agents-and-humans
gemini skills list
```

For local development, link instead:

```bash
gemini skills link /path/to/planning-skills-for-agents-and-humans
```

If Gemini is already running, refresh discovery:

```text
/skills reload
```

Then open the product repository and invoke by skill name:

```text
Use the planning-router skill on what I have and recommend the smallest useful next move.
```

The `.gemini/commands/` files in this repository are **repo-local convenience wrappers**. Installing the skills does not copy those wrappers into another project. Use natural-language skill invocation unless you intentionally copy/adapt the command files and verify their `@{...}` includes for that project.

See [`docs/gemini-usage.md`](./gemini-usage.md).

## Claude and Claude Design

Build uploadable skill packages:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_claude_skills.py
```

Then upload the ZIPs you need from `dist/claude-skills/` through **Customize → Skills → + → Create skill → Upload a skill** and make sure they are enabled.

Invoke them explicitly when useful:

```text
Use my framing-doc skill on these notes. Separate the problem and outcome from solution ideas. Do not design a solution yet.
```

For repository-authoritative changes, bring accepted decisions back to a repo-aware agent and update the files under `planning/`. See [`docs/claude-skills-installation.md`](./claude-skills-installation.md) and [`docs/claude-design-workflow.md`](./claude-design-workflow.md).

## First run in a product repository

Once the method is available, open the product repository and start with what actually exists. You do not need to rewrite your material into a special format.

If your environment has a router command, use it. Otherwise use the portable prompt:

```text
Use the planning-router skill on what I currently have: notes, requirements, a solution idea, prototype, screenshots, or relevant code.
Choose exactly one smallest planning move that resolves the current consequential uncertainty.
Do not force a fixed sequence. Recommend no planning skill if the change is already small, obvious, and low-risk.
```

Typical outputs live under:

```text
planning/
  frame.md
  shaping.md
  breadboard.md
  slices.md
  context-packet.md
  spikes/
```

Add other artifacts only when their triggering complexity exists.

## The operating loop

**Work where the thinking is happening → open the product repo when a consequential question appears → invoke one skill → save the resolved decision beside the code → carry that accepted state into the next tool, session, or agent.**

For the full grocery-list playthrough, see [`docs/how-it-works-in-practice.md`](./how-it-works-in-practice.md). For exact cross-runtime invocation mappings, see [`docs/agent-invocation-matrix.md`](./agent-invocation-matrix.md).