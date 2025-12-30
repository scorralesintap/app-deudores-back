from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from .exception_handler import (
    validation_exception_handler,
    general_exception_handler,
)

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)