#!/usr/bin/env node

import { writeFile } from 'node:fs/promises';

const endpoint = process.env.PLANNING_SKILLS_MCP_URL
  ?? 'https://planning-skills-mcp-production.up.railway.app/mcp';
const outputPath = process.argv[2] ?? '/tmp/planning-skills-review-demo-data.json';

const baseHeaders = {
  'content-type': 'application/json',
  accept: 'application/json, text/event-stream',
};

async function parseRpcResponse(response) {
  const text = await response.text();
  const dataLine = text.split('\n').find((line) => line.startsWith('data: '));
  const payload = dataLine ? dataLine.slice(6) : text;
  return JSON.parse(payload);
}

const init = await fetch(endpoint, {
  method: 'POST',
  headers: baseHeaders,
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: { name: 'planning-skills-review-demo', version: '1.0.0' },
    },
  }),
});
if (!init.ok) throw new Error(`MCP initialize failed: ${init.status}`);
const sessionId = init.headers.get('mcp-session-id');
if (!sessionId) throw new Error('MCP initialize did not return a session ID.');
await parseRpcResponse(init);

const headers = { ...baseHeaders, 'mcp-session-id': sessionId };
await fetch(endpoint, {
  method: 'POST',
  headers,
  body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }),
});

let id = 2;
async function rpc(method, params = {}) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers,
    body: JSON.stringify({ jsonrpc: '2.0', id: id++, method, params }),
  });
  if (!response.ok) throw new Error(`${method} failed: ${response.status}`);
  return parseRpcResponse(response);
}

async function callTool(name, args = {}) {
  const body = await rpc('tools/call', { name, arguments: args });
  const text = body?.result?.content
    ?.filter((part) => part.type === 'text' && typeof part.text === 'string')
    .map((part) => part.text)
    .join('\n') ?? '';
  if (!text) throw new Error(`Tool ${name} returned no text content.`);
  return text;
}

const listed = await rpc('tools/list');
const tools = listed?.result?.tools ?? [];

const recommendation = await callTool('recommend_planning_workflow', {
  situation: 'I have a rough product idea but I am not sure what planning work I need next. Help me choose the smallest useful move.',
});
const shaping = await callTool('get_planning_skill', { skill: 'shaping' });
const orchestration = await callTool('get_orchestration_manifest');
const contracts = await callTool('get_artifact_contracts');

const output = {
  captured_at: new Date().toISOString(),
  endpoint,
  tools: tools.map((tool) => ({
    name: tool.name,
    title: tool.title,
    description: tool.description,
    annotations: tool.annotations,
    inputSchema: tool.inputSchema,
  })),
  recommendation,
  shaping,
  orchestration,
  contracts,
};

await writeFile(outputPath, JSON.stringify(output, null, 2), 'utf8');

await fetch(endpoint, {
  method: 'DELETE',
  headers: { accept: 'application/json, text/event-stream', 'mcp-session-id': sessionId },
}).catch(() => {});

console.error(`Captured live MCP review data to ${outputPath}`);
