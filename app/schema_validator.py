from typing import Any


def validate_arguments(
    schema: dict[str, Any] | None,
    arguments: Any,
) -> str | None:
    """
    Validate tool arguments against a JSON-Schema-like registry contract.

    Returns:
        None when arguments are valid.
        A human-readable error string when validation fails.

    Validation covers:
    - object arguments
    - required properties
    - additionalProperties
    - primitive/container types
    - minimum / maximum
    - minLength / maxLength
    - enum
    """
    if not isinstance(arguments, dict):
        return "Arguments harus berupa object/dictionary."

    schema = schema or {}

    properties = schema.get("properties") or {}
    required = schema.get("required") or []

    if not isinstance(properties, dict):
        return "Contract properties harus berupa object."

    if not isinstance(required, list):
        return "Contract required harus berupa array."

    # JSON Schema semantics:
    # - omitted / False -> strict object
    # - True -> allow undeclared properties
    additional_properties = schema.get(
        "additionalProperties",
        False,
    )

    if additional_properties is not True:
        unknown = sorted(set(arguments) - set(properties))

        if unknown:
            return (
                "Argument tidak dikenal: "
                + ", ".join(unknown)
            )

    # Reject missing required arguments.
    missing = [
        name
        for name in required
        if name not in arguments
    ]

    if missing:
        return (
            "Argument wajib belum diberikan: "
            + ", ".join(missing)
        )

    # Validate declared argument types and constraints.
    for name, value in arguments.items():
        definition = properties.get(name, {})

        if name not in properties:
            # Allowed when additionalProperties=True.
            continue

        expected = definition.get("type")

        if expected == "string":
            valid = isinstance(value, str)

        elif expected == "integer":
            # bool is technically an int subclass in Python,
            # but must not be accepted as a tool integer.
            valid = (
                isinstance(value, int)
                and not isinstance(value, bool)
            )

        elif expected == "number":
            valid = (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
            )

        elif expected == "boolean":
            valid = isinstance(value, bool)

        elif expected == "object":
            valid = isinstance(value, dict)

        elif expected == "array":
            valid = isinstance(value, list)

        elif expected is None:
            valid = True

        else:
            return (
                f"Contract type tidak didukung untuk argument "
                f"'{name}': {expected}"
            )

        if not valid:
            return (
                f"Argument '{name}' harus bertipe "
                f"{expected}"
            )

        # Numeric minimum / maximum.
        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
        ):
            minimum = definition.get("minimum")
            maximum = definition.get("maximum")

            if minimum is not None and value < minimum:
                return (
                    f"Argument '{name}' harus >= {minimum}"
                )

            if maximum is not None and value > maximum:
                return (
                    f"Argument '{name}' harus <= {maximum}"
                )

        # String minimum / maximum length.
        if isinstance(value, str):
            min_length = definition.get("minLength")
            max_length = definition.get("maxLength")

            if min_length is not None and len(value) < min_length:
                return (
                    f"Argument '{name}' minimal "
                    f"{min_length} karakter"
                )

            if max_length is not None and len(value) > max_length:
                return (
                    f"Argument '{name}' maksimal "
                    f"{max_length} karakter"
                )

        # Enumerated values.
        enum_values = definition.get("enum")

        if enum_values is not None and value not in enum_values:
            return (
                f"Argument '{name}' harus memiliki "
                f"nilai yang termasuk dalam enum: "
                f"{enum_values}"
            )

    return None
