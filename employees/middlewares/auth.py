from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from fastapi import status
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


from employees.web.settings import Settings
from employees.repository.auth_repository import AuthRepository


settings = Settings()


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request, call_next
    ) -> Response:

        if request.url.path in [
            "/docs",
            "/openapi/employees.json",
            "/auth/login",
            "/auth/register",
            "/openapi.json"
        ]:
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content='Usuario no autorizado'
            )
        try:
            auth = AuthRepository()
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = auth.valid_token(auth_token, secret=settings.jwt_secret)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            request.state.user_id = token_payload.get('id')
        return await call_next(request)
