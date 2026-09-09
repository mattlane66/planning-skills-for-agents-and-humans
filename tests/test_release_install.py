from __future__ import annotations

import hashlib
import importlib.util
import json
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-release-install.py"
SPEC = importlib.util.spec_from_file_location("check_release_install", SCRIPT)
assert SPEC and SPEC.loader
checks = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checks
SPEC.loader.exec_module(checks)


class ReleaseInstallTests(unittest.TestCase):
    def _write_skill(self, path: Path, name: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: Test skill.\n---\n\n# {name}\n", encoding="utf-8")

    def _build_fixture(self, root: Path, assets: Path) -> None:
        skill = "demo"
        (root / "skill-inventory.txt").write_text(f"{skill}\n", encoding="utf-8")
        self._write_skill(root / skill / "SKILL.md", skill)
        self._write_skill(root / "skills" / skill / "SKILL.md", skill)
        (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
        (root / "GEMINI.md").write_text("@./AGENTS.md\n", encoding="utf-8")
        (root / ".agent-orchestration.yaml").write_text("version: 1\n", encoding="utf-8")

        codex_manifest = {
            "name": "demo-plugin",
            "version": "1.2.3",
            "skills": "./skills/",
        }
        (root / ".codex-plugin").mkdir()
        (root / ".codex-plugin" / "plugin.json").write_text(
            json.dumps(codex_manifest), encoding="utf-8"
        )
        marketplace = {
            "plugins": [
                {
                    "name": "demo-plugin",
                    "source": {"source": "local", "path": "./"},
                }
            ]
        }
        (root / ".agents" / "plugins").mkdir(parents=True)
        (root / ".agents" / "plugins" / "marketplace.json").write_text(
            json.dumps(marketplace), encoding="utf-8"
        )
        (root / ".gemini" / "commands").mkdir(parents=True)
        (root / ".gemini" / "commands" / "plan.toml").write_text(
            'description = "Plan"\nprompt = """Use @{demo/SKILL.md} and @{AGENTS.md}."""\n',
            encoding="utf-8",
        )

        assets.mkdir()
        upload = assets / "demo.zip"
        with zipfile.ZipFile(upload, "w") as archive:
            archive.writestr("demo/SKILL.md", "---\nname: demo\ndescription: Test.\n---\n")
            archive.writestr("demo/AGENTS.md", "# Agents\n")
            archive.writestr("demo/.agent-orchestration.yaml", "version: 1\n")
            archive.writestr("demo/LICENSE", "MIT\n")

        plugin = assets / "planning-skills-claude-code-plugin-v1.2.3.zip"
        with zipfile.ZipFile(plugin, "w") as archive:
            archive.writestr(
                "claude-code-plugin/.claude-plugin/plugin.json",
                json.dumps({"version": "1.2.3"}),
            )
            archive.writestr(
                "claude-code-plugin/skills/demo/SKILL.md",
                "---\nname: demo\ndescription: Test.\n---\n",
            )
            archive.writestr("claude-code-plugin/commands/plan.md", "# Plan\n")
            archive.writestr("claude-code-plugin/AGENTS.md", "# Agents\n")
            archive.writestr("claude-code-plugin/.agent-orchestration.yaml", "version: 1\n")

        lines = []
        for path in sorted((upload, plugin), key=lambda item: item.name):
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n")
        (assets / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")

    def test_end_to_end_fixture_exercises_all_four_install_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            assets = Path(temporary) / "assets"
            root.mkdir()
            self._build_fixture(root, assets)

            report = checks.run_checks(
                assets,
                "v1.2.3",
                "a" * 40,
                root,
            )

            self.assertEqual("passed", report["status"])
            self.assertEqual(
                ["claude-upload", "claude-code", "codex", "gemini-cli"],
                [surface["runtime"] for surface in report["surfaces"]],
            )
            self.assertIn("without invoking external model runtimes", report["limitations"][0])

    def test_safe_extract_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "bad.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("../escape.txt", "bad")
            with self.assertRaisesRegex(checks.InstallCheckError, "unsafe archive path"):
                checks.safe_extract(archive, Path(temporary) / "out")

    def test_safe_extract_rejects_symlink_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "bad.zip"
            info = zipfile.ZipInfo("demo/link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr(info, "target")
            with self.assertRaisesRegex(checks.InstallCheckError, "symlink"):
                checks.safe_extract(archive, Path(temporary) / "out")

    def test_checksum_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            assets = Path(temporary)
            (assets / "asset.zip").write_bytes(b"actual")
            (assets / "SHA256SUMS").write_text(
                f"{'0' * 64}  asset.zip\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(checks.InstallCheckError, "checksum mismatch"):
                checks.validate_checksums(assets)

    def test_real_source_install_surfaces_are_discoverable(self) -> None:
        root = Path(__file__).resolve().parents[1]
        skills = checks.load_inventory(root)
        tag = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))[
            "version"
        ]
        codex = checks.validate_codex_source_install(root, f"v{tag}", skills)
        gemini = checks.validate_gemini_source_install(root, skills)
        self.assertEqual(len(skills), codex["skill_count"])
        self.assertEqual(len(skills), gemini["skill_count"])
        self.assertGreater(gemini["command_count"], 0)


if __name__ == "__main__":
    unittest.main()
