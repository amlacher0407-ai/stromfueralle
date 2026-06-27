from fastapi import Request
from sqlalchemy.orm import Session

from app.database import get_db  # noqa: F401 — re-exported for routes


class NotAuthenticatedException(Exception):
    pass


def require_login(request: Request) -> str:
    user = request.session.get("user")
    if not user:
        raise NotAuthenticatedException()
    return user
