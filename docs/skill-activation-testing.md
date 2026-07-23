# Skill activation testing

`evals/skill-activation-cases.json` is the shared routing corpus for Claude, Codex, Gemini, Claude Design, and MCP clients.

Each skill has positive requests that should activate it and negative requests that distinguish it from adjacent skills. The automated tests validate inventory coverage and fixture quality. Runtime evaluations should additionally confirm that the actual client:

1. selects the intended skill for every positive case;
2. does not select it for its negative cases;
3. stops at the documented human gate;
4. produces the expected artifact type;
5. does not continue into implementation unless explicitly requested.

Use the same corpus after changing a skill description, renaming a skill, or changing plugin discovery metadata. Record runtime/version and failures rather than treating one client result as universal.
