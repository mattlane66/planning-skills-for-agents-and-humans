import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import { createServer } from 'node:http';
import { dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { collectPlanningDiagrams } from './markdown.mjs';
import { viewerHtml } from './page.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const defaultVendorRoot = resolve(here, '..', 'node_modules', 'mermaid', 'dist');

function sendJson(response, statusCode, value) {
  response.writeHead(statusCode, {
    'cache-control': 'no-store',
    'content-type': 'application/json; charset=utf-8',
  });
  response.end(JSON.stringify(value));
}

function contentType(path) {
  return {
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.mjs': 'text/javascript; charset=utf-8',
    '.map': 'application/json; charset=utf-8',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
  }[extname(path)] || 'application/octet-stream';
}

async function fileStamp(path) {
  try {
    const details = await stat(path);
    return `${details.mtimeMs}:${details.size}`;
  } catch (error) {
    return `missing:${error.code || 'error'}`;
  }
}

export function watchPlanningFiles(filePaths, onChange, intervalMs = 400) {
  const stamps = new Map();
  let checking = false;

  const check = async () => {
    if (checking) return;
    checking = true;
    try {
      for (const path of filePaths) {
        const next = await fileStamp(path);
        const previous = stamps.get(path);
        stamps.set(path, next);
        if (previous !== undefined && previous !== next) onChange(path);
      }
    } finally {
      checking = false;
    }
  };

  void check();
  const timer = setInterval(check, intervalMs);
  timer.unref?.();
  return () => clearInterval(timer);
}

export async function startViewer({
  filePaths,
  cwd = process.cwd(),
  host = '127.0.0.1',
  port = 3456,
  vendorRoot = defaultVendorRoot,
  watchIntervalMs = 400,
} = {}) {
  if (!Array.isArray(filePaths) || filePaths.length === 0) {
    throw new Error('Provide at least one Markdown file to watch.');
  }

  const absolutePaths = filePaths.map((path) => resolve(cwd, path));
  await collectPlanningDiagrams(filePaths, cwd);
  await stat(resolve(vendorRoot, 'mermaid.esm.min.mjs'));

  let revision = 1;
  const eventClients = new Set();

  const broadcast = () => {
    revision += 1;
    for (const response of eventClients) {
      response.write(`event: reload\ndata: ${revision}\n\n`);
    }
  };

  const server = createServer(async (request, response) => {
    let requestUrl;
    try {
      requestUrl = new URL(request.url || '/', `http://${request.headers.host || host}`);
    } catch {
      response.writeHead(400).end('Bad request');
      return;
    }

    if (requestUrl.pathname === '/') {
      response.writeHead(200, { 'cache-control': 'no-store', 'content-type': 'text/html; charset=utf-8' });
      response.end(viewerHtml);
      return;
    }

    if (requestUrl.pathname === '/health') {
      sendJson(response, 200, { ok: true, revision, files: filePaths });
      return;
    }

    if (requestUrl.pathname === '/api/diagrams') {
      try {
        const files = await collectPlanningDiagrams(filePaths, cwd);
        sendJson(response, 200, {
          revision,
          files: files.map(({ path, diagrams }) => ({ path, diagrams })),
        });
      } catch (error) {
        sendJson(response, 500, { error: error instanceof Error ? error.message : String(error) });
      }
      return;
    }

    if (requestUrl.pathname === '/events') {
      response.writeHead(200, {
        'cache-control': 'no-cache',
        connection: 'keep-alive',
        'content-type': 'text/event-stream',
      });
      response.write(`event: ready\ndata: ${revision}\n\n`);
      eventClients.add(response);
      request.on('close', () => eventClients.delete(response));
      return;
    }

    if (requestUrl.pathname.startsWith('/vendor/')) {
      let relativePath;
      try {
        relativePath = decodeURIComponent(requestUrl.pathname.slice('/vendor/'.length));
      } catch {
        response.writeHead(400).end('Bad request');
        return;
      }
      const requestedPath = resolve(vendorRoot, relativePath);
      const allowedPrefix = `${resolve(vendorRoot)}${sep}`;
      if (!requestedPath.startsWith(allowedPrefix)) {
        response.writeHead(403).end('Forbidden');
        return;
      }
      try {
        const details = await stat(requestedPath);
        if (!details.isFile()) throw new Error('Not a file');
        response.writeHead(200, {
          'cache-control': 'public, max-age=31536000, immutable',
          'content-type': contentType(requestedPath),
        });
        createReadStream(requestedPath).pipe(response);
      } catch {
        response.writeHead(404).end('Not found');
      }
      return;
    }

    response.writeHead(404).end('Not found');
  });

  const stopWatching = watchPlanningFiles(absolutePaths, broadcast, watchIntervalMs);
  const keepAlive = setInterval(() => {
    for (const response of eventClients) response.write(': keep-alive\n\n');
  }, 15000);
  keepAlive.unref?.();

  await new Promise((resolveListening, reject) => {
    server.once('error', reject);
    server.listen(port, host, resolveListening);
  });

  const address = server.address();
  const actualPort = typeof address === 'object' && address ? address.port : port;
  const url = `http://${host}:${actualPort}`;

  return {
    url,
    close: async () => {
      stopWatching();
      clearInterval(keepAlive);
      for (const response of eventClients) response.end();
      await new Promise((resolveClose, reject) => server.close((error) => (error ? reject(error) : resolveClose())));
    },
  };
}
