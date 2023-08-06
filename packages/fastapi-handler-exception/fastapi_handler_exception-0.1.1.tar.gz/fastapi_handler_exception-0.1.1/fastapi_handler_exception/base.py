# Built-In
from typing import Any, Callable, Type, Iterable, Dict, Tuple, Union

# Third-Party
from fastapi import FastAPI, Request
from fastapi.responses import Response

# Internal
from fastapi_handler_exception.parsers import parse_exception, response_exception


class HandlerExceptionSetter:
    def __init__(
        self,
        force_status_code: bool = False,
        *,
        content_callback: Callable[[Request, Exception, int], Any] = parse_exception,
        response_callback: Callable[[Request, Any, int], Response] = response_exception,
        content_callback_kwargs: Dict[str, Any] = {},
        response_callback_kwargs: Dict[str, Any] = {},
    ):
        self.force_status_code = force_status_code
        self.content_callback = content_callback
        self.content_callback_kwargs = content_callback_kwargs
        self.response_callback = response_callback
        self.response_callback_kwargs = response_callback_kwargs

    def create_exception_handler(
        self, exception_class: Type[Exception], status_code: int = 500
    ) -> Callable[[Request, Exception], Response]:
        def exception_handler(request: Request, exception: exception_class) -> Response:
            if self.force_status_code:
                _status_code = status_code
            else:
                _status_code = getattr(exception, "status_code", status_code)

            content = self.content_callback(
                request, exception, _status_code, **self.content_callback_kwargs
            )
            response = self.response_callback(
                request, content, _status_code, **self.response_callback_kwargs
            )
            return response

        return exception_handler

    def add_handlers(
        self, app: FastAPI, handlers: Iterable[Tuple[Type[Exception], int]]
    ) -> Dict[Union[int, Type[Exception]], Callable]:
        for handler in handlers:
            exception_handler = self.create_exception_handler(handler[0], handler[1])
            app.add_exception_handler(handler[0], exception_handler)

        return app.exception_handlers
