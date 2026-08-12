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
  assert.ok(item.description.length <= 241, `${item.sourcePath || item.slug} has an overlong description.`);
  if (item.description.length >= 239) assert.ok(item.description.endsWith('…'), `${item.sourcePath || item.slug} has a hard-cut description.`);
}

const routes = new Set(['#/', '#/skills', '#/guides/start-here', '#/examples']);
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
assert.equal(document.querySelector('.primary-nav a[href="#/examples"]')?.textContent, 'Examples');
assert.equal(document.querySelector('.primary-nav a[aria-current="page"]')?.textContent, 'Overview');
await click('[data-action="select-entry"][data-entry="uncertainty"]');
assert.equal(document.querySelector('.recommendation a')?.getAttribute('href'), '#/skills/planning-router/guide');

await click('#search-trigger');
const search = document.querySelector('#global-search');
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

await click('#mobile-search-trigger');
await click('[data-action="close-search"]');
assert.equal(document.activeElement?.id, 'mobile-search-trigger', 'Mobile search should restore focus to the visible mobile trigger.');

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
assert.ok(trailFiles.indexOf('03-breadboard.md') < trailFiles.indexOf('04-kickoff.md'), 'Breadboarding must precede optional kickoff in the worked sequence.');
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
assert.ok(contrast(cssToken('planning-strong'), '#ffffff') >= 4.5, 'Planning buttons must meet WCAG AA contrast.');
assert.ok(contrast(cssToken('reflection'), '#ffffff') >= 4.5, 'Reflection labels must meet WCAG AA contrast.');
assert.match(html, /viewport-fit=cover/);
assert.match(styles, /100dvh/);
assert.match(styles, /safe-area-inset-bottom/);
assert.deepEqual(runtimeErrors, [], `Runtime errors were reported:\n${runtimeErrors.join('\n')}`);

dom.window.close();
console.log(`Portal integrity validation passed (${routes.size} routes, complete TOCs, ranked search, embedded references, semantics, and mobile safeguards).`);
