import assert from 'node:assert/strict';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';

const siteDirectory = path.resolve(import.meta.dirname, '..');
const htmlPath = path.join(siteDirectory, 'index.html');

function findChrome() {
  const candidates = [
    process.env.CHROME_BIN,
    'google-chrome',
    'google-chrome-stable',
    'chromium',
    'chromium-browser',
  ].filter(Boolean);
  for (const candidate of candidates) {
    const probe = spawnSync(candidate, ['--version'], { encoding: 'utf8' });
    if (probe.status === 0) return { executable: candidate, version: (probe.stdout || probe.stderr).trim() };
  }
  throw new Error(`No Chrome/Chromium executable found. Tried: ${candidates.join(', ')}`);
}

class CdpClient {
  constructor(url) {
    this.url = url;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = new Map();
  }

  async connect() {
    assert.equal(typeof WebSocket, 'function', 'Real-browser smoke requires Node.js with global WebSocket support (Node 22+).');
    this.socket = new WebSocket(this.url);
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('Timed out connecting to Chrome DevTools Protocol')), 10_000);
      this.socket.addEventListener('open', () => {
        clearTimeout(timer);
        resolve();
      }, { once: true });
      this.socket.addEventListener('error', (event) => {
        clearTimeout(timer);
        reject(event.error || new Error('Chrome DevTools Protocol WebSocket failed'));
      }, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(String(event.data));
      if (message.id && this.pending.has(message.id)) {
        const { resolve, reject } = this.pending.get(message.id);
        this.pending.delete(message.id);
        if (message.error) reject(new Error(`${message.error.code}: ${message.error.message}`));
        else resolve(message.result || {});
        return;
      }
      if (message.method) {
        for (const listener of this.listeners.get(message.method) || []) listener(message.params || {});
      }
    });
  }

  on(method, listener) {
    const listeners = this.listeners.get(method) || [];
    listeners.push(listener);
    this.listeners.set(method, listeners);
  }

  call(method, params = {}) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket?.close();
  }
}

async function waitFor(predicate, description, timeoutMs = 12_000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Timed out waiting for ${description}`);
}

async function main() {
  const chrome = findChrome();
  const userDataDir = await mkdtemp(path.join(tmpdir(), 'planning-skills-browser-smoke-'));
  const publisherDir = await mkdtemp(path.join(tmpdir(), 'planning-publisher-browser-smoke-'));
  const publisherHtml = path.join(publisherDir, 'shaped-work.html');
  const publisherSvgDir = path.join(publisherDir, 'boards');
  const repositoryRoot = path.resolve(siteDirectory, '..');
  const publisherRun = spawnSync(
    'python3',
    [
      path.join(repositoryRoot, 'scripts', 'publish-shaped-work.py'),
      '--planning-dir',
      path.join(repositoryRoot, 'tests', 'fixtures', 'planning-publisher-current-contract'),
      '--output',
      publisherHtml,
      '--svg-dir',
      publisherSvgDir,
    ],
    { encoding: 'utf8' },
  );
  assert.equal(
    publisherRun.status,
    0,
    `Planning Publisher fixture generation failed:\n${publisherRun.stderr || publisherRun.stdout}`,
  );
  const publisherUrl = pathToFileURL(publisherHtml).href;
  const targetUrl = process.env.PORTAL_SMOKE_URL || pathToFileURL(htmlPath).href;
  const requiresDirectFile = !process.env.PORTAL_SMOKE_URL;
  const args = [
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-background-networking',
    '--allow-file-access-from-files',
    '--disable-default-apps',
    '--disable-extensions',
    '--disable-sync',
    '--metrics-recording-only',
    '--no-first-run',
    '--remote-debugging-port=0',
    `--user-data-dir=${userDataDir}`,
    targetUrl,
  ];
  const processHandle = spawn(chrome.executable, args, { stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  let debuggingUrl = '';
  processHandle.stderr.setEncoding('utf8');
  processHandle.stderr.on('data', (chunk) => {
    stderr += chunk;
    const match = stderr.match(/DevTools listening on (ws:\/\/[^\s]+)/);
    if (match) debuggingUrl = match[1];
  });

  let client;
  const runtimeErrors = [];
  try {
    await waitFor(() => debuggingUrl, 'Chrome DevTools endpoint');
    const endpoint = new URL(debuggingUrl);
    const targets = await fetch(`http://${endpoint.host}/json/list`).then((response) => response.json());
    const page = targets.find((target) => target.type === 'page' && target.url === targetUrl) || targets.find((target) => target.type === 'page');
    assert.ok(page?.webSocketDebuggerUrl, 'Chrome did not expose the portal page target.');

    client = new CdpClient(page.webSocketDebuggerUrl);
    await client.connect();
    client.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      runtimeErrors.push(`exception: ${exceptionDetails?.text || 'unknown runtime exception'}`);
    });
    client.on('Runtime.consoleAPICalled', ({ type, args: consoleArgs }) => {
      if (!['error', 'assert'].includes(type)) return;
      runtimeErrors.push(`console.${type}: ${(consoleArgs || []).map((entry) => entry.value ?? entry.description ?? '').join(' ')}`);
    });
    client.on('Log.entryAdded', ({ entry }) => {
      if (entry?.level === 'error') runtimeErrors.push(`log.error: ${entry.text}`);
    });
    await Promise.all([
      client.call('Runtime.enable'),
      client.call('Page.enable'),
      client.call('Log.enable'),
    ]);

    const evaluate = async (expression) => {
      const result = await client.call('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
      if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'Runtime.evaluate failed');
      return result.result?.value;
    };

    await waitFor(() => evaluate('window.__PLANNING_PORTAL_READY__ === true'), 'portal readiness');
    assert.equal(await evaluate('document.title'), 'Planning Skills Lab — Watch a plan take shape');
    assert.equal(await evaluate('document.querySelector("h1")?.textContent'), 'Watch a plan take shape.');
    assert.ok(await evaluate('(document.body.textContent || "").length > 1000'), 'Portal rendered too little content.');
    if (requiresDirectFile) assert.equal(await evaluate('location.protocol'), 'file:', 'Smoke test must exercise direct file:// opening.');

    // Exercise a real keyboard activation on the focused Next button.
    await evaluate('document.querySelector(\'[data-action="next-walkthrough-stage"]\').focus(); true');
    assert.equal(await evaluate('document.activeElement?.getAttribute("data-action")'), 'next-walkthrough-stage');
    await client.call('Input.dispatchKeyEvent', {
      type: 'keyDown',
      key: 'Enter',
      code: 'Enter',
      text: '\r',
      unmodifiedText: '\r',
      windowsVirtualKeyCode: 13,
      nativeVirtualKeyCode: 13,
    });
    await client.call('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13 });
    await waitFor(
      () => evaluate('document.querySelector("#walkthrough-stage-title")?.textContent === "Separate the problem from the idea."'),
      'keyboard-driven stage change',
    );

    // Jump to the behavior stage and prove Mermaid rendered in the real browser.
    await evaluate('document.querySelector(\'[data-action="select-walkthrough-stage"][data-stage-index="4"]\').click(); true');
    await waitFor(
      () => evaluate('Boolean(document.querySelector(\'.walkthrough-mermaid[data-processed="true"] svg\'))'),
      'Mermaid SVG rendering',
    );

    // Re-run the initial view at a phone-sized viewport and reject document-level horizontal overflow.
    await client.call('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 1,
      mobile: true,
    });
    await client.call('Page.reload', { ignoreCache: true });
    await waitFor(() => evaluate('window.__PLANNING_PORTAL_READY__ === true'), 'mobile portal readiness');
    assert.ok(await evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Phone viewport has document-level horizontal overflow.');
    assert.equal(await evaluate('window.innerWidth'), 390);

    // Exercise the generated Planning Publisher artifact in the same real browser.
    await client.call('Emulation.clearDeviceMetricsOverride');
    await client.call('Page.navigate', { url: publisherUrl });
    await waitFor(
      () => evaluate('document.title === "Checkout Assist · Shaped Work"'),
      'Planning Publisher shaped-work page',
    );
    assert.ok(
      await evaluate('Boolean(document.querySelector('[data-plan-id="SK1"]'))'),
      'Targeted sketch did not render with its stable ID.',
    );
    assert.equal(
      await evaluate('document.querySelector("details.shape-alt")?.open'),
      false,
      'Unselected candidate should be collapsed by default.',
    );

    await evaluate('document.querySelector('[data-plan-id="U1"]').click(); true');
    await waitFor(
      () => evaluate('document.querySelectorAll('[data-plan-id="U1"].hit').length > 0'),
      'stable-ID inspector highlight',
    );
    assert.ok(
      await evaluate('document.querySelector("#inspector")?.classList.contains("show")'),
      'Stable-ID inspector did not open.',
    );

    await evaluate('document.querySelector('[data-scope="V1"]').click(); true');
    await waitFor(
      () => evaluate('document.body.classList.contains("scope-mode")'),
      'slice isolation mode',
    );
    assert.ok(
      await evaluate('document.querySelectorAll("[data-plan-id].dim").length > 0'),
      'Slice isolation did not dim out-of-scope planning elements.',
    );
    await evaluate('document.querySelector('[data-scope=""]').click(); true');
    await waitFor(
      () => evaluate('!document.body.classList.contains("scope-mode")'),
      'full-system restoration',
    );

    await client.call('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 1,
      mobile: true,
    });
    await client.call('Page.reload', { ignoreCache: true });
    await waitFor(
      () => evaluate('document.readyState === "complete" && document.title === "Checkout Assist · Shaped Work"'),
      'mobile Planning Publisher readiness',
    );
    assert.ok(
      await evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'),
      'Planning Publisher phone viewport has document-level horizontal overflow.',
    );

    assert.deepEqual(runtimeErrors, [], `Real browser reported runtime errors:\n${runtimeErrors.join('\n')}`);
    console.log(`PASS real-browser smoke: ${chrome.version}`);
    console.log(`PASS ${requiresDirectFile ? 'direct file:// open, ' : ''}portal interactions + generated Planning Publisher stable-ID/slice/mobile interactions`);
  } finally {
    client?.close();
    processHandle.kill('SIGTERM');
    await Promise.race([
      new Promise((resolve) => processHandle.once('exit', resolve)),
      new Promise((resolve) => setTimeout(resolve, 2_000)),
    ]);
    await rm(userDataDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
    await rm(publisherDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  }
}

await main();
