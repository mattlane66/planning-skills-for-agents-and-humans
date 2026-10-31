import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';

const fakeJPEG = Buffer.from([0xff, 0xd8, 0xff, 0xd9]).toString('base64');
test('MCP handshake, tool listing, opening, and image response', async (t) => {
  const child = spawn(process.execPath, [new URL('../src/mcp.mjs', import.meta.url).pathname], { stdio: ['pipe','pipe','pipe'] });
  t.after(() => { child.kill(); });
  const responses = new Map();
  const next = new Map();
  const lines = createInterface({input:child.stdout});
  lines.on('line', line => {
    const item = JSON.parse(line);
    if (next.has(item.id)) { next.get(item.id)(item); next.delete(item.id); }
    else responses.set(item.id,item);
  });
  let id = 0;
  async function ask(method, params = {}) {
    const requestID = ++id;
    const response = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`No MCP reply for ${method}`)), 5000);
      next.set(requestID, value => {clearTimeout(timer);resolve(value);});
    });
    child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:requestID,method,params})+'\n');
    return response;
  }
  assert.equal((await ask('initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'test',version:'1'}})).result.serverInfo.name,'planning-skills-look');
  const list = (await ask('tools/list')).result.tools;
  assert.ok(list.some(tool => tool.name === 'look_watch'));
  const start = await ask('tools/call',{name:'look_open',arguments:{}});
  const url = new URL(start.result.content[0].text.match(/http:\/\/127\.0\.0\.1:\d+\/\?token=\S+/)[0]);
  const port = url.port, token = url.searchParams.get('token');
  const root = `http://127.0.0.1:${port}`;
  await fetch(root+'/api/heartbeat',{method:'POST',headers:{'X-Look-Token':token,'Content-Type':'application/json'},body:JSON.stringify({source:'screen'})});
  const pending = ask('tools/call',{name:'look_capture',arguments:{focus:'only diagrams'}});
  let request;
  for (let i=0;i<25;i++) {
    const r = await fetch(root+'/api/next',{headers:{'X-Look-Token':token}});
    ({request} = await r.json());
    if (request) break;
    await new Promise(resolve=>setTimeout(resolve,20));
  }
  assert.ok(request);
  const uploaded = await fetch(root+`/api/frame/${request.id}`,{method:'POST',headers:{'X-Look-Token':token,'Content-Type':'application/json'},body:JSON.stringify({mime:'image/jpeg',data:fakeJPEG,source:'screen'})});
  assert.equal(uploaded.status,200);
  const finished = (await pending).result;
  assert.equal(finished.content[1].type,'image');
  assert.equal(finished.content[1].data,fakeJPEG);
  assert.match(finished.content[0].text,/only diagrams/);
  const stop = (await ask('tools/call',{name:'look_stop',arguments:{}})).result;
  assert.match(stop.content[0].text,/stopped/i);
});
