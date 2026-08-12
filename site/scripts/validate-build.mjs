import { readFile, stat } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, '..');
const output = resolve(siteRoot, 'index.html');
const [html, details] = await Promise.all([readFile(output, 'utf8'), stat(output)]);

const checks = [
  [html.startsWith('<!doctype html>'), 'has an HTML doctype'],
  [html.includes('data-portal-build="standalone"'), 'is marked as a standalone build'],
  [html.includes('Turn fuzzy work into a buildable plan.'), 'contains the primary portal content'],
  [html.includes('Simple Grocery List'), 'contains example content'],
  [html.includes('Planning Router'), 'contains the skill catalog'],
  [html.includes('templates/shaping.md'), 'contains canonical templates'],
  [html.includes('shaping/references/fit-checks.md'), 'contains canonical skill references'],
  [html.includes('viewport-fit=cover'), 'includes iPhone safe-area viewport support'],
  [!/<script[^>]+src=/i.test(html), 'has no external script dependency'],
  [!/<link[^>]+rel=["']stylesheet/i.test(html), 'has no external stylesheet dependency'],
  [details.size > 500_000, 'contains the bundled application and documentation corpus'],
];

const failures = checks.filter(([passed]) => !passed).map(([, label]) => label);
if (failures.length > 0) {
  console.error(`Standalone validation failed: ${failures.join(', ')}`);
  process.exit(1);
}

console.log(`Standalone validation passed (${checks.length} checks, ${(details.size / 1024 / 1024).toFixed(2)} MiB).`);
