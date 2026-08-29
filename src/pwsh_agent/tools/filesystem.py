import json
import pwsh_agent.powershell.runner as pwsh
from .result import ToolResult, ToolStatus
from pwsh_agent.powershell.result import PwshResult
from pwsh_agent.config import SCRIPTS_DIR

def list_files(path) -> ToolResult:
    """List files in the specified directory."""
    result = pwsh.run(
        str(SCRIPTS_DIR / "list_files.ps1"),
        "-Path", path
    )

    return serialize_tool_result(result)


def list_directory(path) -> ToolResult:
    """List all files and directories in the specified directory."""
    result = pwsh.run(
        str(SCRIPTS_DIR / "list_directory.ps1"),
        "-Path", path
    )

    return serialize_tool_result(result)


def get_current_directory() -> ToolResult:
    """Get the current working directory."""
    result = pwsh.run(
        str(SCRIPTS_DIR / "get_current_directory.ps1"),
        timeout=10,
        max_output=10_000
    )

    return serialize_tool_result(result)


def find_files(path, pattern, limit=50) -> ToolResult:
    """Find files in the specified directory matching the pattern."""
    result = pwsh.run(
        str(SCRIPTS_DIR / "find_files.ps1"),
        "-Path", path,
        "-Pattern", pattern,
        "-First", str(limit),
        timeout=45
    )

    return serialize_tool_result(result)


def serialize_tool_result(pwsh_result: PwshResult) -> ToolResult:
    """Convert a PwshResult to a ToolResult."""
    status=ToolStatus.SUCCESS if pwsh_result.success else ToolStatus.ERROR
    error=None if pwsh_result.success else pwsh_result.stderr

    try:
        content = json.loads(pwsh_result.stdout) if pwsh_result.success else None
    except json.JSONDecodeError:
        status = ToolStatus.ERROR
        content = None
        error = "Invalid JSON output from PowerShell"

    return ToolResult(
        status=status,
        content=content,
        error=error,
        meta={
            "exit_code": pwsh_result.exit_code,
            "truncated": pwsh_result.truncated
        }
    )