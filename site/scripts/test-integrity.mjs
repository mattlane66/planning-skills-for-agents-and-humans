import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { JSDOM, VirtualConsole } from 'jsdom';

const siteDirectory = path.resolve(import.meta.dirname, '..');
const htmlPath = path.join(siteDirectory, 'index.html');
const contentPath = path.join(siteDirectory, 'src', 'generated', 'content.json');
const stylesPath = path.join(siteDirectory, 'src', 'styles.css');
const [html, contentRaw, styles] = await Promise.all([
  readFile(htmlPath, 'utf8'),
  readFile(contentPath, 'utf8'),
  readFile(stylesPath, 'utf8'),
]);
const content = JSON.parse(contentRaw);
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
const route = async (hash) => {
  window.location.hash = hash;
  await wait(25);
};
const click = async (selector) => {
  const target = document.querySelector(selector);
  assert.ok(target, `Expected interactive target: ${selector}`);
  target.click();
  await wait(25);
  return target;
};

for (let attempts = 0; attempts < 100 && !window.__PLANNING_PORTAL_READY__; attempts += 1) await wait(20);
assert.equal(window.__PLANNING_PORTAL_READY__, true, 'The embedded application did not become ready.');

const resourcePaths = new Set(content.resources.map((item) => item.sourcePath));
const templatePaths = [...resourcePaths].filter((sourcePath) => sourcePath.startsWith('templates/'));
const skillReferencePaths = [...resourcePaths].filter((sourcePath) => sourcePath.includes('/references/'));
assert.equal(templatePaths.length, 20, 'Every canonical template should be embedded.');
assert.equal(skillReferencePaths.length, 8, 'Every canonical skill reference should be embedded.');
for (const item of [...content.docs, ...content.skills, ...content.resources, ...content.examples]) {
  assert.ok(item.description.length <= 240, `${item.sourcePath || item.slug} has an overlong description.`);
  assert.ok(!item.description.endsWith('…'), `${item.sourcePath || item.slug} has a truncated description.`);
}

const routes = new Set(['#/', '#/compass', '#/map', '#/skills', '#/guides/start-here', '#/examples']);
for (const skill of content.skills) {
  routes.add(`#/skills/${skill.slug}`);
  routes.add(`#/skills/${skill.slug}/guide`);
}
for (const guide of content.docs) routes.add(`#/guides/${guide.slug}`);
for (const resource of content.resources) routes.add(`#/resources/${resource.slug}`);
for (const example of content.examples) {
  routes.add(`#/examples/${example.slug}`);
  for (const file of example.files.filter((item) => item.name !== 'README.md')) {
    routes.add(`#/examples/${example.slug}?file=${encodeURIComponent(file.name)}`);
  }
}

for (const targetRoute of routes) {
  await route(targetRoute);
  assert.ok(document.querySelector('main#main-content'), `${targetRoute} did not render the main landmark.`);
  assert.equal(document.querySelector('.not-found'), null, `${targetRoute} rendered the portal 404.`);
  assert.equal(document.querySelectorAll('h1').length, 1, `${targetRoute} should render exactly one h1.`);

  const navigationLabels = [...document.querySelectorAll('nav')].map((nav) => nav.getAttribute('aria-label')).filter(Boolean);
  assert.equal(new Set(navigationLabels).size, navigationLabels.length, `${targetRoute} has duplicate navigation landmark labels.`);

  for (const anchor of document.querySelectorAll('a[href*="section="]')) {
    const href = anchor.getAttribute('href');
    const query = href.includes('?') ? href.slice(href.indexOf('?') + 1) : '';
    const section = new URLSearchParams(query).get('section');
    assert.ok(section && document.getElementById(section), `${targetRoute} links to missing section ${section || '(empty)'}.`);
  }

  for (const anchor of document.querySelectorAll('.markdown-body a[href]')) {
    const href = anchor.getAttribute('href') || '';
    assert.ok(!/^#[^/]/.test(href), `${targetRoute} contains a raw same-page hash that would bypass the router: ${href}`);
    assert.ok(!new RegExp(`^https://github\\.com/[^/]+/[^/]+/blob/main/.+\\.md(?:#.*)?$`).test(href), `${targetRoute} sends an embedded Markdown reference to GitHub: ${href}`);
  }
}

await route('#/');
assert.deepEqual(
  [...document.querySelectorAll('.primary-nav a')].map((item) => item.textContent),
  ['Walkthrough', 'Compass', 'Model', 'Reference'],
  'Primary navigation should center the experiential layer and demote the repository indexes.',
);
assert.equal(document.querySelector('.primary-nav a[aria-current="page"]')?.textContent, 'Walkthrough');
assert.equal(document.querySelector('main h1')?.textContent, 'Watch a plan take shape.');
assert.deepEqual(
  [...document.querySelectorAll('.walkthrough-progress button strong')].map((item) => item.textContent),
  ['Source', 'Frame', 'Requirements', 'Shape', 'Behavior', 'Slice', 'Handoff', 'Reality'],
  'The walkthrough must preserve the predetermined applied-example order.',
);
assert.equal(document.querySelectorAll('.walkthrough-ledger li').length, 8);
assert.equal(document.querySelectorAll('.walkthrough-ledger li.is-done').length, 0);
assert.equal(document.querySelector('.decision-options'), null, 'The applied walkthrough must not be a quiz.');
assert.equal(document.querySelector('[role="radiogroup"]'), null, 'The walkthrough should not ask the reader to guess the next move.');
assert.equal(document.querySelector('[data-action="select-lab-answer"]'), null, 'Retired quiz actions must not survive in the rendered experience.');
assert.match(document.querySelector('.walkthrough-input')?.textContent || '', /What the human brings/i);
assert.match(document.querySelector('.walkthrough-exchange')?.textContent || '', /Human[\s\S]*Planning agent/i);
assert.match(document.querySelector('.walkthrough-output')?.textContent || '', /Source notes/i);
await click('[data-action="select-walkthrough-stage"][data-stage-index="2"]');
assert.equal(document.querySelectorAll('.requirements-matrix tbody tr').length, 6, 'The Requirements stage must show all accepted criteria.');
assert.match(document.querySelector('.appetite-boundary')?.textContent || '', /Appetite[\s\S]*Cut line/i);
await click('[data-action="select-walkthrough-stage"][data-stage-index="3"]');
assert.equal(document.querySelector('#walkthrough-stage-title')?.textContent, 'Select a direction.');
assert.match(document.querySelector('.walkthrough-exchange')?.textContent || '', /Choose A/i);
assert.equal(document.querySelectorAll('.walkthrough-ledger li.is-done').length, 3);
assert.equal(document.querySelectorAll('.shape-path-button').length, 2, 'The Shape stage must expose both viable paths.');
assert.equal(document.querySelectorAll('.shape-fit-matrix .fit-check').length, 12, 'Both shapes must be checked against all six requirements.');
assert.match(document.querySelector('.fit-gate-explainer')?.textContent || '', /both A and B meet R0–R5[\s\S]*does not select one/i);
assert.equal(document.querySelectorAll('.shape-tradeoff-table tbody tr').length, 4, 'The Shape stage must compare the eligible paths after fit.');
assert.match(document.querySelector('.human-shape-decision')?.textContent || '', /human selected Shape A[\s\S]*clearest path to a breadboard/i);
await click('[data-action="inspect-shape"][data-shape="b"]');
assert.match(document.querySelector('.shape-path-detail')?.textContent || '', /Viable evidence only—not build scope/i);
await click('[data-action="select-walkthrough-stage"][data-stage-index="4"]');
assert.ok(document.querySelector('.walkthrough-breadboard .walkthrough-mermaid'), 'The Behavior stage must expose the selected-design breadboard.');
await click('[data-action="select-walkthrough-stage"][data-stage-index="5"]');
assert.deepEqual([...document.querySelectorAll('.task-group-card > header > span')].map((item) => item.textContent), ['TG1 · V1', 'TG2 · V2']);
assert.equal(document.querySelectorAll('.task-group-card > ol li').length, 6, 'The Slice stage must show the tasks inside both vertical groups.');
assert.match(document.querySelector('.dumplink-context')?.textContent || '', /optional here/i);
await click('[data-action="select-walkthrough-stage"][data-stage-index="6"]');
assert.match(document.querySelector('.handoff-assembly')?.textContent || '', /Planning context[\s\S]*Target-repository context[\s\S]*Complete build-agent packet/i);
assert.match(document.querySelector('.context-packet')?.textContent || '', /What planning contributes[\s\S]*Do not build yet[\s\S]*Return to planning if/i);
assert.deepEqual([...document.querySelectorAll('.packet-detail summary strong')].map((item) => item.textContent), ['Scope and authority', 'Behavior to preserve', 'Target-repository context', 'Execution and verification']);
assert.match(document.querySelector('[data-packet-section="repository-context"]')?.textContent || '', /Resolve in target repo/i);
assert.match(document.querySelector('.provenance-ledger')?.textContent || '', /Human selected shape A[\s\S]*Planning agent packaged context/i);

await route('#/compass');
assert.deepEqual(
  [...document.querySelectorAll('.home-principles li strong')].map((item) => item.textContent),
  ['Explore', 'Decide', 'Build'],
  'The compass should reduce the model to exploration, human decisions, and one-slice build scope.',
);
const entryExpectations = [
  ['fuzzy', 'Frame the problem', '#/skills/framing-doc/guide'],
  ['exploring', 'Shape the work', '#/skills/shaping/guide'],
  ['candidate', 'Candidate-shape breadboard', '#/skills/breadboarding/guide'],
  ['selected', 'Selected-design breadboard', '#/skills/breadboarding/guide'],
  ['behavior', 'Select one build slice', '#/skills/dumplink/guide'],
  ['slice', 'Package the build context', '#/skills/feed-planning-context/guide'],
  ['built', 'Reflect on drift', '#/skills/breadboard-reflection/guide'],
];
for (const [entry, heading, href] of entryExpectations) {
  await click(`[data-action="select-entry"][data-entry="${entry}"]`);
  assert.equal(document.querySelector('.recommendation h2')?.textContent, heading);
  assert.equal(document.querySelector('.recommendation .button')?.getAttribute('href'), href);
}
assert.equal(document.querySelector('.home-next-links a[href="#/skills/planning-router/guide"]')?.textContent.trim().startsWith('Still unsure?'), true);

await route('#/map?stage=selected-design');
assert.deepEqual(
  [...document.querySelectorAll('.map-stage')].map((item) => item.dataset.mapStage),
  ['explore', 'direction-gate', 'selected-design', 'slice-gate', 'prepare', 'build', 'reflect'],
  'The rendered map must preserve the canonical promotion order.',
);
assert.equal(document.querySelector('.map-stage.is-selected')?.dataset.mapStage, 'selected-design');
assert.equal(document.querySelectorAll('.planning-map [data-map-stage*="kickoff"]').length, 0, 'Kickoff must not be rendered as a required stage.');
assert.match(document.querySelector('.map-optional')?.textContent || '', /Kickoff orientation/i);
assert.match(document.querySelector('.kickoff-placement')?.textContent || '', /after slice selection/i);

await click('#search-trigger');
const search = document.querySelector('#global-search');
assert.equal(search.getAttribute('aria-label'), 'Search all portal content');
search.value = 'shaping';
search.dispatchEvent(new window.Event('input', { bubbles: true }));
await wait(25);
assert.equal(document.querySelector('.search-result strong')?.textContent, 'Shaping', 'Exact skill title should rank first.');
assert.equal(document.querySelector('.search-result .result-type')?.textContent, 'Skill');
const totalResults = Number(document.querySelector('.search-results')?.dataset.resultTotal);
const shownResults = document.querySelectorAll('.search-result').length;
assert.ok(totalResults >= shownResults && shownResults <= 15, 'Search should expose the real total and cap only the displayed set.');
assert.match(document.querySelector('.search-results .system-label')?.textContent || '', totalResults > shownResults ? new RegExp(`Showing ${shownResults} of ${totalResults}`) : new RegExp(`${totalResults} results`));
document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
await wait(25);

await click('#search-trigger');
await click('[data-action="close-search"]');
assert.equal(document.activeElement?.id, 'search-trigger', 'Search should restore focus to its trigger.');

await route('#/skills');
for (const button of document.querySelectorAll('[data-action="filter-skills"]')) {
  assert.ok(['true', 'false'].includes(button.getAttribute('aria-pressed')), 'Skill filters should expose pressed state.');
}
assert.equal(document.querySelector('.menu-button')?.getAttribute('aria-controls'), 'primary-navigation');

await route('#/guides/repository-overview');
assert.ok(document.querySelector('.markdown-body a[href^="#/resources/"]'), 'Repository guide should route linked supporting Markdown inside the portal.');
assert.ok(document.querySelector('.markdown-body a[href="#/"]'), 'The site/index.html link should return to the portal overview.');
assert.ok(document.querySelector('.markdown-body a[href="#/skills/shaping/guide"]'), 'Canonical skill links should open authoritative guides.');

await route('#/examples/simple-grocery-list?file=02-shaping.md');
const trailFiles = [...document.querySelectorAll('.artifact-stage')].map((anchor) => new URLSearchParams(anchor.getAttribute('href').split('?')[1]).get('file'));
assert.deepEqual(trailFiles.slice(0, 5), ['00-source-notes.md', '01-frame.md', '02-shaping.md', '03-breadboard.md', '05-breadboard-reflection.md'], 'The required story must omit kickoff and preserve reflection after planning.');
assert.equal(document.querySelector('.optional-artifacts .artifact-stage')?.getAttribute('href')?.includes('04-kickoff.md'), true, 'Kickoff must appear only in the optional branch.');
assert.match(document.querySelector('.optional-artifacts .artifact-stage em')?.textContent || '', /After selected design \+ V1/i);
assert.match(document.querySelector('.artifact-gap')?.textContent || '', /Implementation/i);
assert.match(document.querySelector('.learning-notes')?.textContent || '', /accepted before selection/i);

function luminance(hex) {
  const channels = hex.match(/[a-f\d]{2}/gi).map((value) => Number.parseInt(value, 16) / 255).map((value) => (
    value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4
  ));
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
}
function contrast(foreground, background) {
  const values = [luminance(foreground), luminance(background)].sort((left, right) => right - left);
  return (values[0] + 0.05) / (values[1] + 0.05);
}
const cssToken = (name) => styles.match(new RegExp(`--${name}:\\s*(#[a-f\\d]{6})`, 'i'))?.[1];
assert.ok(contrast(cssToken('faint'), '#fbfcfa') >= 4.5, 'Faint small text must meet WCAG AA contrast.');
assert.ok(contrast(cssToken('planning'), '#fbfcfa') >= 4.5, 'Planning labels must meet WCAG AA contrast on the page background.');
assert.ok(contrast(cssToken('planning-strong'), '#ffffff') >= 4.5, 'Planning buttons must meet WCAG AA contrast.');
assert.ok(contrast(cssToken('reflection'), '#ffffff') >= 4.5, 'Reflection labels must meet WCAG AA contrast.');
assert.match(html, /viewport-fit=cover/);
assert.match(styles, /100dvh/);
assert.match(styles, /safe-area-inset-bottom/);
assert.match(styles, /-webkit-text-size-adjust:\s*100%/);
assert.match(styles, /touch-action:\s*manipulation/);
const mobileStyles = styles.slice(styles.indexOf('@media (max-width: 620px)'), styles.indexOf('@media (prefers-reduced-motion'));
assert.match(mobileStyles, /\.walkthrough-progress\s*\{[\s\S]*?margin-bottom:/, 'The iPhone progress rail should remain compact and horizontally scrollable.');
assert.match(mobileStyles, /\.walkthrough-progress button\s*\{[\s\S]*?min-height:\s*52px;/, 'Mobile stage controls should be comfortable touch targets.');
assert.match(mobileStyles, /\.walkthrough-controls > \.button,[\s\S]*?min-height:\s*50px;/, 'The walkthrough controls should be thumb-friendly on iPhone.');
assert.match(mobileStyles, /\.packet-row\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'The final build packet should stack on a phone.');
assert.match(mobileStyles, /\.assembly-flow\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'The handoff assembly should stack on a phone.');
assert.match(mobileStyles, /\.packet-detail-body dl > div\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'Expanded handoff fields should stack on a phone.');
assert.match(styles, /@media \(max-width: 960px\)[\s\S]*?\.handoff-workspace,[\s\S]*?\.assembly-flow\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'The handoff should stack before its desktop columns can overflow.');
assert.match(mobileStyles, /\.fit-gate-explainer p,[\s\S]*?\.packet-detail-body dd ul\s*\{[\s\S]*?font-size:\s*12px;/, 'Applied walkthrough body text should remain readable on a phone.');
assert.match(styles, /\.walkthrough-input\.is-open \.walkthrough-panel-body,[\s\S]*?display:\s*block;/, 'Mobile walkthrough supporting panels should expand on demand.');
assert.match(mobileStyles, /\.task-group-sequence\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'Dumplink task groups should stack vertically on a phone.');
assert.match(mobileStyles, /\.task-group-dependency > svg\s*\{[\s\S]*?rotate\(90deg\)/, 'The task-group dependency arrow should rotate with the mobile sequence.');
assert.match(mobileStyles, /\.planning-map\s*\{[\s\S]*?grid-template-columns:\s*1fr;/, 'The planning map should collapse to one column on narrow screens.');
assert.match(mobileStyles, /\.map-stage-wrap:nth-child\(n\) \.map-connector\s*\{[\s\S]*?rotate\(90deg\)/, 'Mobile map arrows should become a vertical sequence.');
assert.doesNotMatch(mobileStyles, /\.walkthrough-exchange\s*\{[^}]*display:\s*none;/, 'The human-agent exchange must remain visible on iPhone-sized screens.');
assert.deepEqual(runtimeErrors, [], `Runtime errors were reported:\n${runtimeErrors.join('\n')}`);

dom.window.close();
console.log(`Portal integrity validation passed (${routes.size} routes, complete TOCs, ranked search, embedded references, semantics, and mobile safeguards).`);
