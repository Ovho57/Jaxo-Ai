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

All generated files are created under `workspace/`.


## Optional voice support
Voice is optional; JAXO works without it. To add spoken replies and microphone input:
```bash
pip install -r requirements-voice.txt
```
Then run JAXO and use `/voice` to toggle spoken responses or `/listen` to dictate a prompt.

On Linux/WSL, PyAudio may need PortAudio development headers and a microphone device. WSL microphone passthrough is not available in every setup. On Windows, if PyAudio installation fails, install a compatible PyAudio wheel or use a supported Python version. Microphone transcription uses Google's speech-recognition web service; audio is sent to that service for transcription.


## JAXO Premium key portal

The premium key is distributed through the separately deployed password-protected portal in `premium-key-portal/`. The portal password and premium key are configured as Cloudflare Worker secrets; never put either value in the repository or a public `.env` file.

See [the portal deployment guide](../premium-key-portal/README.md).