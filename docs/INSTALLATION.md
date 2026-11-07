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
