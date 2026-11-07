# JAXO Roadmap

JAXO is an early-stage project. This roadmap describes direction, not promises or completed features.

## Current focus

- [ ] Publish and organize the complete Python source
- [ ] Verify clean installation on Linux, Windows, and WSL
- [ ] Stabilize OpenRouter chat and error handling
- [ ] Keep the terminal interface compact and readable
- [ ] Test GitHub tools and document their limits
- [ ] Add basic automated tests

## Planned improvements

- [ ] Safer local file editing with explicit approval
- [ ] Clear tool-use confirmations and useful error messages
- [ ] Better conversation history and session controls
- [ ] More robust GitHub repository workflows
- [ ] Optional specialist workflows behind one JAXO assistant identity
- [ ] Browser integration research, with user approval and clear permissions

## Security and reliability goals

- Never store API keys in source control.
- Keep local workspace data out of public commits.
- Validate file paths before reading or writing.
- Require confirmation before potentially destructive actions.
- Make tool permissions and limitations visible.
- Test changes before describing them as working.

## Status labels

- **Done:** implemented and tested.
- **In progress:** actively being developed.
- **Planned:** not implemented yet.

A roadmap item should only be marked done after it has been implemented and verified.
