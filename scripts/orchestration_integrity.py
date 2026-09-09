#!/usr/bin/env python3
"""Validate canonical planning metadata and structured execution-graph integrity."""

from __future__ import annotations

import pathlib
import re
import sys
from collections.abc import Mapping
from typing import Any

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
ORCHESTRATION_PATH = ROOT / ".agent-orchestration.yaml"
CONTRACT_PATH = ROOT / "contracts" / "planning-integrity.yaml"
STABLE_IDS_PATH = ROOT / "docs" / "stable-ids.md"


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML mapping key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def load_yaml_unique(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UniqueKeyLoader)


def _source_path(root: pathlib.Path, source_ref: str) -> pathlib.Path:
    return root / source_ref.split("#", 1)[0]


def validate_gate_definitions(orchestration: Mapping[str, Any], contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    gates = orchestration.get("hard_promotion_gates", {})
    definitions = contract.get("gate_definitions", {})
    if not isinstance(gates, Mapping):
        return [".agent-orchestration.yaml hard_promotion_gates must be a mapping"]
    if not isinstance(definitions, Mapping):
        return ["planning-integrity gate_definitions must be a mapping"]

    referenced: set[str] = set()
    for gate_name, tokens in gates.items():
        if not isinstance(tokens, list) or not all(isinstance(token, str) for token in tokens):
            errors.append(f"hard promotion gate {gate_name!r} must be a list of string tokens")
            continue
        if len(tokens) != len(set(tokens)):
            errors.append(f"hard promotion gate {gate_name!r} contains duplicate tokens")
        referenced.update(tokens)

    defined = set(definitions)
    missing = sorted(referenced - defined)
    extra = sorted(defined - referenced)
    if missing:
        errors.append(f"hard promotion gate tokens missing definitions: {', '.join(missing)}")
    if extra:
        errors.append(f"gate definitions not used by any hard promotion gate: {', '.join(extra)}")

    for token, definition in definitions.items():
        if not isinstance(definition, Mapping):
            errors.append(f"gate definition {token!r} must be a mapping")
            continue
        if not definition.get("kind") or not definition.get("meaning"):
            errors.append(f"gate definition {token!r} requires kind and meaning")
    return errors


def parse_stable_id_table(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    row_pattern = re.compile(r"^\| `([^`]+)` \| (.*?) \| `([^`]+)` \|$")
    for line in text.splitlines():
        match = row_pattern.match(line)
        if match:
            rows.append(match.groups())
    return rows


def validate_id_contract(contract: Mapping[str, Any], stable_ids_text: str) -> list[str]:
    errors: list[str] = []
    namespaces = contract.get("id_namespaces", {})
    if not isinstance(namespaces, Mapping):
        return ["planning-integrity id_namespaces must be a mapping"]

    planning = namespaces.get("planning", {})
    research = namespaces.get("lead_user_study", {})
    planning_defaults = planning.get("defaults", {}) if isinstance(planning, Mapping) else {}
    research_defaults = research.get("defaults", {}) if isinstance(research, Mapping) else {}
    if not isinstance(planning_defaults, Mapping) or not isinstance(research_defaults, Mapping):
        return ["planning and lead_user_study ID defaults must be mappings"]

    for namespace_name, defaults in (
        ("planning", planning_defaults),
        ("lead_user_study", research_defaults),
    ):
        for prefix, definition in defaults.items():
            if not isinstance(definition, Mapping):
                errors.append(f"{namespace_name} ID {prefix!r} definition must be a mapping")
                continue
            meaning = definition.get("meaning")
            example = definition.get("example")
            pattern = definition.get("pattern")
            if not all(isinstance(value, str) and value for value in (meaning, example, pattern)):
                errors.append(f"{namespace_name} ID {prefix!r} requires meaning, example, and pattern")
                continue
            try:
                if re.fullmatch(pattern, example) is None:
                    errors.append(
                        f"{namespace_name} ID {prefix!r} example {example!r} does not match {pattern!r}"
                    )
            except re.error as exc:
                errors.append(f"{namespace_name} ID {prefix!r} has invalid regex {pattern!r}: {exc}")

    actual_collisions = set(planning_defaults) & set(research_defaults)
    declared_collisions = set(research.get("collisions_with_planning", [])) if isinstance(research, Mapping) else set()
    if actual_collisions != declared_collisions:
        errors.append(
            "Lead User/planning ID collision declaration mismatch: "
            f"actual={sorted(actual_collisions)}, declared={sorted(declared_collisions)}"
        )

    rendered_rows = parse_stable_id_table(stable_ids_text)
    expected_rows = [
        (prefix, definition["meaning"], definition["example"])
        for prefix, definition in planning_defaults.items()
        if isinstance(definition, Mapping)
        and all(key in definition for key in ("meaning", "example"))
    ]
    if rendered_rows != expected_rows:
        errors.append("docs/stable-ids.md planning defaults do not match the machine-readable ID contract")

    lead_user_paragraph = ""
    marker = "Lead User study files"
    if marker in stable_ids_text:
        lead_user_paragraph = stable_ids_text.split(marker, 1)[1].split("\n\n", 1)[0]
    mentioned_research_prefixes = set(re.findall(r"`([A-Z]+)`", lead_user_paragraph))
    missing_from_docs = sorted(set(research_defaults) - mentioned_research_prefixes)
    if missing_from_docs:
        errors.append(
            "docs/stable-ids.md omits Lead User study-local prefixes: "
            + ", ".join(missing_from_docs)
        )
    return errors


def validate_manifest_references(
    root: pathlib.Path, orchestration: Mapping[str, Any], contract: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    source_refs: list[tuple[str, str]] = []

    gate_source = contract.get("gate_source")
    if isinstance(gate_source, str):
        source_refs.append(("gate_source", gate_source))

    namespaces = contract.get("id_namespaces", {})
    if isinstance(namespaces, Mapping):
        for namespace_name, namespace in namespaces.items():
            if isinstance(namespace, Mapping) and isinstance(namespace.get("source"), str):
                source_refs.append((f"id_namespaces.{namespace_name}.source", namespace["source"]))

    execution_graph = contract.get("execution_graph", {})
    if isinstance(execution_graph, Mapping) and isinstance(execution_graph.get("source"), str):
        source_refs.append(("execution_graph.source", execution_graph["source"]))

    for label, source_ref in source_refs:
        if not _source_path(root, source_ref).is_file():
            errors.append(f"{label} references missing file: {source_ref}")

    for group_name in contract.get("orchestration_reference_groups", []):
        group = orchestration.get(group_name, {})
        if not isinstance(group, Mapping):
            errors.append(f"orchestration reference group {group_name!r} must be a mapping")
            continue
        for key, relative_path in group.items():
            if not isinstance(relative_path, str) or not relative_path:
                errors.append(f"{group_name}.{key} must be a non-empty repository path")
                continue
            if not (root / relative_path).is_file():
                errors.append(f"{group_name}.{key} references missing file: {relative_path}")
    return errors


def _dependency_cycle(nodes: Mapping[str, Any]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node_id: str) -> list[str] | None:
        if node_id in visited:
            return None
        if node_id in visiting:
            start = stack.index(node_id)
            return stack[start:] + [node_id]
        visiting.add(node_id)
        stack.append(node_id)
        node = nodes.get(node_id, {})
        dependencies = node.get("depends_on", []) if isinstance(node, Mapping) else []
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency in nodes:
                    cycle = visit(dependency)
                    if cycle:
                        return cycle
        stack.pop()
        visiting.remove(node_id)
        visited.add(node_id)
        return None

    for node_id in nodes:
        cycle = visit(node_id)
        if cycle:
            return cycle
    return None


def validate_execution_graph(graph: Mapping[str, Any], contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    graph_contract = contract.get("execution_graph", {})
    namespaces = contract.get("id_namespaces", {})
    planning = namespaces.get("planning", {}) if isinstance(namespaces, Mapping) else {}
    planning_defaults = planning.get("defaults", {}) if isinstance(planning, Mapping) else {}
    node_prefix = graph_contract.get("node_prefix") if isinstance(graph_contract, Mapping) else None
    node_definition = planning_defaults.get(node_prefix, {}) if isinstance(planning_defaults, Mapping) else {}
    node_pattern = node_definition.get("pattern") if isinstance(node_definition, Mapping) else None

    nodes = graph.get("nodes", {})
    if not isinstance(nodes, Mapping):
        return ["execution graph nodes must be a mapping"]

    dependency_pairs: set[tuple[str, str]] = set()
    for node_id, node in nodes.items():
        if not isinstance(node_id, str):
            errors.append(f"execution graph node ID must be a string: {node_id!r}")
            continue
        if isinstance(node_pattern, str) and re.fullmatch(node_pattern, node_id) is None:
            errors.append(f"execution graph node ID {node_id!r} is outside the {node_prefix} namespace")
        if not isinstance(node, Mapping):
            errors.append(f"execution graph node {node_id!r} must be a mapping")
            continue
        dependencies = node.get("depends_on", [])
        if not isinstance(dependencies, list) or not all(isinstance(dep, str) for dep in dependencies):
            errors.append(f"execution graph node {node_id!r} depends_on must be a list of node IDs")
            continue
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"execution graph node {node_id!r} contains duplicate dependencies")
        for dependency in dependencies:
            if dependency not in nodes:
                errors.append(f"execution graph node {node_id!r} depends on missing node {dependency!r}")
            else:
                dependency_pairs.add((dependency, node_id))

    cycle = _dependency_cycle(nodes)
    if cycle:
        errors.append("execution graph dependency cycle: " + " -> ".join(cycle))

    edges = graph.get("edges", [])
    edge_pairs: list[tuple[str, str]] = []
    if not isinstance(edges, list):
        errors.append("execution graph edges must be a list")
    else:
        for index, edge in enumerate(edges):
            if not isinstance(edge, Mapping):
                errors.append(f"execution graph edge {index} must be a mapping")
                continue
            source = edge.get("from")
            target = edge.get("to")
            if not isinstance(source, str) or not isinstance(target, str):
                errors.append(f"execution graph edge {index} requires string from/to node IDs")
                continue
            if source not in nodes:
                errors.append(f"execution graph edge {index} references missing source node {source!r}")
            if target not in nodes:
                errors.append(f"execution graph edge {index} references missing target node {target!r}")
            edge_pairs.append((source, target))
        if len(edge_pairs) != len(set(edge_pairs)):
            errors.append("execution graph contains duplicate dependency edges")
        if set(edge_pairs) != dependency_pairs:
            errors.append(
                "execution graph edges do not match node depends_on declarations: "
                f"edges={sorted(set(edge_pairs))}, dependencies={sorted(dependency_pairs)}"
            )

    configured_states = graph_contract.get("runtime_states", []) if isinstance(graph_contract, Mapping) else []
    runtime_state = graph.get("runtime_state", {})
    if not isinstance(runtime_state, Mapping):
        errors.append("execution graph runtime_state must be a mapping")
        return errors
    if set(runtime_state) != set(configured_states):
        errors.append(
            "execution graph runtime_state keys do not match canonical states: "
            f"actual={sorted(runtime_state)}, expected={sorted(configured_states)}"
        )

    memberships: dict[str, str] = {}
    for state_name in configured_states:
        refs = runtime_state.get(state_name, [])
        if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
            errors.append(f"runtime_state.{state_name} must be a list of node IDs")
            continue
        if len(refs) != len(set(refs)):
            errors.append(f"runtime_state.{state_name} contains duplicate node IDs")
        for ref in refs:
            if ref not in nodes:
                errors.append(f"runtime_state.{state_name} references missing node {ref!r}")
            previous = memberships.get(ref)
            if previous is not None and previous != state_name:
                errors.append(f"execution graph node {ref!r} appears in both {previous} and {state_name}")
            memberships[ref] = state_name

    policy = graph.get("execution_policy", {})
    max_active = policy.get("max_active_groups") if isinstance(policy, Mapping) else None
    if not isinstance(max_active, int) or isinstance(max_active, bool) or max_active < 1:
        errors.append("execution_policy.max_active_groups must be a positive integer")
    else:
        active = runtime_state.get("active", [])
        if isinstance(active, list) and len(active) > max_active:
            errors.append(
                f"runtime_state.active has {len(active)} nodes but max_active_groups is {max_active}"
            )
    return errors


def validate_repository(root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        orchestration = load_yaml_unique(root / ".agent-orchestration.yaml")
        contract = load_yaml_unique(root / "contracts" / "planning-integrity.yaml")
        graph = load_yaml_unique(root / "templates" / "execution-graph.yaml")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"unable to load canonical YAML: {exc}"]

    if not isinstance(orchestration, Mapping) or not isinstance(contract, Mapping) or not isinstance(graph, Mapping):
        return ["canonical orchestration, integrity contract, and execution graph must be YAML mappings"]

    stable_ids_text = (root / "docs" / "stable-ids.md").read_text(encoding="utf-8")
    errors.extend(validate_gate_definitions(orchestration, contract))
    errors.extend(validate_id_contract(contract, stable_ids_text))
    errors.extend(validate_manifest_references(root, orchestration, contract))
    errors.extend(validate_execution_graph(graph, contract))

    active_scope = orchestration.get("scope_contract", {}).get("active_scope", {})
    scope_rules = active_scope.get("rules", []) if isinstance(active_scope, Mapping) else []
    policy = graph.get("execution_policy", {})
    if "exactly_one_active_scope" in scope_rules and isinstance(policy, Mapping):
        if policy.get("max_active_groups") != 1:
            errors.append(
                "execution graph max_active_groups must be 1 while the canonical scope contract requires exactly_one_active_scope"
            )
    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print("Orchestration integrity FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Orchestration integrity passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
