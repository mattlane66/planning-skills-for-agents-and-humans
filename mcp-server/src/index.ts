#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { readFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, '..', '..');

const skills = {
  'framing-doc': {
    title: 'Framing Doc',
    description: 'Turn messy source material into a frame with current reality, boundaries, current approach/result, and desired outcome.',
    path: 'framing-doc/SKILL.md',
  },
  shaping: {
    title: 'Shaping',
    description: 'Define requirements/criteria, compare alternative approaches, and detail the selected direction before implementation.',
    path: 'shaping/SKILL.md',
  },
  breadboarding: {
    title: 'Breadboarding',
    description: 'Map places/screens/states, affordances, stores, and wiring so behavior is concrete before implementation.',
    path: 'breadboarding/SKILL.md',
  },
  'breadboard-reflection': {
    title: 'Breadboard Reflection',
    description: 'Compare a breadboard to implementation, repair drift, and identify design smells.',
    path: 'breadboard-reflection/SKILL.md',
  },
  'kickoff-doc': {
    title: 'Kickoff Doc',
    description: 'Turn a kickoff conversation into a builder-facing reference doc organized around the territory being built.',
    path: 'kickoff-doc/SKILL.md',
  },
  'feed-planning-context': {
    title: 'Feed Planning Context',
    description: 'Package planning artifacts into compact context for agent implementation without overloading context.',
    path: 'feed-planning-context/SKILL.md',
  },
} as const;

type SkillName = keyof typeof skills;

const artifactTemplates = {
  frame: `# Frame\n\n## Source material\n\n## Current reality\n\n## Current approach and result\n\n## Desired outcome\n\n## Boundaries\n\n## Requirements / criteria\n\n| ID | Criterion | Must have? | Notes |\n| --- | --- | --- | --- |\n`,
  shaping: `# Shaping\n\n## Problem frame\n\n## Requirements / criteria\n\n| ID | Criterion | Must have? | Why it matters |\n| --- | --- | --- | --- |\n\n## Alternative shapes\n\n| Option | Mechanism | Strengths | Risks |\n| --- | --- | --- | --- |\n\n## Fit check\n\n| Criterion | Option A | Option B | Option C | Notes |\n| --- | --- | --- | --- | --- |\n\n## Selected direction\n\n## Unknowns / spikes\n`,
  breadboard: `# Breadboard\n\n## Places\n\n| Place ID | Place / screen / state | Purpose |\n| --- | --- | --- |\n\n## Affordances\n\n| Affordance ID | Place ID | User can... | Visible result |\n| --- | --- | --- | --- |\n\n## Stores / state\n\n| Store ID | Data / state | Owner | Notes |\n| --- | --- | --- | --- |\n\n## Wiring\n\n| From | Action | To | System behavior |\n| --- | --- | --- | --- |\n\n## Slices\n\n| Slice ID | Scope | Dependencies | Verification target |\n| --- | --- | --- | --- |\n`,
  kickoff: `# Kickoff Doc\n\n## Territory\n\n## What we are building\n\n## What we are not building\n\n## Requirements / constraints\n\n## Risks and unknowns\n\n## First slice\n\n## Verification target\n`,
  'context-packet': `# Agent Context Packet\n\n## Active task\n\n## Source artifacts\n\n## Authority order\n\n## Must-preserve constraints\n\n## Stable IDs in scope\n\n## Non-goals\n\n## Current slice\n\n## Verification target\n`,
} as const;

type ArtifactName = keyof typeof artifactTemplates;

const server = new McpServer({
  name: 'planning-skills-for-agents-and-humans',
  version: '0.1.0',
});

server.tool('list_planning_skills', 'List the available planning skills and their intended uses.', {}, async () => {
  const text = Object.entries(skills)
    .map(([name, skill]) => `- ${name}: ${skill.description}`)
    .join('\n');

  return {
    content: [{ type: 'text', text }],
  };
});

server.tool(
  'get_planning_skill',
  'Return the SKILL.md instructions for a specific planning skill.',
  {
    skill: z.enum(Object.keys(skills) as [SkillName, ...SkillName[]]),
  },
  async ({ skill }) => {
    const skillInfo = skills[skill];
    const content = await readFile(join(repoRoot, skillInfo.path), 'utf8');

    return {
      content: [
        {
          type: 'text',
          text: `# ${skillInfo.title}\n\n${content}`,
        },
      ],
    };
  },
);

server.tool(
  'recommend_planning_workflow',
  'Recommend which planning skills to use based on a brief situation description.',
  {
    situation: z.string().min(1).describe('The planning situation, source material, or user goal.'),
  },
  async ({ situation }) => {
    const normalized = situation.toLowerCase();
    const recommendations: SkillName[] = [];

    if (normalized.includes('transcript') || normalized.includes('notes') || normalized.includes('messy') || normalized.includes('problem')) {
      recommendations.push('framing-doc');
    }

    if (normalized.includes('compare') || normalized.includes('option') || normalized.includes('shape') || normalized.includes('direction')) {
      recommendations.push('shaping');
    }

    if (normalized.includes('screen') || normalized.includes('flow') || normalized.includes('state') || normalized.includes('breadboard') || normalized.includes('system')) {
      recommendations.push('breadboarding');
    }

    if (normalized.includes('implement') || normalized.includes('agent') || normalized.includes('context') || normalized.includes('build')) {
      recommendations.push('feed-planning-context');
    }

    if (normalized.includes('drift') || normalized.includes('reflection') || normalized.includes('compare to implementation')) {
      recommendations.push('breadboard-reflection');
    }

    const defaultWorkflow: SkillName[] = ['framing-doc', 'shaping', 'breadboarding', 'feed-planning-context'];
    const workflow = recommendations.length > 0 ? Array.from(new Set(recommendations)) : defaultWorkflow;

    return {
      content: [
        {
          type: 'text',
          text: `Recommended workflow:\n\n${workflow.map((name, index) => `${index + 1}. ${name} — ${skills[name].description}`).join('\n')}`,
        },
      ],
    };
  },
);

server.tool(
  'get_artifact_template',
  'Return a starter Markdown template for a planning artifact.',
  {
    artifact: z.enum(Object.keys(artifactTemplates) as [ArtifactName, ...ArtifactName[]]),
  },
  async ({ artifact }) => {
    return {
      content: [{ type: 'text', text: artifactTemplates[artifact] }],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
