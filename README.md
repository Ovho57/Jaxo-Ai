# JAXO

**Your terminal. Your AI. Your workflow.**

JAXO is a standalone, general-purpose terminal AI assistant. It can chat, reason, help with code, create folders and files in its workspace, and assemble multi-file project drafts with your approval.

## Current capabilities
- Local first-run account creation and login.
- OpenRouter-compatible model connection.
- General-purpose terminal conversation.
- Workspace folder creation, file creation, listing and reading.
- Multi-file project creation with path validation and explicit confirmation.
- Early Evolution Engine foundation: source inventory, improvement planning, backups and test runner.

## Not yet implemented
- Automatic self-modification (patch application is disabled).
- GitHub repository creation/publishing from inside JAXO.
- Browser automation and unrestricted terminal execution.
- Verified end-to-end runtime on all operating systems.

## Quick start
See [Installation](docs/INSTALLATION.md).

## Safety
JAXO's file tools are restricted to `workspace/`. Writes require confirmation. Do not put API keys or passwords in prompts or generated project files. Keep `.env` private.

## Development
Run tests with:
```bash
python -m unittest discover -s tests -v
```

JAXO is under active development. Features are documented as implemented only after they are tested.
