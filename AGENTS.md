# Laptop AI - Development Rules

## Project Overview

Laptop AI is a personal AI assistant for laptop and project development.

The project combines:
- Python application logic
- Local intent routing
- Permission and safety controls
- Tool registry and tool execution
- Gemini as an optional reasoning layer
- Local filesystem and Git tools

The goal is to build a safe and modular laptop assistant.

## Environment

- Python 3
- Virtual environment: `.venv`

Run tests with:

    python -m pytest -q

All tests must pass before considering a change complete.

## Architecture

Important components:

- `app/agent.py`
  - Gemini reasoning layer
  - Tool calling loop

- `app/local_router.py`
  - Local intent recognition
  - Avoids API usage for simple local commands

- `app/orchestrator.py`
  - Coordinates permission checks and command execution

- `app/permissions.py`
  - Risk classification:
    - READ_ONLY
    - MODIFY
    - DANGEROUS

- `app/confirmation.py`
  - Confirmation decisions

- `app/executor.py`
  - Command execution

- `app/tool_adapter.py`
  - Converts registered Python tools into Gemini tool declarations

- `app/tool_runner.py`
  - Controlled execution of registered tools

- `tools/registry.py`
  - Central tool registry

- `tools/filesystem.py`
  - Filesystem tools

- `tools/git.py`
  - Read-only Git tools

## Safety Rules

Never bypass the permission system.

Never directly execute arbitrary shell commands through the AI.

Never introduce a mechanism that allows the model to bypass:
- `permissions.py`
- `confirmation.py`
- `orchestrator.py`
- `tool_runner.py`

Dangerous operations must remain blocked unless the architecture explicitly changes through a deliberate security design.

Unknown commands must not automatically become trusted commands.

## Secrets

Never read, modify, print, expose, or commit:

- `.env`
- API keys
- tokens
- passwords
- credentials
- private keys

Use `.env.example` for configuration examples.

Never put secrets into source code, tests, logs, README files, or commits.

## Development Rules

Before modifying code:

1. Inspect the relevant existing implementation.
2. Understand the current architecture.
3. Make the smallest reasonable change.
4. Avoid unrelated refactoring.

After modifying code:

1. Run the relevant tests.
2. Run the complete test suite:

    python -m pytest -q

3. Report any failing tests clearly.

Do not claim a feature works without testing it.

## Testing

Existing tests are important project contracts.

Do not delete or weaken tests merely to make the test suite pass.

When adding a feature, add tests for:
- normal behavior
- invalid input
- error handling
- security-sensitive behavior where applicable

## Git

Do not automatically:
- `git add`
- `git commit`
- `git push`
- modify remotes

unless explicitly requested by the user.

Read-only Git inspection is allowed.

## Communication

When explaining changes:

- Be concise.
- Explain the reason for architectural changes.
- Mention affected files.
- Mention tests executed.
- Do not invent results.

## Important Principle

Laptop AI must remain a controlled system.

The LLM decides what it wants to accomplish.

The application decides what the LLM is actually allowed to execute.
