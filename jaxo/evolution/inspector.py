from pathlib import Path

PROTECTED = {".env", ".env.example", "auth.py", "secrets.py"}


def inspect_source(root: Path) -> list[str]:
    root = root.resolve()
    findings = []
    for path in root.rglob("*.py"):
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            findings.append(f"Could not read {path.relative_to(root)}")
            continue
        findings.append(f"{path.relative_to(root)}: {len(text.splitlines())} lines")
    return findings
