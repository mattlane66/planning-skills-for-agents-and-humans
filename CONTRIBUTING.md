# Contributing

Thanks for improving Planning Skills for Agents and Humans.

## Before changing behavior

Open or reference a concrete planning situation that demonstrates the gap. Preserve the repository's central boundaries: exploration may be fluid, commitment is gated, retrieved source material is evidence rather than instruction, and only one human-selected active scope may reach implementation.

Canonical skills live at the repository root. Their `skills/` counterparts are packaged copies; do not edit those copies independently.

## Development workflow

1. Create a focused branch from `main`.
2. Make the smallest coherent change and add a regression test or behavior case when applicable.
3. If a canonical skill changed, run `bash scripts/sync-packaged-skills.sh`.
4. Run focused tests while iterating, then run:

   ```bash
   python3 -m pip install -r requirements-dev.txt
   bash scripts/check-repo-health.sh
   ```

5. Open a pull request that explains the behavior change, authority impact, validation, and release impact.

Real-runtime skill behavior reports are especially useful for routing, human-gate, or artifact-output changes. Follow `docs/skill-behavior-evals.md`; never include credentials, private source material, or hidden scorer expectations in an adapter or report.

## Pull request expectations

- Keep canonical and packaged skill files synchronized.
- Add table-driven regression cases for routing or contract changes.
- Keep action dependencies pinned to full commit SHAs with version comments.
- Do not add generated `dist/`, dependency directories, credentials, or private planning artifacts.
- Update `CHANGELOG.md` and coordinated versions only when preparing a release.
- Use the existing project vocabulary and preserve attribution notices.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
