from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "lead-user-research" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validation_schema import (  # noqa: E402
    ENUM_DOMAINS,
    ENUM_RULES,
    REGISTRY_CONTAINERS,
    REGISTRY_FIELD_TYPES,
    validate_registry_enums,
    validate_registry_fields,
)


class LeadUserValidationSchemaTests(unittest.TestCase):
    def test_every_registry_has_declared_field_schema(self) -> None:
        self.assertEqual(set(REGISTRY_CONTAINERS), set(REGISTRY_FIELD_TYPES))

    def test_every_declared_registry_field_rejects_a_wrong_type(self) -> None:
        candidates = ["x", [], {}, True, 7, None, object()]
        for registry, fields in REGISTRY_FIELD_TYPES.items():
            container_type = REGISTRY_CONTAINERS[registry]
            for field, allowed_names in fields.items():
                allowed_runtime_names = set(allowed_names)
                wrong = next(
                    value
                    for value in candidates
                    if (
                        (value is None and "none" not in allowed_runtime_names)
                        or (value is not None and type(value).__name__ not in allowed_runtime_names)
                    )
                )
                row = {field: wrong}
                payload = [row] if container_type is list else row
                errors: list[str] = []
                validate_registry_fields(registry, payload, errors)
                self.assertTrue(
                    any(field in error and "invalid type" in error for error in errors),
                    f"{registry}:{field} accepted malformed {type(wrong).__name__}",
                )

    def test_every_declared_enum_domain_is_bound_to_registry_state(self) -> None:
        bound = {domain_name for _, _, domain_name in ENUM_RULES}
        self.assertEqual(set(ENUM_DOMAINS), bound)

    def test_every_enum_rule_rejects_unknown_value(self) -> None:
        for registry, path, domain_name in ENUM_RULES:
            payload = self._payload_for_path(path, "__INVALID_ENUM__")
            errors: list[str] = []
            validate_registry_enums(registry, payload, errors)
            self.assertTrue(
                any(domain_name in error and "__INVALID_ENUM__" in error for error in errors),
                f"{registry}:{path} did not enforce {domain_name}",
            )

    def test_schema_and_state_modules_match_packaged_copy(self) -> None:
        for name in ("validation_schema.py", "validation_state.py", "validate_study.py"):
            self.assertEqual(
                (ROOT / "lead-user-research" / "scripts" / name).read_bytes(),
                (ROOT / "skills" / "lead-user-research" / "scripts" / name).read_bytes(),
                name,
            )

    @staticmethod
    def _payload_for_path(path: str, value):
        tokens = path.split(".")

        def build(index: int):
            token = tokens[index]
            last = index == len(tokens) - 1
            if token == "[]":
                return [value if last else build(index + 1)]
            if token == "*":
                return {"sample": value if last else build(index + 1)}
            if token.endswith("[]"):
                key = token[:-2]
                return {key: [value if last else build(index + 1)]}
            return {token: value if last else build(index + 1)}

        return build(0)


if __name__ == "__main__":
    unittest.main()
