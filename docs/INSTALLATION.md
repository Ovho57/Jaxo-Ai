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


## Premium key email delivery (optional)

To let users request the shared JAXO Premium key by email, configure an SMTP account in your private `.env` file. Copy the SMTP host, port, username, app password, and verified sender address from your email provider:

```dotenv
JAXO_SMTP_HOST=smtp.your-provider.example
JAXO_SMTP_PORT=587
JAXO_SMTP_USER=your-smtp-username
JAXO_SMTP_PASSWORD=your-smtp-app-password
JAXO_EMAIL_FROM=JAXO <verified-sender@example.com>
```

Never commit `.env` or share SMTP credentials. The public `.env.example` contains placeholders only. Without these settings, the email option displays a setup message and does not claim that an email was sent. The email option sends the same shared key to any address entered; it is not individual paid licensing or identity verification.
