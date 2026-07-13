import assert from 'node:assert/strict';
import test from 'node:test';
import { recommendPlanningWorkflow } from './recommend.js';

test('routes fuzzy source material to framing', () => {
  assert.deepEqual(recommendPlanningWorkflow('I have a messy transcript and an unclear problem'), ['framing-doc']);
});

test('routes option comparison to shaping', () => {
  assert.deepEqual(recommendPlanningWorkflow('Compare options and tradeoffs before choosing a direction'), ['shaping']);
});

test('routes a selected direction to breadboarding', () => {
  assert.deepEqual(recommendPlanningWorkflow('We have a selected direction and need a behavior map'), ['breadboarding']);
});

test('does not treat an unshaped build request as ready for context feeding', () => {
  assert.deepEqual(recommendPlanningWorkflow('Build me an onboarding dashboard'), [
    'framing-doc',
    'shaping',
    'breadboarding',
    'feed-planning-context',
  ]);
});

test('routes a selected slice to context feeding', () => {
  assert.deepEqual(recommendPlanningWorkflow('The selected slice is ready for implementation'), ['feed-planning-context']);
});

test('uses Dumplink only when task grouping signals are present', () => {
  assert.deepEqual(recommendPlanningWorkflow('Create vertical task groups with dependency sequence and scope cuts'), ['dumplink']);
  assert.equal(recommendPlanningWorkflow('What should I do next?').includes('dumplink'), false);
});

test('uses Statechart only when state-complexity signals are present', () => {
  assert.deepEqual(
    recommendPlanningWorkflow('Derive a statechart from the accepted breadboard for retries and timeouts'),
    ['statechart'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Use the approved breadboard to document lifecycle guard conditions'),
    ['statechart'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('We need a state machine for retries and lifecycle transitions'),
    ['breadboarding', 'statechart'],
  );
  assert.equal(recommendPlanningWorkflow('What should I do next?').includes('statechart'), false);
});

test('routes implementation drift to reflection', () => {
  assert.deepEqual(recommendPlanningWorkflow('Compare the breadboard to implementation reality'), ['breadboard-reflection']);
});
