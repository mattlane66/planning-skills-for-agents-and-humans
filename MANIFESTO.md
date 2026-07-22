# The Work Should Get Clearer

A practical manifesto for teams using AI to build useful software.

This repo exists to help teams move from unclear intent to useful shipped work without losing the thread.

Do not go straight from idea to tickets.

Move from real struggle → clear frame → shaped path → visible behavior → working slices → shipped learning.

The work should get clearer at every step.

---

## Values

**Understanding the struggle before accepting the request.**  
A request is often a clue, not the real problem.

**Framing the problem before writing the plan.**  
A team needs to know the trigger, current situation, current approach, current result, desired outcome, evidence, and boundary.

**Mapping the behavior before polishing the screen.**  
Rough flows, sketches, and fit checks reveal how the thing works faster than finished-looking mockups.

**Checking system reality before trusting the idea.**  
The data, code, permissions, edge cases, and legacy constraints are part of the design.

**Building end-to-end slices before handing work across functions.**  
“Backend done” or “design done” is not progress until useful behavior can be observed, tested, and demonstrated through the appropriate surface.

**Using process to support judgment, not replace it.**  
The process exists to help people think, decide, and collaborate.

**Letting reality update the plan.**  
Plans are guesses. Real use teaches the team what the plan could not know.

**Using AI to preserve intent and execute bounded work.**  
AI should help carry context, assist in shaping options, spiking unknowns, and structuring clear demoable slices. It should not invent the strategy.

---

## The operating loop

```text
Observe the current situation
→ Frame
→ Criteria
→ Appetite
→ Candidate shapes
→ Fit Check
→ Select
→ Reconcile visual evidence when needed
→ Breadboard
→ Optional statechart
→ Select an end-to-end slice
→ Add contracts, executable evidence, task grouping, and kickoff reference when needed
→ Feed a compact context packet
→ Build with drift checks
→ Reflect and decide how to resolve drift
→ Launch
→ Learn
```

The loop is not a ceremony.  
It is a way to stop intent from getting lost.

---

## When to use each skill

| Moment | Use |
|---|---|
| Raw notes, transcript, interview, or request need to become a clear problem | [`framing-doc`](./framing-doc/SKILL.md) |
| A framed problem needs criteria, appetite, alternatives, fit checks, and a selected direction | [`shaping`](./shaping/SKILL.md) |
| A visual introduces missing or conflicting evidence | [`sketch-reconciliation`](./sketch-reconciliation/SKILL.md) |
| A selected path needs observable behavior, state, affordances, and wiring | [`breadboarding`](./breadboarding/SKILL.md) |
| A selected stateful scope needs a precise transition model | [`statechart`](./statechart/SKILL.md) |
| A selected slice crosses a meaningful data or system boundary | [`interface-contracts`](./interface-contracts/SKILL.md) |
| A selected slice needs fixtures, examples, edge cases, and acceptance checks | [`executable-breadboards`](./executable-breadboards/SKILL.md) |
| Work inside a selected slice needs vertical task groups, risk-aware sequence, dependencies, or scope cuts | [`dumplink`](./dumplink/SKILL.md) |
| Builders need a durable orientation reference after the selected artifacts have converged | [`kickoff-doc`](./kickoff-doc/SKILL.md) |
| An implementation agent needs the authoritative subset for one selected slice | [`feed-planning-context`](./feed-planning-context/SKILL.md) |
| Implementation reality needs to be compared with accepted intent | [`breadboard-reflection`](./breadboard-reflection/SKILL.md) |

Use these skills when the work changes modes and intent could get lost.

Do not use them to add ceremony.

---

## Principles

### 1. Do not go from idea to tickets.

A request is only a starting point.

Before assigning or prototyping, ask:

- Who is struggling?
- What are they trying to do?
- Why does it matter now?
- Is this worth shaping into real work?

Use `framing-doc` when messy notes, interviews, transcripts, or stakeholder requests need to become a clear problem frame.

---

### 2. Start with the real moment.

Good framing starts with a specific situation.

Ask:

- What was happening?
- What did people try?
- What failed?
- What did they want to be better?

A good frame names:

- the situation
- what people do now
- what happens now
- the better result they want
- what is inside and outside the work
- how much evidence we have

---

### 3. Watch the work before solving it.

When the problem is very unclear, study the real workflow (contextual inquiry).

Write down the steps, workarounds, tool-switching, waiting, rework, and extra effort.

The workaround often points toward a better solution.

---

### 4. Treat doing nothing as evidence.

If people do nothing, it may not mean they do not care.

It may mean every available option feels too costly, risky, confusing, unfamiliar, or hard to start.

---

### 5. Set the appetite before scope grows.

Do not ask only, “How long will this take?”

Ask, “How much time and talent is this problem worth?”

Appetite forces useful tradeoffs before the solution gets too big.

Define the requirements or criteria first. Set the appetite and cut line before comparative shape sketching or selection; preserve premature mechanism ideas in a parking lot until the budget is explicit.

---

### 6. Shape only when the problem is clear.

The team is ready to shape when it can explain:

- the struggle
- the current approach
- the current result
- the desired outcome
- the boundary

If it cannot, the mandate to shape is not wise.

Use `shaping` when the problem is clear enough to compare paths, make tradeoffs, expose risks, and choose a direction.

---

### 7. Shape with the people who know the truth.

Bring in the people who can remove doubt:

- product
- design
- engineering

Also include:

- support
- sales
- data
- operations
- legal
- security
- subject experts

Do not pass hard questions through layers of translation.

---

### 8. Shaping is work, not talk.

A shaping session should change the material.

The team should leave with clearer paths, sketches, system notes, tradeoffs, risks, and cuts.

If nothing changes on the board, it was only a meeting.

---

### 9. A button is never just a button.

A small interface choice can require models, routes, components, permissions, flags, data reads, data writes, performance work, missing infrastructure, or legacy-code changes.

Put that system reality into the shape.

---

### 10. Show behavior before making it beautiful.

Use affordance maps, breadboards, tables, sketches, or quick prototypes.

Show:

- where users go
- what they can do
- how the system responds
- what changes state
- where the flow branches
- what can fail

Do this before polished screens.

Use `breadboarding` when the chosen path needs to become observable behavior, state, affordances, and wiring.

---

### 11. Compare paths before committing.

Do not fall in love with the first idea.

Compare possible paths against:

- the problem frame
- the accepted criteria
- the appetite and cut line
- technical limits
- cost
- risk
- complexity
- user value

Add the project-specific fitness criteria that matter—such as reliability, accessibility, compatibility, customer forces, cost, and effort—without disguising mechanisms as requirements.

---

### 12. Test only the unknowns that block a decision.

When the team cannot answer a hard question, run a focused test (e.g., a spike).

Come back with evidence that resolves or sharpens the decision, not an unbounded report.

---

### 13. Shape a path, not a full spec.

A good shape gives firm boundaries and leaves room for judgment.

It shows where the walls, pipes, and wires probably go.

It does not choose every fixture.

---

### 14. Start with product territory, not tasks.

Before tickets, name the product areas that will change.

Ask:

- Where does the feature appear?
- Where do users enter?
- What changes?
- What can wait?

Then define small end-to-end slices.

Use `kickoff-doc` after the selected artifacts have converged when builders need a durable map of the shaped territory. Treat it as orientation, not as build scope or sequence.

---

### 15. Build small end-to-end slices.

A slice should produce an observable, testable, demonstrable end-to-end result through the appropriate UI, API, CLI, job, event, or other product surface.

Progress means useful behavior works from end to end.

Before asking an AI agent to build, use `feed-planning-context` to give it only the authoritative context for the selected slice:

- the frame
- the selected shape
- the relevant breadboard behavior
- the constraints
- the non-goals
- the current slice
- relevant contracts, executable examples, or Dumplink task group, when present
- the execution contract
- the verification target

---

### 16. Wire first, polish later.

Ugly working software tells the truth.

Prove the flow, data, state, permissions, and edge cases before finishing the surface.

---

### 17. Track uncertainty, not activity.

A task list can lie.

Show:

- what is still unknown
- what is wired
- what can be demoed
- what has been tested
- what is finished enough
- what changed
- what is blocked

---

### 18. Protect the appetite without dismissing good ideas.

New ideas need clear buckets:

- blocker
- fix
- non-blocker
- enhancement
- later bet
- discard

Good ideas are welcome.

They are not automatically part of this version.

---

### 19. Use QA and accessibility to find reality.

Bring QA and accessibility in early enough to change the behavior.

They reveal what the happy path hides:

- missing data
- moved items
- deletion
- replies
- permissions
- mobile issues
- screen reader problems
- odd states
- support confusion

---

### 20. Meet when judgment is needed.

Use live sessions for hard, unclear decisions.

Use longer async time for building.

Do not use meetings to cover for unclear work.

---

### 21. Use cooldown for launch prep, not hidden build work.

Cooldown is for beta testing, staff rollout, cross-platform testing, support prep, launch notes, feedback monitoring, and deciding what not to change.

If the core feature is still being built during cooldown, the scope was too large.

---

### 22. Treat drift as information.

Plans are guesses. Reality teaches.

When the build no longer matches the plan, choose one:

- update the plan
- update the code
- cut scope
- create a new bet

Silent drift is the failure.

Use `breadboard-reflection` to preserve accepted intent and current implementation reality separately, compare them, and prepare an explicit decision: update the code, update the plan, or split/cut the slice. Do not silently rewrite either truth.

---

### 23. Use AI to preserve intent, not invent it.

Humans frame and shape.

Tools help us get unstuck and preserve context.

Agents execute bounded work.

Reality informs proposed artifact updates. A human decision, or an already explicit user instruction, authorizes which truth changes.

Do not give AI a blurry task and call the result strategy.

---

## Go / No-Go Checks

### [Frame](./templates/frame.md) Go

Can we clearly say and answer:

- What is the real struggling moment?
- What do people do now?
- What happens now?
- What better result do they want?
- What will we change, and what will we leave alone?
- Do we have evidence, or only a strong hunch?
- What goes wrong if we do nothing?

### Criteria and Appetite Go

Can we clearly say and answer:

- Which needs and constraints will judge every candidate shape?
- Which are must-haves, nice-to-haves, or explicitly out of scope?
- What fixed time or scope budget does the bet deserve?
- What is the cut line?
- Which unknowns require a spike or revisit?

### [Shape](./templates/shaping.md) Go

Can we clearly say and answer:

- What path did we choose?
- Does this improve an existing feature, get more people to use it, get people to use it more, or support a new workflow?
- Which parts need to be obvious, used often, or available only for rare cases?
- What are the main parts?
- How does the system behave under the interface?
- Where are the risky logic, data, permissions, or dependencies?
- What did we cut?
- What still needs a focused test?
- Why does this fit within the appetite?
- Where do builders still have room to decide?

### Build Go

Can we clearly say and answer:

- Where does the feature start?
- What product areas change?
- What are the end-to-end slices?
- What should work first, second, and third?
- What counts as done enough?
- What is not part of launch?

---

## Anti-Patterns to Refuse

Do not build from blur.  
Do not ask for solutions before understanding the struggle.  
Do not confuse a feature request with a framed opportunity.  
Do not skip shaping because the work sounds simple.  
Do not shape without technical truth.  
Do not shape without subject-matter truth.  
Do not let polished artifacts fake certainty.  
Do not start with tickets.  
Do not split work only by function.  
Do not polish before wiring.  
Do not track activity while uncertainty stays hidden.  
Do not let every good idea into the current version.  
Do not use meetings to cover for unclear work.  
Do not bring QA in only at the end.  
Do not use cooldown as hidden build time.  
Do not let AI invent missing intent.  
Do not let drift run silent.

Treat **silent drift** as failure.

---

## The Human Clause

This is not a machine for controlling people.

It is a way to help people do better work together.

Leave room for judgment.  
Let builders make local decisions.  
Let designers explore.  
Let engineers push back.  
Let QA reveal reality.  
Let subject experts change the frame.  
Let good ideas wait.  
Let imperfect first versions ship when they solve the real problem.

If the process becomes theater, stop.  
If it becomes bureaucracy, cut it down.  
If it removes judgment, loosen it.  
If it hides reality, change it.

The right amount of process is the amount that helps the work get clearer.

No more.

---

Do not go from idea to tickets. Move from real struggle to clear opportunity, from clear opportunity to shaped path, from shaped path to visible behavior, from visible behavior to working slices, and from shipped reality back into learning.

<img width="2172" height="724" alt="Opportunity-Solution_Model" src="https://github.com/user-attachments/assets/543154e4-7640-4627-8263-693257235b02" />
This opportunity-solution system is a high-level boundary-location fit model. It identifies what is required to produce a design (the elements within “The Field”) and defines what a successful design must achieve—namely, outperform the current baseline outcome.
