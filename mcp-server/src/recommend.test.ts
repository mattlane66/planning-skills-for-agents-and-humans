import assert from 'node:assert/strict';
import test from 'node:test';
import { recommendPlanningWorkflow } from './recommend.js';

test('routes fuzzy source material to framing', () => {
  assert.deepEqual(recommendPlanningWorkflow('I have a messy transcript and an unclear problem'), ['framing-doc']);
});

test('routes option comparison to shaping', () => {
  assert.deepEqual(recommendPlanningWorkflow('Compare options and tradeoffs before choosing a direction'), ['shaping']);
});

test('routes fit-check shorthand from the shaping conversation', () => {
  assert.deepEqual(recommendPlanningWorkflow('show me R x A'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('can you show me A × R — rotate the fit check'), ['shaping']);
});

test('routes spike and shape-update shorthand to shaping', () => {
  assert.deepEqual(recommendPlanningWorkflow('Please spike A2'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Can you spike the local LLM piece?'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow("Let's update A with Approach 1"), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Add R that date and locale can change independently'), ['shaping']);
  for (const prompt of ['Update A', 'Revise B', 'update A2', 'revise A2', 'put parser into A2']) {
    assert.deepEqual(recommendPlanningWorkflow(prompt), ['shaping']);
  }
  assert.deepEqual(recommendPlanningWorkflow('Put this into a context packet'), ['feed-planning-context']);
  assert.notDeepEqual(recommendPlanningWorkflow('Put these notes into a planning artifact'), ['shaping']);
  assert.notDeepEqual(recommendPlanningWorkflow('Do not update A'), ['shaping']);
  assert.deepEqual(
    recommendPlanningWorkflow('There was a spike in traffic; run it yourself'),
    ['feed-planning-context'],
  );
  assert.deepEqual(recommendPlanningWorkflow('Spike in traffic; run it yourself'), ['feed-planning-context']);
  assert.deepEqual(recommendPlanningWorkflow('We should spike A2'), ['shaping']);
});

test('routes a dropped visual to dedicated sketch reconciliation', () => {
  assert.deepEqual(
    recommendPlanningWorkflow(
      "We're missing something. We should make sure that there's an explicit affordance for the date, so it's always clear what the state is and how it's changing as we interact with natural language in the field. See this sketch. [Image #1]",
    ),
    ['sketch-reconciliation'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Incorporate the attached screenshot without silently changing scope'),
    ['sketch-reconciliation'],
  );
  assert.deepEqual(recommendPlanningWorkflow('Sketch alternative shapes'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Compare sketch approaches before choosing one'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Sketch two alternative approaches and compare them'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Sketch and compare two directions'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Compare wireframe options before choosing one'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('Compare mockup alternatives'), ['shaping']);
  assert.deepEqual(recommendPlanningWorkflow('What does this sketch change?'), ['sketch-reconciliation']);
  assert.deepEqual(recommendPlanningWorkflow('This mockup contradicts the selected shape'), ['sketch-reconciliation']);
  assert.deepEqual(recommendPlanningWorkflow('What is different in this screenshot?'), ['sketch-reconciliation']);
  assert.deepEqual(recommendPlanningWorkflow('See this. [Image #1]'), ['sketch-reconciliation']);
  assert.deepEqual(recommendPlanningWorkflow('See this image'), ['sketch-reconciliation']);
  assert.deepEqual(recommendPlanningWorkflow('Compare Image #1 to Shape A'), ['sketch-reconciliation']);
  assert.notDeepEqual(recommendPlanningWorkflow('The wireframe uses a dropdown'), ['sketch-reconciliation']);
  assert.notDeepEqual(recommendPlanningWorkflow('Add a dropdown to the mockup'), ['sketch-reconciliation']);
  assert.notDeepEqual(recommendPlanningWorkflow('The wireframe uses a drop-down'), ['sketch-reconciliation']);
  assert.notDeepEqual(recommendPlanningWorkflow('Do not reconcile this sketch'), ['sketch-reconciliation']);
});

test('routes a selected direction to breadboarding', () => {
  assert.deepEqual(recommendPlanningWorkflow('We have a selected direction and need a behavior map'), ['breadboarding']);
  assert.deepEqual(recommendPlanningWorkflow("let's breadboard A"), ['breadboarding']);
});

test('routes explicit current-state mapping to descriptive breadboarding', () => {
  assert.deepEqual(
    recommendPlanningWorkflow('Map the existing system behavior from code and tests before proposing changes'),
    ['breadboarding'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Create a current-state breadboard and cite the observed behavior'),
    ['breadboarding'],
  );
});

test('routes conversational slicing shorthand to breadboarding', () => {
  assert.deepEqual(recommendPlanningWorkflow("Let's slice it"), ['breadboarding']);
  assert.deepEqual(recommendPlanningWorkflow('Create vertical slices from this'), ['breadboarding']);
  assert.deepEqual(
    recommendPlanningWorkflow('Do not slice it; make an implementation plan for the first slice'),
    ['executable-breadboards', 'feed-planning-context'],
  );
  assert.deepEqual(recommendPlanningWorkflow('Break this into slices'), ['breadboarding']);
  assert.deepEqual(recommendPlanningWorkflow('Create a vertical slice'), ['breadboarding']);
  for (const prompt of [
    "Don't create vertical slices yet",
    'We should not slice it',
    'No need to slice it',
    "Don't break this into slices",
    "Don't make vertical slices yet",
    'No need for vertical slices',
  ]) {
    assert.notDeepEqual(recommendPlanningWorkflow(prompt), ['breadboarding']);
  }
});

test('routes slice planning and execution verification without restarting the workflow', () => {
  assert.deepEqual(
    recommendPlanningWorkflow(
      "Please make an implementation plan for the first slice. include how you will test it yourself to ensure it's working.",
    ),
    ['executable-breadboards', 'feed-planning-context'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow(
      'Please run the app yourself and interact with it in order to verify that it works. Cover all cases like "add brazil" or "feb 12" or "paris feb 18"',
    ),
    ['feed-planning-context'],
  );
  for (const prompt of [
    'Plan the implementation of the first slice',
    'Implementation plan for the current slice',
    'Implementation plan for this slice',
    'Implementation plan for V1',
    'Implementation plan for V2',
    'Implementation plan for slice V2',
  ]) {
    assert.deepEqual(recommendPlanningWorkflow(prompt), ['executable-breadboards', 'feed-planning-context']);
  }
  for (const prompt of [
    'Run it yourself',
    'Test the app yourself',
    'Verify it works',
    'Start the app and click through it',
  ]) {
    assert.deepEqual(recommendPlanningWorkflow(prompt), ['feed-planning-context']);
  }
  assert.deepEqual(
    recommendPlanningWorkflow('Update a context packet, then run the app yourself'),
    ['feed-planning-context'],
  );
  assert.notDeepEqual(recommendPlanningWorkflow('Do not run it yourself'), ['feed-planning-context']);
  assert.notDeepEqual(recommendPlanningWorkflow('Users should interact with it'), ['feed-planning-context']);
  assert.deepEqual(
    recommendPlanningWorkflow('Do not click anything; run the app yourself'),
    ['feed-planning-context'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('Add an acceptance test to verify it works'),
    ['executable-breadboards'],
  );
  const core = ['framing-doc', 'shaping', 'breadboarding', 'feed-planning-context'];
  assert.deepEqual(recommendPlanningWorkflow('Build me an onboarding dashboard and run the app yourself'), core);
  assert.deepEqual(recommendPlanningWorkflow('Implement user authentication and verify it works'), core);
  assert.deepEqual(recommendPlanningWorkflow('Build this feature, test the app yourself'), core);
  assert.deepEqual(
    recommendPlanningWorkflow('Implement the selected slice and run it yourself'),
    ['feed-planning-context'],
  );
  assert.deepEqual(recommendPlanningWorkflow('Then open the app and click through it'), ['feed-planning-context']);
  assert.deepEqual(recommendPlanningWorkflow('Please also verify it works'), ['feed-planning-context']);
  for (const prompt of [
    'The selected slice is not ready for implementation',
    'We do not have a selected slice; implement it',
    'No context packet exists; build it',
    'The next slice has not been selected; build it',
    "We don't have a context packet; build it",
    'Without a context packet, implement it',
    "The selected slice isn't ready; implement it",
  ]) {
    assert.deepEqual(recommendPlanningWorkflow(prompt), core);
  }
  assert.deepEqual(recommendPlanningWorkflow('Create an onboarding dashboard and run it yourself'), core);
  assert.deepEqual(recommendPlanningWorkflow('Make the app and test it yourself'), core);
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
  assert.deepEqual(
    recommendPlanningWorkflow('Inside the selected slice, use Dumplink to create task groups, risk states, and scope cuts'),
    ['dumplink'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('No selected slice exists. Use Dumplink pre-slice exploration for candidate groups only'),
    ['dumplink'],
  );
  assert.deepEqual(
    recommendPlanningWorkflow('The selected shape is accepted but no slice is selected. Create a Dumplink build sequence and agent handoff'),
    ['breadboarding'],
  );
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
