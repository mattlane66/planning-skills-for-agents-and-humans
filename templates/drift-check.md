# Drift Check

Use this template during implementation or after implementation when you need to verify that the current work still matches the selected planning artifacts.

Return only one of the two forms below.

## No drift

```text
No planning drift found.
```

## Drift

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## Rules

- Do not implement changes inside a drift check.
- Do not expand scope.
- Do not invent new requirements.
- Do not treat rejected alternatives as active scope.
- Do not silently update planning artifacts.
- If implementation reality conflicts with the plan, recommend a planning update, contract update, executable breadboard update, or slice split before continuing.
