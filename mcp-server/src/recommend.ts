export const skillNames = [
  'framing-doc',
  'shaping',
  'breadboarding',
  'interface-contracts',
  'executable-breadboards',
  'dumplink',
  'breadboard-reflection',
  'kickoff-doc',
  'feed-planning-context',
] as const;

export type SkillName = (typeof skillNames)[number];

const coreWorkflow: SkillName[] = [
  'framing-doc',
  'shaping',
  'breadboarding',
  'feed-planning-context',
];

function includesAny(value: string, terms: string[]): boolean {
  return terms.some((term) => value.includes(term));
}

function unique(values: SkillName[]): SkillName[] {
  return Array.from(new Set(values));
}

export function recommendPlanningWorkflow(situation: string): SkillName[] {
  const normalized = situation.toLowerCase();

  if (includesAny(normalized, ['planning drift', 'implementation reality', 'compare to implementation', 'reflect on the breadboard'])) {
    return ['breadboard-reflection'];
  }

  const explicitBuildHandoff = includesAny(normalized, [
    'selected slice',
    'context packet',
    'ready for implementation',
    'handoff to an agent',
    'handoff to the agent',
  ]);

  const genericBuildRequest = includesAny(normalized, ['build ', 'implement ', 'coding agent', 'implementation agent']);

  if (genericBuildRequest && !explicitBuildHandoff) {
    return coreWorkflow;
  }

  const recommendations: SkillName[] = [];

  if (includesAny(normalized, ['transcript', 'raw notes', 'messy notes', 'fuzzy request', 'unclear problem', 'problem frame'])) {
    recommendations.push('framing-doc');
  }

  const selectedDirection = includesAny(normalized, ['selected shape', 'chosen shape', 'selected direction', 'chosen direction']);
  if (!selectedDirection && includesAny(normalized, ['criteria', 'requirement', 'compare options', 'alternative', 'shape', 'tradeoff', 'direction'])) {
    recommendations.push('shaping');
  }

  if (selectedDirection || includesAny(normalized, ['breadboard', 'affordance', 'places and stores', 'behavior map', 'wiring'])) {
    recommendations.push('breadboarding');
  }

  if (includesAny(normalized, ['interface contract', 'api contract', 'boundary contract', 'data exchange', 'nullability', 'enum value'])) {
    recommendations.push('interface-contracts');
  }

  if (includesAny(normalized, ['fixture', 'example run', 'expected output', 'edge case', 'acceptance test', 'executable breadboard'])) {
    recommendations.push('executable-breadboards');
  }

  if (includesAny(normalized, ['task group', 'dependency sequence', 'risk state', 'scope cut', 'dumplink'])) {
    recommendations.push('dumplink');
  }

  if (explicitBuildHandoff || includesAny(normalized, ['feed context', 'package context', 'execution contract'])) {
    recommendations.push('feed-planning-context');
  }

  if (includesAny(normalized, ['kickoff transcript', 'kickoff notes', 'builder-facing reference'])) {
    recommendations.push('kickoff-doc');
  }

  return recommendations.length > 0 ? unique(recommendations) : coreWorkflow;
}
