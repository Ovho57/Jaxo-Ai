"""Guarded patch application. This module deliberately does not auto-edit source."""
from pathlib import Path


def validate_patch_targets(root: Path, relative_paths: list[str]) -> list[Path]:
    root = root.resolve()
    protected = {"auth.py", "client.py", ".env", ".env.example"}
    targets = []
    for item in relative_paths:
        candidate = Path(item)
        if candidate.is_absolute() or ".." in candidate.parts or candidate.name in protected:
            raise ValueError(f"Protected or unsafe self-edit target: {item}")
        target = (root / candidate).resolve()
        if root not in target.parents:
            raise ValueError(f"Target escapes project root: {item}")
        targets.append(target)
    return targets


def apply_patch(*_args, **_kwargs):
    raise NotImplementedError(
        "Automatic self-editing is not enabled yet. The Evolution Engine currently supports "
        "inspection and planning only; reviewed diff application and rollback will be added "
        "after dedicated isolation and security tests."
    )
