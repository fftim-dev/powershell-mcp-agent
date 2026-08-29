from enum import StrEnum
from typing import Any
import json


class ToolStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"


class ToolResult():
    def __init__(self, status: ToolStatus, content: Any = None, error: str | None = None, meta: dict | None = None):
        self.status = status
        self.content = content
        self.error = error
        self.meta = meta or {}

    @property
    def dict(self):
        return {
            "status": self.status.value,
            "content": self.content,
            "error": self.error,
            "meta": self.meta
        }

    @property
    def json(self):
        return json.dumps(self.dict)