"""Rollback is intentionally backup-restore only; no automatic execution yet."""
from pathlib import Path
import shutil


def restore_backup(backup: Path, destination: Path, *, approved: bool = False) -> None:
    if not approved:
        raise PermissionError("Explicit user approval is required to restore a backup.")
    backup, destination = backup.resolve(), destination.resolve()
    if not backup.is_dir() or not destination.is_dir():
        raise ValueError("Backup and destination must both be existing directories.")
    for child in destination.iterdir():
        if child.name in {".env", ".git", ".venv"}:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for child in backup.iterdir():
        target = destination / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)
