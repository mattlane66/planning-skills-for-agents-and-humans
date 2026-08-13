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
  [html.includes('Watch a plan take shape.'), 'contains the primary collaboration walkthrough'],
  [html.includes('Human + agent'), 'shows the human and agent exchange'],
  [html.includes('Plan so far'), 'contains the accumulating planning result'],
  [html.includes('A complete handoff has two sources.'), 'shows how planning and repository context form the build packet'],
  [html.includes('What planning contributes'), 'contains the compact planning subset'],
  [html.includes('What the complete packet must contain'), 'contains the inspectable complete handoff fields'],
  [html.includes('Compare the plan with reality.'), 'contains the post-build reality check'],
  [html.includes('Accepted requirements matrix'), 'contains the requirements matrix'],
  [html.includes('Two viable paths through the same matrix'), 'contains both shaped paths'],
  [html.includes('Fit is a gate, not a score.'), 'explains why both shapes can fit before a human selection'],
  [html.includes('P1 Grocery list page'), 'contains the selected-design breadboard diagram'],
  [html.includes('Tasks become vertical, judgeable groups'), 'contains the task-group sequence'],
  [!html.includes('data-action="select-lab-answer"'), 'does not contain the retired planning quiz'],
  [html.includes('Selected-design breadboard'), 'contains the selected-design promotion stage'],
  [html.includes('Kickoff is optional orientation. It does not define scope or sequence.'), 'places kickoff outside the required sequence'],
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
