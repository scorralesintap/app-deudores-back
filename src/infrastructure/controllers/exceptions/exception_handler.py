import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


def create_error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": False,
            "data": None,
            "message": message
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    messages = []
    for error in errors:
        msg = error["msg"]
        if msg.startswith("Value error, "):
            msg = msg.replace("Value error, ", "")
        messages.append(msg)
    message = "; ".join(messages) if messages else "Error de validación"
    return create_error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Exception: {str(exc)} - Path: {request.url.path}", exc_info=True)
    return create_error_response(status.HTTP_400_BAD_REQUEST, str(exc))