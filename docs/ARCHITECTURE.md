# JAXO standalone architecture

JAXO is one general-purpose assistant, not a collection of visible specialist agents.

## Core
- `main.py`: terminal entry point and local account gate.
- `jaxo/client.py`: OpenRouter-compatible chat transport.
- `jaxo/brain.py`: conversation loop and tool dispatch.
- `jaxo/tools.py`: workspace file/folder operations.
- `jaxo/project_builder.py`: multi-file project creation with preflight validation and confirmation.
- `jaxo/evolution/`: source inspection, planning, backups and test utilities.

## Workspace boundary
File tools operate only below `workspace/`. Absolute paths, parent traversal and symlink traversal are rejected. Writes require an interactive confirmation. Existing project-builder targets are never overwritten.

## Evolution status
The current Evolution Engine is an early foundation. It can inventory source files, produce a plan, create backups and run the test suite. Automatic source patch application is deliberately disabled. It must not edit authentication, API transport, environment files or its own safety checks. A future patch workflow must show a diff, require explicit approval, test in an isolated worktree, and support rollback before activation.
