import pwsh_agent.powershell.exec as pwsh
from pwsh_agent.config import SCRIPTS_DIR

def list_files(path) -> str:
    """List files in the specified directory."""
    return pwsh.run(
        str(SCRIPTS_DIR / "list_files.ps1"),
        "-Path", path
    )


def get_current_directory() -> str:
    """Get the current working directory."""
    return pwsh.run(str(SCRIPTS_DIR / "get_current_directory.ps1"))


def find_files(path, pattern, limit=50) -> str:
    """Find files in the specified directory matching the pattern."""
    return pwsh.run(
        str(SCRIPTS_DIR / "find_files.ps1"),
        "-Path", path,
        "-Pattern", pattern,
        "-First", str(limit)
    )