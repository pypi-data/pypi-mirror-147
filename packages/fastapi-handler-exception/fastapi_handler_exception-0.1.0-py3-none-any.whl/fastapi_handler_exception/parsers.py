# Built-In
from http import HTTPStatus
from typing import Any, Dict

# Third-Party
from fastapi import Request
from fastapi.responses import JSONResponse


def parse_exception(
    request: Request,
    exception: Exception,
    status_code: int,
    show_error: bool = False,
    show_detail: bool = True,
    show_message: bool = True,
    show_data: bool = False,
) -> Dict[str, Any]:
    content = {}

    if show_error:
        try:
            exception_class = exception.__class__
            exception_model = f"{exception_class.__module__}.".replace("builtins.", "")
            content["error"] = f"{exception_model}{exception_class.__name__}"
        except AttributeError:
            content["error"] = "Exception"

    if show_detail:
        try:
            content["detail"] = HTTPStatus(status_code).phrase
        except ValueError:
            content["detail"] = "Unknown Error"

    if show_message:
        content["error_message"] = str(exception) or "unknown_error"

    if show_data and (data := getattr(exception, "data")):
        content["data"] = data


    return content


def response_exception(
    request: Request, content: Any, status_code: int = 500
) -> JSONResponse:
    return JSONResponse(content=content, status_code=status_code)
