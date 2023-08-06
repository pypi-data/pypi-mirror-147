from typing import Any

class ValidationError(Exception):
    code: Any
    timestamp: Any
    def __init__(self, message, code, timestamp: Any | None = ...) -> None: ...

class LicenseError(Exception): ...
