#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { recommendPlanningWorkflow, type SkillName } from './recommend.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, '..', '..');

const skills: Record<SkillName, { title: string; description: string; path: string }> = {
  'framing-doc': {
    title: 'Framing Doc',
    description: 'Turn messy source material into a frame with current reality, boundaries, current approach/result, and desired outcome.',
    path: 'framing-doc/SKILL.md',
  },
  shaping: {
    title: 'Shaping',
    description: 'Define requirements and criteria, compare alternative approaches, and detail the selected direction before implementation.',
    path: 'shaping/SKILL.md',
  },
  breadboarding: {
    title: 'Breadboarding',
    description: 'Map places, affordances, stores, state, and wiring so behavior is concrete before implementation.',
    path: 'breadboarding/SKILL.md',
  },
  'interface-contracts': {
    title: 'Interface Contracts',
    description: 'Turn selected breadboard wires or slices into plain-language contracts for boundary-crossing data exchanges.',
    path: 'interface-contracts/SKILL.md',
  },
  'executable-breadboards': {
    title: 'Executable Breadboards',
    description: 'Turn a selected slice into a testable handoff with examples, fixtures, expected outputs, edge cases, and acceptance tests.',
    path: 'executable-breadboards/SKILL.md',
  },
  dumplink: {
    title: 'Dumplink',
    description: 'Turn selected shaped work into vertical task groups, dependency-aware sequence, risk states, scope cuts, and a bounded handoff.',
    path: 'dumplink/SKILL.md',
  },
  'breadboard-reflection': {
    title: 'Breadboard Reflection',
    description: 'Compare a breadboard to implementation, repair drift, and identify design smells.',
    path: 'breadboard-reflection/SKILL.md',
  },
  'kickoff-doc': {
    title: 'Kickoff Doc',
    description: 'Turn a kickoff conversation into a builder-facing reference organized around the territory being built.',
    path: 'kickoff-doc/SKILL.md',
  },
  'feed-planning-context': {
    title: 'Feed Planning Context',
    description: 'Package planning artifacts into compact context for agent implementation without overloading context.',
    path: 'feed-planning-context/SKILL.md',
  },
};

const artifactTemplates = {
  frame: 'templates/frame.md',
  shaping: 'templates/shaping.md',
  breadboard: 'templates/breadboard.md',
  'interface-contract': 'templates/interface-contracts.md',
  'executable-breadboard': 'templates/executable-breadboard.md',
  dumplink: 'templates/dumplink.md',
  kickoff: 'templates/kickoff.md',
  'context-packet': 'templates/context-packet.md',
  reflection: 'templates/breadboard-reflection.md',
  'drift-check': 'templates/drift-check.md',
  'agent-run-log': 'templates/agent-run-log.md',
  'orchestration-plan': 'templates/orchestration-plan.md',
} as const;

type ArtifactName = keyof typeof artifactTemplates;

const server = new McpServer({
  name: 'planning-skills-for-agents-and-humans',
  version: '1.1.0',
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
