from tools.registry import list_tools


SUPPORTED_TYPES = {
    "object",
    "string",
    "integer",
    "number",
    "boolean",
    "array",
}

CONSTRAINTS = {
    "minimum",
    "maximum",
    "minLength",
    "maxLength",
    "enum",
}


def test_registry_schemas_have_valid_root_contract():
    for tool_name, tool in list_tools().items():
        schema = tool.get("parameters")

        assert isinstance(schema, dict), (
            f"{tool_name}: parameters harus object"
        )

        assert schema.get("type") == "object", (
            f"{tool_name}: root type harus object"
        )

        properties = schema.get("properties", {})
        assert isinstance(properties, dict), (
            f"{tool_name}: properties harus object"
        )


def test_registry_required_properties_are_declared():
    for tool_name, tool in list_tools().items():
        schema = tool["parameters"]

        properties = schema.get("properties", {})
        required = schema.get("required", [])

        assert isinstance(required, list), (
            f"{tool_name}: required harus array"
        )

        unknown = set(required) - set(properties)

        assert not unknown, (
            f"{tool_name}: required tidak didefinisikan: "
            f"{sorted(unknown)}"
        )


def test_registry_additional_properties_is_boolean():
    for tool_name, tool in list_tools().items():
        schema = tool["parameters"]

        additional = schema.get(
            "additionalProperties",
            False,
        )

        assert isinstance(additional, bool), (
            f"{tool_name}: additionalProperties harus bool"
        )


def test_registry_property_types_are_supported():
    for tool_name, tool in list_tools().items():
        properties = (
            tool["parameters"]
            .get("properties", {})
        )

        for name, definition in properties.items():
            assert isinstance(definition, dict), (
                f"{tool_name}.{name}: definition harus object"
            )

            value_type = definition.get("type")

            assert value_type in SUPPORTED_TYPES, (
                f"{tool_name}.{name}: "
                f"type tidak didukung: {value_type!r}"
            )


def test_registry_constraints_have_valid_types():
    for tool_name, tool in list_tools().items():
        properties = (
            tool["parameters"]
            .get("properties", {})
        )

        for name, definition in properties.items():
            for constraint in CONSTRAINTS:
                if constraint not in definition:
                    continue

                value = definition[constraint]

                if constraint == "enum":
                    assert isinstance(value, list), (
                        f"{tool_name}.{name}.enum "
                        "harus array"
                    )

                elif constraint in {
                    "minimum",
                    "maximum",
                }:
                    assert (
                        isinstance(value, (int, float))
                        and not isinstance(value, bool)
                    ), (
                        f"{tool_name}.{name}.{constraint} "
                        "harus number"
                    )

                elif constraint in {
                    "minLength",
                    "maxLength",
                }:
                    assert (
                        isinstance(value, int)
                        and not isinstance(value, bool)
                        and value >= 0
                    ), (
                        f"{tool_name}.{name}.{constraint} "
                        "harus integer >= 0"
                    )


def test_registry_schema_contract_is_valid():
    tools = list_tools()

    assert tools, "Registry tidak boleh kosong"

    for tool_name, tool in tools.items():
        schema = tool["parameters"]

        assert schema["type"] == "object"

        properties = schema.get("properties", {})
        required = schema.get("required", [])

        assert set(required) <= set(properties)

        for name, definition in properties.items():
            assert definition["type"] in SUPPORTED_TYPES
