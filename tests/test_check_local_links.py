from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-local-links.py"


class LocalLinkTests(unittest.TestCase):
    def test_virtual_environment_markdown_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copied_script = root / "scripts" / SCRIPT.name
            copied_script.parent.mkdir()
            shutil.copyfile(SCRIPT, copied_script)
            (root / "README.md").write_text("# Project\n", encoding="utf-8")

            for directory in (".venv", "venv", "env"):
                third_party = root / directory / "share" / "README.md"
                third_party.parent.mkdir(parents=True)
                third_party.write_text("[missing](not-present.md)\n", encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(copied_script)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("passed across 1 files", completed.stdout)


if __name__ == "__main__":
    unittest.main()
