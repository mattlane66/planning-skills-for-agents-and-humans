# Fit Checks Reference

Load this reference when comparing shapes, checking appetite, resolving a failed row, or preparing a decision-ready summary.

## Requirements against shapes

Use one matrix with the full requirement text and binary values.

```md
| Req | Requirement | Status | CURRENT | A | B |
|---|---|---|:---:|:---:|:---:|
| R0 | Person can complete the core job without administrator help | Core goal | ❌ | ✅ | ✅ |
| R1 | Existing audit history remains available | Must-have | ✅ | ✅ | ❌ |
```

Rules:

- use only `✅` or `❌` in shape cells
- unknown is `❌` until resolved or explicitly accepted
- explain failures below the table
- compare against `CURRENT` when an existing system matters
- do not add weights that obscure a must-have failure

If every visible row passes but a shape still feels wrong, look for a missing requirement rather than manipulating the score.

## Reverse fit check

Check whether each mechanism is justified by one or more accepted requirements.

```md
| Shape part | Mechanism | Requirement(s) served | Justified? |
|---|---|---|:---:|
| B1 | Persist draft after each completed section | R1, R3 | ✅ |
| B2 | Add CSV export | — | ❌ |
```

An unjustified part must be:

- removed
- placed below the cut line
- or supported by a newly accepted requirement followed by a rerun of the main fit check

Implementation convenience does not create product scope by itself.

## Appetite fit

Requirement fit does not prove that a shape fits the bet.

```md
| Shape | Fits appetite? | Required cuts | Accepted uncertainty | Spike |
|---|:---:|---|---|---|
| A | ✅ | Defer bulk migration | Moderate operational load | — |
| B | ❌ | Remove custom permissions and historical import | Unknown provider limits | SP1 |
```

Name the actual cut. Avoid vague entries such as `reduce scope`.

When no shape fits:

1. cut mechanisms that do not serve a must-have
2. reduce the shaped boundary
3. change the appetite through a human decision
4. stop the bet

Do not silently expand the budget.

## Component-scoped comparison

When one part contains a real local alternative, run a local matrix instead of inflating the top-level shape list.

```md
### B3: Restoration mechanism

| Req | Requirement | B3-A: URL state | B3-B: server draft |
|---|---|:---:|:---:|
| R2 | State survives refresh | ✅ | ✅ |
| R3 | Shared links restore the same view | ✅ | ❌ |
```

Use a component-scoped comparison only when the choice can be made locally without changing the overall direction.

## Failure handling

When a fit row fails, choose one explicit move:

- improve the shape
- cut the failing mechanism or requirement from this bet through a human decision
- add a focused spike
- reject the shape
- revise a requirement that was incorrectly framed

Never convert an unknown into a pass merely to complete the table.

## Decision-ready summary

Before selection, present:

- which requirements distinguish the candidates
- which shapes fail a must-have
- which shapes exceed appetite
- the meaningful cuts
- unresolved spikes
- the strongest reason to choose each viable shape
- the strongest reason not to choose it

End with an explicit selection gate. Do not select on the user's behalf.
