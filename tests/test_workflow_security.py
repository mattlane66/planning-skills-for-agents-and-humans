import pathlib
import re
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
ACTION_PIN = re.compile(r"^\s*uses:\s+[^\s@]+@[0-9a-f]{40}\s+#\s+v\d", re.MULTILINE)
ANY_ACTION = re.compile(r"^\s*uses:\s+", re.MULTILINE)


class WorkflowSecurityTests(unittest.TestCase):
    def test_every_action_is_pinned_to_a_full_sha_with_a_version_comment(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(
                len(ANY_ACTION.findall(text)),
                len(ACTION_PIN.findall(text)),
                path.name,
            )

    def test_workflows_have_least_privilege_and_bounded_jobs(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.yml")):
            payload = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
            self.assertIn("permissions", payload, path.name)
            self.assertEqual("read", payload["permissions"].get("contents"), path.name)
            for job_name, job in payload["jobs"].items():
                self.assertIn("timeout-minutes", job, f"{path.name}:{job_name}")

    def test_checkout_never_persists_credentials(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.yml")):
            payload = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
            for job in payload["jobs"].values():
                for step in job.get("steps", []):
                    if str(step.get("uses", "")).startswith("actions/checkout@"):
                        self.assertEqual(
                            "false",
                            step.get("with", {}).get("persist-credentials"),
                            path.name,
                        )

    def test_release_requires_main_ancestry_health_and_assets(self) -> None:
        text = (WORKFLOWS / "release.yml").read_text(encoding="utf-8")
        for requirement in (
            "git merge-base --is-ancestor",
            "scripts/release.py preflight",
            "scripts/check-repo-health.sh",
            "scripts/release.py assets",
            "sha256sum --check SHA256SUMS",
            "dist/release/*",
        ):
            self.assertIn(requirement, text)
        payload = yaml.load(text, Loader=yaml.BaseLoader)
        self.assertEqual("read", payload["permissions"]["contents"])
        self.assertEqual("write", payload["jobs"]["publish"]["permissions"]["contents"])


if __name__ == "__main__":
    unittest.main()
