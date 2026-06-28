"""FastAPI application entrypoint (CP1 scaffolding).

- Mounts the /api/v1 router (health only for CP1).
- Consistent error envelope: {code, message, details, correlation_id}.
- CORS placeholder (origins from config.md active profile).
No business logic, auth, DB, or AI here — those arrive in later coding prompts.
"""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(
    title=settings.get("app_name", "Agentic AI Strategic Governance Platform"),
    version=settings.get("version", "0.1.0"),
)

# --- CORS placeholder (restrict to approved frontend origin) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get("cors_origins", ["http://localhost:5173"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _envelope(code: str, message: str, details=None) -> dict:
    return {
        "code": code,
        "message": message,
        "details": details,
        "correlation_id": str(uuid.uuid4()),
    }


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content=_envelope(f"http_{exc.status_code}", str(exc.detail)))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422,
                        content=_envelope("validation_error", "Request validation failed", exc.errors()))


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content=_envelope("internal_error", "An unexpected error occurred"))


# --- Routers under /api/v1 ---
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {"name": settings.get("app_name"), "see": "/api/v1/health"}
