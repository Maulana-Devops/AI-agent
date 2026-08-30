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
    """Safely execute registered tools according to their risk level."""

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
