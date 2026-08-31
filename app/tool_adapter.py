from tools.registry import list_tools


def get_tool_declarations():
    """
    Return explicit function declarations for Gemini.

    Registry menjadi single source of truth untuk:
    - nama tool
    - description
    - parameters
    - risk

    Gemini hanya menerima metadata tool.
    Gemini tidak menerima direct access ke Python functions.
    """
    declarations = []

    for name, data in list_tools().items():
        declarations.append(
            {
                "name": name,
                "description": data["description"],
                "parameters": data["parameters"],
            }
        )

    return declarations
