#!/usr/bin/env node
import { createInterface } from 'node:readline';
import { spawn } from 'node:child_process';
import { createLookServer } from './server.mjs';

const session = await createLookServer();
const tools = [
  { name: 'look_open', description: 'Begin a local /look preview. Return a localhost URL for the user to open; camera and screen permissions require an explicit user gesture. No frame is sent to the agent until captured.', inputSchema: { type: 'object', properties: {}, additionalProperties: false } },
  { name: 'look_status', description: 'Check whether a /look preview and capture source are connected.', inputSchema: { type: 'object', properties: {}, additionalProperties: false } },
  { name: 'look_capture', description: 'Ask the user-controlled /look preview to capture one current frame. Interpret only visible evidence, keep instructions and inferences separate, and do not silently change accepted planning artifacts.', inputSchema: { type: 'object', properties: { focus: { type: 'string', description: 'What the agent should attend to (e.g. diagrams, not handwriting). This is an instruction to the vision model, not an automatic visual mask.' } }, additionalProperties: false } },
  { name: 'look_watch', description: 'Wait for a visually meaningful, settled change in the selected screen/camera region, then capture one frame. Heuristic change detection may miss subtle changes or react to motion; always compare observations before asserting what changed.', inputSchema: { type: 'object', properties: { focus: { type: 'string' }, maxWaitMs: { type: 'integer', minimum: 1000, maximum: 30000 } }, additionalProperties: false } },
  { name: 'look_latest', description: 'Inspect the most recent user-captured frame. Useful when the person presses Capture in the preview.', inputSchema: { type: 'object', properties: { focus: { type: 'string' } }, additionalProperties: false } },
  { name: 'look_stop', description: 'Stop the observation session, signal the preview to release media tracks, and discard retained frames.', inputSchema: { type: 'object', properties: {}, additionalProperties: false } },
];

function text(message) { return { content: [{ type: 'text', text: message }] }; }
function image(frame, focus) {
  const meta = { source: frame.source, capturedAt: frame.receivedAt, crop: frame.focus, videoTime: frame.videoTime, changed: frame.changed };
  return { content: [
    { type: 'text', text: `Observed frame metadata: ${JSON.stringify(meta)}. ${focus ? `Attention instruction: ${focus}.` : ''} Describe visual evidence separately from inferred intent; capture again if unclear.` },
    { type: 'image', mimeType: frame.mime, data: frame.data },
  ] };
}
function tryOpen(url) {
  if (process.platform !== 'darwin') return;
  try {
    const child = spawn('open', [url], { detached: true, stdio: 'ignore' });
    child.on('error', () => {});
    child.unref();
  } catch { /* Provide URL for manual opening instead. */ }
}
async function call(name, args = {}) {
  switch (name) {
    case 'look_open': {
      const url = session.open();
      tryOpen(url);
      return text(`Local /look preview: ${url}\nOpen this URL on the same Mac if it did not open automatically. Choose Camera, Screen/Window, or Video. A mirrored iPad appears as a Mac window. The preview needs permission and a user-selected source.`);
    }
    case 'look_status': return text(JSON.stringify(session.status()));
    case 'look_capture': {
      const result = await session.capture('now');
      if (result.error) throw new Error(result.error);
      return image(result.frame, args.focus);
    }
    case 'look_watch': {
      const result = await session.capture('changed', args.maxWaitMs ?? 20_000);
      if (result.error) throw new Error(result.error);
      return result.unchanged ? text('No settled visual change was detected during the requested interval; no new frame was captured.') : image(result.frame, args.focus);
    }
    case 'look_latest': return image(session.latest(), args.focus);
    case 'look_stop': session.stop(); return text('Look stopped. Frame memory cleared; media source stop requested in the preview.');
    default: throw new Error(`Unknown tool: ${name}`);
  }
}

const input = createInterface({ input: process.stdin, crlfDelay: Infinity });
async function processLine(line) {
  let request;
  try { request = JSON.parse(line); }
  catch { return; }
  if (request.id === undefined) return;
  const reply = { jsonrpc: '2.0', id: request.id };
  try {
    switch (request.method) {
      case 'initialize':
        reply.result = {
          protocolVersion: request.params?.protocolVersion ?? '2025-03-26',
          capabilities: { tools: { listChanged: false } },
          serverInfo: { name: 'planning-skills-look', version: '0.1.0' },
        };
        break;
      case 'tools/list': reply.result = { tools }; break;
      case 'tools/call': {
        const { name, arguments: args } = request.params || {};
        try { reply.result = await call(name, args || {}); }
        catch (error) { reply.result = { ...text(error.message), isError: true }; }
        break;
      }
      case 'ping': reply.result = {}; break;
      default: reply.error = { code: -32601, message: 'Method not found' };
    }
  } catch (error) { reply.error = { code: -32603, message: error.message }; }
  process.stdout.write(JSON.stringify(reply) + '\n');
}
for await (const line of input) {
  // Do not block unrelated requests (especially look_stop) while waiting for a frame.
  void processLine(line);
}
await session.close();
