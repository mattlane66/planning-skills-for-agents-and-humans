from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_claude_skills.py"
SPEC = importlib.util.spec_from_file_location("build_claude_skills", SCRIPT)
assert SPEC and SPEC.loader
packager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packager)


class ClaudeSkillPackagingTests(unittest.TestCase):
    def test_all_packages_build_with_hidden_support_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "packages"
            packages = packager.build_packages(output)

            self.assertEqual(len(packages), 11)
            with zipfile.ZipFile(output / "framing-doc.zip") as archive:
                self.assertIn("framing-doc/.agent-orchestration.yaml", archive.namelist())

    def test_repo_root_is_never_a_valid_output_directory(self) -> None:
        with self.assertRaisesRegex(packager.PackagingError, "unsafe"):
            packager.prepare_output_dir(packager.ROOT, {"framing-doc.zip"})

    def test_unrelated_output_contents_are_preserved_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "packages"
            output.mkdir()
            unrelated = output / "keep-me.txt"
            unrelated.write_text("important\n", encoding="utf-8")

            with self.assertRaisesRegex(packager.PackagingError, "unexpected entries"):
                packager.prepare_output_dir(output, {"framing-doc.zip"})
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "important\n")

    def test_package_named_directory_is_preserved_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "packages"
            nested = output / "framing-doc.zip"
            nested.mkdir(parents=True)

            with self.assertRaisesRegex(packager.PackagingError, "unsafe entry types"):
                packager.prepare_output_dir(output, {"framing-doc.zip"})
            self.assertTrue(nested.is_dir())

    def test_output_symlink_is_preserved_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "packages"
            output.mkdir()
            target = root / "important.txt"
            target.write_text("important\n", encoding="utf-8")
            marker = output / ".claude-skills-output"
            marker.symlink_to(target)

            with self.assertRaisesRegex(packager.PackagingError, "unsafe entry types"):
                packager.prepare_output_dir(output, {"framing-doc.zip"})
            self.assertEqual(target.read_text(encoding="utf-8"), "important\n")

    def test_symlinked_output_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target"
            target.mkdir()
            output = root / "packages"
            output.symlink_to(target, target_is_directory=True)

            with self.assertRaisesRegex(packager.PackagingError, "symlinked"):
                packager.prepare_output_dir(output, {"framing-doc.zip"})
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
