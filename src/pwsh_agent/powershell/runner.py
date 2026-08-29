import subprocess
from .result import PwshResult
from pathlib import Path

def run(script: str, *args, timeout: int = 20, max_output: int = 100_000) -> PwshResult:
    """Run a command in PowerShell and return the output."""
    if not script:
        return PwshResult(stdout="", stderr="No script provided.", exit_code=1)
    if not Path(script).is_file():
        return PwshResult(stdout="", stderr=f"Script not found: {script}", exit_code=1)
    
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-File", script, *args],
            capture_output=True, 
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return PwshResult(stdout="", stderr="Command timed out.", exit_code=1)

    stdout = result.stdout.strip()
    return PwshResult(stdout=stdout[:max_output], stderr=result.stderr.strip(), exit_code=result.returncode, truncated=len(stdout)>max_output)