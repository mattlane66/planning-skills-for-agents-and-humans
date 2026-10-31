---
description: Open the optional local Look preview to observe a paper sketch, screen, mirrored iPad, or video through the user-approved MCP bridge.
argument-hint: visual region or behavior to observe
---

Use the optional `look` MCP server tools if available. Call `look_open` to give the user a local preview and let them explicitly select Camera, Screen/Window, or Recording. Do not claim access to a camera or screen before the user has granted permission and selected a source.

Then follow the user's attention instructions:

$ARGUMENTS

Use `look_capture` to inspect the current view, `look_watch` for a bounded settled-change capture, and `look_latest` for a manually captured frame. Capture an initial frame before comparing changes. Do not infer hidden behavior or interpret unreadable handwriting as intent. If reconciling planning artifacts, read `sketch-reconciliation/SKILL.md` and preserve its observation, provenance, stable ID, and human decision gates. End the observation session with `look_stop` when requested.

If the MCP tools are not connected, explain how to configure them from `look/README.md` rather than pretending a camera is available.
