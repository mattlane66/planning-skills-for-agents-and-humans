import { createServer } from 'node:http';
import { randomBytes, timingSafeEqual } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const ASSETS = {
  '/': { file: '../public/index.html', type: 'text/html; charset=utf-8' },
  '/app.js': { file: '../public/app.js', type: 'text/javascript; charset=utf-8' },
  '/style.css': { file: '../public/style.css', type: 'text/css; charset=utf-8' },
};
const MAX_BODY = 7_000_000;
const MAX_IMAGE = 5_000_000;
const MAX_WAIT_MS = 30_000;
const FRESH_MS = 5_000;

function json(res, status, value) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
  res.end(JSON.stringify(value));
}
function errorMessage(error) { return error instanceof Error ? error.message : String(error); }
async function readJSON(req) {
  let length = 0;
  const chunks = [];
  for await (const chunk of req) {
    length += chunk.length;
    if (length > MAX_BODY) throw new Error('Request exceeds the frame size limit');
    chunks.push(chunk);
  }
  const data = Buffer.concat(chunks).toString('utf8');
  return data ? JSON.parse(data) : {};
}
function checkedFrame(body) {
  if (!body || body.mime !== 'image/jpeg' || typeof body.data !== 'string' || !/^[A-Za-z0-9+/]+={0,2}$/.test(body.data)) {
    throw new Error('Only base64-encoded JPEG frames are accepted');
  }
  const bytes = Buffer.from(body.data, 'base64');
  if (!bytes.length || bytes.length > MAX_IMAGE || bytes[0] !== 0xff || bytes[1] !== 0xd8 || bytes[bytes.length - 2] !== 0xff || bytes[bytes.length - 1] !== 0xd9) {
    throw new Error('Invalid or oversized JPEG frame');
  }
  return {
    mime: 'image/jpeg', data: body.data, receivedAt: new Date().toISOString(),
    source: String(body.source || 'unknown').slice(0, 60),
    focus: body.focus && typeof body.focus === 'object' ? {
      x: Number(body.focus.x), y: Number(body.focus.y),
      width: Number(body.focus.width), height: Number(body.focus.height),
    } : null,
    videoTime: Number.isFinite(body.videoTime) ? body.videoTime : null,
    changed: body.changed === true,
  };
}

export async function createLookServer({ port = 0, host = '127.0.0.1' } = {}) {
  // Deliberately never bind to an externally reachable interface.
  if (host !== '127.0.0.1') throw new Error('Look only binds to 127.0.0.1');
  const token = randomBytes(24).toString('base64url');
  const state = {
    previewAt: 0, source: null, pending: new Map(), latest: null,
    stopped: false, requestCounter: 0,
  };
  let address;
  function authenticate(req, url) {
    const submitted = req.headers['x-look-token'] || (url.pathname === '/' ? url.searchParams.get('token') : null);
    if (typeof submitted !== 'string') return false;
    const received = Buffer.from(submitted);
    const expected = Buffer.from(token);
    return received.length === expected.length && timingSafeEqual(received, expected);
  }
  function status() {
    return {
      connected: !!(state.source && Date.now() - state.previewAt < FRESH_MS && !state.stopped),
      source: state.source, hasFrame: !!state.latest, stopped: state.stopped,
      pending: state.pending.size,
    };
  }
  function resolvePending(id, result) {
    const task = state.pending.get(id);
    if (!task) return false;
    state.pending.delete(id);
    clearTimeout(task.timer);
    task.resolve(result);
    return true;
  }
  function rejectPending(reason) {
    for (const [id, task] of state.pending) {
      state.pending.delete(id);
      clearTimeout(task.timer);
      task.reject(new Error(reason));
    }
  }
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url || '/', 'http://127.0.0.1');
      if (req.headers.host !== `127.0.0.1:${address?.port}`) {
        return json(res, 403, { error: 'Invalid local host' });
      }
      res.setHeader('Referrer-Policy', 'no-referrer');
      res.setHeader('X-Frame-Options', 'DENY');
      res.setHeader('Content-Security-Policy', "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src 'self' blob:; img-src 'self' data: blob:; base-uri 'none'; frame-ancestors 'none'");
      if (!['/app.js', '/style.css'].includes(url.pathname) && !authenticate(req, url)) return json(res, 401, { error: 'Unauthorized session' });
      if (req.method === 'GET' && ASSETS[url.pathname]) {
        const asset = ASSETS[url.pathname];
        const contents = await readFile(fileURLToPath(new URL(asset.file, import.meta.url)));
        res.writeHead(200, { 'Content-Type': asset.type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
        return res.end(contents);
      }
      if (req.method === 'GET' && url.pathname === '/api/status') return json(res, 200, status());
      if (req.method === 'POST' && url.pathname === '/api/heartbeat') {
        const body = await readJSON(req);
        if (typeof body.source !== 'string' || body.source.length > 60) return json(res, 400, { error: 'Invalid source' });
        if (state.source !== (body.source || null)) state.latest = null;
        state.source = body.source || null;
        state.previewAt = Date.now();
        return json(res, 200, { ok: true });
      }
      if (req.method === 'POST' && url.pathname === '/api/resume') {
        state.stopped = false;
        return json(res, 200, { ok: true });
      }
      if (req.method === 'POST' && url.pathname === '/api/stop') {
        state.stopped = true;
        state.previewAt = 0; state.source = null; state.latest = null;
        rejectPending('Look session stopped by user');
        return json(res, 200, { ok: true });
      }
      if (req.method === 'GET' && url.pathname === '/api/next') {
        if (state.stopped) return json(res, 200, { stop: true });
        const task = state.pending.values().next().value;
        return json(res, 200, { request: task ? { id: task.id, mode: task.mode, maxWaitMs: task.maxWaitMs } : null });
      }
      if (req.method === 'POST' && url.pathname === '/api/manual-frame') {
        const frame = checkedFrame(await readJSON(req));
        state.latest = frame;
        return json(res, 200, { ok: true, receivedAt: frame.receivedAt });
      }
      if (req.method === 'POST' && url.pathname.startsWith('/api/frame/')) {
        const id = url.pathname.slice('/api/frame/'.length);
        if (!state.pending.has(id)) return json(res, 404, { error: 'Capture request expired' });
        const body = await readJSON(req);
        if (body.status === 'error') {
          resolvePending(id, { error: String(body.message || 'Preview could not capture frame').slice(0, 200) });
          return json(res, 200, { ok: true });
        }
        if (body.status === 'unchanged') {
          resolvePending(id, { unchanged: true });
          return json(res, 200, { ok: true });
        }
        const frame = checkedFrame(body);
        state.latest = frame;
        resolvePending(id, { frame });
        return json(res, 200, { ok: true });
      }
      return json(res, 404, { error: 'Not found' });
    } catch (error) {
      return json(res, errorMessage(error).includes('size limit') ? 413 : 400, { error: errorMessage(error) });
    }
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, host, resolve);
  });
  address = server.address();
  const url = `http://127.0.0.1:${address.port}/?token=${token}`;
  return {
    url, token, port: address.port, status,
    open() { state.stopped = false; return url; },
    latest() { if (!state.latest) throw new Error('No frame captured yet. Capture one in the preview first.'); return state.latest; },
    async capture(mode = 'now', maxWaitMs = 20_000) {
      if (mode !== 'now' && mode !== 'changed') throw new Error('Mode must be now or changed');
      if (!status().connected) throw new Error('Preview is not connected to an active camera, screen, or video. Open /look and select a source.');
      if (state.pending.size) throw new Error('Another capture is in progress');
      const requestedWait = Math.min(MAX_WAIT_MS, Math.max(1_000, Math.floor(maxWaitMs)));
      return new Promise((resolve, reject) => {
        const id = String(++state.requestCounter);
        const timer = setTimeout(() => {
          state.pending.delete(id);
          reject(new Error('Timed out waiting for the preview to return a frame'));
        }, requestedWait + 3_000);
        state.pending.set(id, { id, mode, maxWaitMs: requestedWait, timer, resolve, reject });
      });
    },
    stop() {
      state.stopped = true;
      state.previewAt = 0;
      state.source = null;
      state.latest = null;
      rejectPending('Look session stopped');
    },
    async close() {
      this.stop();
      await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    },
  };
}
