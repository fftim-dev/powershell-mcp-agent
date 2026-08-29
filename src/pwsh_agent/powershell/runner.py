import subprocess
from .result import PwshResult

def run(script: str, *args) -> PwshResult:
    """Run a command in PowerShell and return the output."""
    if not script:
        return PwshResult(stdout="", stderr="No script provided.", exit_code=1)
    
    result = subprocess.run(
        ["powershell", "-NoProfile", "-File", script, *args],
        capture_output=True, 
        text=True
    )

    return PwshResult(stdout=result.stdout.strip(), stderr=result.stderr.strip(), exit_code=result.returncode)