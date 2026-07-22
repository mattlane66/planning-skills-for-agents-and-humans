#!/usr/bin/env python3
"""Build self-contained Claude upload ZIPs from the canonical skill folders."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "skill-inventory.txt"
DESCRIPTIONS = ROOT / "claude-skill-descriptions.tsv"
SUPPORT_DIRS = ("docs", "templates", "hooks")
SUPPORT_FILES = (
    "AGENTS.md",
    ".agent-orchestration.yaml",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "skill-inventory.txt",
)
ACTION_WORDS = re.compile(
    r"\b(create|produce|map|shape|compare|reconcile|model|define|plan|prepare|feed|inspect|reflect|turn|derive)\b",
    re.IGNORECASE,
)
CONTEXT_WORDS = re.compile(
    r"\b(when|for|from|into|before|after|needs?|selected|existing|implementation|handoff|notes?|transcripts?|requests?|slice|system|code)\b",
    re.IGNORECASE,
)
LOCAL_PATH = re.compile(
    r"(?:AGENTS\.md|\.agent-orchestration\.yaml|(?:docs|templates|hooks)/[A-Za-z0-9._/-]+)"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class PackagingError(RuntimeError):
    """Raised when canonical metadata or a generated package is invalid."""


def load_inventory() -> list[str]:
    if not INVENTORY.is_file():
        raise PackagingError("missing skill-inventory.txt")
    skills = [line.strip() for line in INVENTORY.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(skills) != len(set(skills)):
        raise PackagingError("skill-inventory.txt contains duplicate skill names")
    return skills


def load_descriptions() -> dict[str, str]:
    if not DESCRIPTIONS.is_file():
        raise PackagingError("missing claude-skill-descriptions.tsv")
    descriptions: dict[str, str] = {}
    for line_number, line in enumerate(DESCRIPTIONS.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            raise PackagingError(f"description line {line_number} must contain exactly one tab")
        skill, description = (part.strip() for part in parts)
        if not skill or not description:
            raise PackagingError(f"description line {line_number} has an empty field")
        if skill in descriptions:
            raise PackagingError(f"duplicate Claude description for {skill}")
        descriptions[skill] = description
    return descriptions


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackagingError(f"missing opening frontmatter marker: {path}")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise PackagingError(f"missing closing frontmatter marker: {path}") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        if ":" not in line:
            raise PackagingError(f"invalid frontmatter line in {path}: {line!r}")
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = json.loads(value)
        fields[key.strip()] = value
    return fields, lines


def validate_metadata(skills: list[str], descriptions: dict[str, str]) -> None:
    if set(descriptions) != set(skills):
        missing = sorted(set(skills) - set(descriptions))
        extra = sorted(set(descriptions) - set(skills))
        raise PackagingError(f"Claude description inventory mismatch; missing={missing}, extra={extra}")
    for skill in skills:
        source = ROOT / skill / "SKILL.md"
        if not source.is_file():
            raise PackagingError(f"missing canonical skill: {skill}/SKILL.md")
        fields, _ = parse_frontmatter(source)
        if fields.get("name") != skill:
            raise PackagingError(f"{skill} frontmatter name must match its folder")
        description = descriptions[skill]
        if len(description) > 200:
            raise PackagingError(f"{skill} Claude description exceeds 200 characters")
        if not ACTION_WORDS.search(description):
            raise PackagingError(f"{skill} description does not clearly state what the skill does")
        if not CONTEXT_WORDS.search(description):
            raise PackagingError(f"{skill} description does not signal when to use it")


def rewrite_upload_file(path: Path, description: str | None, skills: list[str]) -> None:
    fields, lines = parse_frontmatter(path) if description is not None else ({}, path.read_text(encoding="utf-8").splitlines())
    if description is not None:
        in_frontmatter = False
        replaced = False
        for index, line in enumerate(lines):
            if line == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                break
            if in_frontmatter and line.startswith("description:"):
                lines[index] = f"description: {json.dumps(description, ensure_ascii=False)}"
                replaced = True
                break
        if not replaced:
            raise PackagingError(f"no frontmatter description found in {path}")
    text = "\n".join(lines) + "\n"
    for skill in skills:
        text = text.replace(f"`{skill}/SKILL.md`", f"the `{skill}` skill")
        text = text.replace(f"{skill}/SKILL.md", f"the {skill} skill")
    if "${CLAUDE_PLUGIN_ROOT}" in text:
        raise PackagingError(f"Claude Code-only path remains in {path}")
    path.write_text(text, encoding="utf-8")


def copy_support(package_root: Path) -> None:
    for directory in SUPPORT_DIRS:
        source = ROOT / directory
        if source.is_dir():
            shutil.copytree(source, package_root / directory)
    for filename in SUPPORT_FILES:
        source = ROOT / filename
        if source.is_file():
            shutil.copy2(source, package_root / filename)


def prepare_output_dir(output_dir: Path, expected_packages: set[str]) -> Path:
    """Prepare a package directory without recursively deleting arbitrary paths."""
    requested_output = output_dir.expanduser()
    if requested_output.is_symlink():
        raise PackagingError(f"refusing symlinked Claude package output directory: {requested_output}")
    output_dir = requested_output.resolve()
    protected = {ROOT, Path.cwd().resolve(), Path.home().resolve(), *ROOT.parents}
    if output_dir in protected:
        raise PackagingError(f"refusing unsafe Claude package output directory: {output_dir}")

    if output_dir.exists() and not output_dir.is_dir():
        raise PackagingError(f"Claude package output is not a directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    allowed_entries = expected_packages | {".claude-skills-output"}
    unexpected = sorted(path.name for path in output_dir.iterdir() if path.name not in allowed_entries)
    if unexpected:
        raise PackagingError(
            f"refusing to clean non-package output directory {output_dir}; unexpected entries={unexpected}"
        )

    invalid_types = sorted(
        path.name for path in output_dir.iterdir() if path.is_symlink() or not path.is_file()
    )
    if invalid_types:
        raise PackagingError(
            f"refusing to clean Claude package output with unsafe entry types: {invalid_types}"
        )

    for package in output_dir.glob("*.zip"):
        package.unlink()
    (output_dir / ".claude-skills-output").write_text(
        "Generated by scripts/build_claude_skills.py.\n",
        encoding="utf-8",
    )
    return output_dir


def build_packages(output_dir: Path) -> list[Path]:
    skills = load_inventory()
    descriptions = load_descriptions()
    validate_metadata(skills, descriptions)
    output_dir = prepare_output_dir(output_dir, {f"{skill}.zip" for skill in skills})
    packages: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="claude-skills-") as temporary:
        stage = Path(temporary)
        for skill in skills:
            package_root = stage / skill
            shutil.copytree(ROOT / skill, package_root)
            copy_support(package_root)
            rewrite_upload_file(package_root / "SKILL.md", descriptions[skill], skills)
            agents = package_root / "AGENTS.md"
            if agents.is_file():
                rewrite_upload_file(agents, None, skills)
            package = output_dir / f"{skill}.zip"
            with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(package_root.rglob("*")):
                    if path.is_file() and not any(part in {".git", "__pycache__"} for part in path.parts):
                        archive.write(path, path.relative_to(stage))
            packages.append(package)
    validate_packages(output_dir, skills, descriptions)
    return packages


def _path_exists(names: set[str], candidate: str) -> bool:
    candidate = candidate.rstrip(".,;:")
    return candidate in names or any(name.startswith(candidate.rstrip("/") + "/") for name in names)


def validate_packages(output_dir: Path, skills: list[str] | None = None, descriptions: dict[str, str] | None = None) -> None:
    skills = skills or load_inventory()
    descriptions = descriptions or load_descriptions()
    expected = {f"{skill}.zip" for skill in skills}
    found = {path.name for path in output_dir.glob("*.zip")}
    if found != expected:
        raise PackagingError(f"Claude ZIP inventory mismatch; missing={sorted(expected-found)}, extra={sorted(found-expected)}")
    for skill in skills:
        package = output_dir / f"{skill}.zip"
        with zipfile.ZipFile(package) as archive:
            names = set(archive.namelist())
            if not names or any(not name.startswith(f"{skill}/") for name in names):
                raise PackagingError(f"{package.name} must contain only the {skill}/ root folder")
            skill_path = f"{skill}/SKILL.md"
            if skill_path not in names:
                raise PackagingError(f"{package.name} is missing {skill_path}")
            text = archive.read(skill_path).decode("utf-8")
            with tempfile.TemporaryDirectory() as temporary:
                extracted = Path(temporary) / "SKILL.md"
                extracted.write_text(text, encoding="utf-8")
                fields, _ = parse_frontmatter(extracted)
            if fields.get("name") != skill:
                raise PackagingError(f"{package.name} has the wrong skill name")
            if fields.get("description") != descriptions[skill]:
                raise PackagingError(f"{package.name} does not contain the optimized description")
            if "${CLAUDE_PLUGIN_ROOT}" in text:
                raise PackagingError(f"{package.name} contains a Claude Code-only path")
            if re.search(r"[A-Za-z0-9-]+/SKILL\.md", text):
                raise PackagingError(f"{package.name} explicitly references another skill file")
            documents = [text]
            agents_path = f"{skill}/AGENTS.md"
            if agents_path in names:
                documents.append(archive.read(agents_path).decode("utf-8"))
            for document in documents:
                candidates = set(LOCAL_PATH.findall(document))
                for link in MARKDOWN_LINK.findall(document):
                    link = link.split("#", 1)[0].strip()
                    if link and not re.match(r"(?:https?:|mailto:|#)", link):
                        candidates.add(link)
                for candidate in candidates:
                    normalized = candidate.removeprefix("./")
                    if not _path_exists(names, f"{skill}/{normalized}"):
                        raise PackagingError(f"{package.name} references missing file: {candidate}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=ROOT / "dist" / "claude-skills")
    parser.add_argument("--check", action="store_true", help="validate existing packages without rebuilding")
    args = parser.parse_args()
    output = args.output.expanduser()
    if args.check:
        validate_metadata(load_inventory(), load_descriptions())
        validate_packages(output)
        print(f"Validated uploadable Claude skill ZIPs in {output.resolve()}")
    else:
        packages = build_packages(output)
        print(f"Built and validated {len(packages)} uploadable Claude skill ZIPs in {output.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except PackagingError as exc:
        raise SystemExit(f"Claude skill packaging failed: {exc}") from exc
