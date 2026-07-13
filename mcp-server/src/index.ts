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
  statechart: {
    title: 'Statechart',
    description: 'Turn a selected stateful portion of a breadboard into a transition table and Mermaid statechart without replacing the breadboard.',
    path: 'statechart/SKILL.md',
  },
  'interface-contracts': {
    title: 'Interface Contracts',
    description: 'Turn selected breadboard wires or slices into plain-language contracts for boundary-crossing data exchanges.',
    path: 'interface-contracts/SKILL.md',
  },
  'executable-breadboards': {
    title: 'Executable Breadboards',
    description: 'Turn a selected slice into a buildable, testable handoff with examples, fixtures, expected outputs, edge cases, and acceptance tests.',
    path: 'executable-breadboards/SKILL.md',
  },
  dumplink: {
    title: 'Dumplink',
    description: 'Turn a shaped project into vertical task groups, risk states, dependency-aware sequence, scope cuts, and a bounded agent handoff.',
    path: 'dumplink/SKILL.md',
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
  statechart: `# Statechart\n\n## Source\n- Breadboard:\n- Scope or slice:\n\n## State inventory\n\n| State ID | Source breadboard IDs | State | Parent state | Meaning | Status |\n| --- | --- | --- | --- | --- | --- |\n\n## Transition table\n\n| Transition ID | From | Trigger type | Event | Guard | Effect | To | Source wiring | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n\n## Mermaid statechart\n\n\`\`\`mermaid\nstateDiagram-v2\n\`\`\`\n\n## Gaps and proposed breadboard updates\n`,
  'interface-contract': `# Interface Contract\n\n## Contract ID\n\n## Boundary\n\n## Source artifact\n\n## Purpose\n\n## Inputs\n\n| Field | Required? | Type / shape | Notes |\n| --- | --- | --- | --- |\n\n## Outputs\n\n| Field | Required? | Type / shape | Notes |\n| --- | --- | --- | --- |\n\n## Branches and error cases\n\n| Case | Condition | Expected behavior |\n| --- | --- | --- |\n\n## Open decisions\n`,
  'executable-breadboard': `# Executable Breadboard\n\n## Selected slice\n\n## Source breadboard rows\n\n## Interface contracts in scope\n\n## Fixtures / starting data\n\n## Example runs\n\n| Run ID | Starting state | Action | Expected visible result | Expected state change |\n| --- | --- | --- | --- | --- |\n\n## Edge cases\n\n| Edge ID | Case | Expected behavior |\n| --- | --- | --- |\n\n## Acceptance tests\n\n| Test ID | Proves | How to verify |\n| --- | --- | --- |\n\n## Open decisions\n`,
  dumplink: `# Dumplink Plan\n\n## Project boundary\n\n## Task dump\n\n| ID | Task | Type | Known/Unknown | Notes |\n| --- | --- | --- | --- | --- |\n\n## Task groups\n\n| ID | Name | Included tasks | User/system behavior produced | Risk state | Cuttable? | Notes |\n| --- | --- | --- | --- | --- | --- | --- |\n\n## Dependency map\n\n| From | To | Why this dependency exists | Risk if delayed |\n| --- | --- | --- | --- |\n\n## Build sequence\n\n| Order | Task group | Why now | Demo/checkpoint | Exit condition |\n| --- | --- | --- | --- | --- |\n\n## Scope cuts\n\n| Cut option | Remove/defer | Preserved behavior | Cost of cutting | Later decision |\n| --- | --- | --- | --- | --- |\n\n## Acceptance checks\n\n## Agent handoff packet\n\nActive slice:\nSource artifacts:\nMust preserve:\nDo not build:\nTask group to implement:\nRelevant tasks:\nKnown unknowns:\nAcceptance check:\nStop condition:\n`,
  kickoff: `# Kickoff Doc\n\n## Territory\n\n## What we are building\n\n## What we are not building\n\n## Requirements / constraints\n\n## Risks and unknowns\n\n## First slice\n\n## Verification target\n`,
  'context-packet': `# Agent Context Packet\n\n## Active task\n\n## Source artifacts\n\n## Authority order\n\n## Must-preserve constraints\n\n## Stable IDs in scope\n\n## Non-goals\n\n## Relevant executable breadboard\n\n## Relevant interface contracts\n\n## Relevant Dumplink plan\n\n## Current slice\n\n## Execution contract\n- Goal condition:\n- Required checks:\n- Allowed files / areas:\n- Out-of-scope changes:\n- Return-to-planning conditions:\n- Checkpoint cadence:\n- Verification caveats:\n\n## Verification target\n`,
  reflection: `# Breadboard Reflection\n\n## Implementation reality synced\n\n## Selected breadboard says\n\n## Current implementation does\n\n## Drift found\n\n| ID | Drift | Risk | Recommended move |\n| --- | --- | --- | --- |\n\n## Planning updates\n\n## Implementation follow-ups\n`,
  'drift-check': `# Drift Check\n\nReturn only one of the two forms below.\n\n## No drift\n\nNo planning drift found.\n\n## Drift\n\nPlanning drift found:\n- Selected artifact says:\n- Current implementation direction is:\n- Risk:\n- Recommended move:\n`,
  'agent-run-log': `# Agent Run Log\n\n## Task\n\n## Mode\n\n## Source artifacts used\n\n## Authority order\n\n## Selected slice\n\n## Files inspected\n\n## Files changed\n\n## Decisions made\n\n## Drift checks\n\n## Planning updates needed\n\n## Verification run\n\n## Handoff notes\n`,
  'orchestration-plan': `# Agent Orchestration Plan\n\n## Active mode\n\n## Required source artifacts\n\n## Allowed outputs\n\n## Forbidden moves\n\n## Human decision gate\n\n## Next mode\n\n## Drift / reflection checkpoint\n`,
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

    if (
      normalized.includes('statechart') ||
      normalized.includes('state machine') ||
      normalized.includes('lifecycle') ||
      normalized.includes('timeout') ||
      normalized.includes('retry') ||
      normalized.includes('guard')
    ) {
      recommendations.push('statechart');
    }

    if (normalized.includes('boundary') || normalized.includes('contract') || normalized.includes('api') || normalized.includes('interface')) {
      recommendations.push('interface-contracts');
    }

    if (normalized.includes('fixture') || normalized.includes('example run') || normalized.includes('expected output') || normalized.includes('acceptance test') || normalized.includes('testable')) {
      recommendations.push('executable-breadboards');
    }

    if (normalized.includes('task group') || normalized.includes('dependency') || normalized.includes('sequence') || normalized.includes('scope cut') || normalized.includes('dumplink')) {
      recommendations.push('dumplink');
    }

    if (normalized.includes('implement') || normalized.includes('agent') || normalized.includes('context') || normalized.includes('build')) {
      recommendations.push('feed-planning-context');
    }

    if (normalized.includes('drift') || normalized.includes('reflection') || normalized.includes('compare to implementation')) {
      recommendations.push('breadboard-reflection');
    }

    const defaultWorkflow: SkillName[] = ['framing-doc', 'shaping', 'breadboarding', 'dumplink', 'feed-planning-context'];
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
  'Return a starter Markdown template for a planning, orchestration, or reflection artifact.',
  {
    artifact: z.enum(Object.keys(artifactTemplates) as [ArtifactName, ...ArtifactName[]]),
  },
  async ({ artifact }) => {
    return {
      content: [{ type: 'text', text: artifactTemplates[artifact] }],
    };
  },
);

server.tool(
  'get_orchestration_manifest',
  'Return the tool-neutral orchestration manifest for planning harnesses.',
  {},
  async () => {
    const content = await readFile(join(repoRoot, '.agent-orchestration.yaml'), 'utf8');

    return {
      content: [{ type: 'text', text: content }],
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
