from .models import UserModel, Application, RefreshSessionModel
from .models import Vacancy
from .schemas import CreateUser, RefreshSessionCreate, RefreshSessionUpdate
from .schemas import UpdateUser
from .schemas import CreateApplication
from .schemas import CreateVacancy
from .schemas import UpdateVacancy
from ..DAO import BaseDAO
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from .utils import Hasher


class UserDAO(BaseDAO[UserModel, CreateUser, UpdateUser]):
    model = UserModel

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ) -> UserModel:
        kwargs["password"] = Hasher.hash_password(kwargs["password"])
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()


class VacancyDAO(BaseDAO[Vacancy, CreateVacancy, UpdateVacancy]):
    model = Vacancy

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ) -> UserModel:
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()


class ApplicationDAO(BaseDAO[Application, CreateApplication, None]):
    model = Application

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ) -> UserModel:
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()


class RefreshSessionDAO(
    BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]
):
    model = RefreshSessionModel

    @classmethod
    async def add(cls, session, **kwargs):
        if isinstance(kwargs, dict):
            create_data = kwargs
        else:
            create_data = kwargs.model_dump(exclude_unset=True)
        try:
            stmt = insert(cls.model).values(**create_data).returning(cls.model)
            result = await session.execute(stmt)
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
            print(msg)
            return None
