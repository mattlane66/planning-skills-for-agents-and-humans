import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import axe from 'axe-core';
import { JSDOM, VirtualConsole } from 'jsdom';

const siteDirectory = path.resolve(import.meta.dirname, '..');
const htmlPath = path.join(siteDirectory, 'index.html');
const html = await readFile(htmlPath, 'utf8');
const virtualConsole = new VirtualConsole();
const dom = new JSDOM(html, {
  url: pathToFileURL(htmlPath).href,
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  virtualConsole,
  beforeParse(window) {
    window.scrollTo = () => {};
    window.HTMLElement.prototype.scrollIntoView = () => {};
    window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
    window.ResizeObserver = class { observe() {} unobserve() {} disconnect() {} };
    window.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 120, height: 24 });
    window.SVGElement.prototype.getComputedTextLength = () => 120;
    window.document.execCommand = () => true;
  },
});

const { window } = dom;
const { document } = window;
const wait = (milliseconds = 0) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));
for (let attempts = 0; attempts < 100 && !window.__PLANNING_PORTAL_READY__; attempts += 1) await wait(20);
assert.equal(window.__PLANNING_PORTAL_READY__, true, 'The embedded application did not become ready.');
window.eval(axe.source);

const scenarios = [
  ['collaboration walkthrough', '#/'],
  ['planning compass', '#/compass'],
  ['planning map', '#/map?stage=selected-design'],
  ['skills', '#/skills'],
  ['guide', '#/guides/start-here'],
  ['skill guide', '#/skills/shaping/guide'],
  ['resource', '#/resources/templates%2Fshaping.md'],
  ['example', '#/examples/simple-grocery-list?file=03-breadboard.md'],
];

for (const [label, hash] of scenarios) {
  window.location.hash = hash;
  await wait(30);
  const result = await window.axe.run(document, {
    rules: {
      'color-contrast': { enabled: false },
    },
  });
  assert.equal(result.violations.length, 0, `${label} has automated accessibility violations:\n${JSON.stringify(result.violations.map((violation) => ({
    id: violation.id,
    impact: violation.impact,
    targets: violation.nodes.map((node) => node.target.join(' ')),
  })), null, 2)}`);
}

window.location.hash = '#/';
await wait(25);
for (const [index, label] of [[2, 'requirements matrix'], [3, 'shape comparison'], [4, 'breadboard'], [5, 'slice groups'], [6, 'build handoff'], [7, 'reality comparison']]) {
  document.querySelector(`[data-action="select-walkthrough-stage"][data-stage-index="${index}"]`)?.click();
  await wait(20);
  const stageResult = await window.axe.run(document, { rules: { 'color-contrast': { enabled: false } } });
  assert.equal(stageResult.violations.length, 0, `${label} has automated accessibility violations: ${JSON.stringify(stageResult.violations.map((item) => item.id))}`);
}

window.location.hash = '#/';
await wait(25);
document.querySelector('#search-trigger').click();
await wait(25);
const dialogResult = await window.axe.run(document, {
  rules: {
    'color-contrast': { enabled: false },
  },
});
assert.equal(dialogResult.violations.length, 0, `Search dialog has automated accessibility violations:\n${JSON.stringify(dialogResult.violations.map((violation) => ({
  id: violation.id,
  impact: violation.impact,
  targets: violation.nodes.map((node) => node.target.join(' ')),
})), null, 2)}`);

dom.window.close();
console.log(`Automated accessibility validation passed (${scenarios.length} routes plus search dialog; color contrast covered by deterministic token checks).`);
