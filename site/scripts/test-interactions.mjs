import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { JSDOM, VirtualConsole } from 'jsdom';

const siteDirectory = path.resolve(import.meta.dirname, '..');
const htmlPath = path.join(siteDirectory, 'index.html');
const html = await readFile(htmlPath, 'utf8');
const runtimeErrors = [];
const virtualConsole = new VirtualConsole();
virtualConsole.on('error', (message) => runtimeErrors.push(String(message)));
virtualConsole.on('jsdomError', (error) => runtimeErrors.push(error.message));

const dom = new JSDOM(html, {
  url: pathToFileURL(htmlPath).href,
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  virtualConsole,
  beforeParse(window) {
    window.scrollTo = () => {};
    window.HTMLElement.prototype.scrollIntoView = () => {};
    window.matchMedia = (query) => ({
      matches: /max-width:\s*900px/.test(query) && window.innerWidth <= 900,
      addEventListener() {},
      removeEventListener() {},
    });
    window.ResizeObserver = class {
      observe() {}
      unobserve() {}
      disconnect() {}
    };
    window.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 120, height: 24 });
    window.SVGElement.prototype.getComputedTextLength = () => 120;
    window.document.execCommand = () => true;
  },
});

const { window } = dom;
const { document } = window;
const wait = (milliseconds = 0) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));
const route = async (hash) => {
  window.location.hash = hash;
  await wait(20);
};
const click = async (selector) => {
  const target = document.querySelector(selector);
  assert.ok(target, `Expected interactive target: ${selector}`);
  target.click();
  await wait(20);
  return target;
};

for (let attempts = 0; attempts < 100 && !window.__PLANNING_PORTAL_READY__; attempts += 1) {
  await wait(20);
}

assert.equal(window.__PLANNING_PORTAL_READY__, true, 'The embedded application did not become ready.');
assert.equal(document.title, 'Planning Skills — From fuzzy work to a buildable plan');
assert.equal(document.querySelector('h1')?.textContent, 'Turn fuzzy work into a buildable plan.');
assert.ok((document.body.textContent || '').length > 1_000, 'The initial page rendered too little content.');

await click('[data-action="select-entry"][data-entry="uncertainty"]');
assert.equal(document.querySelector('.recommendation h2')?.textContent, 'Planning Router');
assert.equal(document.querySelector('[data-entry="uncertainty"]')?.getAttribute('aria-checked'), 'true');

await click('#search-trigger');
const search = document.querySelector('#global-search');
assert.equal(document.activeElement, search, 'Opening search should focus its input.');
search.value = 'statechart retries';
search.dispatchEvent(new window.Event('input', { bubbles: true }));
await wait(20);
assert.match(document.querySelector('.search-results')?.textContent || '', /Statechart/i);
document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
await wait(20);
assert.equal(document.querySelector('.search-dialog'), null, 'Escape should close search.');

await route('#/skills');
assert.equal(document.querySelector('main h1')?.textContent, 'Skills');
await click('[data-action="filter-skills"][data-category="conditional"]');
assert.match(document.querySelector('.skill-groups')?.textContent || '', /Statechart/);
await click('[data-action="select-skill"][data-skill="statechart"]');
assert.equal(document.querySelector('.skill-detail h2')?.textContent, 'Statechart');
await click('[data-action="copy-skill-prompt"][data-skill="statechart"]');
assert.match(document.querySelector('#toast-region')?.textContent || '', /Copied to clipboard/);

const guideLink = document.querySelector('.skill-detail a[href="#/skills/statechart/guide"]');
assert.ok(guideLink, 'The selected skill should link to its authoritative guide.');
guideLink.click();
await wait(40);
assert.ok(document.querySelector('.docs-article'), 'The skill guide should render after navigation.');
assert.match(document.querySelector('.docs-article')?.textContent || '', /statechart/i);

await route('#/examples/simple-grocery-list?file=02-shaping.md');
assert.match(document.querySelector('.example-heading h1')?.textContent || '', /Simple Grocery List/);
assert.ok(document.querySelector('.artifact-stage.is-selected'), 'The selected example artifact should be visible.');
await click('.learning-notes [data-action="copy-text"]');
assert.match(document.querySelector('#toast-region')?.textContent || '', /Copied to clipboard/);

await route('#/');
Object.defineProperty(window, 'innerWidth', { configurable: true, value: 390 });
await click('[data-action="toggle-menu"]');
assert.ok(document.querySelector('.primary-nav.is-open'), 'The mobile menu should open.');
assert.equal(document.querySelector('.menu-button')?.getAttribute('aria-expanded'), 'true');
await click('[data-action="toggle-menu"]');
assert.equal(document.querySelector('.primary-nav.is-open'), null, 'The mobile menu should close.');
assert.equal(document.querySelector('.menu-button')?.getAttribute('aria-expanded'), 'false');

await route('#/skills');
await click('[data-action="select-skill"][data-skill="statechart"]');
assert.equal(document.activeElement?.id, 'skill-detail-title', 'Selecting a skill on mobile should move focus to its updated detail.');

await route('#/guides/start-here');
assert.ok(document.querySelector('.docs-mobile-disclosure'), 'Mobile documentation should expose a compact disclosure navigation.');

assert.deepEqual(runtimeErrors, [], `Runtime errors were reported:\n${runtimeErrors.join('\n')}`);
dom.window.close();

console.log('Direct-open interaction validation passed (home, navigator, search, skills, guide, example, copy, and mobile menu).');
