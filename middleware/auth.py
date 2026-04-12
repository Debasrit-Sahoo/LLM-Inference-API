from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings

class GatewayAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("X-Internal-Gateway-Auth")

        if token != settings.gateway_secret:
            raise HTTPException(status_code=401, detail="unauthorized")

        return await call_next(request)