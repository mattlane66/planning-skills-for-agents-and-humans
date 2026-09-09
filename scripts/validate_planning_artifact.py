#!/usr/bin/env python3
"""Validate minimum machine-readable contracts for planning Markdown artifacts."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections.abc import Mapping
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CONTRACTS = ROOT / "contracts" / "artifact-contracts.yaml"


class ContractError(ValueError):
    """Raised when the artifact contract definition itself is invalid."""


def load_contracts(path: pathlib.Path = DEFAULT_CONTRACTS) -> Mapping[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ContractError("artifact contract file must be a YAML mapping")
    if payload.get("version") != 1:
        raise ContractError("artifact contract file must use version 1")
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, Mapping) or not artifacts:
        raise ContractError("artifact contract file requires a non-empty artifacts mapping")
    return payload


def _compile_pattern(entry: Any, artifact_type: str) -> tuple[re.Pattern[str], str]:
    if isinstance(entry, str):
        pattern_text = entry
        message = f"required pattern did not match: {entry}"
    elif isinstance(entry, Mapping):
        pattern_text = entry.get("pattern")
        message = entry.get("message") or f"required pattern did not match: {pattern_text}"
    else:
        raise ContractError(f"{artifact_type}: required pattern must be a string or mapping")
    if not isinstance(pattern_text, str) or not pattern_text:
        raise ContractError(f"{artifact_type}: required pattern is missing a non-empty pattern")
    try:
        return re.compile(pattern_text), str(message)
    except re.error as exc:
        raise ContractError(f"{artifact_type}: invalid regex {pattern_text!r}: {exc}") from exc


def validate_contract_definitions(
    contracts: Mapping[str, Any], root: pathlib.Path = ROOT
) -> list[str]:
    errors: list[str] = []
    artifacts = contracts.get("artifacts", {})
    gate_usage = contracts.get("gate_usage", {})

    if isinstance(gate_usage, Mapping):
        known = set(artifacts) if isinstance(artifacts, Mapping) else set()
        for gate, artifact_types in gate_usage.items():
            if not isinstance(artifact_types, list) or not all(
                isinstance(item, str) for item in artifact_types
            ):
                errors.append(f"gate_usage.{gate} must be a list of artifact types")
                continue
            for artifact_type in artifact_types:
                if artifact_type not in known:
                    errors.append(
                        f"gate_usage.{gate} references unknown artifact type {artifact_type!r}"
                    )

    if not isinstance(artifacts, Mapping):
        return errors + ["artifacts must be a mapping"]

    for artifact_type, definition in artifacts.items():
        if not isinstance(definition, Mapping):
            errors.append(f"{artifact_type}: contract must be a mapping")
            continue
        template = definition.get("template")
        if not isinstance(template, str) or not template:
            errors.append(f"{artifact_type}: template must be a non-empty path")
            continue
        template_path = root / template
        if not template_path.is_file():
            errors.append(f"{artifact_type}: template does not exist: {template}")
            continue
        template_text = template_path.read_text(encoding="utf-8")
        template_lines = {line.strip() for line in template_text.splitlines()}

        headings = definition.get("required_headings", [])
        if not isinstance(headings, list) or not all(isinstance(item, str) for item in headings):
            errors.append(f"{artifact_type}: required_headings must be a list of strings")
        else:
            for heading in headings:
                if heading not in template_lines:
                    errors.append(
                        f"{artifact_type}: template {template} is missing required heading {heading!r}"
                    )

        labels = definition.get("required_nonempty_labels", [])
        if not isinstance(labels, list) or not all(isinstance(item, str) for item in labels):
            errors.append(f"{artifact_type}: required_nonempty_labels must be a list of strings")
        else:
            for label in labels:
                if not any(line.strip().startswith(label) for line in template_text.splitlines()):
                    errors.append(
                        f"{artifact_type}: template {template} is missing required label {label!r}"
                    )

        patterns = definition.get("required_patterns", [])
        if not isinstance(patterns, list):
            errors.append(f"{artifact_type}: required_patterns must be a list")
        else:
            for entry in patterns:
                try:
                    _compile_pattern(entry, str(artifact_type))
                except ContractError as exc:
                    errors.append(str(exc))
    return errors


def _placeholder_set(contracts: Mapping[str, Any]) -> set[str]:
    raw = contracts.get("placeholder_values", [])
    if not isinstance(raw, list):
        raise ContractError("placeholder_values must be a list")
    return {str(value).strip().casefold() for value in raw}


def _clean_value(value: str) -> str:
    return value.strip().strip("`*_\"'").strip()


def validate_artifact_text(
    artifact_type: str, text: str, contracts: Mapping[str, Any]
) -> list[str]:
    artifacts = contracts.get("artifacts", {})
    if not isinstance(artifacts, Mapping) or artifact_type not in artifacts:
        return [f"unknown artifact type: {artifact_type}"]
    definition = artifacts[artifact_type]
    if not isinstance(definition, Mapping):
        return [f"invalid contract for artifact type: {artifact_type}"]

    errors: list[str] = []
    lines = text.splitlines()
    stripped_lines = {line.strip() for line in lines}

    for heading in definition.get("required_headings", []):
        if heading not in stripped_lines:
            errors.append(f"missing required heading: {heading}")

    for entry in definition.get("required_patterns", []):
        try:
            pattern, message = _compile_pattern(entry, artifact_type)
        except ContractError as exc:
            errors.append(str(exc))
            continue
        if pattern.search(text) is None:
            errors.append(message)

    placeholders = _placeholder_set(contracts)
    for label in definition.get("required_nonempty_labels", []):
        matches = [line.strip() for line in lines if line.strip().startswith(label)]
        if not matches:
            errors.append(f"missing required field: {label}")
            continue
        values = [_clean_value(line[len(label) :]) for line in matches]
        if not any(value and value.casefold() not in placeholders for value in values):
            errors.append(f"required field is empty or placeholder: {label}")

    return errors


def validate_artifact_file(
    artifact_type: str,
    path: pathlib.Path,
    contracts: Mapping[str, Any],
) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"unable to read artifact {path}: {exc}"]
    return validate_artifact_text(artifact_type, text, contracts)


def _emit_result(
    artifact_type: str | None,
    path: pathlib.Path | None,
    errors: list[str],
    as_json: bool,
) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "valid": not errors,
                    "artifact_type": artifact_type,
                    "path": str(path) if path is not None else None,
                    "errors": errors,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if errors:
        print("Planning artifact validation FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        target = artifact_type or "contract definitions"
        print(f"Planning artifact validation passed: {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_type", nargs="?")
    parser.add_argument("path", nargs="?", type=pathlib.Path)
    parser.add_argument("--contracts", type=pathlib.Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--check-contracts", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        contracts = load_contracts(args.contracts)
    except (OSError, yaml.YAMLError, ContractError) as exc:
        _emit_result(args.artifact_type, args.path, [str(exc)], args.as_json)
        return 1

    if args.check_contracts:
        errors = validate_contract_definitions(contracts)
        _emit_result(None, None, errors, args.as_json)
        return 1 if errors else 0

    if not args.artifact_type or args.path is None:
        parser.error("artifact_type and path are required unless --check-contracts is used")

    definition_errors = validate_contract_definitions(contracts)
    errors = definition_errors + validate_artifact_file(args.artifact_type, args.path, contracts)
    _emit_result(args.artifact_type, args.path, errors, args.as_json)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
