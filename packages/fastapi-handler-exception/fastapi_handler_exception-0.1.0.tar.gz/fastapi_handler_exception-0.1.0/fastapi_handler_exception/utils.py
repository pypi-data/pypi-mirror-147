# Built-In
from typing import Any

def add_code(exception: Exception, status_code: int) -> Exception:
    setattr(exception, "status_code", status_code)
    return exception

def add_data(exception: Exception, data: Any) -> Exception:
    setattr(exception, "data", data)
    return exception
