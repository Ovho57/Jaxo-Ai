import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path

ACCOUNT_DIR = Path.home() / ".jaxo"
ACCOUNT_FILE = ACCOUNT_DIR / "account.json"
ITERATIONS = 310_000


def _derive(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS).hex()


def authenticate(console) -> bool:
    console.print("\n[bold green]JAXO local account[/bold green]")
    ACCOUNT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        os.chmod(ACCOUNT_DIR, 0o700)
    except OSError:
        pass

    if ACCOUNT_FILE.exists():
        console.print("[dim]Welcome back. Sign in to continue.[/dim]")
        try:
            account = json.loads(ACCOUNT_FILE.read_text(encoding="utf-8"))
            username = input("Username: ").strip()
            import getpass
            password = getpass.getpass("Password: ")
            salt = bytes.fromhex(account["salt"])
            valid = hmac.compare_digest(_derive(password, salt), account["password_hash"])
            if username == account["username"] and valid:
                console.print("[green]Login successful.[/green]\n")
                return True
            console.print("[red]Incorrect username or password.[/red]")
            return False
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            console.print("[red]Account file is invalid. Back it up and remove it to register again.[/red]")
            return False

    console.print("[yellow]First run: create your local JAXO account.[/yellow]")
    username = input("Choose a username: ").strip()
    import getpass
    password = getpass.getpass("Choose a password (12+ characters): ")
    confirm = getpass.getpass("Confirm password: ")
    if not username or len(password) < 12 or password != confirm:
        console.print("[red]Registration cancelled: use a username, matching passwords, and at least 12 characters.[/red]")
        return False

    salt = secrets.token_bytes(16)
    data = {"username": username, "salt": salt.hex(), "password_hash": _derive(password, salt), "iterations": ITERATIONS}
    fd = os.open(ACCOUNT_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
    console.print("[green]Account created. You are signed in.[/green]\n")
    return True
