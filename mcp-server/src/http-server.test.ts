import assert from 'node:assert/strict';
import test from 'node:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import { createPlanningSkillsHttpServer } from './http-server.js';

function textContent(result: unknown): string {
  if (typeof result !== 'object' || result === null) return '';
  const content = (result as { content?: unknown }).content;
  if (!Array.isArray(content)) return '';
  return content
    .filter((part): part is { type: 'text'; text: string } => {
      if (typeof part !== 'object' || part === null) return false;
      const candidate = part as { type?: unknown; text?: unknown };
      return candidate.type === 'text' && typeof candidate.text === 'string';
    })
    .map((part) => part.text)
    .join('\n');
}

test('serves the planning tools over Streamable HTTP with explicit read-only annotations', async () => {
  const service = createPlanningSkillsHttpServer();
  await new Promise<void>((resolveListen, rejectListen) => {
    service.server.once('error', rejectListen);
    service.server.listen(0, '127.0.0.1', resolveListen);
  });

  const address = service.server.address();
  assert(address && typeof address === 'object');

  const health = await fetch(`http://127.0.0.1:${address.port}/healthz`);
  assert.equal(health.status, 200);
  assert.deepEqual(await health.json(), {
    status: 'ok',
    service: 'planning-skills-for-agents-and-humans',
    transport: 'streamable-http',
  });

  const client = new Client({ name: 'planning-skills-http-test', version: '1.0.0' });
  const transport = new StreamableHTTPClientTransport(
    new URL(`http://127.0.0.1:${address.port}/mcp`),
  );

  try {
    await client.connect(transport);

    const listed = await client.listTools();
    assert.equal(listed.tools.length, 7);
    for (const tool of listed.tools) {
      assert.deepEqual(
        tool.annotations,
        {
          readOnlyHint: true,
          destructiveHint: false,
          openWorldHint: false,
          idempotentHint: true,
        },
        `${tool.name} should advertise the public-plugin safety contract`,
      );
    }

    const recommendation = await client.callTool({
      name: 'recommend_planning_workflow',
      arguments: { situation: 'I have a rough solution idea and want to tease out requirements without selecting it.' },
    });
    assert.match(textContent(recommendation), /shaping/i);
  } finally {
    await client.close();
    await service.close();
  }
});
