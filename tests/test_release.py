from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "release.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("release", SCRIPT)
assert SPEC and SPEC.loader
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def test_extract_release_notes_matches_an_exact_tag_section(self) -> None:
        changelog = """# Changelog

## v1.3.10 — Later

- Wrong section.

## v1.3.1 — Exact

- Exact notes.

## v1.3.0 — Earlier

- Earlier notes.
"""
        self.assertEqual("- Exact notes.\n", release.extract_release_notes(changelog, "v1.3.1"))

    def test_extract_release_notes_rejects_non_semver_and_duplicate_sections(self) -> None:
        with self.assertRaisesRegex(release.ReleaseError, "stable SemVer"):
            release.extract_release_notes("# Changelog\n", "v1.3")
        with self.assertRaisesRegex(release.ReleaseError, "exactly one"):
            release.extract_release_notes("## v1.3.1\nA\n## v1.3.1 — duplicate\nB\n", "v1.3.1")

    def test_validate_release_requires_coordinated_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in release.VERSION_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                payload = {"version": "1.3.1"}
                if relative.name == "package-lock.json":
                    payload["packages"] = {"": {"version": "1.3.1"}}
                path.write_text(json.dumps(payload), encoding="utf-8")
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## v1.3.1 — Patch\n\n- Fixed routing.\n",
                encoding="utf-8",
            )
            self.assertEqual("- Fixed routing.\n", release.validate_release("v1.3.1", root))

            (root / release.VERSION_FILES[0]).write_text(
                json.dumps({"version": "1.3.0"}), encoding="utf-8"
            )
            with self.assertRaisesRegex(release.ReleaseError, "does not match"):
                release.validate_release("v1.3.1", root)

    def test_release_output_cleanup_rejects_unrelated_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "release"
            output.mkdir()
            important = output / "keep-me.txt"
            important.write_text("important\n", encoding="utf-8")
            with self.assertRaisesRegex(release.ReleaseError, "unexpected entries"):
                release.prepare_release_dir(output, {"expected.zip"})
            self.assertEqual("important\n", important.read_text(encoding="utf-8"))

    def test_release_output_cleanup_accepts_a_stale_generated_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "release"
            output.mkdir()
            stale = output / "planning-skills-claude-code-plugin-v1.2.3.zip"
            stale.write_bytes(b"stale")
            release.prepare_release_dir(output, {"planning-skills-claude-code-plugin-v1.3.1.zip"})
            self.assertEqual([], list(output.iterdir()))


if __name__ == "__main__":
    unittest.main()
