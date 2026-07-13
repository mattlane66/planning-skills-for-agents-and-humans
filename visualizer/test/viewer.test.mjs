import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { extractMermaidBlocks } from '../src/markdown.mjs';
import { parseArgs } from '../src/cli.mjs';
import { startViewer } from '../src/server.mjs';

test('extracts multiple Mermaid fences with their nearest headings', () => {
  const diagrams = extractMermaidBlocks(`# System\n\n\`\`\`mermaid\nflowchart LR\n A --> B\n\`\`\`\n\n## Retry\n\n~~~mermaid\nstateDiagram-v2\n A --> B\n~~~`, 'plan.md');
  assert.equal(diagrams.length, 2);
  assert.deepEqual(diagrams.map(({ title, startLine }) => ({ title, startLine })), [
    { title: 'System', startLine: 4 },
    { title: 'Retry', startLine: 11 },
  ]);
});

test('parses viewer CLI options', () => {
  assert.deepEqual(parseArgs(['--port', '0', '--host', 'localhost', '--no-open', 'plan.md']), {
    host: 'localhost',
    port: 0,
    open: false,
    filePaths: ['plan.md'],
  });
  assert.throws(() => parseArgs(['--port', 'invalid', 'plan.md']), /Port must be an integer/);
});

test('serves diagrams and broadcasts a reload when a watched file changes', async () => {
  const directory = await mkdtemp(join(tmpdir(), 'planning-viewer-'));
  const filePath = join(directory, 'plan.md');
  await writeFile(filePath, '# First\n\n```mermaid\nflowchart LR\n A --> B\n```\n');
  const viewer = await startViewer({ filePaths: [filePath], port: 0, watchIntervalMs: 25 });
  const eventsController = new AbortController();
  const eventTimeout = setTimeout(() => eventsController.abort(), 5000);

  try {
    const home = await fetch(viewer.url);
    assert.equal(home.status, 200);
    const homeHtml = await home.text();
    assert.match(homeHtml, /Planning Diagram Viewer/);
    assert.match(homeHtml, /renderInFlight/);
    assert.match(homeHtml, /colorScheme\.matches \? 'dark' : 'default'/);
    assert.match(homeHtml, /colorScheme\.addEventListener\('change'/);
    assert.match(homeHtml, /JSON\.stringify\(error, null, 2\)/);

    const first = await (await fetch(`${viewer.url}/api/diagrams`)).json();
    assert.equal(first.files[0].diagrams.length, 1);

    const vendor = await fetch(`${viewer.url}/vendor/mermaid.esm.min.mjs`);
    assert.equal(vendor.status, 200);
    assert.match(vendor.headers.get('content-type'), /javascript/);

    const events = await fetch(`${viewer.url}/events`, { signal: eventsController.signal });
    assert.equal(events.status, 200);
    assert.ok(events.body);
    const eventReader = events.body.getReader();
    const decoder = new TextDecoder();
    const ready = await eventReader.read();
    assert.match(decoder.decode(ready.value), /event: ready/);

    await writeFile(filePath, '# First\n\n```mermaid\nflowchart LR\n A --> B\n```\n\n## Second\n\n```mermaid\nflowchart TD\n C --> D\n```\n');

    let eventText = '';
    while (!eventText.includes('event: reload')) {
      const event = await eventReader.read();
      if (event.done) break;
      eventText += decoder.decode(event.value, { stream: true });
    }
    clearTimeout(eventTimeout);
    assert.match(eventText, /event: reload/);
    await eventReader.cancel();

    let updated;
    const deadline = Date.now() + 2000;
    while (Date.now() < deadline) {
      updated = await (await fetch(`${viewer.url}/api/diagrams`)).json();
      if (updated.revision > first.revision && updated.files[0].diagrams.length === 2) break;
      await new Promise((resolve) => setTimeout(resolve, 40));
    }
    assert.ok(updated.revision > first.revision);
    assert.equal(updated.files[0].diagrams.length, 2);
  } finally {
    clearTimeout(eventTimeout);
    eventsController.abort();
    await viewer.close();
    await rm(directory, { recursive: true, force: true });
  }
});
