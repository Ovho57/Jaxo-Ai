import os
from pathlib import Path
from rich.prompt import Confirm

WORKSPACE = (Path.cwd() / "workspace").resolve()
MAX_FILE_BYTES = 500_000


def _safe_target(relative_path: str) -> Path:
    raw = Path(relative_path)
    if not relative_path.strip() or raw.is_absolute() or ".." in raw.parts:
        raise ValueError("Use a non-empty relative path inside workspace; '..' and absolute paths are blocked.")
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    target = (WORKSPACE / raw).resolve()
    if target != WORKSPACE and WORKSPACE not in target.parents:
        raise ValueError("Path escapes the workspace.")
    current = WORKSPACE
    for part in raw.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlinks are not allowed in workspace paths.")
    return target


def create_folder(path: str, console) -> str:
    try:
        target = _safe_target(path)
        if target.exists():
            return f"Already exists: {target.relative_to(WORKSPACE)}"
        if not Confirm.ask(f"Create folder [cyan]{target.relative_to(WORKSPACE)}[/cyan]?", default=False):
            return "Cancelled."
        target.mkdir(parents=True, exist_ok=False)
        return f"Created folder: {target.relative_to(WORKSPACE)}"
    except (OSError, ValueError) as exc:
        return f"Could not create folder: {exc}"


def create_file(path: str, content: str, console) -> str:
    try:
        target = _safe_target(path)
        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            return "File is too large (500 KB limit)."
        if target.exists() and not target.is_file():
            return "Target exists and is not a file."
        action = "replace" if target.exists() else "create"
        if not Confirm.ask(f"{action.title()} [cyan]{target.relative_to(WORKSPACE)}[/cyan]?", default=False):
            return "Cancelled."
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(target.name + ".jaxo-tmp")
        temp.write_text(content, encoding="utf-8")
        os.replace(temp, target)
        return f"Saved file: {target.relative_to(WORKSPACE)}"
    except (OSError, ValueError) as exc:
        return f"Could not write file: {exc}"


def read_file(path: str) -> str:
    target = _safe_target(path)
    if not target.is_file():
        raise FileNotFoundError("File not found.")
    if target.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("File exceeds 500 KB read limit.")
    return target.read_text(encoding="utf-8")


def list_files(path: str = ".") -> str:
    target = _safe_target(path) if path != "." else WORKSPACE
    if not target.is_dir():
        raise NotADirectoryError("Folder not found.")
    entries = []
    for item in sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        marker = "/" if item.is_dir() else ""
        entries.append(item.name + marker)
    return "\n".join(entries) if entries else "(empty folder)"


def workspace_tree() -> str:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    lines = [f"workspace/"]
    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", ".venv"})
        depth = len(Path(root).relative_to(WORKSPACE).parts)
        for name in sorted(files):
            lines.append("  " * (depth + 1) + name)
        for name in dirs:
            lines.append("  " * (depth + 1) + name + "/")
    return "\n".join(lines)


TOOL_SPECS = [
    {"type": "function", "function": {"name": "create_folder", "description": "Create a folder inside the JAXO workspace. Always explain the intended path first; the user must approve.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Relative folder path inside workspace"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "create_file", "description": "Create or replace a UTF-8 text file inside the JAXO workspace. The user must approve the write.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "list_files", "description": "List entries in a workspace folder.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "default": "."}}, "required": []}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a text file in the workspace, up to 500 KB.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
]
