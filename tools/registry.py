from tools.filesystem import (
    get_current_directory,
    list_directory,
    read_file,
    create_directory,
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
