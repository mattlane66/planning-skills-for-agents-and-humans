# CI health workflow

Add this file as `.github/workflows/repo-health.yml` to run repo health checks on pull requests and pushes to `main`.

```yaml
name: Repo health

on:
  pull_request:
  push:
    branches: [main]

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Check repo health
        run: bash scripts/check-repo-health.sh
```

The health script checks:

- skill frontmatter
- packaged skill parity
- Claude command wrappers
- Gemini command wrappers
- templates
- key docs
- hooks
- golden eval fixtures
- execution-contract parity
- Dumplink discovery parity
