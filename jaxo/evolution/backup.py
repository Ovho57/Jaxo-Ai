from pathlib import Path
import shutil
from datetime import datetime, timezone


def create_backup(source: Path, backup_root: Path) -> Path:
    source = source.resolve()
    backup_root.mkdir(parents=True, exist_ok=True)
    destination = backup_root / datetime.now(timezone.utc).strftime("backup-%Y%m%dT%H%M%SZ")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".env", ".venv", "__pycache__", ".git"))
    return destination
