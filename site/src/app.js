import DOMPurify from 'dompurify';
import { marked } from 'marked';
import mermaid from 'mermaid';
import content from './generated/content.json';

const REPOSITORY_URL = 'https://github.com/mattlane66/planning-skills-for-agents-and-humans';
const SEARCH_RESULT_LIMIT = 15;
const root = document.getElementById('root');

const state = {
  selectedEntry: 'solution',
  skillCategory: 'all',
  skillQuery: '',
  selectedSkill: 'shaping',
  searchOpen: false,
  searchQuery: '',
  mobileMenuOpen: false,
  restoreFocus: null,
};

const workflowSteps = [
  { title: 'Explore', description: 'Requirements, shapes, fit, and evidence stay fluid.', tone: 'evidence' },
  { title: 'Accept judging inputs', description: 'A person accepts requirements, Appetite, and the cut line.', tone: 'planning', gate: true },
  { title: 'Human selection', description: 'A person selects, revises, or stops after comparing fit.', tone: 'planning', gate: true },
  { title: 'Selected design', description: 'Accepted behavior becomes explicit.', tone: 'planning' },
  { title: 'Slice', description: 'Choose one demoable implementation boundary.', tone: 'implementation' },
  { title: 'Build', description: 'Execute with bounded context and verification.', tone: 'verification' },
  { title: 'Reflect', description: 'Compare accepted intent with reality.', tone: 'reflection' },
];

const entryPoints = [
  {
    id: 'requirements', label: 'Requirements', icon: 'file', recommendation: 'Shaping', slug: 'shaping',
    description: 'Start R-first: clarify needs and constraints, then explore shapes and fit without forcing a fixed sequence.',
  },
  {
    id: 'solution', label: 'A solution idea', icon: 'bulb', recommendation: 'Shaping', slug: 'shaping',
    description: 'Explore requirements, solution shapes, fit, and appetite without selecting on the user’s behalf.',
  },
  {
    id: 'evidence', label: 'Evidence or a prototype', icon: 'flask', recommendation: 'Shaping', slug: 'shaping',
    description: 'Treat existing evidence as a starting point, extract working requirements and shapes, and test what it changes.',
  },
  {
    id: 'uncertainty', label: 'One uncertainty', icon: 'help', recommendation: 'Planning Router', slug: 'planning-router',
    description: 'Identify the smallest next move: a focused spike, candidate breadboard, framing pass, or no planning skill at all.',
  },
];

const skillGroups = [
  { id: 'core', label: 'Core planning moves', skills: ['planning-router', 'framing-doc', 'shaping', 'breadboarding'] },
  { id: 'conditional', label: 'Conditional moves', skills: ['wayfinding', 'sketch-reconciliation', 'statechart', 'interface-contracts', 'executable-breadboards'] },
  { id: 'handoff', label: 'Handoff and reflection', skills: ['dumplink', 'kickoff-doc', 'feed-planning-context', 'breadboard-reflection'] },
];

const skillPresentation = {
  'planning-router': { stage: 'Start here', tone: 'evidence', useWhen: 'You have mixed planning context and do not yet know which move will resolve the current uncertainty.', produces: 'Exactly one recommended next move, or an explicit recommendation to use no planning skill.', gate: 'The router recommends but does not select a solution or scope.' },
  'framing-doc': { stage: 'Start here', tone: 'evidence', useWhen: 'Raw notes, research, requests, or transcripts do not yet express a clear problem and outcome.', produces: 'A concise frame with source, current situation, problem, outcome, and boundaries.', gate: 'A person accepts or revises the problem boundary.' },
  shaping: { stage: 'During shaping', tone: 'planning', useWhen: 'Requirements, a solution idea, a prototype, or mixed evidence needs comparison.', produces: 'Working and accepted requirements, appetite, candidate shapes, fit evidence, and a recorded decision.', gate: 'A person selects, revises, or stops.' },
  breadboarding: { stage: 'Explore or specify', tone: 'planning', useWhen: 'Current, candidate, or selected behavior needs to become concrete as places, affordances, stores, and wiring.', produces: 'A declared current-state, candidate-shape, or selected-design behavior map.', gate: 'Candidate evidence cannot become selected intent without explicit selection and reconciliation.' },
  wayfinding: { stage: 'Across sessions', tone: 'implementation', useWhen: 'A bounded planning destination requires several dependent decisions or investigations across sessions.', produces: 'A shared map of decision, evidence, prototype, and prerequisite tickets.', gate: 'Accepted results still land in their canonical planning artifacts.' },
  'sketch-reconciliation': { stage: 'During shaping', tone: 'implementation', useWhen: 'A screenshot, wireframe, mockup, or whiteboard may clarify or contradict accepted planning.', produces: 'Visual observations, proposed deltas, and synchronized accepted updates.', gate: 'A person accepts or rejects consequential deltas.' },
  statechart: { stage: 'After selection', tone: 'implementation', useWhen: 'Accepted behavior has retries, timeouts, approvals, lifecycle stages, or several valid actions per state.', produces: 'A state inventory, transition table, Mermaid projection, and explicit gaps.', gate: 'The statechart remains derived from accepted selected-design behavior.' },
  'interface-contracts': { stage: 'After selection', tone: 'verification', useWhen: 'A selected slice crosses a meaningful boundary with ambiguous inputs, outputs, branches, or errors.', produces: 'A plain-language contract for the named boundary.', gate: 'Open boundary decisions remain explicit until accepted.' },
  'executable-breadboards': { stage: 'Before build', tone: 'verification', useWhen: 'A selected slice needs fixtures, example runs, edge cases, and acceptance tests.', produces: 'A buildable behavioral handoff with expected results.', gate: 'The executable evidence cannot expand the selected slice.' },
  dumplink: { stage: 'Before build', tone: 'verification', useWhen: 'A selected project needs vertical task groups, dependencies, risk states, sequence, or appetite-based cuts.', produces: 'A project-wide task-group plan with one active group selected separately.', gate: 'A person approves the plan and selects the active group.' },
  'kickoff-doc': { stage: 'Handoff', tone: 'reflection', useWhen: 'Builders need a durable orientation reference after accepted artifacts converge.', produces: 'A builder-facing map of accepted product territory.', gate: 'The kickoff document does not replace build scope or sequence.' },
  'feed-planning-context': { stage: 'Handoff', tone: 'verification', useWhen: 'An implementation agent needs only the authoritative subset for one active task group or slice.', produces: 'A compact context packet with an execution contract and verification target.', gate: 'Working alternatives and candidate evidence stay out of build scope.' },
  'breadboard-reflection': { stage: 'After build', tone: 'reflection', useWhen: 'Implementation exists and may differ from accepted intent.', produces: 'Separate intent and reality records, drift evidence, design smells, and correction options.', gate: 'A person decides whether to fix code, revise the plan, cut, split, or stop.' },
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

const simpleStages = {
  '00-source-notes.md': { label: 'Source notes', description: 'The messy starting point in the user’s words.', tone: 'evidence', prompt: 'Capture [your raw feature notes] without resolving contradictions or promoting solution ideas into accepted requirements.' },
  '01-frame.md': { label: 'Frame', description: 'Clarify the problem, outcome, and boundary.', tone: 'evidence', prompt: 'Use the framing-doc skill on [your source notes]. Create a concise frame, preserve source evidence, and stop for acceptance of the problem boundary.' },
  '02-shaping.md': { label: 'Shaping', description: 'Accept requirements and Appetite, compare fit, then record the human selection.', tone: 'planning', prompt: 'Use the shaping skill on [your accepted frame]. Separate requirements from mechanisms, make Appetite and the cut line explicit, compare viable shapes, and stop for human selection.' },
  '03-breadboard.md': { label: 'Breadboard', description: 'Map accepted selected-design behavior and candidate slices.', tone: 'verification', prompt: 'Use the breadboarding skill in selected-design mode on [your accepted shaping artifact]. Cite the selected shape, accepted requirements, Appetite, and cut line; map behavior before proposing slices.' },
  '04-kickoff.md': { label: 'Kickoff', description: 'Optional builder-facing orientation after a slice is selected.', tone: 'implementation', optional: true, prompt: 'Use the kickoff-doc skill on [your accepted frame, selected shape, accepted breadboard, and selected slice]. Create an orientation reference without redefining scope or sequence.' },
  '05-breadboard-reflection.md': { label: 'Reflection', description: 'Compare accepted intent with implementation reality.', tone: 'reflection', prompt: 'Use the breadboard-reflection skill on [your accepted breadboard and current implementation evidence]. Record reality separately, identify drift, and stop for the correction decision.' },
};

const simpleGroceryNotes = {
  '00-source-notes.md': ['Raw evidence stays distinct from interpretation', 'Early mechanisms remain unselected ideas', 'Contradictions are preserved for framing'],
  '01-frame.md': ['The problem and outcome are stated without choosing a mechanism', 'The boundary is explicit', 'Acceptance belongs to a person'],
  '02-shaping.md': ['Requirements describe needs, not implementation choices', 'Requirements, Appetite, and the cut line are accepted before selection', 'Fit evidence supports an explicit human choice'],
  '03-breadboard.md': ['The mode is selected-design', 'Accepted sources and the selected shape are cited', 'Slices follow the behavior map and remain candidate boundaries until selected'],
  '04-kickoff.md': ['The accepted breadboard and selected slice already exist', 'The document orients builders without redefining scope', 'Build sequence stays in the selected plan or slice'],
  '05-breadboard-reflection.md': ['Implementation reality is recorded separately', 'Drift is compared against accepted intent', 'A person chooses whether code, plan, or scope changes'],
};

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
    ['Overview', '/', 'overview'], ['Skills', '/skills', 'skills'],
    ['Guides', '/guides/start-here', 'guides'], ['Examples', '/examples', 'examples'],
  ];
  return `
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <a class="site-brand" href="#/">Planning Skills</a>
      <nav id="primary-navigation" class="primary-nav ${state.mobileMenuOpen ? 'is-open' : ''}" aria-label="Primary navigation">
        ${items.map(([label, route, id]) => `<a class="nav-link ${active === id ? 'is-active' : ''}" href="#${route}" ${active === id ? 'aria-current="page"' : ''}>${label}</a>`).join('')}
      </nav>
      <div class="header-actions">
        <button id="search-trigger" class="search-trigger" type="button" data-action="open-search">
          ${icon('search', 18)}<span>Search docs</span><kbd>⌘ K</kbd>
        </button>
        <a class="icon-button desktop-github" href="${REPOSITORY_URL}" target="_blank" rel="noreferrer" aria-label="Open repository on GitHub">${icon('github', 24)}</a>
        <button id="mobile-search-trigger" class="icon-button mobile-search" type="button" data-action="open-search" aria-label="Search docs">${icon('search', 24)}</button>
        <button class="icon-button menu-button" type="button" data-action="toggle-menu" aria-controls="primary-navigation" aria-expanded="${state.mobileMenuOpen}" aria-label="${state.mobileMenuOpen ? 'Close' : 'Open'} navigation menu">${icon(state.mobileMenuOpen ? 'close' : 'menu', 26)}</button>
      </div>
    </header>`;
}

function homePage() {
  const selected = entryPoints.find((item) => item.id === state.selectedEntry) || entryPoints[1];
  return `
    <main id="main-content" class="home-page">
      <section class="home-hero">
        <div class="hero-copy">
          <h1>Turn fuzzy work into a buildable plan.</h1>
          <p>Preserve intent from raw evidence through a selected, testable implementation slice.</p>
          <div class="hero-actions">
            <button class="button button-primary" type="button" data-action="focus-navigator">Find your next move ${icon('arrow')}</button>
            <a class="text-link" href="#/guides/start-here">Read the 10-minute guide ${icon('arrow', 18)}</a>
          </div>
        </div>
        <div class="entry-navigator" id="entry-navigator">
          <div class="entry-options" role="radiogroup" aria-label="What are you starting with?">
            <h2>What are you starting with?</h2>
            ${entryPoints.map((item, index) => {
              const selectedItem = item.id === selected.id;
              return `<button class="entry-option tone-${item.id} ${selectedItem ? 'is-selected' : ''}" type="button" role="radio" aria-checked="${selectedItem}" tabindex="${selectedItem ? '0' : '-1'}" data-action="select-entry" data-entry="${item.id}" data-index="${index}">
                <span class="radio-mark" aria-hidden="true"></span>${icon(item.icon, 21)}<span>${escapeHtml(item.label)}</span>
              </button>`;
            }).join('')}
          </div>
          <div class="recommendation" aria-live="polite">
            <span>Recommended next move:</span>
            <h2>${escapeHtml(selected.recommendation)}</h2>
            <p>${escapeHtml(selected.description)}</p>
            <a class="button button-outline planning-button" href="#/skills/${selected.slug}/guide">Open ${escapeHtml(selected.recommendation.toLowerCase())} guide ${icon('arrow', 18)}</a>
          </div>
        </div>
      </section>
      <section class="workflow-band" aria-labelledby="workflow-title">
        <h2 id="workflow-title" class="sr-only">How planning works</h2>
        <ol class="workflow-rail" aria-label="Planning workflow">
          ${workflowSteps.map((step, index) => `<li class="workflow-step tone-${step.tone} ${step.gate ? 'is-gate' : ''}"><span class="step-marker">${index + 1}</span><strong>${step.title}</strong><small>${step.description}</small></li>`).join('')}
        </ol>
      </section>
      <section class="principle-section">
        <div class="principle-copy">
          <h2>Exploration is fluid.<br>Commitment is gated.</h2>
          <p>Move among requirements, shapes, fit checks, focused spikes, and candidate evidence while they remain working material. A person decides what becomes accepted intent.</p>
          <a class="text-link" href="#/guides/human-decision-gates">Understand the human gates ${icon('arrow', 18)}</a>
        </div>
        <div class="planning-loop" aria-label="Collaborative shaping loop">
          <div class="loop-node tone-evidence"><strong>Requirements</strong><span>Needs and constraints</span></div><span aria-hidden="true">↔</span>
          <div class="loop-node tone-planning"><strong>Shapes</strong><span>Mechanisms and trade-offs</span></div><span aria-hidden="true">↔</span>
          <div class="loop-node tone-verification"><strong>Fit checks</strong><span>Criteria and appetite</span></div><span aria-hidden="true">↔</span>
          <div class="loop-node tone-evidence is-dashed"><strong>Candidate evidence</strong><span>Spikes and breadboards</span></div>
        </div>
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
      const queryMatches = !query || `${skill.title} ${skill.description}`.toLowerCase().includes(query);
      return categoryMatches && queryMatches;
    }),
  })).filter((group) => group.items.length > 0);
  const visibleSlugs = new Set(visibleGroups.flatMap((group) => group.items.map((item) => item.slug)));
  const active = skillsBySlug.get(visibleSlugs.has(state.selectedSkill) ? state.selectedSkill : visibleGroups[0]?.items[0]?.slug) || skillsBySlug.get('shaping');
  const detail = skillPresentation[active.slug];
  state.selectedSkill = active.slug;

  return `
    <main id="main-content" class="skills-layout">
      <section id="skill-list" class="skills-main">
        <div class="page-heading"><h1>Skills</h1><p>Use the smallest planning move that prevents an important misunderstanding.</p></div>
        <div class="skill-controls">
          <label class="field-with-icon">${icon('search', 18)}<span class="sr-only">Search skills</span><input id="skill-search" value="${escapeHtml(state.skillQuery)}" placeholder="Search skills"><kbd>/</kbd></label>
          <div class="filter-tabs" aria-label="Filter by category">
            ${['all', 'core', 'conditional', 'handoff'].map((category) => `<button type="button" class="${state.skillCategory === category ? 'is-selected' : ''}" aria-pressed="${state.skillCategory === category}" data-action="filter-skills" data-category="${category}">${category === 'all' ? 'All' : category[0].toUpperCase() + category.slice(1)}</button>`).join('')}
          </div>
        </div>
        <div class="skill-groups" aria-live="polite">
          ${visibleGroups.length ? visibleGroups.map((group) => `<section class="skill-group"><h2>${group.label}</h2><div class="skill-rows">
            ${group.items.map((skill) => {
              const presentation = skillPresentation[skill.slug];
              return `<button type="button" class="skill-row tone-${presentation.tone} ${skill.slug === active.slug ? 'is-selected' : ''}" aria-pressed="${skill.slug === active.slug}" data-action="select-skill" data-skill="${skill.slug}"><strong>${escapeHtml(skill.title)}</strong><span>${escapeHtml(skill.description)}</span><small>${presentation.stage}</small></button>`;
            }).join('')}
          </div></section>`).join('') : '<div class="empty-state"><strong>No skill matches that search.</strong><span>Try “state”, “context”, or “drift”.</span></div>'}
        </div>
      </section>
      <aside class="skill-detail tone-${detail.tone}" aria-labelledby="skill-detail-title" aria-live="polite">
        <div class="skill-detail-heading"><h2 id="skill-detail-title" tabindex="-1">${escapeHtml(active.title)}</h2><p>${escapeHtml(active.description)}</p></div>
        <dl>
          <div><dt>${icon('target')} Use when</dt><dd>${escapeHtml(detail.useWhen)}</dd></div>
          <div><dt>${icon('file')} Produces</dt><dd>${escapeHtml(detail.produces)}</dd></div>
          <div><dt>${icon('user')} Decision / guardrail</dt><dd>${escapeHtml(detail.gate)}</dd></div>
        </dl>
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
  const defaultName = slug === 'simple-grocery-list' ? '02-shaping.md' : artifactFiles[0]?.name || example.files[0]?.name;
  const selected = example.files.find((file) => file.name === requestedFile) || example.files.find((file) => file.name === defaultName) || example.files[0];
  const selectedIndex = artifactFiles.findIndex((file) => file.name === selected.name);
  const previous = selectedIndex > 0 ? artifactFiles[selectedIndex - 1] : null;
  const next = selectedIndex >= 0 && selectedIndex < artifactFiles.length - 1 ? artifactFiles[selectedIndex + 1] : null;
  const isSimple = slug === 'simple-grocery-list';
  const selectedStage = isSimple ? simpleStages[selected.name] : null;
  const prompt = examplePrompt(example, selected, selectedStage);
  const route = `/examples/${slug}?file=${encodeURIComponent(selected.name)}`;
  const rendered = renderMarkdown(selected.raw, selected.sourcePath, route, { headingOffset: 1 });
  const notes = isSimple ? (simpleGroceryNotes[selected.name] || []) : ['Each artifact has one clear job', 'Accepted intent stays separate from exploratory evidence', 'The sequence follows the complexity actually present'];
  queuePostRender(section);
  return `<main id="main-content" class="example-page">
    <div class="example-heading"><h1>${escapeHtml(example.title.replace(/\s+—\s+Step-by-Step Example$/, ''))}</h1><p>${isSimple ? 'See the foundational workflow on a tiny feature without getting lost in implementation detail.' : escapeHtml(example.description)}</p><a class="back-link" href="#/examples">${icon('back', 17)} All examples</a></div>
    <div class="example-workspace">
      <nav class="artifact-trail" aria-label="Example artifacts">
        ${artifactFiles.map((file, index) => {
          const stage = isSimple ? simpleStages[file.name] : null;
          const selectedStage = file.name === selected.name;
          return `<a class="artifact-stage tone-${stage?.tone || 'evidence'} ${stage?.optional ? 'is-optional' : ''} ${selectedStage ? 'is-selected' : ''}" href="#/examples/${slug}?file=${encodeURIComponent(file.name)}" ${selectedStage ? 'aria-current="step"' : ''}><span class="artifact-marker">${index + 1}</span><span><strong>${escapeHtml(stage?.label || fileLabel(file))}</strong>${stage?.optional ? '<em>Optional</em>' : ''}<small>${escapeHtml(stage?.description || file.description)}</small></span></a>`;
        }).join('')}
      </nav>
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
    <div class="dialog-search-row">${icon('search', 21)}<input id="global-search" value="${escapeHtml(state.searchQuery)}" placeholder="Search guides, skills, and examples" aria-label="Search guides, skills, and examples"><button class="icon-button compact" type="button" data-action="close-search" aria-label="Close search">${icon('close', 20)}</button></div>
    <div class="search-results" aria-live="polite" data-result-total="${rankedResults.length}"><p class="system-label">${query ? resultLabel : 'Suggested paths'}</p>
      ${results.length ? results.map((item) => `<a class="search-result" href="#${item.route}"><span class="result-icon">${icon(item.type === 'Skill' ? 'target' : 'file', 18)}</span><span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.description)}</small></span><span class="result-type">${item.type}</span>${icon('arrow', 18)}</a>`).join('') : '<div class="empty-search"><strong>No matching path found.</strong><span>Try a skill name, artifact, or workflow question.</span></div>'}
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
  let active = 'overview';
  let page = homePage();
  const parts = path.split('/').filter(Boolean);
  if (parts[0] === 'skills') {
    active = 'skills';
    page = parts[2] === 'guide' ? guidePage('skill', parts[1], query.get('section')) : skillsPage(parts[1]);
  } else if (parts[0] === 'guides') {
    active = 'guides';
    page = guidePage('guide', parts[1] || 'start-here', query.get('section'));
  } else if (parts[0] === 'resources') {
    active = 'guides';
    page = guidePage('resource', parts[1], query.get('section'));
  } else if (parts[0] === 'examples') {
    active = 'examples';
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
  if (action === 'focus-navigator') {
    document.getElementById('entry-navigator')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    window.setTimeout(() => document.querySelector('.entry-option[aria-checked="true"]')?.focus(), 350);
  }
  if (action === 'select-entry') {
    state.selectedEntry = actionTarget.dataset.entry;
    render({ preserveScroll: true });
    requestAnimationFrame(() => document.querySelector(`[data-entry="${state.selectedEntry}"]`)?.focus());
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
    if (event.key === 'ArrowDown' || event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % entryPoints.length;
    if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + entryPoints.length) % entryPoints.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = entryPoints.length - 1;
    state.selectedEntry = entryPoints[nextIndex].id;
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
