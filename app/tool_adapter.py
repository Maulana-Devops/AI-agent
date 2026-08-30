from tools.registry import list_tools


TOOL_PARAMETERS = {
    "get_current_directory": {},

    "inspect_project": {},
    "create_directory": {
        "path": {
            "type": "string",
            "description": "Path of the directory to create.",
        },
    },

    "write_file": {
        "path": {
            "type": "string",
            "description": "Path of the file to write.",
        },
        "content": {
            "type": "string",
            "description": "Text content to write.",
        },
    },

    "copy_file": {
        "source": {
            "type": "string",
            "description": "Path of the source file.",
        },
        "destination": {
            "type": "string",
            "description": "Path of the destination file.",
        },
    },

    "move_file": {
        "source": {
            "type": "string",
            "description": "Path of the source file.",
        },
        "destination": {
            "type": "string",
            "description": "Path of the destination file.",
        },
    },

    "delete_directory": {
        "path": {
            "type": "string",
            "description": "Path of the directory to delete.",
        },
    },

    "delete_file": {
        "path": {
            "type": "string",
            "description": "Path of the file to delete.",
        },
    },

    "get_file_info": {
        "path": {
            "type": "string",
            "description": "Path of the file or directory.",
        },
    },

    "search_files": {
        "path": {
            "type": "string",
            "description": "Directory to search.",
        },
        "pattern": {
            "type": "string",
            "description": "Filename pattern, such as *.py.",
        },
    },

    "search_file_contents": {
        "path": {
            "type": "string",
            "description": "Directory to search.",
        },
        "query": {
            "type": "string",
            "description": "Text to search for.",
        },
    },

    "list_directory": {
        "path": {
            "type": "string",
            "description": "Directory path to list. Defaults to current directory.",
        },
    },

    "read_file": {
        "path": {
            "type": "string",
            "description": "Path of the text file to read.",
        },
    },

    "git_status": {},

    "git_branch": {},

    "git_log": {
        "limit": {
            "type": "integer",
            "description": "Number of recent commits to show. Must be between 1 and 50.",
        },
    },

    "git_diff": {},

    "git_remote": {},
}


def get_tool_declarations():
    """
    Return explicit function declarations for Gemini.

    Gemini receives only metadata about the available tools.
    It never receives direct access to Python functions.
    """
    declarations = []

    for name, data in list_tools().items():
        properties = TOOL_PARAMETERS.get(name, {})

        declarations.append(
            {
                "name": name,
                "description": data["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                },
            }
        )

    return declarations
