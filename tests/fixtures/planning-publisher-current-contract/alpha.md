---
planning: true
shaping: true
artifact_type: frame
status: accepted
source_of_truth: true
---

# Checkout Assist — Frame

## Source
> Staff re-enter the same order details across two tools.

## Current situation
- Trigger or context: a customer is ready to check out.
- Current approach, workaround, or nonconsumption: staff copy details between tools.
- Current result: checkout is slow and error-prone.
- Struggle or compromise: staff re-check values before submitting.
- Evidence and confidence: observed workflow.

## Transformation frame (x → f() → y)
- x — trigger/context: customer is ready to check out
- x — current approach: copy order details
- x — current result / breakdown: slow, error-prone checkout caused by repeated re-entry
- f() — solution / shape variable: intentionally unspecified
- y — desired outcome: one clear checkout flow
- Gap between x and y: remove repeated handling
- Boundaries that constrain a valid transformation: no account migration

## Operating model (M, optional)
- Authority: Accepted
- Relevant operating conditions: checkout submits into an existing downstream system that remains outside this bet
- Causal assumptions / projected dynamics: invalid totals are rejected downstream and require correction before successful completion
- Evidence refs / confidence: observed workflow; high confidence for the current checkout path
- Revisit conditions: downstream validation or submission behavior changes

## Problem
- Re-entering order details makes checkout slow and increases mistakes.

## Outcome
- Staff can complete checkout from one clear flow and see confirmation immediately.

## Boundaries

### Less about
- replacing the account system
- redesigning inventory

### More about
- one clear checkout path
- visible completion state
