# JAXO

**Your terminal. Your AI. Your workflow.**

JAXO is a standalone, general-purpose terminal AI assistant. It can chat, reason, help with code, create files and projects in its workspace, inspect its own readable source, and retrieve readable text from public websites.

## Current capabilities
- Local first-run account creation and login.
- OpenRouter-compatible model connection.
- General-purpose terminal conversation with an animated Rich thinking indicator.
- Workspace folder creation, file creation, listing and reading.
- Multi-file project creation with path validation and explicit confirmation.
- Read-only inspection of JAXO's own source, tests and documentation.
- Public website inspection for HTML and plain-text pages.

## Website inspection limits
JAXO can fetch public pages over HTTP/HTTPS and extract readable text. It does not execute JavaScript, sign in, bypass paywalls or access controls, or inspect private pages. Some modern sites render their content only in the browser and may return little or no readable text.

## Not yet implemented
- Reviewed self-modification / automatic patch application.
- GitHub repository creation and publishing from inside JAXO.
- Full graphical browser automation.
- Unrestricted terminal execution.
- Verified end-to-end runtime on all operating systems.

## Quick start
See [Installation](docs/INSTALLATION.md).

## Safety
Workspace writes require confirmation. Website inspection blocks localhost/private network addresses, limits response size and redirects, and reads HTML/plain text only. Never put API keys or passwords in prompts or generated project files. Keep `.env` private.

## Development
Run tests with:
```bash
python -m unittest discover -s tests -v
```

JAXO is under active development. Features are documented as implemented only after they are tested.
