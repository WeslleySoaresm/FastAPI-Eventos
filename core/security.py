from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://meu-app-parceiro.com"
]

limiter = Limiter(key_func=get_remote_address)

def setup_security_middlewares(app: FastAPI) -> None:
    """Configura Rate Limiting, CORS e Cabeçalhos HTTP de Segurança."""
    # 1. Rate Limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # 3. Security Headers Middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response