export const skillNames = [
  'planning-router',
  'wayfinding',
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

const defaultNextMove: SkillName[] = ['planning-router'];

export type RecommendationOptions = {
  /** Skills the caller has explicitly ruled out for this recommendation. */
  excludedSkills?: readonly SkillName[];
};

const skillExclusionAliases: Record<SkillName, string[]> = {
  'planning-router': ['planning router', 'planning-router'],
  wayfinding: ['wayfinding', 'wayfinder', 'shared decision map'],
  'framing-doc': ['framing doc', 'framing document', 'framing-doc'],
  shaping: ['shaping', 'shape comparison'],
  'sketch-reconciliation': ['sketch reconciliation', 'reconcile (?:this |the )?(?:sketch|image|screenshot|wireframe|mockup)'],
  breadboarding: ['breadboarding', 'breadboard', 'behavior map'],
  statechart: ['statechart', 'state machine'],
  'interface-contracts': ['interface contract', 'api contract', 'boundary contract', 'interface-contracts'],
  'executable-breadboards': ['executable breadboard', 'executable-breadboards'],
  dumplink: ['dumplink', 'task group', 'task groups'],
  'kickoff-doc': ['kickoff doc', 'kickoff document', 'kickoff-doc'],
  'feed-planning-context': ['feed planning context', 'context packet', 'feed-planning-context'],
  'breadboard-reflection': ['breadboard reflection', 'breadboard-reflection', 'reflect on (?:this |the )?breadboard'],
};

function includesAny(value: string, terms: string[]): boolean {
  return terms.some((term) => value.includes(term));
}

function termIsNegated(value: string, index: number, term: string): boolean {
  const prefix = value.slice(Math.max(0, index - 90), index);
  const suffix = value.slice(index + term.length, index + term.length + 55);
  return matches(prefix, [
    /\b(?:no|without)\s+(?:(?:an?|the|any|accepted|approved|selected|chosen|active|current)\s+){0,4}$/,
    /\b(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+to|avoid|skip|exclude)\s+(?:(?:use|run|invoke|create|make|derive|document|perform|apply|reflect\s+on|route\s+to|have)\s+)?(?:(?:an?|the|this|that|any)\s+){0,2}$/,
  ]) || matches(suffix, [
    /^\s+(?:is|are|was|were|has|have)\s+(?:not|never)\b/,
    /^\s+(?:isn't|aren't|wasn't|weren't|hasn't|haven't|doesn't|doesnt)\b/,
  ]);
}

function includesAnyAffirmed(value: string, terms: string[]): boolean {
  return terms.some((term) => {
    let index = value.indexOf(term);
    while (index >= 0) {
      if (!termIsNegated(value, index, term)) return true;
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

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function explicitSkillExclusions(value: string): Set<SkillName> {
  const exclusions = new Set<SkillName>();
  const lead = String.raw`(?:do\s+not|don't|dont|should\s+not|shouldn't|no\s+need\s+(?:to|for)|avoid|skip|exclude)`;
  const action = String.raw`(?:\s+(?:use|run|invoke|create|make|derive|document|do|perform|apply|route\s+to))?`;

  for (const skill of skillNames) {
    const aliases = skillExclusionAliases[skill]
      .map((alias) => alias.includes('(?:') ? alias : escapeRegExp(alias))
      .join('|');
    const pattern = new RegExp(String.raw`\b${lead}${action}\s+(?:(?:an?|the|this|that)\s+)?(?:${aliases})\b`);
    if (pattern.test(value)) exclusions.add(skill);
  }
  return exclusions;
}

function stripExplicitlyUntrustedQuotedMaterial(value: string): string {
  if (!matches(value.toLowerCase(), [
    /\buntrusted\s+(?:data|input|source|material)\b/,
    /\bdo\s+not\s+follow\s+(?:the\s+)?(?:quoted|embedded|pasted|source)\s+instructions?\b/,
    /\bignore\s+(?:the\s+)?(?:quoted|embedded|pasted|source)\s+instructions?\b/,
  ])) {
    return value;
  }

  return value
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/^\s*>.*$/gm, ' ')
    .replace(/"(?:[^"\\]|\\.)*"/g, ' ')
    .replace(/“[^”]*”/g, ' ')
    .replace(/`[^`]*`/g, ' ');
}

function allowedRoute(route: readonly SkillName[], exclusions: ReadonlySet<SkillName>): SkillName[] {
  return route.filter((skill) => !exclusions.has(skill));
}

function fallbackRoute(exclusions: ReadonlySet<SkillName>): SkillName[] {
  return allowedRoute(defaultNextMove, exclusions);
}

export function recommendPlanningWorkflow(
  situation: string,
  options: RecommendationOptions = {},
): SkillName[] {
  const normalized = stripExplicitlyUntrustedQuotedMaterial(situation).toLowerCase();
  const exclusions = explicitSkillExclusions(normalized);
  for (const skill of options.excludedSkills ?? []) exclusions.add(skill);

  if (includesAnyAffirmed(normalized, ['planning drift', 'implementation reality', 'compare to implementation', 'reflect on the breadboard'])) {
    const route = allowedRoute(['breadboard-reflection'], exclusions);
    if (route.length > 0) return route;
  }

  const activeWayfindingTicket = includesAny(normalized, [
    'active wayfinding ticket:',
    'inside the active wayfinding ticket',
    'route this wayfinding ticket',
  ]);
  const explicitWayfinding = !activeWayfindingTicket && includesAny(normalized, [
    'wayfinding',
    'wayfinder',
    'wayfind this',
    'shared decision map',
    'multi-session planning map',
  ]);
  const multiSessionDecisionRoute = !activeWayfindingTicket
    && includesAny(normalized, [
      'multiple agent sessions',
      'multiple planning sessions',
      'across planning sessions',
      'too large for one planning session',
    ])
    && includesAny(normalized, [
      'dependent decision',
      'dependent decisions',
      'decision dependencies',
      'investigation threads',
      'planning frontier',
    ]);
  if (explicitWayfinding || multiSessionDecisionRoute) {
    const route = allowedRoute(['wayfinding'], exclusions);
    if (route.length > 0) return route;
  }

  const solutionFirstShaping = includesAny(normalized, [
    'solution in my head',
    'solution already in my head',
    'already have a solution',
    'rough solution',
    'proposed solution',
    'start from the solution',
    'start from shape',
    's-first',
  ]) && includesAny(normalized, [
    'requirement',
    'criteria',
    'tease out',
    'extract',
    'shape',
    'refine',
    'fit',
    'capture',
  ]);
  if (solutionFirstShaping) {
    const route = allowedRoute(['shaping'], exclusions);
    if (route.length > 0) return route;
  }

  const multipleCandidateBreadboarding = includesAny(normalized, [
    'alternatives',
    'multiple candidates',
    'candidate shapes',
    'shapes a and b',
    'each shape',
    'each candidate',
  ]) && includesAny(normalized, ['breadboard', 'behavior map']);
  if (multipleCandidateBreadboarding) {
    const route = allowedRoute(['shaping'], exclusions);
    if (route.length > 0) return route;
  }

  const namedCandidateBreadboarding = (
    includesAny(normalized, ['candidate-shape', 'candidate shape', 'candidate breadboard'])
    || matches(normalized, [/\bbreadboard\s+(?:shape\s+)?[a-z]\d*\b/])
  ) && includesAny(normalized, [
    'before selection',
    'before choosing',
    'before any direction is selected',
    'clarify',
    'unclear',
    'judge',
    'coherent',
    'uncertainty',
    'fit implication',
    'test whether',
    'working requirements',
    'appetite is unset',
    'appetite unset',
  ]);
  if (namedCandidateBreadboarding) {
    const route = allowedRoute(['breadboarding'], exclusions);
    if (route.length > 0) return route;
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
    const route = allowedRoute(['sketch-reconciliation'], exclusions);
    if (route.length > 0) return route;
  }

  const optionComparison = matches(normalized, [
    /\bcompare\b[^.;:\n]{0,60}\b(?:options?|alternatives?|shapes?|directions?)\b/,
    /\b(?:options?|alternatives?|shapes?|directions?)\b[^.;:\n]{0,60}\b(?:tradeoffs?|before\s+choosing|before\s+selection)\b/,
  ]);
  if (optionComparison) {
    const route = allowedRoute(['shaping'], exclusions);
    if (route.length > 0) return route;
  }

  const fitCheckShorthand = includesAny(normalized, ['fit check', 'reverse fit', 'rotate the fit', 'working fit'])
    || matches(normalized, [/\b[ra]\s*(?:x|×)\s*[ra]\b/]);
  const spikeShorthand = matches(normalized, [
    /^(?:(?:please|can you|could you|would you|let's|lets|we should|we need to)\s+){0,2}spike\b(?!\s+(?:in|was|traffic|occurred)\b)/,
  ]) || includesAny(normalized, ['focused spike', 'spike this one', 'run a spike']);
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
    const route = allowedRoute(['shaping'], exclusions);
    if (route.length > 0) return route;
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
    const route = allowedRoute(['breadboarding'], exclusions);
    if (route.length > 0) return route;
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
    const route = allowedRoute(['executable-breadboards', 'feed-planning-context'], exclusions);
    if (route.length > 0) return route;
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
    return fallbackRoute(exclusions);
  }

  const executionVerification = (
    includesAnyAffirmed(normalized, [
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
    const route = allowedRoute(['feed-planning-context'], exclusions);
    if (route.length > 0) return route;
  }

  const recommendations: SkillName[] = [];

  if (includesAny(normalized, ['transcript', 'raw notes', 'messy notes', 'fuzzy request', 'unclear problem', 'problem is unclear', 'problem remains unclear', 'problem frame'])) {
    if (!exclusions.has('framing-doc')) recommendations.push('framing-doc');
  }

  const selectedDirection = includesAnyAffirmed(normalized, ['selected shape', 'chosen shape', 'selected direction', 'chosen direction']);
  const currentStateBreadboard = includesAny(normalized, [
    'current-state breadboard',
    'current state breadboard',
    'map current behavior',
    'map the existing system',
    'existing system behavior',
  ]);
  const acceptedBreadboard = includesAnyAffirmed(normalized, [
    'accepted breadboard',
    'approved breadboard',
    'selected breadboard',
    'selected-design breadboard',
  ]);
  if (!selectedDirection && includesAny(normalized, [
    'criteria',
    'requirement',
    'compare options',
    'alternative',
    'shape',
    'tradeoff',
    'option',
    'shaping',
    'direction',
    'solution idea',
    'proposed solution',
    'working fit',
    'appetite',
  ])) {
    if (!exclusions.has('shaping')) recommendations.push('shaping');
  }

  if (!acceptedBreadboard && (currentStateBreadboard || selectedDirection || includesAnyAffirmed(normalized, ['breadboard', 'affordance', 'places and stores', 'behavior map', 'wiring']))) {
    if (!exclusions.has('breadboarding')) recommendations.push('breadboarding');
  }

  const statechartRequested = includesAnyAffirmed(normalized, ['statechart', 'state machine', 'lifecycle', 'retry', 'timeout', 'guard condition']);
  if (statechartRequested && !acceptedBreadboard && !exclusions.has('breadboarding') && !recommendations.includes('breadboarding')) {
    recommendations.push('breadboarding');
  }
  if (statechartRequested && acceptedBreadboard && !exclusions.has('statechart')) {
    recommendations.push('statechart');
  }

  if (!exclusions.has('interface-contracts') && includesAnyAffirmed(normalized, ['interface contract', 'api contract', 'boundary contract', 'data exchange', 'nullability', 'enum value'])) {
    recommendations.push('interface-contracts');
  }

  if (!exclusions.has('executable-breadboards') && includesAnyAffirmed(normalized, ['fixture', 'example run', 'expected output', 'edge case', 'acceptance test', 'executable breadboard'])) {
    recommendations.push('executable-breadboards');
  }

  const dumplinkRequested = includesAny(normalized, ['task group', 'dependency sequence', 'risk state', 'scope cut', 'dumplink']);
  const projectUnavailable = matches(normalized, [
    /\bno\s+(?:selected\s+)?project\b/,
    /\bwithout\s+(?:a\s+)?(?:selected\s+)?project\b/,
    /\bproject\s+(?:has\s+not|hasn't|is\s+not|isn't)\s+(?:been\s+)?(?:selected|bounded)\b/,
    /\bno\s+project\s+boundary\b/,
  ]);
  if (dumplinkRequested) {
    if (projectUnavailable) {
      if (!exclusions.has('shaping') && !recommendations.includes('shaping')) recommendations.push('shaping');
    } else {
      if (!exclusions.has('dumplink')) recommendations.push('dumplink');
    }
  }

  if ((explicitBuildHandoff && !dumplinkRequested) || includesAny(normalized, ['feed context', 'package context', 'execution contract'])) {
    if (!exclusions.has('feed-planning-context')) recommendations.push('feed-planning-context');
  }

  if (includesAny(normalized, ['kickoff transcript', 'kickoff notes', 'builder-facing reference'])) {
    if (!exclusions.has('kickoff-doc')) recommendations.push('kickoff-doc');
  }

  return recommendations.length > 0 ? unique(recommendations) : fallbackRoute(exclusions);
}
