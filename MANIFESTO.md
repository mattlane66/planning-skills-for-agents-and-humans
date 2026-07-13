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
A team needs to know the situation, the current approach, the desired outcome, the boundary, and the [appetite](https://world.hey.com/jason/appetites-instead-of-estimates-192d39ba).

**Mapping the behavior before polishing the screen.**  
Rough flows, sketches, and fit checks reveal how the thing works faster than finished-looking mockups.

**Checking system reality before trusting the idea.**  
The data, code, permissions, edge cases, and legacy constraints are part of the design.

**Building end-to-end slices before handing work across functions.**  
“Backend done” or “design done” is not progress until useful behavior can be clicked, tested, and shown.

**Using process to support judgment, not replace it.**  
The process exists to help people think, decide, and collaborate.

**Letting reality update the plan.**  
Plans are guesses. Real use teaches the team what the plan could not know.

**Using AI to preserve intent and execute bounded work.**  
AI should help carry context, assist in shaping options, spiking unknowns, and structuring clear demoable slices. It should not invent the strategy.

---

## The operating loop

```text
Candidate
→ Trace
→ Frame
→ Appetite
→ Shape
→ Fit Check
→ Behavior Map
→ Starting Points
→ Kickoff
→ End-to-End Slices
→ Wire
→ Polish
→ Cooldown
→ Launch
→ Learn
```

The loop is not a ceremony.  
It is a way to stop intent from getting lost.

---

## When to use each skill

| Moment | Use |
|---|---|
| Raw notes, transcript, interview, or request need to become a clear problem | `/framing-doc` |
| A framed problem needs paths, tradeoffs, risks, and a selected direction | `/shaping` |
| A selected path needs visible behavior, state, affordances, and wiring | `/breadboarding` |
| A selected stateful scope needs a precise transition model | `/statechart` |
| A selected slice crosses a meaningful data or system boundary | `/interface-contracts` |
| A selected slice needs fixtures, examples, edge cases, and acceptance checks | `/executable-breadboards` |
| Selected work needs vertical task groups, risk-aware sequence, dependencies, or scope cuts | `/dumplink` |
| The build team needs a shared reference before creating tasks | `/kickoff-doc` |
| An AI agent needs bounded context to vertically slice | `/feed-planning-context` |
| The implementation has drifted from the plan | `/breadboard-reflection` |

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

Use `/framing-doc` when messy notes, interviews, transcripts, or stakeholder requests need to become a clear problem frame.

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
- how much time the problem is worth
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

---

### 6. Shape only when the problem is clear.

The team is ready to shape when it can explain:

- the struggle
- the current approach
- the current result
- the desired outcome
- the boundary

If it cannot, the mandate to shape is not wise.

Use `/shaping` when the problem is clear enough to compare paths, make tradeoffs, expose risks, and choose a direction.

---

### 7. Shape with the people who know the truth.

Bring in the people who can remove doubt:

- product
- design
- engineering
But also:
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

Use affordance map diagrams (UI breadboards), tables, sketches, or quick prototypes.

Show:

- where users go
- what they can do
- how the system responds
- what changes state
- where the flow branches
- what can fail

Do this before polished screens.

Use `/breadboarding` when the chosen path needs to become visible behavior, state, affordances, and wiring.

---

### 11. Compare paths before committing.

Do not fall in love with the first idea.

Compare possible paths against:

- the problem frame
- inside an appetite
- technical limits
- cost
- risk
- complexity
- user value

...and other specific requirements/criteria (fitness for solving the problem, i.e., standards or rules used to judge the quality of a solution, e.g., various '-ilities', customer forces, costs (time, dev effort, $), risks, compatibility and complexity, purpose-built for problem (reflective), etc.).

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

Use `/kickoff-doc` when the build team needs a shared reference before creating tasks.

---

### 15. Build small end-to-end slices.

A slice should be wired, clicked, tested, and shown.

Progress means useful behavior works from end to end.

Before asking an AI agent to build, use `/feed-planning-context` to give it:

- the frame
- the selected shape
- the relevant behavior map
- the constraints
- the non-goals
- the current slice
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

Use `/breadboard-reflection` when implementation reality disagrees with the plan and the team needs to repair the mismatch.

---

### 23. Use AI to preserve intent, not invent it.

Humans frame and shape.

Tools help us get unstuck and preserve context.

Agents execute bounded work.

Reality updates the artifacts, ideally via agents.

Do not give AI a blurry task and call the result strategy.

---

## Go / No-Go Checks

### [Frame](https://docs.google.com/document/d/1FW840A7WSbQr4ijk7zY4zvIY_-uXoyZbEdTJZXDX54o/edit?usp=sharing) Go

Can we clearly say and answer:

- What is the real struggling moment?
- What do people do now?
- What happens now?
- What better result do they want?
- What will we change, and what will we leave alone?
- How much time will we spend?
- Do we have evidence, or only a strong hunch?
- What goes wrong if we do nothing?

### [Shape](https://docs.google.com/document/d/1Yncw-DhizyI24B8A2xkNF8Z0OllKy3MufqHH4DcjNRw/edit?usp=sharing) Go

Can we clearly say and answer:

- What path did we choose?
- Does this improve an existing feature, get more people to use it, get people to use it more, or support a new workflow?
- Does this need be (or what needs to be) 1.) Obvious, 2. Used often, 3. Rarely used 
- What are the main parts?
- How does the system behave under the interface?
- Where are the risky logic, data, permissions, or dependencies?
- What did we cut?
- What still needs a focused test?
- Why does this fit up to the appetite?
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
