from dataclasses import dataclass
from typing import Any

from tools.registry import get_tool


class ToolExecutionError(Exception):
    """Raised when a tool cannot be executed safely."""


@dataclass
class ToolExecutionResult:
    tool_name: str
    success: bool
    executed: bool
    result: Any = None
    error: str = ""
    requires_confirmation: bool = False


class ToolRunner:
    """Safely execute registered tools according to their contract and risk."""

    @staticmethod
    def _validate_arguments(tool_name: str, tool: dict, arguments: dict[str, Any]):
        """
        Validate tool arguments against the registry contract.

        Validation happens BEFORE:
        - confirmation
        - function invocation

        This guarantees that malformed LLM arguments never reach
        the underlying Python function.
        """
        if not isinstance(arguments, dict):
            return "Arguments harus berupa object/dictionary."

        schema = tool.get("parameters") or {}
        properties = schema.get("properties") or {}
        required = schema.get("required") or []

        # Reject arguments that are not declared by the registry.
        #
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

        # Validate declared argument types.
        for name, value in arguments.items():
            definition = properties.get(name, {})
            expected = definition.get("type")

            if expected == "string":
                valid = isinstance(value, str)

            elif expected == "integer":
                # bool is technically an int subclass in Python,
                # but must not be accepted as a tool integer.
                valid = isinstance(value, int) and not isinstance(value, bool)

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

        return None

    def _validate_semantic_arguments(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str | None:
        """
        Validate value-level constraints declared by the registry.

        Type validation memastikan bentuk data benar.
        Semantic validation memastikan nilainya berada
        dalam domain yang diizinkan.
        """
        tool = get_tool(tool_name)

        if tool is None:
            return f"Tool tidak ditemukan: {tool_name}"

        schema = tool.get("parameters", {})
        properties = schema.get("properties", {})

        for name, value in arguments.items():
            rules = properties.get(name)

            if rules is None:
                continue

            # Numeric minimum / maximum.
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                minimum = rules.get("minimum")
                maximum = rules.get("maximum")

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
                min_length = rules.get("minLength")
                max_length = rules.get("maxLength")

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
            enum_values = rules.get("enum")

            if enum_values is not None and value not in enum_values:
                return (
                    f"Argument '{name}' harus memiliki "
                    f"nilai yang termasuk dalam enum: "
                    f"{enum_values}"
                )

        return None

    def run(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        confirmed: bool = False,
    ) -> ToolExecutionResult:
        arguments = arguments or {}

        tool = get_tool(tool_name)

        if tool is None:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error=f"Tool tidak ditemukan: {tool_name}",
            )

        risk = tool.get("risk")
        function = tool.get("function")

        if function is None:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error=f"Tool tidak memiliki function: {tool_name}",
            )

        if risk == "dangerous":
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error="Tool dangerous diblokir oleh policy.",
            )

        # ---------------------------------------------------------
        # SECURITY BOUNDARY:
        # Validate arguments BEFORE confirmation and execution.
        # ---------------------------------------------------------
        validation_error = self._validate_arguments(
            tool_name,
            tool,
            arguments,
        )

        if validation_error:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error=validation_error,
            )

        semantic_error = self._validate_semantic_arguments(
            tool_name,
            arguments,
        )

        if semantic_error:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error=semantic_error,
            )

        if risk == "modify" and not confirmed:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                requires_confirmation=True,
                error="Konfirmasi diperlukan sebelum menjalankan tool modify.",
            )

        try:
            result = function(**arguments)

            return ToolExecutionResult(
                tool_name=tool_name,
                success=True,
                executed=True,
                result=result,
            )

        except Exception as exc:
            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                executed=False,
                error=str(exc),
            )


tool_runner = ToolRunner()


def run_tool_result(
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    confirmed: bool = False,
) -> ToolExecutionResult:
    """
    Structured tool execution API.

    Agent dapat memeriksa status execution tanpa melakukan
    parsing terhadap pesan error.
    """
    return tool_runner.run(
        name,
        arguments,
        confirmed=confirmed,
    )


def run_tool(
    name: str,
    arguments: dict[str, Any] | None = None,
    *,
    confirmed: bool = False,
):
    """
    Compatibility API used by existing callers.

    Read-only tools execute normally.
    Modify tools require confirmed=True.
    """
    result = run_tool_result(
        name,
        arguments,
        confirmed=confirmed,
    )

    if not result.success:
        raise ToolExecutionError(result.error)

    return result.result
