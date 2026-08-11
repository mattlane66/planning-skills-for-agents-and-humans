#!/usr/bin/env python3
"""Validate a release tag and build deterministic GitHub release assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
STABLE_TAG = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
VERSION_FILES = (
    Path(".claude-plugin/plugin.json"),
    Path(".codex-plugin/plugin.json"),
    Path("mcp-server/package.json"),
    Path("mcp-server/package-lock.json"),
)


class ReleaseError(RuntimeError):
    """Raised when release metadata or generated assets are invalid."""


def load_versions(root: Path = ROOT) -> dict[str, str]:
    versions: dict[str, str] = {}
    for relative in VERSION_FILES:
        path = root / relative
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            value = payload["version"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ReleaseError(f"cannot read version from {relative}") from exc
        if not isinstance(value, str) or not STABLE_TAG.fullmatch(f"v{value}"):
            raise ReleaseError(f"invalid stable version in {relative}: {value!r}")
        if relative.name == "package-lock.json" and payload.get("packages", {}).get("", {}).get("version") != value:
            raise ReleaseError(f"root package version is inconsistent in {relative}")
        versions[relative.as_posix()] = value
    return versions


def extract_release_notes(changelog: str, tag: str) -> str:
    if not STABLE_TAG.fullmatch(tag):
        raise ReleaseError(f"release tag must be exact stable SemVer: {tag}")
    lines = changelog.splitlines()
    heading = re.compile(rf"^## {re.escape(tag)}(?:\s|$)")
    matches = [index for index, line in enumerate(lines) if heading.match(line)]
    if len(matches) != 1:
        raise ReleaseError(f"CHANGELOG.md must contain exactly one section for {tag}")
    start = matches[0] + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    notes = "\n".join(lines[start:end]).strip()
    if not notes:
        raise ReleaseError(f"CHANGELOG.md section for {tag} is empty")
    return notes + "\n"


def validate_release(tag: str, root: Path = ROOT) -> str:
    match = STABLE_TAG.fullmatch(tag)
    if not match:
        raise ReleaseError(f"release tag must be exact stable SemVer: {tag}")
    expected = tag.removeprefix("v")
    versions = load_versions(root)
    mismatches = {path: version for path, version in versions.items() if version != expected}
    if mismatches:
        details = ", ".join(f"{path}={version}" for path, version in sorted(mismatches.items()))
        raise ReleaseError(f"tag {tag} does not match coordinated versions: {details}")
    return extract_release_notes((root / "CHANGELOG.md").read_text(encoding="utf-8"), tag)


def coordinated_tag(root: Path = ROOT) -> str:
    versions = set(load_versions(root).values())
    if len(versions) != 1:
        raise ReleaseError("coordinated versions do not match")
    return f"v{versions.pop()}"


def prepare_release_dir(output: Path, expected_files: set[str]) -> Path:
    requested = output.expanduser()
    if requested.is_symlink():
        raise ReleaseError(f"refusing symlinked release output directory: {requested}")
    output = requested.resolve()
    protected = {ROOT, Path.cwd().resolve(), Path.home().resolve(), *ROOT.parents}
    if output in protected:
        raise ReleaseError(f"refusing unsafe release output directory: {output}")
    if output.exists() and not output.is_dir():
        raise ReleaseError(f"release output is not a directory: {output}")
    output.mkdir(parents=True, exist_ok=True)

    generated_plugin = re.compile(r"^planning-skills-claude-code-plugin-v\d+\.\d+\.\d+\.zip$")
    unexpected = sorted(
        path.name
        for path in output.iterdir()
        if path.name not in expected_files and not generated_plugin.fullmatch(path.name)
    )
    if unexpected:
        raise ReleaseError(f"refusing to clean release output with unexpected entries: {unexpected}")
    invalid = sorted(path.name for path in output.iterdir() if path.is_symlink() or not path.is_file())
    if invalid:
        raise ReleaseError(f"refusing unsafe release output entries: {invalid}")
    for path in output.iterdir():
        path.unlink()
    return output


def build_release_assets(output: Path = ROOT / "dist" / "release") -> list[Path]:
    import build_claude_skills as claude_packager

    versions = load_versions()
    version_set = set(versions.values())
    if len(version_set) != 1:
        raise ReleaseError(f"coordinated versions do not match: {versions}")
    version = version_set.pop()
    skill_names = claude_packager.load_inventory()
    plugin_name = f"planning-skills-claude-code-plugin-v{version}.zip"
    asset_names = {f"{skill}.zip" for skill in skill_names} | {plugin_name, "SHA256SUMS"}
    output = prepare_release_dir(output, asset_names)

    skill_packages = claude_packager.build_packages(ROOT / "dist" / "claude-skills")
    subprocess.run(["bash", str(ROOT / "scripts" / "build-claude-plugin.sh")], cwd=ROOT, check=True)
    plugin_root = ROOT / "dist" / "claude-code-plugin"
    claude_packager.reject_source_symlinks(plugin_root)

    assets: list[Path] = []
    for package in skill_packages:
        target = output / package.name
        shutil.copyfile(package, target)
        assets.append(target)

    plugin_package = output / plugin_name
    claude_packager.write_reproducible_zip(plugin_package, plugin_root, plugin_root.parent)
    assets.append(plugin_package)

    checksum_path = output / "SHA256SUMS"
    checksum_text = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in sorted(assets, key=lambda candidate: candidate.name)
    )
    checksum_path.write_text(checksum_text, encoding="utf-8")
    assets.append(checksum_path)
    return sorted(assets, key=lambda candidate: candidate.name)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight")
    preflight.add_argument("--tag", required=True)
    preflight.add_argument("--notes-output", type=Path, default=ROOT / "release-notes.md")

    assets = subparsers.add_parser("assets")
    assets.add_argument("--output", type=Path, default=ROOT / "dist" / "release")

    subparsers.add_parser("version")

    args = parser.parse_args()
    if args.command == "preflight":
        notes = validate_release(args.tag)
        args.notes_output.write_text(notes, encoding="utf-8")
        print(f"Validated {args.tag} and wrote {args.notes_output}")
    elif args.command == "assets":
        built = build_release_assets(args.output)
        print(f"Built {len(built)} release assets in {args.output.resolve()}")
    else:
        print(coordinated_tag())


if __name__ == "__main__":
    try:
        main()
    except ReleaseError as exc:
        raise SystemExit(f"Release failed: {exc}") from exc
