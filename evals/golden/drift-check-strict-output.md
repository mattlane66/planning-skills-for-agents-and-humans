# Golden eval: drift check strict output

## Input

An implementation appears to add behavior outside the selected slice.

## Expected qualities

A good drift check returns only one of these forms:

```text
No planning drift found.
```

or

```text
Planning drift found:
- Selected artifact says:
- Current implementation direction is:
- Risk:
- Recommended move:
```

## Failure examples

Fail if the drift check:

- implements changes
- invents new requirements
- expands scope
- gives a broad code review
- buries the drift finding in a long explanation
