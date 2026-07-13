Check planning alignment.

Use the active context packet, selected slice, shaping doc, breadboard, relevant statechart rows, interface contracts, executable breadboard, active Dumplink task group, non-goals, and verification target.

Return only one of:

1. No planning drift found.
2. Planning drift found:
   - Selected artifact says:
   - Current implementation direction is:
   - Risk:
   - Recommended move:

Rules:

- Do not expand scope.
- Do not invent new requirements.
- Do not treat discarded alternatives as selected direction.
- Do not silently change the breadboard, statechart, contract, executable breadboard, Dumplink plan, or context packet.
- Treat the statechart as derived from and subordinate to the accepted breadboard.
- If implementation reality conflicts with the plan, propose a planning update or slice split instead of continuing.
