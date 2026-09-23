import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { readFile, realpath, stat } from 'node:fs/promises';
import { dirname, extname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { recommendPlanningWorkflow, skillNames, type SkillName } from './recommend.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, '..', '..');

type SkillMetadataEntry = { title: string; description: string };

function parsePackageVersion(value: unknown): string {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('mcp-server/package.json must contain an object');
  }
  const version = (value as Record<string, unknown>).version;
  if (typeof version !== 'string' || !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
    throw new Error('mcp-server/package.json must contain a valid version');
  }
  return version;
}

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
const serverVersion = parsePackageVersion(
  JSON.parse(await readFile(join(repoRoot, 'mcp-server', 'package.json'), 'utf8')) as unknown,
);

const skills = Object.fromEntries(
  skillNames.map((name) => [name, { ...skillMetadata[name], path: `${name}/SKILL.md` }]),
) as Record<SkillName, SkillMetadataEntry & { path: string }>;

const readableSkillResourceExtensions = new Set([
  '.json',
  '.md',
  '.py',
  '.sh',
  '.txt',
  '.yaml',
  '.yml',
]);

async function readSkillResource(skill: SkillName, requestedResource: string): Promise<string> {
  if (isAbsolute(requestedResource) || requestedResource.includes('\0')) {
    throw new Error('resource must be a relative path inside the selected skill');
  }
  const skillRoot = await realpath(join(repoRoot, skill));
  const target = await realpath(resolve(skillRoot, requestedResource));
  const localPath = relative(skillRoot, target);
  if (!localPath || localPath.startsWith('..') || isAbsolute(localPath)) {
    throw new Error('resource must resolve inside the selected skill');
  }
  if (!readableSkillResourceExtensions.has(extname(target).toLowerCase())) {
    throw new Error('resource must be a supported text file');
  }
  const metadata = await stat(target);
  if (!metadata.isFile() || metadata.size > 1024 * 1024) {
    throw new Error('resource must be a text file no larger than 1 MiB');
  }
  return readFile(target, 'utf8');
}

const artifactTemplates = {
  'wayfinding-map': 'templates/wayfinding-map.md',
  'wayfinding-ticket': 'templates/wayfinding-ticket.md',
  frame: 'templates/frame.md',
  shaping: 'templates/shaping.md',
  breadboard: 'templates/breadboard.md',
  statechart: 'templates/statechart.md',
  slices: 'templates/slices.md',
  'interface-contract': 'templates/interface-contracts.md',
  'executable-breadboard': 'templates/executable-breadboard.md',
  dumplink: 'templates/dumplink.md',
  'execution-graph': 'templates/execution-graph.yaml',
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
  'research-to-frame-handoff': 'lead-user-research/study-templates/research-to-frame-handoff.md',
} as const;

type ArtifactName = keyof typeof artifactTemplates;

export const planningToolAnnotations = {
  readOnlyHint: true,
  destructiveHint: false,
  openWorldHint: false,
  idempotentHint: true,
} as const;

export function createPlanningSkillsServer(): McpServer {
  const server = new McpServer({
    name: 'planning-skills-for-agents-and-humans',
    version: serverVersion,
  });

  server.registerTool(
    'list_planning_skills',
    {
      title: 'List planning skills',
      description: 'List the planning workflows available in this plugin and the user situations each one is intended to address.',
      inputSchema: {},
      annotations: planningToolAnnotations,
    },
    async () => {
      const text = Object.entries(skills)
        .map(([name, skill]) => `- ${name}: ${skill.description}`)
        .join('\n');

      return { content: [{ type: 'text', text }] };
    },
  );

  server.registerTool(
    'get_planning_skill',
    {
      title: 'Get planning skill',
      description: 'Return the canonical instructions for one named planning workflow when the host needs the exact method rather than a summary.',
      inputSchema: { skill: z.enum(Object.keys(skills) as [SkillName, ...SkillName[]]) },
      annotations: planningToolAnnotations,
    },
    async ({ skill }) => {
      const skillInfo = skills[skill];
      const content = await readFile(join(repoRoot, skillInfo.path), 'utf8');
      return { content: [{ type: 'text', text: `# ${skillInfo.title}\n\n${content}` }] };
    },
  );

  server.registerTool(
    'get_skill_resource',
    {
      title: 'Get skill resource',
      description: 'Return a bounded text support file referenced by one planning skill, such as a schema, example, or verification guide.',
      inputSchema: {
        skill: z.enum(Object.keys(skills) as [SkillName, ...SkillName[]]),
        resource: z.string().min(1).describe('Relative path inside the selected skill, for example references/behavior-tracing-and-verification.md.'),
      },
      annotations: planningToolAnnotations,
    },
    async ({ skill, resource }) => {
      try {
        const content = await readSkillResource(skill, resource);
        return { content: [{ type: 'text' as const, text: content }] };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'unknown resource error';
        return {
          isError: true,
          content: [{ type: 'text' as const, text: `Cannot read skill resource: ${message}` }],
        };
      }
    },
  );

  server.registerTool(
    'recommend_planning_workflow',
    {
      title: 'Recommend planning workflow',
      description: 'Recommend the smallest allowed next planning move from trusted project context while respecting explicit exclusions, gated prerequisites, and human promotion gates.',
      inputSchema: {
        situation: z.string().min(1).describe('Trusted user instructions and trusted project state needed to choose the next planning move.'),
        excluded_skills: z.array(z.enum(skillNames)).optional().describe('Planning skills the user or host explicitly ruled out.'),
        source_material: z.string().optional().describe('Optional untrusted notes, transcripts, issue bodies, or other evidence. It is deliberately ignored for routing.'),
      },
      annotations: planningToolAnnotations,
    },
    async ({ situation, excluded_skills }) => {
      const workflow = recommendPlanningWorkflow(situation, { excludedSkills: excluded_skills });
      if (workflow.length === 0) {
        return { content: [{ type: 'text', text: 'No allowed planning move matched. Revisit the exclusions or ask the user for direction.' }] };
      }
      const text = workflow
        .map((name, index) => `${index + 1}. ${name} — ${skills[name].description}`)
        .join('\n');
      return { content: [{ type: 'text', text: `Recommended next move(s):\n\n${text}` }] };
    },
  );

  server.registerTool(
    'get_artifact_template',
    {
      title: 'Get artifact template',
      description: 'Return the canonical starter template for a named planning, orchestration, handoff, or reflection artifact.',
      inputSchema: { artifact: z.enum(Object.keys(artifactTemplates) as [ArtifactName, ...ArtifactName[]]) },
      annotations: planningToolAnnotations,
    },
    async ({ artifact }) => {
      const content = await readFile(join(repoRoot, artifactTemplates[artifact]), 'utf8');
      return { content: [{ type: 'text', text: content }] };
    },
  );

  server.registerTool(
    'get_artifact_contracts',
    {
      title: 'Get artifact contracts',
      description: 'Return the machine-readable minimum artifact contracts and promotion-gate mappings used to validate planning readiness.',
      inputSchema: {},
      annotations: planningToolAnnotations,
    },
    async () => {
      const content = await readFile(join(repoRoot, 'contracts', 'artifact-contracts.yaml'), 'utf8');
      return { content: [{ type: 'text', text: content }] };
    },
  );

  server.registerTool(
    'get_orchestration_manifest',
    {
      title: 'Get orchestration manifest',
      description: 'Return the tool-neutral planning orchestration contract, including collaborative and gated profiles, authority order, active-scope rules, and hard human promotion gates.',
      inputSchema: {},
      annotations: planningToolAnnotations,
    },
    async () => {
      const content = await readFile(join(repoRoot, '.agent-orchestration.yaml'), 'utf8');
      return { content: [{ type: 'text', text: content }] };
    },
  );

  return server;
}
