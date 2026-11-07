# JAXO

**Your terminal. Your AI. Your workflow.**

JAXO is a standalone, general-purpose terminal AI assistant. It can chat, reason, help with code, create files and projects in its workspace, inspect its own readable source, inspect public websites, and perform basic phishing-risk triage.

## Current capabilities
- Local first-run account creation and login.
- OpenRouter-compatible model connection.
- Animated terminal thinking and tool-activity indicators.
- Workspace folder creation, file creation, listing and reading.
- Multi-file project creation with path validation and explicit confirmation.
- Read-only inspection of JAXO's own source, tests and documentation.
- Public website inspection for HTML and plain-text pages.
- Heuristic phishing checks for suspicious URL patterns, redirects, password fields and cross-domain form destinations.
- Optional spoken replies and microphone input (install `requirements-voice.txt`).

## Voice setup
Install the optional voice packages:
```bash
pip install -r requirements-voice.txt
```
Inside JAXO, use `/voice` to toggle spoken answers and `/listen` to dictate a prompt. Microphone input uses the Google speech-recognition web service and therefore needs an internet connection. PyAudio may require operating-system audio development libraries; see the installation guide if it fails.

## Phishing-check limitations
The phishing checker uses URL and page-structure heuristics. It is not an antivirus engine or a live threat-intelligence reputation service. It may miss new phishing pages and may flag legitimate pages. A "no obvious warning signs" result is not proof of safety. Never enter credentials or payment information on a page you do not independently trust.

## Website inspection limits
JAXO fetches public HTML and plain text. It does not execute JavaScript, sign in, bypass paywalls or access controls, or inspect private pages. Sites that render content only in a browser may return little readable text.

## Not yet implemented
- Reviewed self-modification / automatic patch application.
- GitHub repository creation and publishing from inside JAXO.
- Full graphical browser automation.
- Unrestricted terminal execution.
- Verified end-to-end runtime on all operating systems.

## Premium key portal

The optional password-protected key portal is in [premium-key-portal](premium-key-portal/README.md). It requires a Cloudflare account and server-side secrets; do not publish the portal password or key in source files.

## Quick start
See [Installation](docs/INSTALLATION.md).

## Safety
Workspace writes require confirmation. Website requests block private/local network addresses and limit response size and redirects. Never put API keys or passwords in prompts or generated project files. Keep `.env` private.

## Development
Run tests with:
```bash
python -m unittest discover -s tests -v
```

JAXO is under active development. Features are documented as implemented only after they are tested.
