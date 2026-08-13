import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import {
  entryStates,
  groceryBreadboardDiagram,
  groceryRequirements,
  groceryShapeDecision,
  groceryShapePaths,
  grocerySlicePlan,
  invocationSurfaces,
  mapStages,
  promotionRules,
  simpleExampleModel,
  skillGroups,
  skillInvocations,
  skillModel,
  walkthroughStageInvocations,
  walkthroughSteps,
} from '../src/planning-model.js';

const readCanonical = (path) => readFile(new URL(`../../${path}`, import.meta.url), 'utf8');
const [
  shapingSource,
  breadboardingSource,
  dumplinkSource,
  kickoffSource,
  contextSource,
  readmeSource,
  invocationMatrix,
  codexPluginGuide,
  claudeSlashGuide,
  exampleShaping,
  exampleBreadboard,
  exampleReflection,
] = await Promise.all([
  readCanonical('shaping/SKILL.md'),
  readCanonical('breadboarding/SKILL.md'),
  readCanonical('dumplink/SKILL.md'),
  readCanonical('kickoff-doc/SKILL.md'),
  readCanonical('feed-planning-context/SKILL.md'),
  readCanonical('README.md'),
  readCanonical('docs/agent-invocation-matrix.md'),
  readCanonical('docs/codex-plugin.md'),
  readCanonical('docs/claude-slash-commands.md'),
  readCanonical('examples/simple-grocery-list/02-shaping.md'),
  readCanonical('examples/simple-grocery-list/03-breadboard.md'),
  readCanonical('examples/simple-grocery-list/05-breadboard-reflection.md'),
]);

assert.match(shapingSource, /Exploration is fluid\. Commitment is gated\./);
assert.match(shapingSource, /A candidate breadboard is subordinate to its named shape\. It cannot select itself, feed slice selection, define build scope/i);
assert.match(breadboardingSource, /Only an accepted selected-design breadboard can feed slice selection/i);
assert.match(dumplinkSource, /project is the discrete unit of work Dumplink ingests/i);
assert.match(kickoffSource, /Start with the accepted frame, selected shape, accepted breadboard, selected slice/i);
assert.match(kickoffSource, /Do not organize by build sequence/i);
assert.match(contextSource, /kickoff document, for orientation only/i);
assert.match(invocationMatrix, /Codex \| Codex plugin plus natural-language prompts \| No Claude-style slash commands/i);
assert.match(codexPluginGuide, /Install from GitHub/i);
assert.match(codexPluginGuide, /invoke the installed skills there/i);
assert.match(claudeSlashGuide, /namespaces entries as `\/planning-skills:<name>`/i);
const controlledPath = readmeSource.match(/A common \*\*controlled\*\* path is:([^\n]+)/i)?.[1] || '';
assert.ok(controlledPath.indexOf('accepted selected-design breadboard') < controlledPath.indexOf('optional Dumplink'));
assert.ok(controlledPath.indexOf('human-selected active task group') < controlledPath.indexOf('optional kickoff reference'));
assert.ok(controlledPath.indexOf('optional kickoff reference') < controlledPath.indexOf('context packet'));

const stageIndex = (id) => mapStages.findIndex((stage) => stage.id === id);
const entry = (id) => entryStates.find((item) => item.id === id);

assert.deepEqual(
  mapStages.map((stage) => stage.id),
  ['explore', 'direction-gate', 'selected-design', 'slice-gate', 'prepare', 'build', 'reflect'],
  'The portal map must preserve the canonical promotion order.',
);
assert.ok(stageIndex('direction-gate') > stageIndex('explore'));
assert.ok(stageIndex('selected-design') > stageIndex('direction-gate'));
assert.ok(stageIndex('slice-gate') > stageIndex('selected-design'));
assert.ok(stageIndex('prepare') > stageIndex('slice-gate'));
assert.ok(stageIndex('reflect') > stageIndex('build'));

assert.equal(entry('candidate').mapStage, 'explore');
assert.match(entry('candidate').caution, /cannot select itself/i);
assert.match(entry('candidate').stop, /return to shaping/i);
assert.equal(entry('selected').mapStage, 'selected-design');
assert.match(entry('selected').needs, /selected shape/i);
assert.match(entry('selected').needs, /accepted requirements/i);
assert.match(entry('selected').needs, /accepted Appetite/i);

assert.deepEqual(
  skillModel.breadboarding.modes.map((mode) => mode.id),
  ['current-state', 'candidate-shape', 'selected-design'],
  'Breadboarding must remain three explicitly different modes.',
);
assert.match(skillModel.breadboarding.modes[0].authority, /evidence only/i);
assert.match(skillModel.breadboarding.modes[1].authority, /exploratory only/i);
assert.match(skillModel.breadboarding.modes[2].authority, /after acceptance/i);
assert.match(skillModel.breadboarding.gate, /only accepted selected-design/i);

assert.deepEqual(
  promotionRules.selectionRequires,
  ['accepted-requirements', 'accepted-appetite', 'decision-ready-evidence', 'human-selection'],
);
assert.ok(promotionRules.sliceRequires.includes('accepted-selected-design'));
assert.ok(promotionRules.sliceRequires.includes('human-selected-slice'));
assert.equal(promotionRules.kickoff.optional, true);
assert.deepEqual(promotionRules.kickoff.after, ['accepted-selected-design', 'human-selected-slice']);
assert.equal(promotionRules.kickoff.authority, 'orientation-only');

const prepareStage = mapStages.find((stage) => stage.id === 'prepare');
assert.deepEqual(prepareStage.optional, ['Kickoff orientation']);
assert.match(prepareStage.never, /does not define scope or sequence/i);
assert.match(skillModel['kickoff-doc'].needs, /accepted breadboard/i);
assert.match(skillModel['kickoff-doc'].needs, /selected slice/i);
assert.match(skillModel['kickoff-doc'].gate, /optional orientation/i);
assert.match(skillModel.dumplink.useWhen, /selected bounded project/i);
assert.match(skillModel.dumplink.gate, /person approves/i);
assert.match(skillModel['feed-planning-context'].gate, /kickoff prose stay out of build scope/i);

assert.ok(!simpleExampleModel.primaryFiles.includes('04-kickoff.md'), 'Kickoff cannot appear in the required example path.');
assert.deepEqual(simpleExampleModel.optionalFiles, ['04-kickoff.md']);
assert.ok(
  simpleExampleModel.primaryFiles.indexOf('03-breadboard.md') < simpleExampleModel.primaryFiles.indexOf('05-breadboard-reflection.md'),
  'Selected-design breadboarding must precede post-implementation reflection.',
);
assert.match(simpleExampleModel.stages['04-kickoff.md'].description, /after the breadboard and V1 selection/i);
assert.match(simpleExampleModel.notes['05-breadboard-reflection.md'].join(' '), /implementation happened between planning and reflection/i);

assert.deepEqual(
  walkthroughSteps.map((step) => step.id),
  ['source', 'frame', 'requirements', 'shape', 'behavior', 'slice', 'handoff', 'reality'],
  'The walkthrough must move from raw evidence to a reality check without putting kickoff in the required path.',
);
assert.deepEqual(
  walkthroughSteps.map((step) => step.artifact.title),
  ['Source notes', 'Accepted frame', 'Requirements + Appetite', 'Selected shape A', 'Accepted breadboard', 'Active slice — V1', 'Context packet', 'Drift decision'],
);
for (const step of walkthroughSteps) {
  assert.ok(step.input.length > 0, `${step.id} must show the input to the stage.`);
  assert.ok(step.exchange.length > 0, `${step.id} must show the human-agent exchange.`);
  assert.ok(step.artifact.title && step.output && step.why && step.sourceFile, `${step.id} must show its output, consequence, and canonical source.`);
  assert.equal(step.options, undefined, `${step.id} must be a predetermined walkthrough stage, not a quiz.`);
}

const walkthrough = (id) => walkthroughSteps.find((step) => step.id === id);
assert.match(exampleShaping, /Human Decision[\s\S]*Recorded human choice: \*\*A\*\*/i);
assert.match(walkthrough('requirements').output, /R0–R5 are accepted/i);
assert.match(walkthrough('requirements').output, /Appetite: a few focused days/i);
assert.deepEqual(groceryRequirements.map((requirement) => requirement.id), ['R0', 'R1', 'R2', 'R3', 'R4', 'R5']);
assert.equal(walkthrough('requirements').visual.type, 'requirements');
assert.deepEqual(walkthrough('requirements').visual.requirements, groceryRequirements);
for (const requirement of groceryRequirements) {
  assert.match(exampleShaping, new RegExp(`\\| ${requirement.id} \\|`, 'i'), `${requirement.id} must come from the canonical shaping matrix.`);
}
assert.match(walkthrough('shape').exchange.find((turn) => turn.role === 'human')?.text || '', /Choose A/i);
assert.match(walkthrough('shape').output, /One items store/i);
assert.match(walkthrough('shape').input.join(' '), /categories[\s\S]*store-specific behavior/i);
assert.deepEqual(groceryShapePaths.map((path) => path.id), ['a', 'b']);
assert.deepEqual(groceryShapePaths.filter((path) => path.selected).map((path) => path.id), ['a']);
assert.match(groceryShapeDecision.gateText, /both A and B meet R0–R5 and fit the Appetite/i);
assert.deepEqual(groceryShapeDecision.comparisons.map((comparison) => comparison.label), ['Mechanism', 'Strength', 'Required cut', 'Unknown before selection']);
assert.deepEqual(groceryShapeDecision.selection.reasons, [
  'It satisfies all current requirements.',
  'It keeps the state model simpler for a first version.',
  'It supports the clearest path to a breadboard and small vertical slices.',
]);
assert.equal(walkthrough('shape').visual.type, 'shape-fit');
assert.deepEqual(walkthrough('shape').visual.paths, groceryShapePaths);
assert.equal(walkthrough('shape').visual.decision, groceryShapeDecision);
assert.match(exampleShaping, /Both shapes fit the requirements/i);
assert.match(exampleShaping, /\| A \| ✅ \| Keep duplicate handling simple and same-device only \| None before selection \|/i);
assert.match(exampleShaping, /\| B \| ✅ \| Avoid section-management features beyond collapse \| None before selection \|/i);
for (const reason of groceryShapeDecision.selection.reasons) assert.ok(exampleShaping.includes(reason), `Shape A rationale must remain canonical: ${reason}`);
assert.match(walkthrough('behavior').input.join(' '), /Human-selected shape A/i);
assert.match(walkthrough('behavior').exchange.find((turn) => turn.role === 'human')?.text || '', /Accept that behavior/i);
assert.equal(walkthrough('behavior').visual.type, 'breadboard');
assert.equal(walkthrough('behavior').visual.diagram, groceryBreadboardDiagram);
for (const id of ['P1', 'P2', 'P3', 'U1', 'U3', 'U4', 'U5', 'N1', 'N2', 'N3', 'N4', 'N5', 'S1', 'S2']) {
  assert.match(exampleBreadboard, new RegExp(`\\b${id}\\b`), `${id} must come from the canonical selected-design breadboard.`);
  assert.match(groceryBreadboardDiagram, new RegExp(`\\b${id}\\b`), `${id} must remain visible in the walkthrough diagram.`);
}
assert.match(exampleBreadboard, /Human slice selection[\s\S]*V1 — Add and persist grocery items/i);
assert.match(walkthrough('slice').exchange.find((turn) => turn.role === 'human')?.text || '', /Select V1/i);
assert.match(walkthrough('slice').output, /add an item, show duplicate feedback, and restore saved items/i);
assert.equal(walkthrough('slice').visual.type, 'slice-plan');
assert.equal(walkthrough('slice').visual.plan, grocerySlicePlan);
assert.match(grocerySlicePlan.note, /full Dumplink artifact is optional/i);
assert.deepEqual(grocerySlicePlan.groups.map((group) => group.id), ['TG1', 'TG2']);
assert.deepEqual(grocerySlicePlan.groups.map((group) => group.slice), ['V1', 'V2']);
assert.deepEqual(grocerySlicePlan.groups.flatMap((group) => group.tasks.map((task) => task.id)), ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']);
assert.deepEqual(grocerySlicePlan.groups.filter((group) => group.selected).map((group) => group.id), ['TG1']);
assert.match(dumplinkSource, /Do not use this when:[\s\S]*one small, obvious implementation slice/i);
assert.match(dumplinkSource, /Treating sequence order as human approval of the active task group/i);
assert.deepEqual(
  walkthrough('handoff').packet.sections.map((section) => section.label),
  ['Build', 'Preserve', 'Do not build yet', 'Verify', 'Return to planning if'],
);
assert.deepEqual(walkthrough('handoff').packet.assembly.inputs.map((input) => input.id), ['planning', 'repository']);
assert.equal(walkthrough('handoff').packet.assembly.result.id, 'complete');
assert.deepEqual(
  walkthrough('handoff').packet.details.map((section) => section.id),
  ['scope-authority', 'preserve', 'repository-context', 'execution-verification'],
);
assert.ok(
  walkthrough('handoff').packet.details.find((section) => section.id === 'repository-context').rows.every((row) => row.status === 'unresolved'),
  'The planning-only example must not invent target-repository instructions, seams, files, or commands.',
);
assert.match(walkthrough('handoff').output, /complete repository context before coding/i);
assert.match(walkthrough('handoff').exchange.find((turn) => turn.role === 'builder')?.text || '', /inspect the target repository/i);
assert.doesNotMatch(walkthrough('handoff').exchange.map((turn) => turn.text).join(' '), /single-store design/i);
assert.match(walkthrough('handoff').packet.sections.find((section) => section.label === 'Return to planning if').items.join(' '), /split across collections/i);
for (const field of ['Task', 'Source artifacts', 'Authority order', 'Do not use as build scope', 'Must preserve', 'Project language and decisions', 'Relevant behavior', 'Execution contract', 'Open questions', 'Verification target']) {
  assert.match(contextSource, new RegExp(`## ${field}`, 'i'), `The handoff model must remain grounded in the canonical ${field} field.`);
}
assert.deepEqual(walkthrough('handoff').exchange.map((turn) => turn.role), ['agent', 'human', 'builder']);
assert.match(exampleReflection, /recorded without changing the accepted breadboard/i);
assert.match(walkthrough('reality').exchange.find((turn) => turn.role === 'human')?.text || '', /Keep reality separate/i);
assert.match(walkthrough('reality').output, /restore one items store/i);

const modeledSkills = new Set(Object.keys(skillModel));
const groupedSkills = skillGroups.flatMap((group) => group.skills);
assert.equal(new Set(groupedSkills).size, groupedSkills.length, 'A skill may appear in only one navigator group.');
assert.deepEqual(new Set(groupedSkills), modeledSkills, 'Every modeled skill must appear in the navigator exactly once.');
assert.deepEqual(new Set(Object.keys(skillInvocations)), modeledSkills, 'Every canonical skill must have one portable invocation.');
assert.match(invocationSurfaces.portable.environments, /Codex/);
assert.match(invocationSurfaces.claude.note, /namespaced/i);
assert.match(invocationSurfaces.gemini.note, /only/i);
for (const [slug, invocation] of Object.entries(skillInvocations)) {
  assert.match(invocation.prompt, new RegExp(slug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'), `${slug} must name itself in its portable prompt.`);
  if (invocation.claude) assert.match(invocation.claude, /^\/planning-skills:/, `${slug} must use the generated Claude Code namespace.`);
  if (invocation.gemini) assert.match(invocation.gemini, /^\//, `${slug} Gemini shortcut must use slash-command syntax.`);
}
assert.equal(skillInvocations['interface-contracts'].claude, null, 'Direct-only skills must not invent Claude wrapper commands.');
assert.equal(skillInvocations['executable-breadboards'].gemini, null, 'Direct-only skills must not invent Gemini wrapper commands.');

assert.deepEqual(
  Object.keys(walkthroughStageInvocations),
  walkthroughSteps.map((step) => step.id),
  'Every walkthrough stage must explain how its move is invoked.',
);
const walkthroughInvocationSkills = new Set(Object.values(walkthroughStageInvocations).flatMap((stage) => [
  stage.primary?.slug,
  ...(stage.moments || []).map((moment) => moment.slug),
]).filter(Boolean));
assert.deepEqual(walkthroughInvocationSkills, modeledSkills, 'The main path plus contextual branches must expose every canonical skill exactly where it could matter.');
assert.match(walkthroughStageInvocations.source.note.text, /router only when/i);
assert.match(walkthroughStageInvocations.slice.note.text, /Invoke Dumplink only/i);
assert.deepEqual(walkthroughStageInvocations.slice.moments.map((moment) => moment.slug), ['dumplink', 'interface-contracts', 'executable-breadboards']);
assert.deepEqual(walkthroughStageInvocations.handoff.moments.map((moment) => moment.slug), ['kickoff-doc']);
assert.match(walkthroughStageInvocations.handoff.moments[0].fit, /Skipped here/i);
assert.equal(entryStates.length, 7);
assert.equal(new Set(entryStates.map((item) => item.id)).size, entryStates.length);

console.log('Canonical planning-model validation passed (modes, promotion gates, invocation coverage, slice authority, kickoff placement, and example story).');
