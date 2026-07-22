#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { recommendPlanningWorkflow, skillNames, type SkillName } from './recommend.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, '..', '..');

type SkillMetadataEntry = { title: string; description: string };

function parseSkillMetadata(value: unknown): Record<SkillName, SkillMetadataEntry> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('skill-metadata.json must contain an object');
  }

  const raw = value as Record<string, unknown>;
  const unexpected = Object.keys(raw).filter((name) => !skillNames.includes(name as SkillName));
  if (unexpected.length > 0) {
    throw new Error(`skill-metadata.json contains unknown skills: ${unexpected.join(', ')}`);
  }

  const parsed = {} as Record<SkillName, SkillMetadataEntry>;
  for (const name of skillNames) {
    const entry = raw[name];
    if (typeof entry !== 'object' || entry === null || Array.isArray(entry)) {
      throw new Error(`skill-metadata.json is missing metadata for ${name}`);
    }
    const fields = entry as Record<string, unknown>;
    if (
      Object.keys(fields).length !== 2
      || typeof fields.title !== 'string'
      || fields.title.trim() === ''
      || typeof fields.description !== 'string'
      || fields.description.trim() === ''
    ) {
      throw new Error(`skill-metadata.json has invalid metadata for ${name}`);
    }
    parsed[name] = { title: fields.title.trim(), description: fields.description.trim() };
  }
  return parsed;
}

const skillMetadata = parseSkillMetadata(
  JSON.parse(await readFile(join(repoRoot, 'skill-metadata.json'), 'utf8')) as unknown,
);

const skills = Object.fromEntries(
  skillNames.map((name) => [name, { ...skillMetadata[name], path: `${name}/SKILL.md` }]),
) as Record<SkillName, SkillMetadataEntry & { path: string }>;

const artifactTemplates = {
  frame: 'templates/frame.md',
  shaping: 'templates/shaping.md',
  breadboard: 'templates/breadboard.md',
  statechart: 'templates/statechart.md',
  slices: 'templates/slices.md',
  'interface-contract': 'templates/interface-contracts.md',
  'executable-breadboard': 'templates/executable-breadboard.md',
  dumplink: 'templates/dumplink.md',
  kickoff: 'templates/kickoff.md',
  'context-packet': 'templates/context-packet.md',
  reflection: 'templates/breadboard-reflection.md',
  'drift-check': 'templates/drift-check.md',
  'agent-run-log': 'templates/agent-run-log.md',
  'orchestration-plan': 'templates/orchestration-plan.md',
  spike: 'templates/spike.md',
  'sketch-reconciliation': 'templates/sketch-reconciliation.md',
  'decision-log': 'templates/decision-log.md',
  'appetite-card': 'templates/appetite-card.md',
} as const;

type ArtifactName = keyof typeof artifactTemplates;

const server = new McpServer({
  name: 'planning-skills-for-agents-and-humans',
  version: '1.2.0',
});

server.tool('list_planning_skills', 'List the available planning skills and their intended uses.', {}, async () => {
  const text = Object.entries(skills)
    .map(([name, skill]) => `- ${name}: ${skill.description}`)
    .join('\n');

  return { content: [{ type: 'text', text }] };
});

server.tool(
  'get_planning_skill',
  'Return the canonical SKILL.md instructions for a specific planning skill.',
  { skill: z.enum(Object.keys(skills) as [SkillName, ...SkillName[]]) },
  async ({ skill }) => {
    const skillInfo = skills[skill];
    const content = await readFile(join(repoRoot, skillInfo.path), 'utf8');
    return { content: [{ type: 'text', text: `# ${skillInfo.title}\n\n${content}` }] };
  },
);

server.tool(
  'recommend_planning_workflow',
  'Recommend the next planning skills while respecting the method\'s prerequisites and human decision gates.',
  { situation: z.string().min(1).describe('The planning situation, available artifacts, and desired next move.') },
  async ({ situation }) => {
    const workflow = recommendPlanningWorkflow(situation);
    const text = workflow
      .map((name, index) => `${index + 1}. ${name} — ${skills[name].description}`)
      .join('\n');
    return { content: [{ type: 'text', text: `Recommended workflow:\n\n${text}` }] };
  },
);

server.tool(
  'get_artifact_template',
  'Return a canonical starter Markdown template for a planning, orchestration, or reflection artifact.',
  { artifact: z.enum(Object.keys(artifactTemplates) as [ArtifactName, ...ArtifactName[]]) },
  async ({ artifact }) => {
    const content = await readFile(join(repoRoot, artifactTemplates[artifact]), 'utf8');
    return { content: [{ type: 'text', text: content }] };
  },
);

server.tool(
  'get_orchestration_manifest',
  'Return the tool-neutral orchestration manifest for planning harnesses.',
  {},
  async () => {
    const content = await readFile(join(repoRoot, '.agent-orchestration.yaml'), 'utf8');
    return { content: [{ type: 'text', text: content }] };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
