from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from fastapi import status
from ..settings import ALGORITHM, SECRET_KEY

def get_user_id(request: Request):
    return verify_token(request)


def verify_token(request: Request, token: Optional[str] = None) -> Optional[str]:
    if token is None:
        token = get_token(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise status.HTTP_401_UNAUTHORIZED
    except Exception:
        raise status.HTTP_401_UNAUTHORIZED
    return user_id


def get_token(request: Request, auto_error=True):
    authorization: str = request.cookies.get("access_token")
    print(f"token:{authorization}")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        if auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return None
    return param


def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return ip