"""Validated multi-file project creation inside the JAXO workspace."""
from pathlib import PurePosixPath
from rich.prompt import Confirm
from jaxo.tools import WORKSPACE, _safe_target, MAX_FILE_BYTES


def build_project(project_name: str, files: dict[str, str], console) -> str:
    if not project_name.strip() or not files or len(files) > 60:
        return "Project must have a name and between 1 and 60 files."
    prepared = []
    total = 0
    try:
        for relative, content in files.items():
            path = PurePosixPath(relative)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise ValueError(f"Unsafe path: {relative}")
            target = _safe_target(f"{project_name}/{relative}")
            if target.exists():
                raise FileExistsError(f"Refusing to overwrite existing path: {target.relative_to(WORKSPACE)}")
            if not isinstance(content, str):
                raise ValueError(f"Content for {relative} must be text.")
            size = len(content.encode("utf-8"))
            if size > MAX_FILE_BYTES:
                raise ValueError(f"File too large: {relative}")
            total += size
            prepared.append((target, content))
        if total > 2_000_000:
            raise ValueError("Project exceeds the 2 MB total content limit.")
        console.print(f"JAXO proposes creating {len(prepared)} files in workspace/{project_name}/")
        for target, _ in prepared:
            console.print(f"  • {target.relative_to(WORKSPACE)}")
        if not Confirm.ask("Create this project?", default=False):
            return "Project creation cancelled."
        # All paths are validated before the first write. Never overwrite existing files.
        for target, content in prepared:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return f"Created project '{project_name}' with {len(prepared)} files."
    except (OSError, ValueError) as exc:
        return f"Project was not created: {exc}"
