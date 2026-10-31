# Look — optional local visual observation for planning agents

`/look` connects a user-controlled camera, screen/window share, mirrored iPad, or saved screen recording to a vision-capable MCP agent. It is an **input tool**, not a sixteenth Planning Skill or a new authority layer. Frames are observations, not proof of intent, hidden interactions, or authorization to change accepted plans.

## Requirements

- Node.js 20 or later (no npm dependencies).
- Recent browser with camera/screen APIs; `http://127.0.0.1` is treated as a trustworthy local origin in modern browsers.
- A local agent that can connect to an MCP stdio server **and inspect image content**. The transport returns JPEG images as MCP image blocks; vision support depends on the host/model.
- Camera, screen, window, or mirroring permissions must be granted by the human in the browser. `/look` cannot silently activate a camera or screen.

## Use with Codex

Install/configure the optional MCP bridge in your Codex MCP configuration (using an **absolute** path):

```toml
[mcp_servers.look]
command = "node"
args = ["/absolute/path/to/planning-skills-for-agents-and-humans/look/src/mcp.mjs"]
```

Restart the agent to load the tool. In a Codex conversation, ask:

```text
Open Look. I will select the screen where my iPad is mirrored. Look at the rectangles,
not the handwriting. Capture a frame now, then watch for a settled change.
Compare the two visible arrangements and propose updates to my working breadboard.
Do not change accepted planning artifacts without my approval.
```

The agent can invoke `look_open`, `look_capture`, `look_watch`, `look_latest`, `look_status`, and `look_stop`. Codex's client UI may **not** register literal `/look` slash commands; the skill/tool prompt and MCP bridge are the portable invocation. Claude Code may use the optional repository command `.claude/commands/look.md` when the MCP bridge is connected.

## Standalone preview (for local UI checks)

```bash
cd look
npm run start
```

The command prints a local URL and attempts to open it on macOS. This preview alone does **not** send images to an agent: use the MCP connection for agent-driven observation.

## What the person can show

| Source | How to use it |
| --- | --- |
| Paper or whiteboard | Choose **Camera**, grant webcam permission and point it at the work. |
| Figma or an app | Choose **Screen / window**, then select the app window, screen or browser tab the browser offers. |
| iPad + Apple Pencil | Mirror the iPad to your Mac using a supported wired or wireless method, then share the **mirroring window**. No native iPad app is included. |
| Existing screen recording | Choose **Recording**, select a local video, play/pause or scrub to the desired time, then capture or watch. No video is uploaded as a file. |

Drag in the preview to crop a region; **Reset selection** returns to full frame. Cropping is the reliable way to exclude handwriting or other unrelated content. A textual `focus` argument tells the vision model where to attend, but is **not** a privacy mask.

- `look_capture`: capture the current frame, returning an image to the agent.
- `look_watch`: start from the current view, wait up to 30 seconds for a visually changed and then relatively stable view, return one frame. Detection uses a lightweight pixel-difference heuristic—not semantic judgment and not guaranteed event detection. Take an initial frame before calling this tool when comparing before/after states.
- **Capture frame** in the preview + `look_latest`: a human decides the exact moment, then asks the agent to inspect that image.
- `look_stop`: clears images held by the local bridge and tells the browser to release media tracks. The preview's **Stop** button can also stop sharing. Closing the preview releases browser media tracks.

To preserve context, ask the agent to describe `VISIBLE` evidence separately from `NARRATED` instructions and `INFERRED` interpretations, then follow the normal `shaping`, `breadboarding`, or `sketch-reconciliation` gates. A sequence of frames does not automatically reveal behavior, save operations, or what a person meant.

## Security and limits

- Loopback-only server on a random port; per-process random token on privileged API requests; no permissive CORS; no external scripts, external requests, audio capture, or cloud storage.
- Frames stay **in process memory** until stopped, overwritten, or the MCP process exits. They are sent to the connected agent **when a capture tool is called**; the agent/provider may process and retain them under its own policies. Do not assume end-to-end local image analysis.
- No persisted recordings, repository commits, telemetry, microphone capture, or automatic screenshot uploads. Imported videos stay in the local browser; selected JPEG frames may be transmitted to the agent.
- The localhost URL embeds a bearer token. Treat it as private. The HTTP service is intended for a trusted personal workstation, not multi-user machines or exposure through a tunnel/proxy.
- Screen permission UX and browser support vary. Browser-level sharing and camera permissions cannot be bypassed by an agent. Some DRM-protected video sources cannot be captured.
- Browser throttling, camera movement, changes in lighting, and small strokes affect `look_watch`. This is **bounded observation**, not continuous unattended autonomous monitoring.
- Tested in this environment: protocol handshake, authenticated HTTP, manual and requested frame paths, change/no-change responses, stop/restart lifecycle. **Not yet validated on a physical Mac, iPad, or real webcam.**

## Development

```bash
cd look
npm run check
```

This checks Node syntax and runs integration tests without a camera. A physical acceptance test should cover: webcam permission, screen capture, iPad mirroring, video scrubbing, crop accuracy (including portrait orientation), capture during edits, denied permissions, and Stop revocation. The preview is intentionally self-contained and dependency-free.
