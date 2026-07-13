import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

function textContent(result: unknown): string {
  if (typeof result !== 'object' || result === null) {
    return '';
  }

  const content = (result as { content?: unknown }).content;
  if (!Array.isArray(content)) {
    return '';
  }

  return content
    .filter((part): part is { type: 'text'; text: string } => {
      if (typeof part !== 'object' || part === null) return false;
      const candidate = part as { type?: unknown; text?: unknown };
      return candidate.type === 'text' && typeof candidate.text === 'string';
    })
    .map((part) => part.text)
    .join('\n');
}

test('serves the canonical skill inventory and orchestration templates over MCP', async () => {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [resolve('dist/index.js')],
    stderr: 'pipe',
  });
  const client = new Client({ name: 'planning-skills-test', version: '1.1.0' });

  try {
    await client.connect(transport);

    const listed = await client.listTools();
    assert.deepEqual(
      listed.tools.map((tool) => tool.name).sort(),
      [
        'get_artifact_template',
        'get_orchestration_manifest',
        'get_planning_skill',
        'list_planning_skills',
        'recommend_planning_workflow',
      ],
    );

    const inventory = (await readFile(resolve('..', 'skill-inventory.txt'), 'utf8'))
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
    const availableSkills = await client.callTool({
      name: 'list_planning_skills',
      arguments: {},
    });
    const listedSkillNames = textContent(availableSkills)
      .split(/\r?\n/)
      .map((line) => /^- ([^:]+):/.exec(line)?.[1])
      .filter((name): name is string => Boolean(name));
    assert.deepEqual(listedSkillNames, inventory);

    const skill = await client.callTool({
      name: 'get_planning_skill',
      arguments: { skill: 'statechart' },
    });
    assert.match(textContent(skill), /breadboard tables remain the source of truth/i);

    const template = await client.callTool({
      name: 'get_artifact_template',
      arguments: { artifact: 'statechart' },
    });
    assert.match(textContent(template), /## Transition table/);
    assert.match(textContent(template), /stateDiagram-v2/);

    for (const [artifact, heading] of [
      ['slices', /# \[Project\] — Slices/],
      ['spike', /# \[Part\] Spike: \[Title\]/],
      ['decision-log', /# \[Project\] — Decision Log/],
      ['appetite-card', /# \[Project\] — Appetite Card/],
    ] as const) {
      const artifactTemplate = await client.callTool({
        name: 'get_artifact_template',
        arguments: { artifact },
      });
      assert.match(textContent(artifactTemplate), heading);
    }
  } finally {
    await client.close();
  }
});
