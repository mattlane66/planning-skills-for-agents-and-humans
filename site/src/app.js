import DOMPurify from 'dompurify';
import { marked } from 'marked';
import mermaid from 'mermaid';
import content from './generated/content.json';
import {
  entryStates,
  mapStages,
  simpleExampleModel,
  skillGroups,
  skillModel,
  walkthroughSteps,
} from './planning-model.js';

const REPOSITORY_URL = 'https://github.com/mattlane66/planning-skills-for-agents-and-humans';
const SEARCH_RESULT_LIMIT = 15;
const root = document.getElementById('root');

const state = {
  walkthroughStep: 0,
  walkthroughPanels: { input: false, output: false, ledger: false },
  inspectedShape: 'a',
  selectedEntry: 'fuzzy',
  selectedMapStage: 'selected-design',
  skillCategory: 'all',
  skillQuery: '',
  selectedSkill: 'shaping',
  searchOpen: false,
  searchQuery: '',
  mobileMenuOpen: false,
  restoreFocus: null,
};

const requestedGuideGroups = [
  { label: 'Start here', slugs: ['start-here', 'repository-overview', 'manifesto'] },
  { label: 'Core workflow', slugs: ['agent-workflow', 'full-modern-agent-workflow', 'human-decision-gates', 'plan-quality-rubric'] },
  { label: 'Use with agents', slugs: ['codex-usage', 'claude-code-plugin', 'gemini-usage', 'runtime-adapters'] },
  { label: 'Implementation', slugs: ['using-in-a-product-repo', 'agent-context-feeding', 'interface-contracts', 'executable-breadboards', 'dumplink-usage', 'statechart-usage', 'sketch-reconciliation', 'agent-run-records'] },
  { label: 'Tooling', slugs: ['visual-hot-reload', 'canvas-export', 'ci-health-workflow', 'skill-behavior-evals', 'lifecycle-hooks'] },
];

const assignedGuides = new Set(requestedGuideGroups.flatMap((group) => group.slugs));
const guideGroups = [
  ...requestedGuideGroups,
  { label: 'Reference', slugs: content.docs.map((guide) => guide.slug).filter((slug) => !assignedGuides.has(slug)) },
];

const docsBySlug = new Map(content.docs.map((item) => [item.slug, item]));
const skillsBySlug = new Map(content.skills.map((item) => [item.slug, item]));
const resources = content.resources || [];
const resourcesBySlug = new Map(resources.map((item) => [item.slug, item]));
const resourceGroups = ['Skill references', 'Templates', 'Repository reference'].map((label) => ({
  label,
  items: resources.filter((item) => item.category === label),
})).filter((group) => group.items.length > 0);
const routeBySourcePath = new Map([
  ...content.docs.map((item) => [item.sourcePath, `/guides/${item.slug}`]),
  ...content.skills.map((item) => [item.sourcePath, `/skills/${item.slug}/guide`]),
  ...content.examples.flatMap((example) => example.files.map((file) => [file.sourcePath, `/examples/${example.slug}?file=${encodeURIComponent(file.name)}`])),
  ...resources.map((item) => [item.sourcePath, `/resources/${item.slug}`]),
  ['site/index.html', '/'],
]);

const searchItems = [
  ...content.skills.map((item) => ({ ...item, type: 'Skill', route: `/skills/${item.slug}` })),
  ...content.docs.map((item) => ({ ...item, type: 'Guide', route: `/guides/${item.slug}` })),
  ...resources.map((item) => ({ ...item, type: item.category === 'Templates' ? 'Template' : 'Reference', route: `/resources/${item.slug}` })),
  ...content.examples.map((item) => ({
    ...item,
    type: 'Example',
    route: `/examples/${item.slug}`,
    searchText: item.files.map((file) => file.searchText).join(' '),
  })),
];

marked.setOptions({ gfm: true, breaks: false });
mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'strict',
  theme: 'base',
  themeVariables: {
    background: '#fbfcfa', primaryColor: '#fff7e8', primaryTextColor: '#0b1830',
    primaryBorderColor: '#a96800', lineColor: '#526072', secondaryColor: '#eef7f0',
    tertiaryColor: '#eef5ff', fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  },
});

function escapeHtml(value = '') {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  })[character]);
}

function icon(name, size = 20) {
  const paths = {
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    back: '<path d="M19 12H5m6 6-6-6 6-6"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    copy: '<rect x="8" y="8" width="11" height="11" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
    external: '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/>',
    file: '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v5h5M9 12h6M9 16h6"/>',
    bulb: '<path d="M9 18h6M10 22h4"/><path d="M8.5 14.5C7 13.2 6 11.4 6 9.5a6 6 0 0 1 12 0c0 1.9-1 3.7-2.5 5-.8.7-1 1.3-1 1.5h-5c0-.2-.2-.8-1-1.5Z"/>',
    flask: '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 16h9"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.8 9a2.4 2.4 0 1 1 3 2.3c-.8.3-.8 1-.8 1.7M12 17h.01"/>',
    target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M21 12h-3M12 21v-3M3 12h3"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
  };
  if (name === 'github') {
    return `<svg aria-hidden="true" viewBox="0 0 24 24" width="${size}" height="${size}" fill="currentColor"><path d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.6-4-1.6-.5-1.4-1.3-1.8-1.3-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3Z"/></svg>`;
  }
  return `<svg aria-hidden="true" viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${paths[name] || paths.file}</svg>`;
}

function resolveRepoPath(basePath, target) {
  const parts = target.startsWith('/') ? [] : basePath.split('/').slice(0, -1);
  for (const part of target.replace(/^\//, '').split('/')) {
    if (!part || part === '.') continue;
    if (part === '..') parts.pop();
    else parts.push(part);
  }
  return parts.join('/');
}

function splitLocalTarget(href) {
  const hashIndex = href.indexOf('#');
  const fragment = hashIndex >= 0 ? href.slice(hashIndex + 1) : '';
  const withoutFragment = hashIndex >= 0 ? href.slice(0, hashIndex) : href;
  const target = withoutFragment.split('?', 1)[0];
  try {
    return { target: decodeURIComponent(target), fragment };
  } catch {
    return { target, fragment };
  }
}

function headingSlug(value, seen) {
  const base = value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
  const count = seen.get(base) || 0;
  seen.set(base, count + 1);
  return count === 0 ? base : `${base}-${count + 1}`;
}

function replaceHeadingDepth(heading, depth) {
  if (heading.tagName === `H${depth}`) return heading;
  const replacement = document.createElement(`h${depth}`);
  for (const attribute of heading.attributes) replacement.setAttribute(attribute.name, attribute.value);
  while (heading.firstChild) replacement.append(heading.firstChild);
  heading.replaceWith(replacement);
  return replacement;
}

function renderMarkdown(raw, sourcePath, route, { headingOffset = 0 } = {}) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = DOMPurify.sanitize(marked.parse(raw || ''));
  const seen = new Map();
  let foundDocumentTitle = false;
  const normalizedHeadings = [...wrapper.querySelectorAll('h1, h2, h3, h4, h5, h6')].map((heading) => {
    let depth = Number(heading.tagName.slice(1));
    if (headingOffset > 0) depth = Math.min(6, depth + headingOffset);
    else if (depth === 1) {
      if (foundDocumentTitle) depth = 2;
      foundDocumentTitle = true;
    }
    return replaceHeadingDepth(heading, depth);
  });
  const headings = [];

  for (const heading of normalizedHeadings) {
    const title = heading.textContent || '';
    const id = headingSlug(title, seen);
    heading.id = id;
    const anchor = document.createElement('a');
    anchor.className = 'heading-anchor';
    anchor.href = `#${route}${route.includes('?') ? '&' : '?'}section=${encodeURIComponent(id)}`;
    anchor.setAttribute('aria-label', `Link to ${title}`);
    anchor.textContent = '#';
    heading.append(anchor);
    const depth = Number(heading.tagName.slice(1));
    if (depth <= 3) headings.push({ depth, title, id });
  }

  for (const image of wrapper.querySelectorAll('img[src]')) {
    const src = image.getAttribute('src') || '';
    if (!src || /^(?:[a-z][a-z0-9+.-]*:|#)/i.test(src)) continue;
    const { target } = splitLocalTarget(src);
    const resolved = resolveRepoPath(sourcePath, target);
    image.src = content.assets[resolved] || `${REPOSITORY_URL}/raw/main/${resolved}`;
    image.loading = 'lazy';
  }

  for (const checkbox of wrapper.querySelectorAll('input[type="checkbox"]')) {
    const label = checkbox.closest('li')?.textContent?.trim() || 'Checklist item';
    checkbox.setAttribute('aria-label', label);
  }

  for (const anchor of wrapper.querySelectorAll('a[href]')) {
    const href = anchor.getAttribute('href') || '';
    if (anchor.classList.contains('heading-anchor')) continue;
    if (/^(?:https?:|mailto:)/i.test(href)) {
      anchor.target = '_blank';
      anchor.rel = 'noreferrer';
      continue;
    }
    if (!href) continue;
    if (href.startsWith('#')) {
      const fragment = href.slice(1);
      anchor.href = `#${route}${route.includes('?') ? '&' : '?'}section=${encodeURIComponent(fragment)}`;
      continue;
    }
    const { target, fragment } = splitLocalTarget(href);
    const resolved = resolveRepoPath(sourcePath, target);
    const portalRoute = routeBySourcePath.get(resolved);
    if (portalRoute) {
      anchor.href = `#${portalRoute}${fragment ? `${portalRoute.includes('?') ? '&' : '?'}section=${encodeURIComponent(fragment)}` : ''}`;
      continue;
    }
    if (content.assets[resolved]) {
      anchor.href = content.assets[resolved];
      anchor.target = '_blank';
      anchor.rel = 'noreferrer';
      continue;
    }
    const view = target.endsWith('/') ? 'tree' : 'blob';
    anchor.href = `${REPOSITORY_URL}/${view}/main/${resolved}${fragment ? `#${fragment}` : ''}`;
    anchor.target = '_blank';
    anchor.rel = 'noreferrer';
  }

  for (const code of wrapper.querySelectorAll('pre > code.language-mermaid')) {
    const diagram = document.createElement('div');
    diagram.className = 'mermaid markdown-mermaid';
    diagram.textContent = code.textContent;
    code.parentElement.replaceWith(diagram);
  }
  return { html: wrapper.innerHTML, headings };
}

function currentRoute() {
  const raw = location.hash.slice(1) || '/';
  const question = raw.indexOf('?');
  const path = question >= 0 ? raw.slice(0, question) : raw;
  const query = new URLSearchParams(question >= 0 ? raw.slice(question + 1) : '');
  return { path: path.startsWith('/') ? path : `/${path}`, query };
}

function header(active) {
  const items = [
    ['Walkthrough', '/', 'walkthrough'], ['Compass', '/compass', 'compass'],
    ['Model', '/map', 'model'], ['Reference', '/skills', 'reference'],
  ];
  return `
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <a class="site-brand" href="#/"><span aria-hidden="true">PSL</span> Planning Skills Lab</a>
      <nav id="primary-navigation" class="primary-nav ${state.mobileMenuOpen ? 'is-open' : ''}" aria-label="Primary navigation">
        ${items.map(([label, route, id]) => `<a class="nav-link ${active === id ? 'is-active' : ''}" href="#${route}" ${active === id ? 'aria-current="page"' : ''}>${label}</a>`).join('')}
      </nav>
      <div class="header-actions">
        <a class="header-compass-link" href="${REPOSITORY_URL}" target="_blank" rel="noreferrer">Open repository ${icon('external', 16)}</a>
        <button id="search-trigger" class="icon-button header-search" type="button" data-action="open-search" aria-label="Search the reference">${icon('search', 21)}</button>
        <button id="menu-button" class="icon-button menu-button" type="button" data-action="toggle-menu" aria-controls="primary-navigation" aria-expanded="${state.mobileMenuOpen}" aria-label="${state.mobileMenuOpen ? 'Close' : 'Open'} navigation menu">${icon(state.mobileMenuOpen ? 'close' : 'menu', 26)}</button>
      </div>
    </header>`;
}

function walkthroughProgress() {
  return `<nav class="walkthrough-progress" aria-label="Walkthrough stages">
    <ol>${walkthroughSteps.map((step, index) => {
      const done = index < state.walkthroughStep;
      const current = index === state.walkthroughStep;
      return `<li class="${done ? 'is-done' : ''} ${current ? 'is-current' : ''}">
        <button type="button" data-action="select-walkthrough-stage" data-stage-index="${index}" ${current ? 'aria-current="step"' : ''} aria-label="${index + 1}. ${escapeHtml(step.label)}${done ? ', completed' : current ? ', current' : ''}">
          <span aria-hidden="true">${done ? icon('check', 14) : index + 1}</span><strong>${escapeHtml(step.label)}</strong>
        </button>
      </li>`;
    }).join('')}</ol>
  </nav>`;
}

function panelHeading(kind, title, meta = '') {
  const open = state.walkthroughPanels[kind];
  return `<div class="walkthrough-panel-heading"><h3>${escapeHtml(title)}</h3>${meta ? `<small>${escapeHtml(meta)}</small>` : ''}</div>
    <button class="walkthrough-panel-toggle" type="button" data-action="toggle-walkthrough-panel" data-panel="${kind}" aria-controls="walkthrough-${kind}-body" aria-expanded="${open}">
      <span><strong>${escapeHtml(title)}</strong>${meta ? `<small>${escapeHtml(meta)}</small>` : ''}</span>${icon('arrow', 17)}
    </button>`;
}

function inputPanel(step) {
  return `<section class="walkthrough-input walkthrough-panel ${state.walkthroughPanels.input ? 'is-open' : ''}" aria-label="${escapeHtml(step.inputTitle)}">
    ${panelHeading('input', step.inputTitle)}
    <div id="walkthrough-input-body" class="walkthrough-panel-body"><ul>${step.input.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></div>
  </section>`;
}

function roleLabel(role) {
  if (role === 'human') return { label: 'Human', initials: 'H' };
  if (role === 'builder') return { label: 'Build agent', initials: 'BA' };
  return { label: 'Planning agent', initials: 'PA' };
}

function collaborationExchange(step, compact = false) {
  return `<section class="walkthrough-exchange ${compact ? 'is-compact' : ''}" aria-labelledby="exchange-title">
    <div class="exchange-heading"><h3 id="exchange-title">Human + agent</h3><a href="#/skills/${step.skillSlug}/guide">${escapeHtml(step.skill)}</a></div>
    <ol class="collaboration-timeline">${step.exchange.map((turn) => {
      const role = roleLabel(turn.role);
      return `<li class="role-${turn.role}"><span class="role-mark" aria-hidden="true">${role.initials}</span><div><strong>${role.label}</strong><p>${escapeHtml(turn.text)}</p></div></li>`;
    }).join('')}</ol>
  </section>`;
}

function outputPanel(step) {
  return `<section class="walkthrough-output walkthrough-panel ${state.walkthroughPanels.output ? 'is-open' : ''}" aria-label="Output added">
    ${panelHeading('output', 'Output added', step.artifact.status)}
    <div id="walkthrough-output-body" class="walkthrough-panel-body">
      <div class="artifact-preview-card"><span class="artifact-sheet" aria-hidden="true">${icon('file', 24)}</span><div><strong>${escapeHtml(step.artifact.title)}</strong><p>${escapeHtml(step.output)}</p></div></div>
      <p class="why-it-matters"><strong>Why this matters</strong>${escapeHtml(step.why)}</p>
    </div>
  </section>`;
}

function planLedger() {
  const count = state.walkthroughStep + 1;
  return `<section class="walkthrough-ledger walkthrough-panel ${state.walkthroughPanels.ledger ? 'is-open' : ''}" aria-label="Plan so far">
    ${panelHeading('ledger', 'Plan so far', `${count} of ${walkthroughSteps.length}`)}
    <div id="walkthrough-ledger-body" class="walkthrough-panel-body">
      <ol>${walkthroughSteps.map((step, index) => {
        const done = index < state.walkthroughStep;
        const current = index === state.walkthroughStep;
        return `<li class="${done ? 'is-done' : ''} ${current ? 'is-current' : ''}">
          <span class="ledger-status" aria-hidden="true">${done ? icon('check', 14) : index + 1}</span><span><strong>${escapeHtml(step.artifact.title)}</strong><small>${current ? 'Just added' : done ? 'Completed' : 'Future'}</small></span>
        </li>`;
      }).join('')}</ol>
      <p class="ledger-foot">${icon('file', 17)} Build packet grows here</p>
    </div>
  </section>`;
}

function visualHeading(visual, meta = '') {
  return `<header class="stage-visual-heading"><div><h3 id="stage-visual-title">${escapeHtml(visual.title)}</h3><p>${escapeHtml(visual.caption)}</p></div>${meta ? `<span>${escapeHtml(meta)}</span>` : ''}</header>`;
}

function requirementRows(requirements, { includeFit = false } = {}) {
  return requirements.map((requirement) => `<tr>
    <th scope="row"><span>${escapeHtml(requirement.id)}</span></th>
    <td>${escapeHtml(requirement.text)}</td>
    <td><span class="requirement-priority">${escapeHtml(requirement.priority)}</span></td>
    ${includeFit ? '<td><span class="fit-check" aria-label="Shape A fits">✓</span></td><td><span class="fit-check" aria-label="Shape B fits">✓</span></td>' : '<td><span class="accepted-check">Accepted</span></td>'}
  </tr>`).join('');
}

function requirementsVisual(visual) {
  return `<section class="walkthrough-stage-visual requirements-visual" aria-labelledby="stage-visual-title">
    ${visualHeading(visual, 'Accepted before selection')}
    <div class="requirements-visual-layout">
      <div class="walkthrough-table-scroll"><table class="requirements-matrix">
        <thead><tr><th scope="col">ID</th><th scope="col">Requirement</th><th scope="col">Priority</th><th scope="col">Authority</th></tr></thead>
        <tbody>${requirementRows(visual.requirements)}</tbody>
      </table></div>
      <div class="appetite-boundary" role="group" aria-label="Accepted Appetite and cut line">
        <div><strong>Appetite</strong><ul>${visual.appetite.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></div>
        <div><strong>Cut line</strong><p>${escapeHtml(visual.cutLine)}</p></div>
      </div>
    </div>
  </section>`;
}

function inlineCode(value) {
  return escapeHtml(value).replace(/`([^`]+)`/g, '<code>$1</code>');
}

function shapeFitVisual(visual) {
  const inspected = visual.paths.find((path) => path.id === state.inspectedShape) || visual.paths[0];
  const { decision } = visual;
  return `<section class="walkthrough-stage-visual shape-fit-visual" aria-labelledby="stage-visual-title">
    ${visualHeading(visual, 'Human decision required')}
    <div class="shape-path-switcher" aria-label="Inspect candidate shapes">
      ${visual.paths.map((path) => `<button class="shape-path-button ${path.selected ? 'is-selected' : ''} ${path.id === inspected.id ? 'is-inspected' : ''}" type="button" data-action="inspect-shape" data-shape="${path.id}" aria-pressed="${path.id === inspected.id}">
        <span><strong>${escapeHtml(path.label)}</strong><small>${escapeHtml(path.name)}</small></span><em>${escapeHtml(path.status)}</em>
      </button>`).join('')}
    </div>
    <div class="walkthrough-table-scroll"><table class="requirements-matrix shape-fit-matrix">
      <thead><tr><th scope="col">ID</th><th scope="col">Accepted requirement</th><th scope="col">Priority</th>${visual.paths.map((path) => `<th scope="col" class="${path.selected ? 'is-selected-path' : ''}">${escapeHtml(path.label)}<small>${path.selected ? 'Selected' : 'Candidate'}</small></th>`).join('')}</tr></thead>
      <tbody>${requirementRows(visual.requirements, { includeFit: true })}</tbody>
    </table></div>
    <div class="fit-gate-explainer">
      <span aria-hidden="true">PASS</span>
      <div><h4>${escapeHtml(decision.gateTitle)}</h4><p>${escapeHtml(decision.gateText)}</p></div>
    </div>
    <div class="shape-tradeoff-scroll"><table class="shape-tradeoff-table">
      <thead><tr><th scope="col">Decision lens</th><th scope="col" class="is-selected-path">Shape A <small>Selected</small></th><th scope="col">Shape B <small>Eligible</small></th></tr></thead>
      <tbody>${decision.comparisons.map((comparison) => `<tr><th scope="row">${escapeHtml(comparison.label)}</th><td class="is-selected-path">${escapeHtml(comparison.a)}</td><td>${escapeHtml(comparison.b)}</td></tr>`).join('')}</tbody>
    </table></div>
    <section class="human-shape-decision" aria-labelledby="human-shape-decision-title">
      <span aria-hidden="true">H</span><div><h4 id="human-shape-decision-title">${escapeHtml(decision.selection.title)}</h4><p>${escapeHtml(decision.selection.lead)}</p><ul>${decision.selection.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join('')}</ul></div>
    </section>
    <article id="shape-path-detail" class="shape-path-detail ${inspected.selected ? 'is-selected' : ''}" aria-live="polite">
      <header><span>${escapeHtml(inspected.label)}</span><div><h4>${escapeHtml(inspected.name)}</h4><p>${escapeHtml(inspected.tradeoff)}</p></div></header>
      <ul>${inspected.mechanisms.map((item) => `<li>${inlineCode(item)}</li>`).join('')}</ul>
      <p class="shape-authority">${inspected.selected ? 'Recorded authority: selected by the human.' : 'Authority: viable evidence only—not build scope.'}</p>
    </article>
  </section>`;
}

function breadboardVisual(visual) {
  return `<section class="walkthrough-stage-visual walkthrough-breadboard" aria-labelledby="stage-visual-title">
    ${visualHeading(visual, 'Accepted selected design')}
    <div class="breadboard-canvas" role="img" aria-label="Simplified grocery list selected-design breadboard showing item input, duplicate branch, one items store, bought state, display filtering, visible list, duplicate feedback, and local storage">
      <div class="mermaid walkthrough-mermaid">${escapeHtml(visual.diagram)}</div>
    </div>
    <ul class="breadboard-legend" aria-label="Breadboard notation">${visual.legend.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
  </section>`;
}

function slicePlanVisual(visual) {
  const { plan } = visual;
  return `<section class="walkthrough-stage-visual slice-plan-visual" aria-labelledby="stage-visual-title">
    ${visualHeading(visual, 'Dumplink pattern')}
    <ol class="dumplink-moves" aria-label="Dumplink moves"><li><strong>1</strong><span>DUMP</span></li><li>${icon('arrow', 17)}</li><li><strong>2</strong><span>CLUSTER</span></li><li>${icon('arrow', 17)}</li><li><strong>3</strong><span>SEQUENCE</span></li></ol>
    <p class="dumplink-context">${escapeHtml(plan.note)}</p>
    <div class="task-group-sequence">
      ${plan.groups.map((group, index) => `${index > 0 ? `<div class="task-group-dependency" aria-label="Dependency from ${plan.groups[index - 1].id} to ${group.id}">${icon('arrow', 22)}<span>${escapeHtml(plan.dependency)}</span></div>` : ''}<article class="task-group-card ${group.selected ? 'is-active' : ''}">
        <header><span>${escapeHtml(group.id)} · ${escapeHtml(group.slice)}</span><em>${escapeHtml(group.state)}</em><h4>${escapeHtml(group.name)}</h4></header>
        <ol>${group.tasks.map((task) => `<li><span>${escapeHtml(task.id)}</span>${escapeHtml(task.text)}</li>`).join('')}</ol>
        <dl><div><dt>Produces</dt><dd>${escapeHtml(group.produces)}</dd></div><div><dt>Acceptance check</dt><dd>${escapeHtml(group.check)}</dd></div></dl>
      </article>`).join('')}
    </div>
    <p class="task-group-gate"><span aria-hidden="true">H</span><strong>Human gate:</strong> sequence does not activate scope. The recorded selection makes TG1 / V1 the only active group.</p>
  </section>`;
}

function stageVisual(step) {
  if (!step.visual) return '';
  if (step.visual.type === 'requirements') return requirementsVisual(step.visual);
  if (step.visual.type === 'shape-fit') return shapeFitVisual(step.visual);
  if (step.visual.type === 'breadboard') return breadboardVisual(step.visual);
  if (step.visual.type === 'slice-plan') return slicePlanVisual(step.visual);
  return '';
}

function walkthroughControls(step, index) {
  const previous = index > 0 ? walkthroughSteps[index - 1] : null;
  const next = index < walkthroughSteps.length - 1 ? walkthroughSteps[index + 1] : null;
  const nextLabel = step.id === 'handoff' ? 'See implementation reality' : next ? `Continue to ${next.label.toLowerCase()}` : 'Start again';
  const sourceHref = step.id === 'handoff'
    ? '#/examples/simple-grocery-list'
    : `#/examples/simple-grocery-list?file=${encodeURIComponent(step.sourceFile)}`;
  return `<nav class="walkthrough-controls" aria-label="Walkthrough controls">
    ${previous ? `<button class="button button-outline" type="button" data-action="previous-walkthrough-stage">${icon('back', 18)} Previous${step.id === 'handoff' ? ': Slice selection' : ''}</button>` : '<span></span>'}
    <button class="button button-primary" type="button" data-action="${next ? 'next-walkthrough-stage' : 'reset-walkthrough'}">${escapeHtml(nextLabel)} ${next ? icon('arrow', 18) : ''}</button>
    <a class="text-link" href="${sourceHref}">${step.id === 'handoff' ? 'Inspect the source artifacts' : 'See the canonical source'} ${icon('external', 15)}</a>
  </nav>`;
}

function provenanceLedger() {
  const items = [
    ['human', 'Human accepted frame'], ['human', 'Human accepted R0–R5 + Appetite'],
    ['human', 'Human selected shape A'], ['human', 'Human accepted behavior'],
    ['human', 'Human selected V1'], ['agent', 'Planning agent packaged context'],
  ];
  return `<section class="provenance-ledger" aria-labelledby="provenance-title"><h2 id="provenance-title">How it got here</h2><ol>${items.map(([role, label]) => `<li class="role-${role}"><span aria-hidden="true">${role === 'human' ? 'H' : 'PA'}</span><strong>${escapeHtml(label)}</strong>${icon('check', 17)}</li>`).join('')}</ol></section>`;
}

function contextPacket(step) {
  return `<section class="context-packet" aria-labelledby="packet-title"><h2 id="packet-title">What planning contributes</h2>
    <div class="packet-sheet"><header><span>${icon('file', 22)}</span><div><small>Active slice</small><strong>${escapeHtml(step.packet.active)}</strong></div></header>
      ${step.packet.sections.map((section) => `<section class="packet-row tone-${section.tone}"><h3>${escapeHtml(section.label)}</h3><ul>${section.items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></section>`).join('')}
    </div>
    ${collaborationExchange(step, true)}
  </section>`;
}

function handoffAssembly(step) {
  const { assembly } = step.packet;
  const card = (item, type) => `<article class="assembly-card is-${type}">
    <header><span>${icon(type === 'repository' ? 'github' : type === 'complete' ? 'target' : 'file', 22)}</span><div><h3>${escapeHtml(item.title)}</h3><small>${escapeHtml(item.status)}</small></div></header>
    <ul>${item.items.map((entry) => `<li>${escapeHtml(entry)}</li>`).join('')}</ul>
  </article>`;
  return `<section class="handoff-assembly" aria-labelledby="handoff-assembly-title">
    <header><h2 id="handoff-assembly-title">${escapeHtml(assembly.title)}</h2><p>${escapeHtml(assembly.caption)}</p></header>
    <div class="assembly-flow">
      ${card(assembly.inputs[0], 'planning')}
      <span class="assembly-operator is-plus" aria-hidden="true">+</span>
      ${card(assembly.inputs[1], 'repository')}
      <span class="assembly-operator is-arrow" aria-hidden="true">${icon('arrow', 23)}</span>
      ${card(assembly.result, 'complete')}
    </div>
  </section>`;
}

function fullContextPacket(step) {
  return `<section class="full-context-packet" aria-labelledby="full-packet-title">
    <header><div><h2 id="full-packet-title">What the complete packet must contain</h2><p>Planning fields are filled. Repository-specific fields stay visibly unresolved until the target codebase is inspected.</p></div><span>${icon('target', 21)} Inspectable handoff</span></header>
    <div class="packet-details">
      ${step.packet.details.map((section, index) => `<details class="packet-detail" data-packet-section="${escapeHtml(section.id)}" ${section.open ? 'open' : ''}>
        <summary><span>${index + 1}</span><div><strong>${escapeHtml(section.title)}</strong><small>${escapeHtml(section.summary)}</small></div>${icon('arrow', 18)}</summary>
        <div class="packet-detail-body"><dl>${section.rows.map((row) => `<div class="${row.status === 'unresolved' ? 'is-unresolved' : ''}"><dt>${escapeHtml(row.label)}${row.status === 'unresolved' ? '<span>Resolve in target repo</span>' : ''}</dt><dd><ul>${row.values.map((value) => `<li>${escapeHtml(value)}</li>`).join('')}</ul></dd></div>`).join('')}</dl></div>
      </details>`).join('')}
    </div>
  </section>`;
}

function walkthroughPage() {
  const index = Math.max(0, Math.min(state.walkthroughStep, walkthroughSteps.length - 1));
  const step = walkthroughSteps[index];
  const handoff = step.id === 'handoff';
  const reality = step.id === 'reality';
  const heading = handoff ? 'The planning handoff is ready.' : reality ? 'Compare the plan with reality.' : 'Watch a plan take shape.';
  const subheading = handoff
    ? 'Planning resolved the product decisions. Target-repository context completes the build-agent packet.'
    : reality
      ? 'After implementation, the same accepted artifacts make drift visible and decidable.'
      : 'Follow one human and one planning agent from messy notes to a build-ready slice.';
  return `<main id="main-content" class="walkthrough-page ${handoff ? 'is-handoff' : ''}">
    <header class="walkthrough-intro"><h1 tabindex="-1">${heading}</h1><p>${subheading}</p><div><strong>Simple Grocery List</strong><span>${index + 1} of ${walkthroughSteps.length}</span></div></header>
    ${walkthroughProgress()}
    ${handoff ? `${handoffAssembly(step)}<section class="handoff-workspace">${contextPacket(step)}${provenanceLedger()}</section>${fullContextPacket(step)}` : `
      <header class="walkthrough-stage-heading"><span>${index + 1}</span><div><h2 id="walkthrough-stage-title" tabindex="-1">${escapeHtml(step.title)}</h2><p><strong>Human:</strong> ${escapeHtml(step.humanMove)} <i aria-hidden="true">·</i> <strong>Agent:</strong> ${escapeHtml(step.agentMove)}</p></div></header>
      <section class="walkthrough-workspace ${step.visual ? 'has-stage-visual' : ''}" aria-label="${escapeHtml(step.label)} collaboration stage">
        ${inputPanel(step)}${collaborationExchange(step)}${planLedger()}${stageVisual(step)}${outputPanel(step)}
      </section>`}
    ${walkthroughControls(step, index)}
    ${handoff ? '<p class="handoff-note">Planning resolves the slice. Repository inspection completes the execution context.</p>' : ''}
  </main>`;
}

function compassPage() {
  const selected = entryStates.find((item) => item.id === state.selectedEntry) || entryStates[0];
  const selectedSkill = skillsBySlug.get(selected.skill);
  return `
    <main id="main-content" class="home-page compass-page">
      <section class="home-hero">
        <div class="hero-copy compact-hero">
          <p class="system-label">Planning compass</p>
          <h1>What is happening in your work?</h1>
          <p>Pick the closest observable state. Get one next move.</p>
        </div>
        <div class="entry-navigator" id="entry-navigator">
          <div class="entry-options" role="radiogroup" aria-label="What needs to become clearer?">
            <h2 class="sr-only">Choose the current state</h2>
            ${entryStates.map((item, index) => {
              const selectedItem = item.id === selected.id;
              return `<button class="entry-option tone-${item.tone} ${selectedItem ? 'is-selected' : ''}" type="button" role="radio" aria-checked="${selectedItem}" tabindex="${selectedItem ? '0' : '-1'}" data-action="select-entry" data-entry="${item.id}" data-index="${index}">
                <span class="radio-mark" aria-hidden="true"></span><span>${escapeHtml(item.label)}</span>
              </button>`;
            }).join('')}
          </div>
          <div class="recommendation tone-${selected.tone}" aria-live="polite">
            <span>Next move</span>
            <h2>${escapeHtml(selected.recommendation)}</h2>
            <p>${escapeHtml(selected.description)}</p>
            <dl class="recommendation-facts">
              <div><dt>${icon('file', 17)} Needs</dt><dd>${escapeHtml(selected.needs)}</dd></div>
              <div><dt>${icon('check', 17)} Stop when</dt><dd>${escapeHtml(selected.stop)}</dd></div>
            </dl>
            <p class="recommendation-caution">${icon('user', 17)} ${escapeHtml(selected.caution)}</p>
            <div class="recommendation-actions">
              <a class="button button-planning" href="#/skills/${selected.skill}/guide">${escapeHtml(selected.actionLabel || `Open ${selectedSkill?.title || selected.recommendation}`)} ${icon('arrow', 18)}</a>
              <a class="text-link" href="#/map?stage=${selected.mapStage}">See where this sits ${icon('arrow', 17)}</a>
            </div>
          </div>
        </div>
      </section>
      <section class="home-principles" aria-labelledby="principles-title">
        <div><p class="system-label">The whole idea</p><h2 id="principles-title">Explore freely. Promote deliberately.</h2></div>
        <ul>
          <li><strong>Explore</strong><span>Requirements, shapes, and evidence can loop.</span></li>
          <li><strong>Decide</strong><span>People accept direction, behavior, and slices.</span></li>
          <li><strong>Build</strong><span>Agents receive one selected slice—not the whole history.</span></li>
        </ul>
        <div class="home-next-links">
          <a class="button button-outline" href="#/map">Understand the planning model ${icon('arrow', 18)}</a>
          <a class="text-link" href="#/">Return to the hands-on experience ${icon('arrow', 18)}</a>
          <a class="text-link" href="#/skills/planning-router/guide">Still unsure? Use the router ${icon('arrow', 18)}</a>
        </div>
      </section>
    </main>`;
}

function mapPage(requestedStage) {
  if (requestedStage && mapStages.some((item) => item.id === requestedStage)) state.selectedMapStage = requestedStage;
  const selected = mapStages.find((item) => item.id === state.selectedMapStage) || mapStages[0];
  return `<main id="main-content" class="map-page">
    <header class="map-heading">
      <div><p class="system-label">Planning model</p><h1>How authority moves through the work.</h1></div>
      <p>This is a promotion model, not a task recipe. Exploration can loop; only explicit decisions make material buildable.</p>
    </header>
    <section class="map-workspace" aria-label="Interactive planning map">
      <div class="planning-map" role="list" aria-label="Planning stages">
        ${mapStages.map((item, index) => `<div class="map-stage-wrap" role="listitem">
          <button type="button" class="map-stage kind-${item.kind} ${item.id === selected.id ? 'is-selected' : ''}" aria-pressed="${item.id === selected.id}" data-action="select-map-stage" data-map-stage="${item.id}">
            <span class="map-stage-kind">${item.kind === 'gate' ? 'Human decision' : item.kind === 'loop' ? 'Exploration loop' : item.kind === 'artifact' ? 'Accepted behavior' : item.kind === 'reflection' ? 'Reality check' : item.kind === 'build' ? 'Active build' : 'Conditional support'}</span>
            <span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.short)}</small></span>
            ${item.helpers ? `<span class="map-stage-chips">${item.helpers.map((helper) => `<em>${escapeHtml(helper)}</em>`).join('')}</span>` : ''}
            ${item.optional ? `<span class="map-optional">${item.optional.map((helper) => `<em>${escapeHtml(helper)}</em>`).join('')}</span>` : ''}
          </button>
          ${index < mapStages.length - 1 ? `<span class="map-connector" aria-hidden="true">${icon('arrow', 20)}</span>` : ''}
        </div>`).join('')}
      </div>
      <div class="map-detail kind-${selected.kind}" role="region" aria-labelledby="map-detail-title" aria-live="polite">
        <p class="system-label">${selected.kind === 'gate' ? 'Human decision' : 'Authority check'}</p>
        <h2 id="map-detail-title" tabindex="-1">${escapeHtml(selected.title)}</h2>
        <p>${escapeHtml(selected.summary)}</p>
        <dl>
          <div><dt>Needs</dt><dd>${escapeHtml(selected.needs)}</dd></div>
          <div><dt>Stop when</dt><dd>${escapeHtml(selected.stop)}</dd></div>
          <div><dt>Never</dt><dd>${escapeHtml(selected.never)}</dd></div>
        </dl>
        <a class="button button-planning" href="#${selected.route}">Open the relevant guide ${icon('arrow', 18)}</a>
      </div>
    </section>
    <section class="kickoff-placement" aria-labelledby="kickoff-placement-title">
      <span class="optional-line" aria-hidden="true"></span>
      <div><p class="system-label">Optional side branch after slice selection</p><h2 id="kickoff-placement-title">Kickoff orients. It never kicks off the sequence.</h2><p>Use it only after the selected-design breadboard and active slice already exist. Scope still comes from the selected project, slice, contracts, and accepted behavior.</p></div>
      <a class="text-link" href="#/skills/kickoff-doc/guide">Open kickoff reference ${icon('arrow', 18)}</a>
    </section>
  </main>`;
}

function skillsPage(routeSlug) {
  if (routeSlug && skillsBySlug.has(routeSlug)) state.selectedSkill = routeSlug;
  const query = state.skillQuery.trim().toLowerCase();
  const visibleGroups = skillGroups.map((group) => ({
    ...group,
    items: group.skills.map((slug) => skillsBySlug.get(slug)).filter(Boolean).filter((skill) => {
      const categoryMatches = state.skillCategory === 'all' || group.id === state.skillCategory;
      const presentation = skillModel[skill.slug];
      const queryMatches = !query || `${skill.title} ${presentation.useWhen} ${presentation.produces} ${presentation.needs}`.toLowerCase().includes(query);
      return categoryMatches && queryMatches;
    }),
  })).filter((group) => group.items.length > 0);
  const visibleSlugs = new Set(visibleGroups.flatMap((group) => group.items.map((item) => item.slug)));
  const active = skillsBySlug.get(visibleSlugs.has(state.selectedSkill) ? state.selectedSkill : visibleGroups[0]?.items[0]?.slug) || skillsBySlug.get('shaping');
  const detail = skillModel[active.slug];
  state.selectedSkill = active.slug;

  return `
    <main id="main-content" class="skills-layout">
      <section id="skill-list" class="skills-main">
        <div class="page-heading"><h1>Reference</h1><p>The canonical details live here. Start with the experience or compass; open a skill when you need its exact contract.</p></div>
        <nav class="reference-paths" aria-label="Reference collections"><a href="#/guides/start-here">Guides</a><a href="#/examples">Source examples</a><a href="${REPOSITORY_URL}" target="_blank" rel="noreferrer">GitHub repository ${icon('external', 14)}</a></nav>
        <div class="skill-controls">
          <label class="field-with-icon">${icon('search', 18)}<span class="sr-only">Search skills</span><input id="skill-search" value="${escapeHtml(state.skillQuery)}" placeholder="Search skills"><kbd>/</kbd></label>
          <div class="filter-tabs" aria-label="Filter by category">
            ${['all', 'core', 'conditional', 'handoff'].map((category) => `<button type="button" class="${state.skillCategory === category ? 'is-selected' : ''}" aria-pressed="${state.skillCategory === category}" data-action="filter-skills" data-category="${category}">${category === 'all' ? 'All' : category[0].toUpperCase() + category.slice(1)}</button>`).join('')}
          </div>
        </div>
        <div class="skill-groups" aria-live="polite">
          ${visibleGroups.length ? visibleGroups.map((group) => `<section class="skill-group"><div class="skill-group-heading"><h2>${group.label}</h2><p>${escapeHtml(group.description)}</p></div><div class="skill-rows">
            ${group.items.map((skill) => {
              const presentation = skillModel[skill.slug];
              return `<button type="button" class="skill-row tone-${presentation.tone} ${skill.slug === active.slug ? 'is-selected' : ''}" aria-pressed="${skill.slug === active.slug}" data-action="select-skill" data-skill="${skill.slug}"><strong>${escapeHtml(skill.title)}</strong><span>${escapeHtml(presentation.useWhen)}</span><small>${presentation.stage}</small></button>`;
            }).join('')}
          </div></section>`).join('') : '<div class="empty-state"><strong>No skill matches that search.</strong><span>Try “state”, “context”, or “drift”.</span></div>'}
        </div>
      </section>
      <aside class="skill-detail tone-${detail.tone}" aria-labelledby="skill-detail-title" aria-live="polite">
        <div class="skill-detail-heading"><p class="system-label">${escapeHtml(detail.stage)}</p><h2 id="skill-detail-title" tabindex="-1">${escapeHtml(active.title)}</h2><p>${escapeHtml(detail.useWhen)}</p></div>
        <dl>
          <div><dt>${icon('target')} Needs</dt><dd>${escapeHtml(detail.needs)}</dd></div>
          <div><dt>${icon('file')} Produces</dt><dd>${escapeHtml(detail.produces)}</dd></div>
          <div><dt>${icon('user')} Boundary</dt><dd>${escapeHtml(detail.gate)}</dd></div>
        </dl>
        ${detail.modes ? `<div class="mode-strip" aria-label="Breadboarding modes">${detail.modes.map((mode) => `<div><strong>${escapeHtml(mode.label)}</strong><span>${escapeHtml(mode.role)}</span><small>${escapeHtml(mode.authority)}</small></div>`).join('')}</div>` : ''}
        <div class="skill-detail-actions">
          <a class="button button-planning" href="#/skills/${active.slug}/guide">${icon('external', 18)} Open guide</a>
          <button class="button button-outline" type="button" data-action="copy-skill-prompt" data-skill="${active.slug}">${icon('copy', 18)} Copy starter prompt</button>
          <code>${escapeHtml(active.sourcePath)}</code>
        </div>
        <a class="detail-next-link" href="#/skills/${active.slug}/guide">Read the authoritative instructions ${icon('arrow', 17)}</a>
        <button class="detail-back-link" type="button" data-action="back-to-skill-list">${icon('back', 17)} Back to the skill list</button>
      </aside>
    </main>`;
}

function sidebarGroups(kind) {
  if (kind === 'skill') {
    return skillGroups.map((group) => ({
      label: group.label,
      items: group.skills.map((slug) => skillsBySlug.get(slug)).filter(Boolean).map((item) => ({
        ...item, route: `/skills/${item.slug}/guide`,
      })),
    }));
  }
  return [
    ...guideGroups.map((group) => ({
      label: group.label,
      items: group.slugs.map((slug) => docsBySlug.get(slug)).filter(Boolean).map((item) => ({
        ...item, route: `/guides/${item.slug}`,
      })),
    })),
    ...resourceGroups.map((group) => ({
      label: group.label,
      items: group.items.map((item) => ({ ...item, route: `/resources/${item.slug}` })),
    })),
  ];
}

function sidebarSections(groups, activeSlug, labelPrefix, mobile = false) {
  return groups.map((group) => `<section><h3>${escapeHtml(group.label)}</h3>${mobile ? '<div class="mobile-guide-links">' : `<nav aria-label="${escapeHtml(`${group.label} ${labelPrefix}`)}">`}${group.items.map((item) => `<a class="${item.slug === activeSlug ? 'is-active' : ''}" href="#${item.route}" ${item.slug === activeSlug ? 'aria-current="page"' : ''}>${escapeHtml(item.title)}</a>`).join('')}${mobile ? '</div>' : '</nav>'}</section>`).join('');
}

function guideSidebar(kind, activeSlug) {
  const groups = sidebarGroups(kind);
  const heading = kind === 'skill' ? 'Skills' : 'Guides and references';
  const current = groups.flatMap((group) => group.items).find((item) => item.slug === activeSlug);
  return `<aside class="docs-sidebar" aria-labelledby="docs-sidebar-title"><h2 id="docs-sidebar-title">${heading}</h2>
    <div class="docs-sidebar-groups">${sidebarSections(groups, activeSlug, kind === 'skill' ? 'skill guides' : 'documentation')}</div>
    <details class="docs-mobile-disclosure"><summary><span>Browse ${kind === 'skill' ? 'skills' : 'documentation'}</span><small>${escapeHtml(current?.title || '')}</small></summary><div class="docs-mobile-groups">${sidebarSections(groups, activeSlug, 'mobile documentation', true)}</div></details>
  </aside>`;
}

function guidePage(kind, slug, section) {
  const source = kind === 'skill' ? skillsBySlug : kind === 'resource' ? resourcesBySlug : docsBySlug;
  const item = source.get(slug);
  if (!item) return notFoundPage();
  const isSkill = kind === 'skill';
  const route = isSkill ? `/skills/${slug}/guide` : kind === 'resource' ? `/resources/${slug}` : `/guides/${slug}`;
  const orderedItems = sidebarGroups(isSkill ? 'skill' : 'guide').flatMap((group) => group.items);
  const index = orderedItems.findIndex((entry) => entry.sourcePath === item.sourcePath);
  const previous = index > 0 ? orderedItems[index - 1] : null;
  const next = index >= 0 && index < orderedItems.length - 1 ? orderedItems[index + 1] : null;
  const rendered = renderMarkdown(item.raw, item.sourcePath, route);
  const visibleHeadings = rendered.headings.filter((heading) => heading.depth === 2 || heading.depth === 3);
  queuePostRender(section);
  return `<main id="main-content" class="docs-layout">
    ${guideSidebar(isSkill ? 'skill' : 'guide', slug)}
    <article class="docs-article">
      <div class="article-utilities"><span><a href="#${isSkill ? '/skills' : '/guides/start-here'}">${isSkill ? 'Skills' : 'Guides'}</a> / ${escapeHtml(item.title)}</span><a href="${REPOSITORY_URL}/blob/main/${item.sourcePath}" target="_blank" rel="noreferrer">Edit on GitHub ${icon('external', 15)}</a></div>
      <div class="markdown-body">${rendered.html}</div>
      <nav class="article-pagination" aria-label="Guide pagination">
        ${previous ? `<a href="#${previous.route}">${icon('back', 17)}<span><small>Previous</small><strong>${escapeHtml(previous.title)}</strong></span></a>` : '<span></span>'}
        ${next ? `<a href="#${next.route}"><span><small>Next</small><strong>${escapeHtml(next.title)}</strong></span>${icon('arrow', 17)}</a>` : ''}
      </nav>
    </article>
    <aside class="page-toc" aria-labelledby="page-toc-title"><h2 id="page-toc-title">On this page</h2><span class="reading-rule" aria-hidden="true"><i></i></span><nav aria-label="Sections in ${escapeHtml(item.title)}">${visibleHeadings.map((heading) => `<a class="depth-${heading.depth}" href="#${route}?section=${encodeURIComponent(heading.id)}">${escapeHtml(heading.title)}</a>`).join('')}</nav></aside>
  </main>`;
}

function exampleIndexPage() {
  return `<main id="main-content" class="example-index"><div class="page-heading"><h1>Examples</h1><p>Follow real artifact sequences and see why each planning move exists.</p></div><div class="example-index-list">
    ${content.examples.map((example, index) => `<a href="#/examples/${example.slug}"><span class="example-number">${String(index + 1).padStart(2, '0')}</span><span><strong>${escapeHtml(example.title)}</strong><small>${escapeHtml(example.description)}</small></span>${icon('arrow')}</a>`).join('')}
  </div></main>`;
}

function fileLabel(file) {
  return file.title.replace(/^[^—]+—\s*/, '').replace(/Step-by-Step Example/, 'Overview');
}

function firstPrompt(markdown) {
  const match = (markdown || '').match(/(?:Example prompt:\s*)?```(?:text)?\s*\n([\s\S]*?)```/i);
  return match ? match[1].trim() : '';
}

function examplePrompt(example, selected, stage) {
  const sourcePrompt = firstPrompt(selected.raw);
  if (sourcePrompt) return { text: sourcePrompt, label: 'Copy source prompt', description: 'source prompt' };
  if (stage?.prompt) return { text: stage.prompt, label: 'Copy suggested prompt', description: 'suggested prompt' };
  return {
    text: `Use ${selected.sourcePath} as a worked reference for ${selected.title}. Apply the same artifact role to [your source material], keep working evidence separate from accepted intent, and do not cross any applicable human decision gate.`,
    label: 'Copy suggested prompt',
    description: 'suggested prompt',
  };
}

function examplePage(slug, requestedFile, section) {
  const example = content.examples.find((item) => item.slug === slug);
  if (!example) return notFoundPage();
  const artifactFiles = example.files.filter((file) => file.name !== 'README.md');
  const isSimple = slug === 'simple-grocery-list';
  const primaryFiles = isSimple
    ? simpleExampleModel.primaryFiles.map((name) => artifactFiles.find((file) => file.name === name)).filter(Boolean)
    : artifactFiles;
  const optionalFiles = isSimple
    ? simpleExampleModel.optionalFiles.map((name) => artifactFiles.find((file) => file.name === name)).filter(Boolean)
    : [];
  const defaultName = primaryFiles[0]?.name || artifactFiles[0]?.name || example.files[0]?.name;
  const selected = example.files.find((file) => file.name === requestedFile) || example.files.find((file) => file.name === defaultName) || example.files[0];
  const selectedIndex = primaryFiles.findIndex((file) => file.name === selected.name);
  const previous = selectedIndex > 0 ? primaryFiles[selectedIndex - 1] : null;
  const next = selectedIndex >= 0 && selectedIndex < primaryFiles.length - 1 ? primaryFiles[selectedIndex + 1] : null;
  const selectedStage = isSimple ? simpleExampleModel.stages[selected.name] : null;
  const prompt = examplePrompt(example, selected, selectedStage);
  const route = `/examples/${slug}?file=${encodeURIComponent(selected.name)}`;
  const rendered = renderMarkdown(selected.raw, selected.sourcePath, route, { headingOffset: 1 });
  const notes = isSimple ? (simpleExampleModel.notes[selected.name] || []) : ['Each artifact has one clear job', 'Accepted intent stays separate from exploratory evidence', 'The set follows the complexity actually present'];
  const simpleTrail = isSimple ? `<nav class="artifact-trail" aria-label="Grocery-list planning story">
    <p class="system-label">Required story</p>
    ${primaryFiles.map((file, index) => {
      const stage = simpleExampleModel.stages[file.name];
      const selectedItem = file.name === selected.name;
      const buildGap = file.name === '05-breadboard-reflection.md' ? `<div class="artifact-gap"><span>${icon('check', 16)}</span><div><strong>Implementation</strong><small>The selected V1 is built here. This example omits the code.</small></div></div>` : '';
      return `${buildGap}<a class="artifact-stage tone-${stage.tone} ${selectedItem ? 'is-selected' : ''}" href="#/examples/${slug}?file=${encodeURIComponent(file.name)}" ${selectedItem ? 'aria-current="step"' : ''}><span class="artifact-marker">${index + 1}</span><span><strong>${escapeHtml(stage.label)}</strong><small>${escapeHtml(stage.description)}</small></span></a>`;
    }).join('')}
    <div class="optional-artifacts"><p class="system-label">Optional orientation</p>${optionalFiles.map((file) => {
      const stage = simpleExampleModel.stages[file.name];
      const selectedItem = file.name === selected.name;
      return `<a class="artifact-stage is-optional tone-${stage.tone} ${selectedItem ? 'is-selected' : ''}" href="#/examples/${slug}?file=${encodeURIComponent(file.name)}" ${selectedItem ? 'aria-current="step"' : ''}><span class="artifact-marker">↳</span><span><strong>${escapeHtml(stage.label)}</strong><em>After selected design + V1</em><small>${escapeHtml(stage.description)}</small></span></a>`;
    }).join('')}</div>
  </nav>` : `<nav class="artifact-trail" aria-label="Example artifacts">${artifactFiles.map((file, index) => {
    const selectedItem = file.name === selected.name;
    return `<a class="artifact-stage tone-evidence ${selectedItem ? 'is-selected' : ''}" href="#/examples/${slug}?file=${encodeURIComponent(file.name)}" ${selectedItem ? 'aria-current="step"' : ''}><span class="artifact-marker">${index + 1}</span><span><strong>${escapeHtml(fileLabel(file))}</strong><small>${escapeHtml(file.description)}</small></span></a>`;
  }).join('')}</nav>`;
  queuePostRender(section);
  return `<main id="main-content" class="example-page">
    <div class="example-heading"><p class="system-label">Worked example</p><h1>${escapeHtml(example.title.replace(/\s+—\s+Step-by-Step Example$/, ''))}</h1><p>${isSimple ? 'Follow the decisions, not a pile of documents. Optional artifacts sit outside the required story.' : escapeHtml(example.description)}</p><a class="back-link" href="#/examples">${icon('back', 17)} All examples</a></div>
    <div class="example-workspace">
      ${simpleTrail}
      <article class="artifact-preview"><div class="markdown-body">${rendered.html}</div></article>
      <aside class="learning-notes"><h2>What to notice</h2><ul>${notes.map((note) => `<li>${escapeHtml(note)}</li>`).join('')}</ul>
        <div class="example-actions"><a class="button button-planning" href="${REPOSITORY_URL}/blob/main/${selected.sourcePath}" target="_blank" rel="noreferrer">${icon('external', 18)} Open source file</a><button class="button button-outline" type="button" data-action="copy-text" data-copy="${escapeHtml(prompt.text)}">${icon('copy', 18)} ${prompt.label}</button><code>${escapeHtml(selected.sourcePath)}</code></div>
        <div class="artifact-pagination">${previous ? `<a href="#/examples/${slug}?file=${encodeURIComponent(previous.name)}">${icon('back', 17)}<span><small>Previous</small>${escapeHtml(fileLabel(previous))}</span></a>` : '<span></span>'}${next ? `<a href="#/examples/${slug}?file=${encodeURIComponent(next.name)}"><span><small>Next</small>${escapeHtml(fileLabel(next))}</span>${icon('arrow', 17)}</a>` : ''}</div>
      </aside>
    </div>
    <section class="try-section"><h2>Try it yourself</h2><p>Use this ${prompt.description} with your AI partner, then compare the result with the source artifact.</p><div class="prompt-block"><code>${escapeHtml(prompt.text)}</code><button type="button" data-action="copy-text" data-copy="${escapeHtml(prompt.text)}" aria-label="${prompt.label}">${icon('copy', 18)}</button></div></section>
  </main>`;
}

function notFoundPage() {
  return `<main id="main-content" class="not-found"><p class="system-label">404</p><h1>This path is outside the map.</h1><p>Return to the portal and choose the smallest useful next move.</p><a class="button button-primary" href="#/">Back to overview</a></main>`;
}

function rankSearchResults(query) {
  const normalized = query.trim().toLowerCase();
  if (!normalized) return [];
  const terms = normalized.split(/\s+/).filter(Boolean);
  return searchItems.map((item, order) => {
    const title = item.title.toLowerCase();
    const slug = decodeURIComponent(item.slug || '').toLowerCase().replace(/[-_/]+/g, ' ');
    const description = (item.description || '').toLowerCase();
    const searchText = (item.searchText || '').toLowerCase();
    const haystack = `${title} ${slug} ${description} ${searchText}`;
    if (!terms.every((term) => haystack.includes(term))) return null;
    let score = 0;
    if (title === normalized) score += 1_000;
    if (slug === normalized) score += 700;
    if (title.startsWith(normalized)) score += 350;
    if (title.includes(normalized)) score += 220;
    if (slug.includes(normalized)) score += 160;
    for (const term of terms) {
      if (title.split(/\W+/).includes(term)) score += 90;
      else if (title.includes(term)) score += 55;
      if (description.includes(term)) score += 20;
      if (searchText.includes(term)) score += 4;
    }
    if (item.type === 'Skill') score += 25;
    return { item, score, order };
  }).filter(Boolean).sort((left, right) => right.score - left.score || left.order - right.order).map(({ item }) => item);
}

function searchDialog() {
  if (!state.searchOpen) return '';
  const query = state.searchQuery.trim().toLowerCase();
  const rankedResults = query
    ? rankSearchResults(query)
    : searchItems.filter((item) => ['start-here', 'shaping', 'simple-grocery-list'].includes(item.slug));
  const results = rankedResults.slice(0, SEARCH_RESULT_LIMIT);
  const resultLabel = rankedResults.length > results.length ? `Showing ${results.length} of ${rankedResults.length} results` : `${rankedResults.length} results`;
  return `<div class="dialog-backdrop" data-action="close-search-backdrop"><section class="search-dialog" role="dialog" aria-modal="true" aria-labelledby="search-dialog-title"><h2 id="search-dialog-title" class="sr-only">Search documentation</h2>
    <div class="dialog-search-row">${icon('search', 21)}<input id="global-search" value="${escapeHtml(state.searchQuery)}" placeholder="Search all portal content" aria-label="Search all portal content"><button class="icon-button compact" type="button" data-action="close-search" aria-label="Close search">${icon('close', 20)}</button></div>
    <div class="search-results" aria-live="polite" data-result-total="${rankedResults.length}"><p class="system-label">${query ? resultLabel : 'Suggested paths'}</p>
      ${results.length ? results.map((item) => `<a class="search-result" href="#${item.route}"><span class="result-icon">${icon(item.type === 'Skill' ? 'target' : 'file', 18)}</span><span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.description)}</small></span><span class="result-type">${item.type}</span>${icon('arrow', 18)}</a>`).join('') : '<div class="empty-search"><strong>No matching path found.</strong><span>Try a skill, guide, example, template, or reference.</span></div>'}
    </div>
  </section></div>`;
}

let pendingSection = '';
function queuePostRender(section) {
  pendingSection = section || '';
}

async function postRender() {
  const diagrams = [...document.querySelectorAll('.mermaid:not([data-processed])')];
  if (diagrams.length) {
    try {
      await mermaid.run({ nodes: diagrams, suppressErrors: true });
    } catch (error) {
      console.warn('A Mermaid diagram could not be rendered.', error);
    }
  }
  if (pendingSection) {
    document.getElementById(pendingSection)?.scrollIntoView({ block: 'start' });
    pendingSection = '';
  }
}

function render({ preserveScroll = false } = {}) {
  const { path, query } = currentRoute();
  let active = 'walkthrough';
  let page = walkthroughPage();
  const parts = path.split('/').filter(Boolean);
  if (parts[0] === 'compass') {
    active = 'compass';
    page = compassPage();
  } else if (parts[0] === 'skills') {
    active = 'reference';
    page = parts[2] === 'guide' ? guidePage('skill', parts[1], query.get('section')) : skillsPage(parts[1]);
  } else if (parts[0] === 'map') {
    active = 'model';
    page = mapPage(query.get('stage'));
  } else if (parts[0] === 'guides') {
    active = 'reference';
    page = guidePage('guide', parts[1] || 'start-here', query.get('section'));
  } else if (parts[0] === 'resources') {
    active = 'reference';
    page = guidePage('resource', parts[1], query.get('section'));
  } else if (parts[0] === 'examples') {
    active = 'reference';
    page = parts[1] ? examplePage(parts[1], query.get('file'), query.get('section')) : exampleIndexPage();
  } else if (path !== '/') {
    page = notFoundPage();
  }

  root.innerHTML = `${header(active)}${page}${searchDialog()}<div id="toast-region" aria-live="polite"></div>`;
  document.body.classList.toggle('dialog-open', state.searchOpen);
  if (!preserveScroll && !query.get('section')) window.scrollTo({ top: 0, behavior: 'auto' });

  if (state.searchOpen) {
    requestAnimationFrame(() => {
      const input = document.getElementById('global-search');
      input?.focus();
      input?.setSelectionRange(input.value.length, input.value.length);
    });
  } else if (state.restoreFocus) {
    const target = state.restoreFocus;
    state.restoreFocus = null;
    requestAnimationFrame(() => document.getElementById(target)?.focus());
  }
  requestAnimationFrame(postRender);
}

function openSearch(trigger) {
  state.restoreFocus = trigger?.id || 'search-trigger';
  state.searchQuery = '';
  state.searchOpen = true;
  state.mobileMenuOpen = false;
  render({ preserveScroll: true });
}

function closeSearch() {
  state.searchOpen = false;
  render({ preserveScroll: true });
}

function starterPrompt(skill) {
  return `Use the ${skill.title} skill on [source material].\n\nPreserve working versus accepted intent, make unknowns explicit, and do not cross any applicable human decision gate.`;
}

async function copyText(value) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
    } else {
      const textarea = document.createElement('textarea');
      textarea.value = value;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.append(textarea);
      textarea.select();
      document.execCommand('copy');
      textarea.remove();
    }
    showToast('Copied to clipboard');
  } catch {
    showToast('Copy failed — select the text manually');
  }
}

function showToast(message) {
  const region = document.getElementById('toast-region');
  if (!region) return;
  region.innerHTML = `<div class="toast">${icon('check', 17)} ${escapeHtml(message)}</div>`;
  window.setTimeout(() => { if (region) region.innerHTML = ''; }, 1800);
}

function focusWalkthroughStage() {
  requestAnimationFrame(() => {
    document.querySelector('.walkthrough-progress [aria-current="step"]')?.scrollIntoView({ behavior: 'auto', block: 'nearest', inline: 'center' });
    (document.getElementById('walkthrough-stage-title') || document.querySelector('.walkthrough-intro h1'))?.focus({ preventScroll: true });
  });
}

document.addEventListener('click', (event) => {
  const actionTarget = event.target.closest('[data-action]');
  const action = actionTarget?.dataset.action;
  if (action === 'open-search') openSearch(actionTarget);
  if (action === 'close-search') closeSearch();
  if (action === 'close-search-backdrop' && event.target === actionTarget) closeSearch();
  if (action === 'toggle-menu') {
    state.mobileMenuOpen = !state.mobileMenuOpen;
    render({ preserveScroll: true });
  }
  if (action === 'select-walkthrough-stage') {
    state.walkthroughStep = Math.max(0, Math.min(Number(actionTarget.dataset.stageIndex), walkthroughSteps.length - 1));
    state.walkthroughPanels = { input: false, output: false, ledger: false };
    render();
    focusWalkthroughStage();
  }
  if (action === 'next-walkthrough-stage') {
    state.walkthroughStep = Math.min(walkthroughSteps.length - 1, state.walkthroughStep + 1);
    state.walkthroughPanels = { input: false, output: false, ledger: false };
    render();
    focusWalkthroughStage();
  }
  if (action === 'previous-walkthrough-stage') {
    state.walkthroughStep = Math.max(0, state.walkthroughStep - 1);
    state.walkthroughPanels = { input: false, output: false, ledger: false };
    render();
    focusWalkthroughStage();
  }
  if (action === 'reset-walkthrough') {
    state.walkthroughStep = 0;
    state.walkthroughPanels = { input: false, output: false, ledger: false };
    render();
    focusWalkthroughStage();
  }
  if (action === 'toggle-walkthrough-panel') {
    const panel = actionTarget.dataset.panel;
    if (Object.prototype.hasOwnProperty.call(state.walkthroughPanels, panel)) {
      state.walkthroughPanels[panel] = !state.walkthroughPanels[panel];
      render({ preserveScroll: true });
      requestAnimationFrame(() => document.querySelector(`[data-action="toggle-walkthrough-panel"][data-panel="${panel}"]`)?.focus());
    }
  }
  if (action === 'inspect-shape') {
    state.inspectedShape = actionTarget.dataset.shape === 'b' ? 'b' : 'a';
    render({ preserveScroll: true });
    requestAnimationFrame(() => document.querySelector(`[data-action="inspect-shape"][data-shape="${state.inspectedShape}"]`)?.focus());
  }
  if (action === 'select-entry') {
    state.selectedEntry = actionTarget.dataset.entry;
    render({ preserveScroll: true });
    requestAnimationFrame(() => document.querySelector(`[data-entry="${state.selectedEntry}"]`)?.focus());
  }
  if (action === 'select-map-stage') {
    const nextStage = actionTarget.dataset.mapStage;
    state.selectedMapStage = nextStage;
    const nextHash = `#/map?stage=${encodeURIComponent(nextStage)}`;
    if (location.hash === nextHash) render({ preserveScroll: true });
    else location.hash = nextHash;
    requestAnimationFrame(() => document.getElementById('map-detail-title')?.focus({ preventScroll: true }));
  }
  if (action === 'filter-skills') {
    state.skillCategory = actionTarget.dataset.category;
    render({ preserveScroll: true });
  }
  if (action === 'select-skill') {
    state.selectedSkill = actionTarget.dataset.skill;
    render({ preserveScroll: true });
    if (window.matchMedia('(max-width: 900px)').matches) {
      requestAnimationFrame(() => {
        document.querySelector('.skill-detail')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        document.getElementById('skill-detail-title')?.focus({ preventScroll: true });
      });
    }
  }
  if (action === 'back-to-skill-list') {
    document.getElementById('skill-list')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    window.setTimeout(() => document.querySelector('.skill-row.is-selected')?.focus(), 350);
  }
  if (action === 'copy-skill-prompt') copyText(starterPrompt(skillsBySlug.get(actionTarget.dataset.skill)));
  if (action === 'copy-text') copyText(actionTarget.dataset.copy || '');
  if (event.target.closest('.primary-nav a, .site-brand')) state.mobileMenuOpen = false;
});

document.addEventListener('input', (event) => {
  if (event.target.id === 'skill-search') {
    state.skillQuery = event.target.value;
    render({ preserveScroll: true });
    requestAnimationFrame(() => {
      const input = document.getElementById('skill-search');
      input?.focus();
      input?.setSelectionRange(input.value.length, input.value.length);
    });
  }
  if (event.target.id === 'global-search') {
    state.searchQuery = event.target.value;
    render({ preserveScroll: true });
  }
});

document.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    openSearch(document.activeElement);
    return;
  }
  if (event.key === 'Escape' && state.searchOpen) {
    event.preventDefault();
    closeSearch();
    return;
  }
  if (event.key === 'Escape' && state.mobileMenuOpen) {
    event.preventDefault();
    state.mobileMenuOpen = false;
    render({ preserveScroll: true });
    requestAnimationFrame(() => document.getElementById('menu-button')?.focus());
    return;
  }
  if (!state.searchOpen && event.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
    const { path } = currentRoute();
    if (path.startsWith('/skills')) {
      event.preventDefault();
      document.getElementById('skill-search')?.focus();
    }
  }
  const radio = event.target.closest?.('.entry-option[role="radio"]');
  if (radio && ['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft', 'Home', 'End'].includes(event.key)) {
    event.preventDefault();
    const currentIndex = Number(radio.dataset.index);
    let nextIndex = currentIndex;
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % entryStates.length;
    if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + entryStates.length) % entryStates.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = entryStates.length - 1;
    state.selectedEntry = entryStates[nextIndex].id;
    render({ preserveScroll: true });
    requestAnimationFrame(() => document.querySelector(`[data-entry="${state.selectedEntry}"]`)?.focus());
  }
  if (state.searchOpen && event.key === 'Tab') {
    const dialog = document.querySelector('.search-dialog');
    const focusable = [...(dialog?.querySelectorAll('input, button, a[href]') || [])];
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault(); first.focus();
    }
  }
});

window.addEventListener('hashchange', () => {
  state.searchOpen = false;
  state.mobileMenuOpen = false;
  render();
});

render();
window.__PLANNING_PORTAL_READY__ = true;
