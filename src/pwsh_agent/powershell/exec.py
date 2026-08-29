import subprocess

def run(script: str, *args) -> str:
    """Run a command in PowerShell and return the output."""
    if not script:
        return "No script provided."
    
    result = subprocess.run(
        ["powershell", "-NoProfile", "-File", script, *args],
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    
    return result.stdout.strip()