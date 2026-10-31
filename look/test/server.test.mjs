import { test } from 'node:test';
import assert from 'node:assert/strict';
import { request as httpRequest } from 'node:http';
import { createLookServer } from '../src/server.mjs';

const fakeJPEG = Buffer.from([0xff, 0xd8, 0xff, 0xd9]).toString('base64');
const frame = { mime: 'image/jpeg', data: fakeJPEG, source: 'screen', focus: { x: .1, y: .2, width: .5, height: .4 } };
async function client(session, path, method = 'GET', body, authenticated = true) {
  const root = `http://127.0.0.1:${session.port}`;
  const response = await fetch(root + path, {
    method, headers: { ...(authenticated ? { 'X-Look-Token': session.token } : {}), ...(body ? { 'Content-Type': 'application/json' } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  return { code: response.status, body: await response.json() };
}

test('preview is local-only, assets load, and API requires session token', async (t) => {
  const look = await createLookServer(); t.after(() => look.close());
  const root = `http://127.0.0.1:${look.port}`;
  assert.equal((await fetch(root + '/')).status, 401);
  assert.equal((await fetch(look.url)).status, 200);
  assert.equal((await fetch(root + '/app.js')).status, 200);
  assert.equal((await fetch(root + '/style.css')).status, 200);
  assert.equal((await client(look, '/api/status', 'GET', null, false)).code, 401);
  assert.equal((await client(look, '/api/status')).body.connected, false);
  const invalidHostCode = await new Promise((resolve, reject) => {
    const req = httpRequest(root + '/api/status', {headers:{Host:'look.attacker.test','X-Look-Token':look.token}}, response => {response.resume();resolve(response.statusCode);});
    req.on('error',reject);req.end();
  });
  assert.equal(invalidHostCode,403);
  await assert.rejects(() => createLookServer({host: '0.0.0.0'}), /127.0.0.1/);
});

test('manual capture is held in session memory and cleared on stop', async (t) => {
  const look = await createLookServer(); t.after(() => look.close());
  assert.equal((await client(look, '/api/manual-frame', 'POST', frame)).code, 200);
  assert.equal(look.latest().data, fakeJPEG);
  assert.equal(look.latest().source, 'screen');
  assert.equal((await client(look, '/api/manual-frame', 'POST', {mime:'image/jpeg', data:'abc'})).code, 400);
  look.stop();
  assert.throws(() => look.latest(), /No frame captured/);
});

test('agent capture uses the requested browser frame without persistence', async (t) => {
  const look = await createLookServer(); t.after(() => look.close());
  await client(look, '/api/heartbeat', 'POST', {source:'screen'});
  const pending = look.capture('now', 3000);
  const response = (await client(look, '/api/next')).body;
  assert.equal(response.request.mode, 'now');
  const done = await client(look, `/api/frame/${response.request.id}`, 'POST', frame);
  assert.equal(done.code, 200);
  const result = await pending;
  assert.equal(result.frame.source, 'screen');
  assert.equal(result.frame.focus.width, .5);
  assert.equal((await client(look, `/api/frame/${response.request.id}`, 'POST', frame)).code, 404);
});

test('watch can report no change, and stop rejects an in-flight capture', async (t) => {
  const look = await createLookServer(); t.after(() => look.close());
  await client(look, '/api/heartbeat', 'POST', {source:'camera'});
  const wait = look.capture('changed', 1000);
  const { request } = (await client(look, '/api/next')).body;
  assert.equal(request.mode, 'changed');
  await client(look, `/api/frame/${request.id}`, 'POST', {status:'unchanged'});
  assert.deepEqual(await wait, {unchanged:true});
  const blocked = look.capture('changed', 1000);
  const blockedRejection = assert.rejects(blocked, /stopped/);
  const stop = await client(look, '/api/stop', 'POST');
  assert.equal(stop.code, 200);
  await blockedRejection;
  assert.equal((await client(look, '/api/next')).body.stop, true);
  await client(look, '/api/resume', 'POST');
  await client(look, '/api/heartbeat', 'POST', {source:'screen'});
  assert.equal(look.status().connected, true);
});

test('preview errors return promptly rather than timing out', async (t) => {
  const look = await createLookServer(); t.after(() => look.close());
  await client(look, '/api/heartbeat', 'POST', {source:'recording'});
  const pending = look.capture('now', 1000);
  const {request} = (await client(look, '/api/next')).body;
  const result = await client(look, `/api/frame/${request.id}`, 'POST', {status:'error',message:'video not ready'});
  assert.equal(result.code, 200);
  assert.deepEqual(await pending, {error:'video not ready'});
});
