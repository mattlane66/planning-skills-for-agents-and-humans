import assert from 'node:assert/strict';
import test from 'node:test';
import { recommendPlanningWorkflow } from './recommend.js';

test('routes comparison across candidate breadboards to shaping', () => {
  assert.deepEqual(
    recommendPlanningWorkflow('Breadboard Shapes A and B only as needed to compare the alternatives before choosing'),
    ['shaping'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Use behavior maps for each candidate shape and compare their fit'),
    ['shaping'],
  );
});

test('routes one named candidate uncertainty to candidate-shape breadboarding', () => {
  assert.deepEqual(
    recommendPlanningWorkflow('Breadboard Shape A to test whether the checkout handoff is coherent before selection'),
    ['breadboarding'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Use a candidate-shape breadboard to clarify this uncertainty before choosing'),
    ['breadboarding'],
  );
});
