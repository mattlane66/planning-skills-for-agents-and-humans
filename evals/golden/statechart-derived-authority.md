# Statechart Derived-Authority Contract

A valid Statechart output must:

- use an accepted breadboard and selected scope as input
- preserve source breadboard IDs for states and transitions
- make the transition table the primary behavioral output
- treat Mermaid as a projection of the table
- mark unsupported behavior as inferred or missing
- propose breadboard updates for gaps
- state that the breadboard remains authoritative

It must not invent retries, timeouts, cancellation, hierarchy, parallel regions, or other behavior absent from the accepted breadboard.
