import subprocess
import sys
from pathlib import Path


def run_tests(project_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=project_root,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
