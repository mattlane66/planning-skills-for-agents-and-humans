#!/usr/bin/env python3
"""Exercise release/install surfaces in fresh layouts without invoking model runtimes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import tempfile
import tomllib
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEMVER_TAG = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$")
GEMINI_INCLUDE = re.compile(r"@\{([^{}]+)\}")


class InstallCheckError(RuntimeError):
    """Raised when a release or source-install surface cannot be consumed safely."""


def load_inventory(root: Path = ROOT) -> list[str]:
    path = root / "skill-inventory.txt"
    skills = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not skills or len(skills) != len(set(skills)):
        raise InstallCheckError("skill-inventory.txt must contain unique skill names")
    return skills


def parse_skill_name(path: Path) -> str:
    match = FRONTMATTER_NAME.search(path.read_text(encoding="utf-8"))
    if not match:
        raise InstallCheckError(f"missing skill name frontmatter: {path}")
    return match.group(1).strip()


def _safe_zip_member(info: zipfile.ZipInfo) -> None:
    path = PurePosixPath(info.filename)
    if path.is_absolute() or ".." in path.parts:
        raise InstallCheckError(f"unsafe archive path: {info.filename}")
    mode = info.external_attr >> 16
    if stat.S_ISLNK(mode):
        raise InstallCheckError(f"symlink is not allowed in release archive: {info.filename}")


def safe_extract(archive_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            _safe_zip_member(info)
        archive.extractall(destination)


def validate_checksums(assets_dir: Path) -> dict[str, str]:
    sums_path = assets_dir / "SHA256SUMS"
    if not sums_path.is_file():
        raise InstallCheckError("release assets are missing SHA256SUMS")
    declared: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, name = line.split("  ", 1)
        except ValueError as exc:
            raise InstallCheckError(f"invalid SHA256SUMS row: {line!r}") from exc
        if name in declared:
            raise InstallCheckError(f"duplicate SHA256SUMS entry: {name}")
        path = assets_dir / name
        if not path.is_file():
            raise InstallCheckError(f"SHA256SUMS references missing asset: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise InstallCheckError(f"checksum mismatch for {name}")
        declared[name] = digest
    return declared


def validate_claude_uploads(assets_dir: Path, skills: list[str]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="release-claude-upload-") as temporary:
        root = Path(temporary)
        for skill in skills:
            package = assets_dir / f"{skill}.zip"
            if not package.is_file():
                raise InstallCheckError(f"missing Claude upload asset: {package.name}")
            destination = root / skill
            destination.mkdir()
            safe_extract(package, destination)
            installed = destination / skill
            skill_file = installed / "SKILL.md"
            if not skill_file.is_file():
                raise InstallCheckError(f"{package.name} does not install {skill}/SKILL.md")
            if parse_skill_name(skill_file) != skill:
                raise InstallCheckError(f"{package.name} installs the wrong skill identity")
            for support in ("AGENTS.md", ".agent-orchestration.yaml", "LICENSE"):
                if not (installed / support).is_file():
                    raise InstallCheckError(f"{package.name} is missing support file {support}")
    return {
        "runtime": "claude-upload",
        "install_source": "release skill ZIPs",
        "skill_count": len(skills),
        "checks": ["safe extraction", "skill identity", "self-contained support files"],
    }


def validate_claude_code_plugin(
    assets_dir: Path, release_tag: str, skills: list[str]
) -> dict[str, Any]:
    version = release_tag.removeprefix("v")
    package = assets_dir / f"planning-skills-claude-code-plugin-v{version}.zip"
    if not package.is_file():
        raise InstallCheckError(f"missing Claude Code plugin asset: {package.name}")
    with tempfile.TemporaryDirectory(prefix="release-claude-code-") as temporary:
        root = Path(temporary)
        safe_extract(package, root)
        with zipfile.ZipFile(package) as archive:
            top_levels = {
                path.parts[0]
                for path in (PurePosixPath(name) for name in archive.namelist())
                if path.parts
            }
        if top_levels != {"claude-code-plugin"}:
            raise InstallCheckError(
                f"Claude Code plugin must have one claude-code-plugin/ root: {sorted(top_levels)}"
            )
        installed = root / "claude-code-plugin"
        manifest_path = installed / ".claude-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("version") != version:
            raise InstallCheckError("Claude Code plugin manifest version does not match release tag")
        for skill in skills:
            skill_file = installed / "skills" / skill / "SKILL.md"
            if not skill_file.is_file() or parse_skill_name(skill_file) != skill:
                raise InstallCheckError(f"Claude Code plugin cannot discover skill {skill}")
        if not (installed / "commands" / "plan.md").is_file():
            raise InstallCheckError("Claude Code plugin is missing commands/plan.md")
        if not (installed / "AGENTS.md").is_file() or not (
            installed / ".agent-orchestration.yaml"
        ).is_file():
            raise InstallCheckError("Claude Code plugin is missing shared orchestration context")
    return {
        "runtime": "claude-code",
        "install_source": package.name,
        "skill_count": len(skills),
        "checks": ["safe extraction", "manifest version", "skill discovery", "plan command surface"],
    }


def _copy_source_install(root: Path, destination: Path, paths: list[str]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for relative in paths:
        source = root / relative
        target = destination / relative
        if source.is_dir():
            shutil.copytree(source, target)
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        else:
            raise InstallCheckError(f"source-install path is missing: {relative}")


def validate_codex_source_install(
    root: Path, release_tag: str, skills: list[str]
) -> dict[str, Any]:
    version = release_tag.removeprefix("v")
    with tempfile.TemporaryDirectory(prefix="release-codex-") as temporary:
        installed = Path(temporary) / "checkout"
        _copy_source_install(
            root,
            installed,
            [
                ".codex-plugin",
                ".agents/plugins/marketplace.json",
                "skills",
                "AGENTS.md",
                ".agent-orchestration.yaml",
            ],
        )
        manifest = json.loads(
            (installed / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        if manifest.get("version") != version:
            raise InstallCheckError("Codex plugin manifest version does not match release tag")
        skills_path = manifest.get("skills")
        if not isinstance(skills_path, str):
            raise InstallCheckError("Codex plugin manifest does not declare a skills path")
        skill_root = (installed / skills_path).resolve()
        if skill_root != (installed / "skills").resolve():
            raise InstallCheckError("Codex plugin skills path does not resolve to installed skills/")
        discovered = []
        for skill in skills:
            skill_file = skill_root / skill / "SKILL.md"
            if not skill_file.is_file() or parse_skill_name(skill_file) != skill:
                raise InstallCheckError(f"Codex source install cannot discover skill {skill}")
            discovered.append(skill)
        marketplace = json.loads(
            (installed / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        plugins = marketplace.get("plugins", [])
        if not any(
            item.get("name") == manifest.get("name") for item in plugins if isinstance(item, dict)
        ):
            raise InstallCheckError("Codex marketplace does not expose the installed plugin")
    return {
        "runtime": "codex",
        "install_source": "release SHA Git checkout / local marketplace",
        "skill_count": len(discovered),
        "checks": ["fresh source layout", "manifest version", "marketplace discovery", "skill discovery"],
    }


def _stage_gemini_command_includes(root: Path, installed: Path, commands: list[Path]) -> int:
    includes: set[str] = set()
    for command in commands:
        payload = tomllib.loads(command.read_text(encoding="utf-8"))
        prompt = payload.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise InstallCheckError(f"Gemini command has no prompt: {command.name}")
        for include in GEMINI_INCLUDE.findall(prompt):
            if "{{" in include or "}}" in include:
                continue
            includes.add(include)

    for include in sorted(includes):
        source = root / include
        if not source.is_file():
            raise InstallCheckError(f"Gemini command references missing source include: {include}")
        target = installed / include
        if not target.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return len(includes)


def validate_gemini_source_install(root: Path, skills: list[str]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="release-gemini-") as temporary:
        installed = Path(temporary) / "checkout"
        _copy_source_install(
            root,
            installed,
            [
                ".gemini",
                "GEMINI.md",
                "AGENTS.md",
                ".agent-orchestration.yaml",
                *skills,
            ],
        )
        for skill in skills:
            skill_file = installed / skill / "SKILL.md"
            if not skill_file.is_file() or parse_skill_name(skill_file) != skill:
                raise InstallCheckError(f"Gemini source install cannot discover canonical skill {skill}")

        commands = sorted((installed / ".gemini" / "commands").glob("*.toml"))
        if not commands:
            raise InstallCheckError("Gemini source install contains no command wrappers")
        resolved_includes = _stage_gemini_command_includes(root, installed, commands)
        if resolved_includes == 0:
            raise InstallCheckError("Gemini command smoke resolved no static repository includes")
        for command in commands:
            payload = tomllib.loads(command.read_text(encoding="utf-8"))
            prompt = payload["prompt"]
            for include in GEMINI_INCLUDE.findall(prompt):
                if "{{" in include or "}}" in include:
                    continue
                if not (installed / include).is_file():
                    raise InstallCheckError(
                        f"Gemini command {command.name} has missing include after install: {include}"
                    )
    return {
        "runtime": "gemini-cli",
        "install_source": "release SHA Git/native skill install",
        "skill_count": len(skills),
        "command_count": len(commands),
        "checks": [
            "fresh source layout",
            "canonical skill discovery",
            "TOML parse",
            "static include resolution",
        ],
    }


def run_checks(
    assets_dir: Path, release_tag: str, release_sha: str, root: Path = ROOT
) -> dict[str, Any]:
    if not SEMVER_TAG.fullmatch(release_tag):
        raise InstallCheckError(f"release tag must be exact stable SemVer: {release_tag}")
    if not re.fullmatch(r"[0-9a-f]{40}", release_sha):
        raise InstallCheckError("release SHA must be a full 40-character lowercase Git SHA")
    assets_dir = assets_dir.resolve()
    skills = load_inventory(root)
    checksums = validate_checksums(assets_dir)
    surfaces = [
        validate_claude_uploads(assets_dir, skills),
        validate_claude_code_plugin(assets_dir, release_tag, skills),
        validate_codex_source_install(root, release_tag, skills),
        validate_gemini_source_install(root, skills),
    ]
    return {
        "schema_version": 1,
        "status": "passed",
        "release_tag": release_tag,
        "release_sha": release_sha,
        "checksum_asset_count": len(checksums),
        "surfaces": surfaces,
        "limitations": [
            "These checks exercise fresh install/discovery/use surfaces without invoking external model runtimes.",
            "Claude/Codex/Gemini model behavior is evaluated separately through blind runtime behavior evaluations.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--release-sha", required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    try:
        report = run_checks(args.assets_dir, args.release_tag, args.release_sha)
    except (
        InstallCheckError,
        OSError,
        json.JSONDecodeError,
        tomllib.TOMLDecodeError,
        zipfile.BadZipFile,
    ) as exc:
        raise SystemExit(f"Release install check failed: {exc}") from exc
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Release install checks passed; wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
