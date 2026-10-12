#!/usr/bin/env node
// Capture the real DWC Requests Shaping Board for the README preview.
// Uses the Chrome/Chromium installed on GitHub-hosted Ubuntu runners.
import { spawn, spawnSync } from 'node:child_process';
import { mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

const output = process.argv[2];
if (!output) throw new Error('Usage: node scripts/capture-shaping-board-preview.mjs output.png');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const boardUrl = pathToFileURL(path.join(root, 'site/shaping-board/index.html')).href;
const chrome = [process.env.CHROME_BIN, 'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']
  .filter(Boolean).find(bin => spawnSync(bin, ['--version'], { encoding: 'utf8' }).status === 0);
if (!chrome) throw new Error('Chrome or Chromium is needed to capture the Shaping Board preview');

const profile = await mkdtemp(path.join(tmpdir(), 'shaping-board-preview-'));
const browser = spawn(chrome, [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
  '--disable-background-networking', '--allow-file-access-from-files',
  '--no-first-run', '--disable-extensions', '--disable-sync',
  '--force-device-scale-factor=1', '--window-size=1600,950',
  '--remote-debugging-port=0', '--user-data-dir=' + profile, boardUrl,
], { stdio: ['ignore', 'ignore', 'pipe'] });
let stderr = '';
browser.stderr.on('data', chunk => { stderr += chunk; });
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
let socket;
const pending = new Map();
let nextId = 1;
try {
  let endpoint;
  for (let i = 0; i < 200; i++) {
    try {
      const [port] = (await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).trim().split(/\r?\n/);
      if (/^\d+$/.test(port)) {
        const targets = await fetch('http://127.0.0.1:' + port + '/json/list').then(r => r.json());
        endpoint = targets.find(x => x.type === 'page' && x.url === boardUrl)?.webSocketDebuggerUrl;
        if (endpoint) break;
      }
    } catch (error) {
      if (error?.code !== 'ENOENT' && !(error instanceof TypeError)) throw error;
    }
    if (browser.exitCode !== null) throw new Error('Chrome stopped: ' + stderr);
    await delay(100);
  }
  if (!endpoint) throw new Error('Chrome debugging endpoint did not start: ' + stderr);
  socket = new WebSocket(endpoint);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, { once: true });
    socket.addEventListener('error', reject, { once: true });
  });
  socket.addEventListener('message', event => {
    const payload = JSON.parse(String(event.data));
    if (!pending.has(payload.id)) return;
    const { resolve, reject } = pending.get(payload.id);
    pending.delete(payload.id);
    payload.error ? reject(new Error(payload.error.message)) : resolve(payload.result || {});
  });
  const call = (method, params = {}) => new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
  const evaluate = async expression => {
    const result = await call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
    return result.result?.value;
  };
  await call('Runtime.enable');
  await call('Emulation.setDeviceMetricsOverride', { width: 1600, height: 950, deviceScaleFactor: 1, mobile: false });
  await call('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
  let ready = false;
  for (let i = 0; i < 100; i++) {
    if (await evaluate('document.querySelectorAll("[data-view=cmp]").length === 1 && document.querySelectorAll("[data-view=paths]").length >= 1')) {
      ready = true;
      break;
    }
    await delay(100);
  }
  if (!ready) throw new Error('The real Shaping Board did not render');
  await evaluate('document.querySelector("[data-view=cmp]").click(); document.fonts.ready.then(() => true)');
  if (!await evaluate('document.querySelectorAll(".cm").length === 4')) {
    throw new Error('Candidate comparison view is incomplete');
  }
  const { data } = await call('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
  const screenshot = Buffer.from(data, 'base64');
  if (screenshot.length < 10000) throw new Error('Screenshot unexpectedly small');
  await writeFile(output, screenshot);
  console.log('Captured Shaping Board preview: ' + screenshot.length + ' bytes');
} finally {
  socket?.close();
  browser.kill('SIGTERM');
  await delay(250);
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}
