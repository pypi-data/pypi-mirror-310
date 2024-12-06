import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware

from ..config import StarbearServerPlugin


class APITokensMiddleware(BaseHTTPMiddleware):
    """Allow access to certain routes based on API tokens.

    Arguments:
        app: The application this middleware is added to.
    """

    def __init__(self, app, mapper):
        super().__init__(app)
        self.mapper = mapper

    async def dispatch(self, request, call_next):
        key = request.headers.get("X-API-KEY", None)
        if not key:
            return await call_next(request)
        user = self.mapper(key)
        if user:
            request.session["user"] = user
        return await call_next(request)


@dataclass
class TokenData:
    email: str
    expiry: Optional[datetime.datetime] = None
    plain: bool = True


@dataclass
class APITokens(StarbearServerPlugin):
    # Configuration file in which the tokens are located
    file: Optional[Path] = None

    # Default tokens
    defaults: Optional[dict[str, TokenData]] = None

    def cap_require(self):
        return ["session"]

    def cap_export(self):
        return ["email"]

    def setup(self, server):
        server.app.add_middleware(
            APITokensMiddleware,
            mapper=None,
        )
