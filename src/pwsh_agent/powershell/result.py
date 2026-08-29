class PwshResult:
    def __init__(self, stdout, stderr, exit_code, truncated=False):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.truncated = truncated

    @property
    def success(self) -> bool:
        return self.exit_code == 0