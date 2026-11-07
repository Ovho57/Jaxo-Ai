# Troubleshooting

JAXO is under active development. Some issues may be caused by missing application source files rather than your computer.

## The repository does not contain main.py

The application source has not yet been published. The command `python main.py` will fail until the project source is added.

## Python is not found

Check your installation:

```bash
python --version
python3 --version
```

On Windows, try:

```powershell
py --version
```

Install a supported Python version if none of these commands work.

## A module is missing

Activate the virtual environment, then install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the error names a package that is not in `requirements.txt`, report it with the full error message.

## API key or authentication errors

- Confirm that your local `.env` file is in the project root.
- Check that the variable name matches the version of JAXO you are running.
- Confirm that the key is active and has available provider credits.
- Do not post your API key in a GitHub issue or screenshot.

## Model or provider errors

Check the provider's service status, model availability, account limits, and the model identifier configured in your local environment.

## GitHub tool errors

- Confirm that Git is installed.
- Check that the repository URL is correct.
- Confirm that you have permission to access the repository.
- Do not assume a tool action succeeded unless JAXO reports a successful result.

## Syntax or import errors

Make sure you are running the intended project version and that all source files have been downloaded. Include the complete traceback when reporting a bug, but remove tokens, API keys, and private paths first.

## Reporting a problem

Open a GitHub issue at https://github.com/Ovho57/Jaxo-Ai/issues and include:

1. Your operating system and Python version.
2. The command you ran.
3. The complete error message with secrets removed.
4. Steps to reproduce the issue.
