import uuid
from datetime import timedelta, datetime, timezone
from jose import jwt
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from fastapi.security.utils import get_authorization_scheme_param
from .users.schemas import Token, RefreshSessionUpdate
from .users.service import UserService
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from .users.DAO import UserDAO, RefreshSessionDAO
from .users.models import RefreshSessionModel
from .users.utils import Hasher
from .session import async_session



login_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"чек на валидность токена"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/loging/token")


class TokenUtils:

    @classmethod
    async def get_current_user(cls, token):
        user_id = cls.verify_token(None, token)
        async with async_session() as session:
            current_user = await UserService.get_object(session=session, object_id=uuid.UUID(user_id))
        return current_user

    @classmethod
    def verify_token(cls, request, token=None):
        if token is None:
            token = cls.get_token(request)
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise status.HTTP_404_NOT_FOUND
        except Exception:
            raise status.HTTP_400_BAD_REQUEST
        return user_id

    @classmethod
    def get_token(cls, request, auto_error=True):
        authorization: str = request.cookies.get("access_token")

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

    @classmethod
    async def create_token(cls, user_id: uuid.UUID):
        access_token = cls._create_access_token(user_id)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = cls._create_refresh_token()

        async with async_session() as session:
            await RefreshSessionDAO.add(
                session,
                user_id=user_id,
                refresh_token=refresh_token,
                expires_in=refresh_token_expires.total_seconds(),
            )
            await session.commit()
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @classmethod
    async def logout(cls, token: uuid.UUID) -> None:
        async with async_session() as session:
            refresh_session = await RefreshSessionDAO.find_one_or_none(
                session, RefreshSessionModel.refresh_token == token
            )
            if refresh_session:
                await RefreshSessionDAO.delete(session, id=refresh_session.id)
            await session.commit()

    @classmethod
    async def refresh_token(cls, token: uuid.UUID):
        async with async_session() as session:
            refresh_session = await RefreshSessionDAO.find_one_or_none(
                session, RefreshSessionModel.refresh_token == token
            )

            if refresh_session is None:
                raise status.HTTP_404_NOT_FOUND
            if datetime.now(timezone.utc) >= refresh_session.created_at + timedelta(
                    seconds=refresh_session.expires_in
            ):
                await RefreshSessionDAO.delete(session, id=refresh_session.id)
                raise status.HTTP_204_NO_CONTENT

            user = await UserDAO.find_one_or_none(session, id=refresh_session.user_id)
            if user is None:
                raise status.HTTP_404_NOT_FOUND

            access_token = cls._create_access_token(user.id)
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            refresh_token = cls._create_refresh_token()

            await RefreshSessionDAO.update(
                session,
                RefreshSessionModel.id == refresh_session.id,
                obj_in=RefreshSessionUpdate(
                    refresh_token=refresh_token,
                    expires_in=refresh_token_expires.total_seconds(),
                ),
            )
            await session.commit()
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        async with async_session() as session:
            db_user = await UserDAO.find_one_or_none(session, email=email)
        if db_user and Hasher.verify_password(db_user.password, password):
            return db_user
        return None

    @classmethod
    async def abort_all_sessions(cls, user_id: uuid.UUID):
        async with async_session() as session:
            await RefreshSessionDAO.delete(
                session, RefreshSessionModel.user_id == user_id
            )
            await session.commit()

    @classmethod
    def _create_access_token(cls, user_id: uuid.UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.utcnow()
                   + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, algorithm=ALGORITHM
        )
        return f"Bearer {encoded_jwt}"

    @classmethod
    def _create_refresh_token(cls):
        return uuid.uuid4()
