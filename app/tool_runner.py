from tools.registry import get_tool


class ToolExecutionError(RuntimeError):
    pass


def run_tool(name: str, arguments: dict | None = None):
    """
    Execute a registered tool.

    The tool runner only resolves and executes registered Python
    functions. It does not provide arbitrary shell execution.
    """
    tool = get_tool(name)

    if tool is None:
        raise ToolExecutionError(
            f"Tool tidak ditemukan: {name}"
        )

    function = tool["function"]
    arguments = arguments or {}

    try:
        return function(**arguments)

    except TypeError as exc:
        raise ToolExecutionError(
            f"Argumen tool tidak valid untuk {name}: {exc}"
        ) from exc

    except Exception as exc:
        raise ToolExecutionError(
            f"Tool {name} gagal dijalankan: {exc}"
        ) from exc
