from tools.filesystem import (
    get_current_directory,
    list_directory,
    read_file,
    create_directory,
    delete_file,
    delete_directory,
    delete_directory,
    move_file,
    copy_file,
    get_file_info,
    search_files,
    write_file,
)

from tools.git import (
    git_status,
    git_branch,
    git_log,
    git_diff,
    git_remote,
)


TOOLS = {
    "get_current_directory": {
        "description": "Get the current working directory.",
        "risk": "read-only",
        "function": get_current_directory,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    "list_directory": {
        "description": "List files and directories in a directory.",
        "risk": "read-only",
        "function": list_directory,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path. Defaults to the current directory.",
                },
            },
        },
    },
    "read_file": {
        "description": "Read a text file.",
        "risk": "read-only",
        "function": read_file,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the text file to read.",
                },
            },
            "required": ["path"],
        },
    },
    "create_directory": {
        "description": "Create a new directory.",
        "risk": "modify",
        "function": create_directory,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the directory to create.",
                },
            },
            "required": ["path"],
        },
    },
    "write_file": {
        "description": "Write text content to a file.",
        "risk": "modify",
        "function": write_file,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to write.",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write.",
                },
            },
            "required": ["path", "content"],
        },
    },
    "copy_file": {
        "description": "Copy a file to a new destination.",
        "risk": "modify",
        "function": copy_file,
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Path of the source file.",
                },
                "destination": {
                    "type": "string",
                    "description": "Path of the destination file.",
                },
            },
            "required": ["source", "destination"],
        },
    },
    "move_file": {
        "description": "Move or rename a file.",
        "risk": "modify",
        "function": move_file,
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Path of the source file.",
                },
                "destination": {
                    "type": "string",
                    "description": "Path of the destination file.",
                },
            },
            "required": ["source", "destination"],
        },
    },
    "delete_file": {
        "description": "Delete a file.",
        "risk": "modify",
        "function": delete_file,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to delete.",
                },
            },
            "required": ["path"],
        },
    },
    "delete_directory": {
        "description": "Delete a directory and its contents.",
        "risk": "modify",
        "function": delete_directory,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the directory to delete.",
                },
            },
            "required": ["path"],
        },
    },
    "delete_directory": {
        "description": "Delete a directory and its contents.",
        "risk": "modify",
        "function": delete_directory,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the directory to delete.",
                },
            },
            "required": ["path"],
        },
    },
    "get_file_info": {
        "description": "Get basic metadata about a file or directory.",
        "risk": "read-only",
        "function": get_file_info,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file or directory.",
                },
            },
            "required": ["path"],
        },
    },
    "search_files": {
        "description": "Search files recursively by filename pattern.",
        "risk": "read-only",
        "function": search_files,
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to search.",
                },
                "pattern": {
                    "type": "string",
                    "description": "Filename pattern, such as *.py.",
                },
            },
            "required": ["path", "pattern"],
        },
    },
    "git_status": {
        "description": "Show the Git working tree status.",
        "risk": "read-only",
        "function": git_status,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    "git_branch": {
        "description": "Show Git branches.",
        "risk": "read-only",
        "function": git_branch,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    "git_log": {
        "description": "Show recent Git commits.",
        "risk": "read-only",
        "function": git_log,
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of commits to show. Must be between 1 and 50.",
                },
            },
        },
    },
    "git_diff": {
        "description": "Show unstaged Git changes.",
        "risk": "read-only",
        "function": git_diff,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    "git_remote": {
        "description": "Show configured Git remotes.",
        "risk": "read-only",
        "function": git_remote,
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
}


def get_tool(name: str):
    return TOOLS.get(name)


def list_tools():
    return {
        name: {
            "description": data["description"],
            "risk": data["risk"],
        }
        for name, data in TOOLS.items()
    }
