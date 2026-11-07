import os
from pathlib import Path
from rich.prompt import Confirm

WORKSPACE = (Path.cwd() / "workspace").resolve()
SOURCE_ROOT = Path(__file__).resolve().parent.parent
MAX_FILE_BYTES = 500_000
SOURCE_EXTENSIONS = {".py", ".md", ".toml", ".txt", ".yml", ".yaml"}
SOURCE_EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "workspace", ".pytest_cache"}
SOURCE_EXCLUDED_NAMES = {".env", ".env.example", ".env.local", ".env.production"}


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


def _safe_source_target(relative_path: str) -> Path:
    raw = Path(relative_path)
    if not relative_path.strip() or raw.is_absolute() or ".." in raw.parts:
        raise ValueError("Use a relative source path; absolute paths and '..' are blocked.")
    if any(part in SOURCE_EXCLUDED_DIRS for part in raw.parts):
        raise ValueError("That source location is excluded.")
    if raw.name in SOURCE_EXCLUDED_NAMES or raw.name.startswith(".env"):
        raise ValueError("Environment and secret files are never readable by JAXO.")
    target = SOURCE_ROOT / raw
    if target.is_symlink():
        raise ValueError("Symlinked source files are not readable.")
    resolved = target.resolve()
    if resolved != SOURCE_ROOT and SOURCE_ROOT not in resolved.parents:
        raise ValueError("Source path escapes the JAXO installation.")
    if resolved.suffix.lower() not in SOURCE_EXTENSIONS:
        raise ValueError("Only source, documentation, and text configuration files can be read.")
    if not resolved.is_file():
        raise FileNotFoundError("Source file not found.")
    if resolved.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Source file exceeds the 500 KB read limit.")
    return resolved


def list_source_files() -> str:
    """List readable files in JAXO's own installation, excluding secrets and runtime data."""
    entries = []
    for path in sorted(SOURCE_ROOT.rglob("*")):
        relative = path.relative_to(SOURCE_ROOT)
        if any(part in SOURCE_EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        if path.name in SOURCE_EXCLUDED_NAMES or path.name.startswith(".env"):
            continue
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            entries.append(relative.as_posix())
    return "\n".join(entries) if entries else "(no readable source files found)"


def read_source_file(path: str) -> str:
    """Read one allowlisted file from JAXO's own source tree. Read-only; never exposes .env."""
    target = _safe_source_target(path)
    return target.read_text(encoding="utf-8")


def create_folder(path: str, console=None) -> str:
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


def create_file(path: str, content: str, console=None) -> str:
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
        entries.append(item.name + ("/" if item.is_dir() else ""))
    return "\n".join(entries) if entries else "(empty folder)"


def workspace_tree() -> str:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    lines = ["workspace/"]
    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", ".venv"})
        depth = len(Path(root).relative_to(WORKSPACE).parts)
        for name in sorted(dirs):
            lines.append("  " * (depth + 1) + name + "/")
        for name in sorted(files):
            lines.append("  " * (depth + 1) + name)
    return "\n".join(lines)


TOOL_SPECS = [
    {"type": "function", "function": {"name": "create_folder", "description": "Create a folder inside the JAXO workspace. The user must approve.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "create_file", "description": "Create or replace a UTF-8 text file inside the JAXO workspace. The user must approve.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "create_project", "description": "Create a multi-file project in the JAXO workspace. Provide a project folder name and a map of relative file paths to text contents. User approval is required.", "parameters": {"type": "object", "properties": {"name": {"type": "string"}, "files": {"type": "object", "additionalProperties": {"type": "string"}}}, "required": ["name", "files"]}}},
    {"type": "function", "function": {"name": "list_files", "description": "List entries in a workspace folder.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "default": "."}}, "required": []}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a text file in the workspace, up to 500 KB.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "list_source_files", "description": "List JAXO's own readable source files, tests, documentation and text configuration. Secrets, environment files, virtual environments and workspace data are excluded.", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "read_source_file", "description": "Read one file from JAXO's own source tree. Read-only; .env and secret files are blocked. Use list_source_files first to discover paths.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}}
]
