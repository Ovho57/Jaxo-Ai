# Installation

JAXO is currently in early development. These are the intended setup steps for the Python application. The source files must be published in the repository before the final run step will work.

## Requirements

- Python 3.10 or newer
- Git
- An API key from the model provider configured by the application (currently planned around OpenRouter)

## Linux, macOS, and WSL

### 1. Clone the project

```bash
git clone https://github.com/Ovho57/Jaxo-Ai.git
cd Jaxo-Ai
```

### 2. Create and activate a virtual environment

Linux, macOS, or WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

When `requirements.txt` is present:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your API key

Create a local `.env` file in the project root. Do not upload this file to GitHub.

Example configuration (use the variable names required by the application):

```env
OPENROUTER_API_KEY=put_your_key_here
MODEL=openai/gpt-4o-mini
```

Replace the example value with your own key. Never paste your real key into an issue or public chat.

### 5. Run JAXO

The planned entry point is:

```bash
python main.py
```

This command will work once `main.py` and the JAXO source package have been added to the repository.

## Windows

Open PowerShell in the project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
```

Create the local `.env` file as described above. The planned launch command is `py main.py`, once the application source is published.

If PowerShell blocks virtual-environment activation, see Microsoft's execution-policy documentation or use WSL.

## Updating

After the source is published, update your local checkout with:

```bash
git pull
pip install -r requirements.txt
```

## Important

This repository currently contains setup documentation, not the complete runnable application. Check the README and repository files for updates before troubleshooting launch errors.
