# Example: A behavioral spike during onboarding shape comparison

**Illustrative planning example only—not a completed simulation or real usability study.** No results below are observed user behavior. Perform actual runs using the separate [Behavioral Simulation skill](https://github.com/mattlane66/behavioral-simulation-for-agents-and-humans/tree/main/behavioral-simulation), including its evidence records and model configuration.

## Candidate uncertainty

Two Working shapes aim to help a novice user complete a first project:

- **A — Guided setup:** users configure the project before seeing the workspace.
- **B — Start immediately:** users see a sample workspace and configure later.

Question: Might setup effort in A or difficulty finding the next action in B prevent someone from reaching their first meaningful outcome?

## Optional focused spike

- **Fixed comparison:** the same task, user goal, device, starting context, baseline, and constraints for both candidates.
- **Quick simulation mode/grade:** PLAUSIBILITY_SPACE / L0_ROLEPLAY. This finds hypotheses; it does not predict real-user adoption or measured usability.
- **Input provenance:** list human observations separately from explicit assumptions. If no observed user data exists, state that.
- **Probe:** explore varied plausible behaviors, misunderstandings, failed starts, and rival mechanisms for each candidate. Do not ask synthetic respondents to vote for a winner.
- **Output type:** SIMULATED_ESTIMATE, tied to run references, model/version/configuration, scenario, and evidence grade.

## Illustrative hypotheses (NOT simulation results)

| Shape | Potential value/usability breakdown | Discriminating real-world observation |
| --- | --- | --- |
| A | Users may see setup as work before value | Observe first meaningful task completion and where real users abandon the setup |
| B | Users may start fast but fail to understand their next action | Observe unprompted first-task completion and confusion points with real users |

An actual simulation might surface different hypotheses or no useful distinction. The illustration cannot populate a ✅ Fit Check.

## Return to shaping

Record candidate-specific hypotheses with source type and limitations. Revise Working mechanisms or mark the unknown for real-world observation using a prototype. Never promote a simulated preference, completion claim, or score into actual value/usability evidence, accepted requirements, Appetite, or human selection.

If the uncertainty would not change a shape or the next test, **skip the spike**.
