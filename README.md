# ⚡ JAXO AI

<p align="center">
  <strong>Your ideas. Your AI. Your terminal.</strong><br>
  A standalone AI assistant built to help you think, create, code, and get things done.
</p>

<p align="center">
  <a href="#-what-jaxo-can-do">Features</a> •
  <a href="#-get-started">Get started</a> •
  <a href="#-premium-access">Premium</a> •
  <a href="#-safety--transparency">Safety</a>
</p>

---

## 🚀 Meet JAXO

JAXO is a Python-based, terminal AI assistant designed to be more than a chatbot. It can hold conversations, help with coding, work with files in its workspace, build project structures, and inspect its own readable source code.

Whether you're planning an idea, learning something new, or building your next project, JAXO is ready in your terminal.

## ✨ What JAXO can do

- 💬 **AI conversations** — ask questions, explore ideas, and get help.
- 🧠 **Thinking experience** — animated terminal thinking and tool-activity indicators.
- 🧑‍💻 **Coding assistance** — get help understanding and working with code.
- 📁 **Workspace tools** — create folders and files, list contents, and read files.
- 🏗️ **Project building** — generate multi-file project structures with path checks and confirmation.
- 🔍 **Source inspection** — read JAXO's own accessible source, tests, and documentation.
- 🌐 **Website inspection** — retrieve and inspect public HTML and plain-text pages.
- 🛡️ **Basic phishing checks** — flag suspicious URL and page patterns.
- 🎙️ **Optional voice** — speak prompts and hear spoken replies with the voice packages installed.

> JAXO is actively being developed. Check the sections below for current limitations.

## ⚡ Get started

### 1. Clone the repository

```bash
git clone -b jaxo-standalone https://github.com/Ovho57/Jaxo-Ai.git
cd Jaxo-Ai
```

### 2. Set up Python

Create and activate a virtual environment:

```bash
python -m venv .venv
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure your AI connection

Follow the [Installation Guide](docs/INSTALLATION.md) to configure your model provider and environment settings.

### 4. Launch JAXO

```bash
python main.py
```

That's it. Start chatting and explore the commands available inside JAXO.

## 👑 Premium access

Want to unlock JAXO's premium features?

1. Open the [JAXO Premium Key](premium-key/KEY.txt) file.
2. Copy the key.
3. Start JAXO and enter `/license`.
4. Paste the key when prompted.

**Important:** The key file is in this repository. Anyone who can access the repository can read it, so this setup is convenient key sharing—not private or secure license distribution.

## 🎙️ Optional voice setup

Install the voice dependencies:

```bash
pip install -r requirements-voice.txt
```

Then use `/voice` to toggle spoken replies and `/listen` to dictate a prompt.

Microphone input uses Google's speech-recognition web service and requires an internet connection. PyAudio may also need operating-system audio libraries.

## 🛡️ Safety & transparency

- Workspace writes require confirmation.
- Website requests block private/local network addresses and limit response size and redirects.
- The phishing checker uses heuristics; it is not antivirus software or a live threat-intelligence service.
- A page with no obvious warning signs is **not guaranteed safe**.
- JAXO does not execute website JavaScript, sign in to websites, bypass paywalls, or access private pages.
- Keep API keys and passwords out of prompts and generated files. Never commit your `.env` file.

## 🧭 What's still being built

Some planned capabilities are not implemented yet, including:

- Reviewed self-modification and automatic patch application.
- GitHub repository creation and publishing from inside JAXO.
- Full graphical browser automation.
- Unrestricted terminal execution.
- Verified end-to-end runtime support on every operating system.

## 🧪 Run the tests

```bash
python -m unittest discover -s tests -v
```

## 🤝 Contribute

Found a bug or have an idea? Open an issue or submit a pull request. Clear bug reports and focused improvements are always welcome.

---

<p align="center">
  <strong>⚡ JAXO AI — Build boldly. Think freely.</strong><br>
  <sub>Made for curious minds and builders.</sub>
</p>
