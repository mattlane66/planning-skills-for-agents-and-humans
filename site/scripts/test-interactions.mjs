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
virtualConsole.on('warn', (message) => runtimeErrors.push(String(message)));
virtualConsole.on('jsdomError', (error) => runtimeErrors.push(error.message));

const dom = new JSDOM(html, {
  url: pathToFileURL(htmlPath).href,
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  virtualConsole,
  beforeParse(window) {
    window.scrollTo = () => {};
    window.__scrollIntoViewCalls = [];
    window.HTMLElement.prototype.scrollIntoView = function scrollIntoView(options) {
      window.__scrollIntoViewCalls.push({ label: this.getAttribute?.('aria-label') || '', options });
    };
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
assert.equal(document.title, 'Planning Skills Lab — Watch a plan take shape');
assert.equal(document.querySelector('h1')?.textContent, 'Watch a plan take shape.');
assert.ok((document.body.textContent || '').length > 1_000, 'The initial page rendered too little content.');
assert.equal(document.querySelectorAll('.walkthrough-progress li').length, 8);
assert.equal(document.querySelectorAll('.walkthrough-ledger li').length, 8);
assert.equal(document.querySelectorAll('.walkthrough-ledger li.is-done').length, 0);
assert.equal(document.querySelector('.walkthrough-progress [aria-current="step"] strong')?.textContent, 'Source');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Start with the messy reality.');
assert.equal(document.querySelectorAll('.collaboration-timeline li').length, 3);
assert.ok(document.querySelector('.walkthrough-input'));
assert.ok(document.querySelector('.walkthrough-output'));
assert.equal(document.querySelector('.decision-options'), null, 'The walkthrough must not render quiz choices.');
assert.equal(document.querySelector('[data-action="select-lab-answer"]'), null, 'The retired quiz action must be absent.');
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /No skill required yet[\s\S]*plugin makes a skill available/i);
assert.equal(document.querySelector('.optional-skill-moments')?.open, false, 'Optional skills should stay compact until requested.');
await click('.optional-skill-moments > summary');
assert.equal(document.querySelector('.optional-skill-moments')?.open, true);
assert.match(document.querySelector('.skill-moment')?.textContent || '', /Planning Router[\s\S]*recommend exactly one smallest next move/i);
assert.match(document.querySelector('.skill-moment .invocation-shortcuts')?.textContent || '', /\/planning-skills:plan[\s\S]*\/plan/i);
await click('.skill-moment .invocation-surface.is-portable .invocation-copy');
assert.match(document.querySelector('#toast-region')?.textContent || '', /Copied to clipboard/);

await click('[data-action="next-walkthrough-stage"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Separate the problem from the idea.');
assert.equal(document.querySelectorAll('.walkthrough-ledger li.is-done').length, 1);
assert.match(document.querySelector('.walkthrough-output')?.textContent || '', /Problem: needed-item state is easy to lose/i);
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Run this move with Framing Doc[\s\S]*\/planning-skills:frame/i);
assert.match(document.querySelector('.optional-skill-moments')?.textContent || '', /Wayfinding[\s\S]*Skipped here/i);

await click('[data-action="next-walkthrough-stage"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Agree on what will judge the options.');
assert.equal(document.querySelector('#stage-visual-title')?.textContent, 'Accepted requirements matrix');
assert.equal(document.querySelectorAll('.requirements-matrix tbody tr').length, 6);
assert.equal(document.querySelectorAll('.accepted-check').length, 6);
assert.match(document.querySelector('.appetite-boundary')?.textContent || '', /A few focused days[\s\S]*No accounts/i);
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Run this move with Shaping[\s\S]*requirements, Appetite, and a cut line/i);

await click('[data-action="select-walkthrough-stage"][data-stage-index="3"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Select a direction.');
assert.match(document.querySelector('.collaboration-timeline')?.textContent || '', /Choose A/i);
assert.match(document.querySelector('.walkthrough-output')?.textContent || '', /One items store/i);
assert.equal(document.querySelectorAll('.walkthrough-ledger li.is-done').length, 3);
assert.match(document.querySelector('.walkthrough-ledger li.is-current')?.textContent || '', /Selected shape A/i);
assert.equal(document.querySelectorAll('.shape-path-button').length, 2);
assert.equal(document.querySelectorAll('.shape-fit-matrix .fit-check').length, 12);
assert.match(document.querySelector('.fit-gate-explainer')?.textContent || '', /Fit is a gate, not a score[\s\S]*both A and B meet R0–R5/i);
assert.equal(document.querySelectorAll('.shape-tradeoff-table tbody tr').length, 4);
assert.match(document.querySelector('.human-shape-decision')?.textContent || '', /Why the human selected Shape A[\s\S]*simpler for a first version/i);
assert.match(document.querySelector('.shape-path-detail')?.textContent || '', /Single list \+ filter[\s\S]*Recorded authority/i);
assert.match(document.querySelector('.optional-skill-moments')?.textContent || '', /Sketch Reconciliation[\s\S]*visual may change the plan/i);
await click('[data-action="inspect-shape"][data-shape="b"]');
assert.equal(document.querySelector('[data-action="inspect-shape"][data-shape="b"]')?.getAttribute('aria-pressed'), 'true');
assert.match(document.querySelector('.shape-path-detail')?.textContent || '', /Needed \+ Bought sections[\s\S]*not build scope/i);
assert.ok(document.querySelector('.shape-path-button.is-selected[data-shape="a"]'), 'Inspecting B must not change the recorded selection of A.');

await click('[data-action="next-walkthrough-stage"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Make the selected idea behave.');
assert.match(document.querySelector('.collaboration-timeline')?.textContent || '', /Accept that behavior/i);
assert.match(document.querySelector('.walkthrough-output')?.textContent || '', /duplicate check/i);
assert.equal(document.querySelector('#stage-visual-title')?.textContent, 'Selected-design breadboard');
assert.ok(document.querySelector('.walkthrough-breadboard .walkthrough-mermaid'), 'The behavior stage should render the breadboard diagram.');
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Run this move with Breadboarding[\s\S]*selected-design/i);
assert.match(document.querySelector('.optional-skill-moments')?.textContent || '', /Statechart[\s\S]*lifecycle behavior/i);
for (let attempts = 0; attempts < 50 && !document.querySelector('.walkthrough-mermaid svg'); attempts += 1) await wait(20);
assert.ok(document.querySelector('.walkthrough-mermaid[data-processed="true"] svg'), 'Mermaid should transform the canonical breadboard text into an SVG.');
assert.match(document.querySelector('.breadboard-canvas')?.textContent || '', /P1 Grocery list page[\s\S]*P2 Duplicate feedback[\s\S]*P3 Local storage/i);

await click('[data-action="next-walkthrough-stage"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Choose one buildable result.');
assert.equal(document.querySelector('#stage-visual-title')?.textContent, 'Tasks become vertical, judgeable groups');
assert.equal(document.querySelectorAll('.task-group-card').length, 2);
assert.equal(document.querySelectorAll('.task-group-card > ol li').length, 6);
assert.match(document.querySelector('.task-group-card.is-active')?.textContent || '', /TG1 · V1[\s\S]*T1[\s\S]*T2[\s\S]*T3/i);
assert.match(document.querySelector('.task-group-dependency')?.textContent || '', /item model and persistence boundary/i);
assert.match(document.querySelector('.dumplink-context')?.textContent || '', /full Dumplink artifact is optional/i);
assert.match(document.querySelector('.task-group-gate')?.textContent || '', /sequence does not activate scope/i);
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Select directly when the slice is obvious/i);
assert.deepEqual(
  [...document.querySelectorAll('.skill-moment h3')].map((item) => item.textContent),
  ['Dumplink', 'Interface Contracts', 'Executable Breadboards'],
);

await click('[data-action="select-walkthrough-stage"][data-stage-index="6"]');
assert.equal(document.querySelector('main h1')?.textContent, 'The planning handoff is ready.');
assert.ok(window.__scrollIntoViewCalls.some((call) => /7\. Handoff, current/.test(call.label) && call.options?.inline === 'center'), 'The active stage should stay centered in the mobile progress rail.');
assert.match(document.querySelector('.walkthrough-intro > p')?.textContent || '', /Target-repository context completes the build-agent packet/i);
assert.equal(document.querySelectorAll('.assembly-card').length, 3);
assert.match(document.querySelector('.assembly-flow')?.textContent || '', /Planning context[\s\S]*Target-repository context[\s\S]*Complete build-agent packet/i);
assert.equal(document.querySelectorAll('.packet-row').length, 5);
assert.deepEqual(
  [...document.querySelectorAll('.packet-row h3')].map((item) => item.textContent),
  ['Build', 'Preserve', 'Do not build yet', 'Verify', 'Return to planning if'],
);
assert.match(document.querySelector('.packet-row.tone-human')?.textContent || '', /categories[\s\S]*store logic/i);
assert.match(document.querySelector('.packet-row:last-child')?.textContent || '', /split across collections/i);
assert.equal(document.querySelector('#packet-title')?.textContent, 'What planning contributes');
assert.equal(document.querySelectorAll('.packet-detail').length, 4);
assert.equal(document.querySelector('[data-packet-section="scope-authority"]')?.open, true);
assert.match(document.querySelector('[data-packet-section="repository-context"]')?.textContent || '', /intentionally not invented here[\s\S]*Resolve in target repo/i);
await click('[data-packet-section="repository-context"] > summary');
assert.equal(document.querySelector('[data-packet-section="repository-context"]')?.open, true, 'The full handoff sections should be inspectable in place.');
assert.match(document.querySelector('[data-packet-section="execution-verification"]')?.textContent || '', /Goal condition[\s\S]*Return to planning[\s\S]*Finish line/i);
assert.equal(document.querySelectorAll('.provenance-ledger li').length, 6);
assert.match(document.querySelector('.walkthrough-exchange.is-compact')?.textContent || '', /Build agent/i);
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Run this move with Feed Planning Context[\s\S]*\/planning-skills:feed-context/i);
assert.match(document.querySelector('.optional-skill-moments')?.textContent || '', /Kickoff Doc[\s\S]*orientation/i);

await click('[data-action="next-walkthrough-stage"]');
assert.equal(document.querySelector('main h1')?.textContent, 'Compare the plan with reality.');
assert.match(document.querySelector('.collaboration-timeline')?.textContent || '', /separate array/i);
assert.match(document.querySelector('.walkthrough-output')?.textContent || '', /restore one items store/i);
assert.match(document.querySelector('.walkthrough-invocation')?.textContent || '', /Run this move with Breadboard Reflection[\s\S]*\/planning-skills:reflect-breadboard/i);
await click('[data-action="reset-walkthrough"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Start with the messy reality.');

await route('#/compass');
assert.equal(document.querySelector('h1')?.textContent, 'What is happening in your work?');

await click('[data-action="select-entry"][data-entry="candidate"]');
assert.equal(document.querySelector('.recommendation h2')?.textContent, 'Candidate-shape breadboard');
assert.equal(document.querySelector('[data-entry="candidate"]')?.getAttribute('aria-checked'), 'true');
assert.match(document.querySelector('.recommendation-caution')?.textContent || '', /cannot select itself/i);

await click('[data-action="select-entry"][data-entry="selected"]');
assert.equal(document.querySelector('.recommendation h2')?.textContent, 'Selected-design breadboard');
assert.match(document.querySelector('.recommendation-facts')?.textContent || '', /accepted requirements/i);
document.querySelector('[data-entry="selected"]')?.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'End', bubbles: true }));
await wait(20);
assert.equal(document.querySelector('[data-entry="built"]')?.getAttribute('aria-checked'), 'true', 'Keyboard navigation should reach the final work state.');

await route('#/map?stage=selected-design');
assert.equal(document.querySelector('main h1')?.textContent, 'How authority moves through the work.');
assert.equal(document.querySelector('.map-stage.is-selected strong')?.textContent, 'Selected-design breadboard');
assert.match(document.querySelector('.kickoff-placement')?.textContent || '', /optional side branch after slice selection/i);
await click('[data-action="select-map-stage"][data-map-stage="prepare"]');
assert.match(document.querySelector('.map-detail')?.textContent || '', /Kickoff is optional orientation/i);

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
assert.equal(document.querySelector('main h1')?.textContent, 'Reference');
assert.equal(document.querySelectorAll('.skill-row').length, 13, 'The invocation reference should cover every canonical skill.');
assert.match(document.querySelector('.invocation-primer')?.textContent || '', /plugin makes skills available[\s\S]*Natural language is the portable default/i);
assert.equal(document.querySelectorAll('.runtime-invocation-list a').length, 4);
await click('[data-action="filter-skills"][data-category="conditional"]');
assert.match(document.querySelector('.skill-groups')?.textContent || '', /Statechart/);
await click('[data-action="select-skill"][data-skill="statechart"]');
assert.equal(document.querySelector('.skill-detail h2')?.textContent, 'Statechart');
assert.match(document.querySelector('.skill-invocation-detail .is-portable code')?.textContent || '', /installed statechart skill/i);
assert.match(document.querySelector('.skill-invocation-detail .invocation-shortcuts')?.textContent || '', /\/planning-skills:statechart[\s\S]*\/statechart/i);
await click('.skill-invocation-detail .invocation-surface.is-portable .invocation-copy');
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

await route('#/examples/simple-grocery-list');
assert.match(document.querySelector('.artifact-stage.is-selected')?.getAttribute('href') || '', /file=00-source-notes\.md/, 'A step-by-step example should open at its first artifact.');
assert.equal(document.querySelectorAll('.optional-artifacts .artifact-stage').length, 1, 'Kickoff should be shown only as optional orientation.');
assert.match(document.querySelector('.artifact-gap')?.textContent || '', /Implementation/i, 'The example should make the implementation gap before reflection visible.');

await route('#/');
Object.defineProperty(window, 'innerWidth', { configurable: true, value: 390 });
await click('[data-action="toggle-walkthrough-panel"][data-panel="input"]');
assert.ok(document.querySelector('.walkthrough-input.is-open'), 'The mobile input panel should expand in place.');
assert.equal(document.querySelector('[data-action="toggle-walkthrough-panel"][data-panel="input"]')?.getAttribute('aria-expanded'), 'true');
await click('[data-action="toggle-menu"]');
assert.ok(document.querySelector('.primary-nav.is-open'), 'The mobile menu should open.');
assert.equal(document.querySelector('.menu-button')?.getAttribute('aria-expanded'), 'true');
document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
await wait(20);
assert.equal(document.querySelector('.primary-nav.is-open'), null, 'The mobile menu should close.');
assert.equal(document.querySelector('.menu-button')?.getAttribute('aria-expanded'), 'false');
assert.equal(document.activeElement?.id, 'menu-button', 'Closing the mobile menu with Escape should restore focus to its trigger.');

await route('#/skills');
await click('[data-action="select-skill"][data-skill="statechart"]');
assert.equal(document.activeElement?.id, 'skill-detail-title', 'Selecting a skill on mobile should move focus to its updated detail.');

await route('#/guides/start-here');
assert.ok(document.querySelector('.docs-mobile-disclosure'), 'Mobile documentation should expose a compact disclosure navigation.');

assert.deepEqual(runtimeErrors, [], `Runtime errors were reported:\n${runtimeErrors.join('\n')}`);
dom.window.close();

console.log('Direct-open interaction validation passed (home, state navigator, planning map, search, skills, guide, example, copy, and mobile menu).');
