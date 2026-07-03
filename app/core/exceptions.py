from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings


# ── Domain Exceptions ──────────────────────────────────────────────────────────

class AppException(Exception):
    """Base exception for all application-level errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: int | str) -> None:
        super().__init__(
            message=f"{resource} with id '{identifier}' not found.",
            status_code=404,
        )


class ConflictException(AppException):
    """Raised when a resource already exists or a conflict is detected."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=409)


# ── Exception Handlers ─────────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "meta": None,
                "data": None,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation failed",
                "meta": {"errors": exc.errors()},
                "data": None,
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
            content={
                "success": False,
                "message": exc.detail,
                "meta": None,
                "data": None,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        message = str(exc) if settings.debug else "Internal server error"
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": message,
                "meta": None,
                "data": None,
            },
        )
