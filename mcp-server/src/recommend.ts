export const skillNames = [
  'framing-doc',
  'shaping',
  'sketch-reconciliation',
  'breadboarding',
  'statechart',
  'interface-contracts',
  'executable-breadboards',
  'dumplink',
  'kickoff-doc',
  'feed-planning-context',
  'breadboard-reflection',
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

function includesAnyUnnegated(value: string, terms: string[]): boolean {
  return terms.some((term) => {
    let index = value.indexOf(term);
    while (index >= 0) {
      const prefix = value.slice(Math.max(0, index - 60), index);
      const negated = /\b(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+to|without)\s+(?:\w+\s+){0,3}$/.test(prefix);
      if (!negated) return true;
      index = value.indexOf(term, index + term.length);
    }
    return false;
  });
}

function unique(values: SkillName[]): SkillName[] {
  return Array.from(new Set(values));
}

function matches(value: string, patterns: RegExp[]): boolean {
  return patterns.some((pattern) => pattern.test(value));
}

export function recommendPlanningWorkflow(situation: string): SkillName[] {
  const normalized = situation.toLowerCase();

  if (includesAny(normalized, ['planning drift', 'implementation reality', 'compare to implementation', 'reflect on the breadboard'])) {
    return ['breadboard-reflection'];
  }

  const explicitVisualReference = includesAny(normalized, [
    'this sketch',
    'this screenshot',
    'this wireframe',
    'this mockup',
    'this whiteboard',
    'attached',
    'dropped',
    'drop this',
    'see this',
    '[image',
    'image #',
  ]);
  const alternativeVisualDesign = includesAny(normalized, ['sketch', 'wireframe', 'mockup', 'image'])
    && includesAny(normalized, [
      'alternative',
      'alternatives',
      'option',
      'options',
      'approach',
      'approaches',
      'direction',
      'directions',
      'before choosing',
    ])
    && !explicitVisualReference;
  const negatedVisualReconciliation = matches(normalized, [
    /\b(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+to)\s+(?:reconcile|compare|incorporate|update|change|clarify|drop|attach|see)\b/,
  ]);
  const visualReconciliationAction = includesAny(normalized, [
    'reconcile',
    'compare',
    'incorporate',
    'missing',
    'update',
    'see this',
    'attached',
    'change',
    'changed',
    'contradict',
    'conflict',
    'differ',
    'different',
    'clarify',
  ]) || matches(normalized, [/\b(?:dropped|dropping)\b/, /\bdrop\b(?!-?down\b)/]);
  const visualReconciliation = !negatedVisualReconciliation
    && !alternativeVisualDesign
    && includesAny(normalized, [
      'sketch',
      'image',
      'screenshot',
      'wireframe',
      'mockup',
      'whiteboard',
      'hand-drawn',
      'attached image',
    ])
    && visualReconciliationAction;
  if (visualReconciliation) {
    return ['sketch-reconciliation'];
  }

  const fitCheckShorthand = includesAny(normalized, ['fit check', 'reverse fit', 'rotate the fit'])
    || matches(normalized, [/\b[ra]\s*(?:x|×)\s*[ra]\b/]);
  const spikeShorthand = matches(normalized, [
    /^(?:(?:please|can you|could you|would you|let's|lets|we should|we need to)\s+){0,2}spike\b(?!\s+(?:in|was|traffic|occurred)\b)/,
  ]);
  const negatedShapeUpdate = matches(normalized, [
    /^(?:(?:please|we|you)\s+)?(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+to)\s+(?:add|update|revise|put)\b/,
  ]);
  const shapeUpdateShorthand = !negatedShapeUpdate && (matches(normalized, [
    /\b(?:add|update|revise)\s+r\d*\b/,
    /\b(?:update|revise)\s+shape\s+[a-z]\d*\b/,
    /\bput\s+.+\s+into\s+shape\s+[a-z]\d*\b/,
  ]) || matches(situation, [
    /\b(?:[Uu]pdate|[Rr]evise)\s+(?:[Ss]hape\s+)?[A-Z]\d*\b/,
    /\b[Pp]ut\s+.+\s+into\s+(?:[Ss]hape\s+)?[A-Z]\d*\b/,
  ]));
  if (alternativeVisualDesign || fitCheckShorthand || spikeShorthand || shapeUpdateShorthand) {
    return ['shaping'];
  }

  const negatedSlicing = matches(normalized, [
    /\b(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+(?:to|for)|not\s+ready\s+to)\s+(?:\w+\s+){0,3}(?:slice|create\s+(?:a\s+)?vertical\s+slices?|break\s+(?:this|it)\s+into\s+slices?|make\s+vertical\s+slices?|vertical\s+slices?)\b/,
    /\bnot\s+to\s+slice\b/,
  ]);
  const sliceShorthand = !negatedSlicing && (
    includesAny(normalized, [
      "let's slice",
      'lets slice',
      'slice it',
      'slice this',
      'slice the breadboard',
      'slice the shape',
      'vertical slices',
    ])
    || matches(normalized, [
      /\bbreak\s+(?:this|it)\s+into\s+(?:vertical\s+)?slices?\b/,
      /\bcreate\s+(?:a\s+)?vertical\s+slices?\b/,
    ])
  );
  if (sliceShorthand) {
    return ['breadboarding'];
  }

  const implementationPlanning = includesAny(normalized, [
    'implementation plan',
    'implementation planning',
    'plan the implementation',
    'plan implementation',
  ]);
  const sliceImplementationPlan = implementationPlanning
    && matches(normalized, [
      /\b(?:first|next|active|selected|current|this)\s+slice\b/,
      /\bslice\s+v?\d+\b/,
      /\bfor\s+(?:the\s+)?v\d+\b/,
    ]);
  if (sliceImplementationPlan) {
    return ['executable-breadboards', 'feed-planning-context'];
  }

  const explicitSliceReference = matches(normalized, [
    /\b(?:first|next|active|selected|current|this)\s+slice\b/,
    /\bslice\s+v?\d+\b/,
  ]);
  const negatedBuildHandoff = matches(normalized, [
    /\b(?:not|isn't|is\s+not)\s+ready\s+for\s+implementation\b/,
    /\b(?:selected|next|first|current|active|this)\s+slice\s+(?:is\s+not|isn't)\s+ready\b/,
    /\b(?:selected|next|first|current|active|this)\s+slice\s+(?:has\s+not|hasn't)\s+been\s+selected\b/,
    /\b(?:do\s+not|don't|dont|without)\s+(?:have\s+)?(?:a\s+)?selected\s+slice\b/,
    /\bno\s+(?:selected\s+)?slice\s+(?:has\s+been|is)\s+selected\b/,
    /\b(?:do\s+not|don't|dont)\s+have\s+(?:a\s+)?context\s+packet\b/,
    /\bwithout\s+(?:a\s+)?context\s+packet\b/,
    /\bno\s+(?:selected\s+slice|context\s+packet)\b/,
    /\bcontext\s+packet\s+(?:does\s+not|doesn't|doesnt)\s+exist\b/,
  ]);
  const explicitBuildHandoff = !negatedBuildHandoff && (explicitSliceReference || includesAny(normalized, [
    'selected slice',
    'context packet',
    'ready for implementation',
    'handoff to an agent',
    'handoff to the agent',
  ]));

  const planningBuildLanguage = includesAny(normalized, ['build sequence', 'build plan', 'build handoff']);
  const genericBuildRequest = (!planningBuildLanguage && matches(normalized, [
    /\b(?:build|implement)\b/,
    /\b(?:create|make)\s+(?:(?:an?|the|this|my)\s+)?(?:\w+\s+){0,3}(?:app|application|dashboard|feature|website|site|service|tool|product|prototype)\b/,
  ]))
    || includesAny(normalized, ['coding agent', 'implementation agent']);

  if (genericBuildRequest && !explicitBuildHandoff) {
    return coreWorkflow;
  }

  const executionVerification = (
    includesAnyUnnegated(normalized, [
      'run the app yourself',
      'run it yourself',
      'test it yourself',
      'test the app yourself',
      'exercise the app yourself',
    ])
    || matches(normalized, [
      /^(?:(?:then|please|also|can you|could you|would you|and then)\s+){0,3}(?:run|test|exercise)\s+(?:the\s+)?app\b/,
      /^(?:(?:then|please|also|can you|could you|would you|and then)\s+){0,3}(?:verify(?:\s+that)?\s+it\s+works|interact\s+with\s+it)\b/,
      /^(?:(?:then|please|also|can you|could you|would you|and then)\s+){0,3}(?:start|open)\s+(?:the\s+)?app\s+and\s+(?:click|interact)\b/,
    ])
  );
  if (executionVerification) {
    return ['feed-planning-context'];
  }

  const recommendations: SkillName[] = [];

  if (includesAny(normalized, ['transcript', 'raw notes', 'messy notes', 'fuzzy request', 'unclear problem', 'problem frame'])) {
    recommendations.push('framing-doc');
  }

  const selectedDirection = includesAny(normalized, ['selected shape', 'chosen shape', 'selected direction', 'chosen direction']);
  const currentStateBreadboard = includesAny(normalized, [
    'current-state breadboard',
    'current state breadboard',
    'map current behavior',
    'map the existing system',
    'existing system behavior',
  ]);
  const acceptedBreadboard = includesAny(normalized, [
    'accepted breadboard',
    'approved breadboard',
    'selected breadboard',
    'from the breadboard',
  ]);
  if (!selectedDirection && includesAny(normalized, ['criteria', 'requirement', 'compare options', 'alternative', 'shape', 'tradeoff', 'direction'])) {
    recommendations.push('shaping');
  }

  if (!acceptedBreadboard && (currentStateBreadboard || selectedDirection || includesAny(normalized, ['breadboard', 'affordance', 'places and stores', 'behavior map', 'wiring']))) {
    recommendations.push('breadboarding');
  }

  const statechartRequested = includesAny(normalized, ['statechart', 'state machine', 'lifecycle', 'retry', 'timeout', 'guard condition']);
  if (statechartRequested && !acceptedBreadboard && !recommendations.includes('breadboarding')) {
    recommendations.push('breadboarding');
  }
  if (statechartRequested) {
    recommendations.push('statechart');
  }

  if (includesAny(normalized, ['interface contract', 'api contract', 'boundary contract', 'data exchange', 'nullability', 'enum value'])) {
    recommendations.push('interface-contracts');
  }

  if (includesAny(normalized, ['fixture', 'example run', 'expected output', 'edge case', 'acceptance test', 'executable breadboard'])) {
    recommendations.push('executable-breadboards');
  }

  const dumplinkRequested = includesAny(normalized, ['task group', 'dependency sequence', 'risk state', 'scope cut', 'dumplink']);
  const preSliceCandidatesOnly = includesAny(normalized, ['candidate groups', 'candidates only', 'pre-slice exploration']);
  const committedDumplinkOutput = includesAny(normalized, ['build sequence', 'agent handoff', 'active task group', 'acceptance plan']);
  if (dumplinkRequested) {
    if (negatedBuildHandoff && committedDumplinkOutput && !preSliceCandidatesOnly) {
      if (!recommendations.includes('breadboarding')) recommendations.push('breadboarding');
    } else {
      recommendations.push('dumplink');
    }
  }

  if ((explicitBuildHandoff && !dumplinkRequested) || includesAny(normalized, ['feed context', 'package context', 'execution contract'])) {
    recommendations.push('feed-planning-context');
  }

  if (includesAny(normalized, ['kickoff transcript', 'kickoff notes', 'builder-facing reference'])) {
    recommendations.push('kickoff-doc');
  }

  return recommendations.length > 0 ? unique(recommendations) : coreWorkflow;
}
