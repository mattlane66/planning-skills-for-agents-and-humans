import { build } from 'esbuild';
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, '..');
const buildRoot = resolve(siteRoot, '.build');
const bundlePath = resolve(buildRoot, 'portal.js');

await mkdir(buildRoot, { recursive: true });
await build({
  entryPoints: [resolve(siteRoot, 'src', 'app.js')],
  outfile: bundlePath,
  bundle: true,
  minify: true,
  format: 'iife',
  platform: 'browser',
  target: ['safari15.4'],
  legalComments: 'none',
  logLevel: 'info',
});

const [css, bundledJavaScript] = await Promise.all([
  readFile(resolve(siteRoot, 'src', 'styles.css'), 'utf8'),
  readFile(bundlePath, 'utf8'),
]);
const safeJavaScript = bundledJavaScript.replace(/<\/script/gi, '<\\/script');
const html = `<!doctype html>
<html lang="en" data-portal-build="standalone">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="description" content="A click-through human and agent collaboration walkthrough from messy evidence to a build-ready slice.">
    <meta name="color-scheme" content="light">
    <title>Planning Skills Lab — Watch a plan take shape</title>
    <style>${css}</style>
  </head>
  <body>
    <div id="root">
      <main class="boot-shell">
        <h1>Planning Skills Lab</h1>
        <p>Loading the collaboration walkthrough…</p>
        <noscript>This interactive file needs JavaScript enabled. No network connection is required.</noscript>
      </main>
    </div>
    <script>${safeJavaScript}</script>
  </body>
</html>
`.replace(/[ \t]+$/gm, '');

await writeFile(resolve(siteRoot, 'index.html'), html);
await rm(buildRoot, { recursive: true, force: true });
console.log(`Built site/index.html (${(Buffer.byteLength(html) / 1024 / 1024).toFixed(2)} MiB, self-contained).`);
