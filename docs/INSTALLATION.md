# Install JAXO

## Requirements
- Python 3.10+
- An OpenRouter API key

## Setup
```bash
git clone https://github.com/Ovho57/Jaxo-Ai.git
cd Jaxo-Ai
git checkout jaxo-standalone
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your OpenRouter key in `.env` as `OPENROUTER_API_KEY=...`. Never commit `.env`.

Run:
```bash
python main.py
```

The first run asks you to create a local JAXO username and password. Account data is stored in `~/.jaxo/account.json`; passwords are PBKDF2-HMAC-SHA256 hashes, not plaintext.

By default, JAXO uses the `workspace/` folder. You can select another existing folder at any time with:

```text
/folder /path/to/your/project
```

In WSL, a Windows Desktop folder commonly looks like `/mnt/c/Users/YourName/Desktop`. The selected folder is remembered for the next launch. JAXO can list and read text/code files there and create or edit files and folders. File writes require your approval; environment files and private keys are blocked from reading.


## Optional voice support
Voice is optional; JAXO works without it. To add spoken replies and microphone input:
```bash
pip install -r requirements-voice.txt
```
Then run JAXO and use `/voice` to toggle spoken responses or `/listen` to dictate a prompt.

On Linux/WSL, PyAudio may need PortAudio development headers and a microphone device. WSL microphone passthrough is not available in every setup. On Windows, if PyAudio installation fails, install a compatible PyAudio wheel or use a supported Python version. Microphone transcription uses Google's speech-recognition web service; audio is sent to that service for transcription.

