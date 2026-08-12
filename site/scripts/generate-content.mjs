import { mkdir, readdir, readFile, stat, writeFile } from 'node:fs/promises';
import { basename, dirname, extname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, '..');
const repoRoot = resolve(siteRoot, '..');
const outputPath = resolve(siteRoot, 'src', 'generated', 'content.json');

function normalizePath(value) {
  return value.split('\\').join('/');
}

function stripFrontmatter(markdown) {
  return markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
}

function cleanInline(value) {
  return value
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/[`*_~]/g, '')
    .replace(/<[^>]+>/g, '')
    .trim();
}

function plainText(markdown) {
  return stripFrontmatter(markdown)
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/~~~[\s\S]*?~~~/g, ' ')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^[-*>|]\s*/gm, '')
    .replace(/!?\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/[`*_~]/g, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function titleFrom(markdown, fallback) {
  const match = stripFrontmatter(markdown).match(/^#\s+(.+?)\s*$/m);
  return match ? cleanInline(match[1]) : fallback;
}

function descriptionFrom(markdown) {
  const body = stripFrontmatter(markdown).replace(/^#\s+.+?\r?\n/, '');
  const paragraphs = body.split(/\r?\n\s*\r?\n/).map(plainText).filter(Boolean);
  for (let index = 0; index < paragraphs.length; index += 1) {
    let cleaned = paragraphs[index];
    if (cleaned.length <= 24) continue;
    if (/[:—–]\s*$/.test(cleaned) && paragraphs[index + 1]) cleaned = `${cleaned} ${paragraphs[index + 1]}`;
    if (cleaned.length <= 240) return cleaned;
    const candidate = cleaned.slice(0, 241);
    const sentenceEnd = Math.max(candidate.lastIndexOf('. '), candidate.lastIndexOf('? '), candidate.lastIndexOf('! '));
    const boundary = sentenceEnd >= 120 ? sentenceEnd + 1 : candidate.lastIndexOf(' ');
    return `${candidate.slice(0, boundary > 0 ? boundary : 240).trimEnd()}…`;
  }
  return '';
}

function headingId(value, seen) {
  const base = cleanInline(value).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'section';
  const count = seen.get(base) || 0;
  seen.set(base, count + 1);
  return count === 0 ? base : `${base}-${count + 1}`;
}

function headingsFrom(markdown) {
  const seen = new Map();
  let fence = null;
  let foundDocumentTitle = false;
  return stripFrontmatter(markdown).split(/\r?\n/).flatMap((line) => {
    const fenceMatch = line.match(/^\s*(`{3,}|~{3,})/);
    if (fenceMatch) {
      const marker = fenceMatch[1][0];
      if (!fence) fence = marker;
      else if (fence === marker) fence = null;
      return [];
    }
    if (fence) return [];
    const match = line.match(/^(#{1,3})\s+(.+?)\s*$/);
    if (!match) return [];
    const title = cleanInline(match[2]);
    let depth = match[1].length;
    if (depth === 1) {
      if (foundDocumentTitle) depth = 2;
      foundDocumentTitle = true;
    }
    return [{ depth, title, id: headingId(title, seen) }];
  });
}

function fallbackTitle(path) {
  return basename(path, extname(path))
    .replace(/^\d+-/, '')
    .split('-')
    .filter(Boolean)
    .map((part) => part[0].toUpperCase() + part.slice(1))
    .join(' ');
}

async function markdownRecord(absolutePath, extra = {}) {
  const raw = await readFile(absolutePath, 'utf8');
  const sourcePath = normalizePath(relative(repoRoot, absolutePath));
  return {
    sourcePath,
    title: titleFrom(raw, fallbackTitle(absolutePath)),
    description: descriptionFrom(raw),
    headings: headingsFrom(raw),
    raw: stripFrontmatter(raw),
    searchText: plainText(raw).slice(0, 12000),
    ...extra,
  };
}

async function loadDocs() {
  const rootDocs = [
    ['repository-overview', 'README.md'],
    ['manifesto', 'MANIFESTO.md'],
    ['contributing', 'CONTRIBUTING.md'],
  ];
  const roots = await Promise.all(rootDocs.map(([slug, path]) => (
    markdownRecord(resolve(repoRoot, path), { slug, kind: 'guide' })
  )));
  const names = (await readdir(resolve(repoRoot, 'docs'))).filter((name) => name.endsWith('.md')).sort();
  const nested = await Promise.all(names.map((name) => markdownRecord(resolve(repoRoot, 'docs', name), {
    slug: basename(name, '.md'),
    kind: 'guide',
  })));
  return [...roots, ...nested];
}

async function loadSkills() {
  const metadata = JSON.parse(await readFile(resolve(repoRoot, 'skill-metadata.json'), 'utf8'));
  return Promise.all(Object.entries(metadata).map(async ([slug, item]) => {
    const record = await markdownRecord(resolve(repoRoot, slug, 'SKILL.md'), { slug, kind: 'skill' });
    return { ...record, title: item.title, description: item.description };
  }));
}

async function loadExamples() {
  const examplesRoot = resolve(repoRoot, 'examples');
  const entries = await readdir(examplesRoot, { withFileTypes: true });
  const directories = entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
  return Promise.all(directories.map(async (slug) => {
    const folder = resolve(examplesRoot, slug);
    const files = (await readdir(folder)).filter((name) => name.endsWith('.md')).sort((a, b) => {
      if (a === 'README.md') return -1;
      if (b === 'README.md') return 1;
      return a.localeCompare(b);
    });
    const records = await Promise.all(files.map((name) => markdownRecord(resolve(folder, name), {
      name,
      kind: 'example-file',
    })));
    const overview = records.find((record) => record.name === 'README.md') || records[0];
    return {
      slug,
      title: overview?.title || fallbackTitle(slug),
      description: overview?.description || '',
      sourcePath: normalizePath(relative(repoRoot, folder)),
      files: records,
    };
  }));
}

function markdownTargets(record) {
  const targets = [];
  for (const match of record.raw.matchAll(/(?<!!)\[[^\]]+\]\(([^)]+)\)/g)) {
    const href = match[1].trim().replace(/^<|>$/g, '');
    if (!href || /^(?:[a-z][a-z0-9+.-]*:|#)/i.test(href)) continue;
    const target = href.split(/[?#]/, 1)[0];
    if (!/\.md$/i.test(target)) continue;
    targets.push(resolveRepoPath(record.sourcePath, decodeURIComponent(target)));
  }
  return targets;
}

function resourceCategory(sourcePath) {
  if (sourcePath.startsWith('templates/')) return 'Templates';
  if (sourcePath.includes('/references/')) return 'Skill references';
  return 'Repository reference';
}

async function loadLinkedResources(initialRecords) {
  const known = new Set(initialRecords.map((record) => record.sourcePath));
  const supportPaths = [];
  try {
    const templateNames = await readdir(resolve(repoRoot, 'templates'));
    supportPaths.push(...templateNames.filter((name) => name.endsWith('.md')).map((name) => `templates/${name}`));
  } catch {
    // A missing templates directory is reported by the repository health check.
  }
  for (const skill of initialRecords.filter((record) => record.kind === 'skill')) {
    const referenceRoot = resolve(repoRoot, dirname(skill.sourcePath), 'references');
    try {
      const names = await readdir(referenceRoot);
      supportPaths.push(...names.filter((name) => name.endsWith('.md')).map((name) => normalizePath(relative(repoRoot, resolve(referenceRoot, name)))));
    } catch {
      // Most skills intentionally do not have a references directory.
    }
  }
  const queued = [...new Set([...supportPaths, ...initialRecords.flatMap(markdownTargets)])];
  const resources = [];

  while (queued.length > 0) {
    const sourcePath = queued.shift();
    if (known.has(sourcePath)) continue;
    const absolute = resolve(repoRoot, sourcePath);
    if (!absolute.startsWith(`${repoRoot}/`)) continue;
    try {
      const details = await stat(absolute);
      if (!details.isFile()) continue;
      const record = await markdownRecord(absolute, {
        slug: encodeURIComponent(sourcePath),
        kind: 'resource',
        category: resourceCategory(sourcePath),
      });
      known.add(sourcePath);
      resources.push(record);
      for (const target of markdownTargets(record)) {
        if (!known.has(target)) queued.push(target);
      }
    } catch {
      // The repository link checker reports missing source targets separately.
    }
  }

  return resources.sort((left, right) => (
    left.category.localeCompare(right.category) || left.title.localeCompare(right.title)
  ));
}

function resolveRepoPath(basePath, target) {
  const base = target.startsWith('/') ? [] : basePath.split('/').slice(0, -1);
  for (const part of target.replace(/^\//, '').split('/')) {
    if (!part || part === '.') continue;
    if (part === '..') base.pop();
    else base.push(part);
  }
  return base.join('/');
}

function mimeType(path) {
  const extension = extname(path).toLowerCase();
  return ({
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
  })[extension];
}

async function loadAssets(records) {
  const assets = {};
  for (const record of records) {
    for (const match of record.raw.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)) {
      const target = match[1].trim().replace(/^<|>$/g, '').split(/[?#]/, 1)[0];
      if (!target || /^(?:[a-z][a-z0-9+.-]*:|#)/i.test(target)) continue;
      const sourcePath = resolveRepoPath(record.sourcePath, decodeURIComponent(target));
      const mime = mimeType(sourcePath);
      if (!mime || assets[sourcePath]) continue;
      const absolute = resolve(repoRoot, sourcePath);
      try {
        const details = await stat(absolute);
        if (!details.isFile()) continue;
        const data = await readFile(absolute);
        assets[sourcePath] = `data:${mime};base64,${data.toString('base64')}`;
      } catch {
        // Broken source links remain visible as source links during rendering.
      }
    }
  }
  return assets;
}

const [docs, skills, examples] = await Promise.all([loadDocs(), loadSkills(), loadExamples()]);
const primaryRecords = [...docs, ...skills, ...examples.flatMap((example) => example.files)];
const resources = await loadLinkedResources(primaryRecords);
const records = [...primaryRecords, ...resources];
const assets = await loadAssets(records);
const content = { docs, skills, examples, resources, assets };

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(content)}\n`);
console.log(`Generated ${normalizePath(relative(repoRoot, outputPath))}: ${docs.length} guides, ${skills.length} skills, ${examples.length} examples, ${resources.length} linked references, ${Object.keys(assets).length} embedded images.`);
