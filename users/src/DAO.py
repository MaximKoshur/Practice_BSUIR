from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from .users.models import Base, UserModel
from .users.utils import Hasher

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filter,
        **filter_by
    ):
        stmt = (
            select(cls.model)
            .where(cls.model.is_active == True)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        *filter,
        **filter_by,
    ) -> List[ModelType]:
        stmt = (
            select(cls.model)
            .where(cls.model.is_active==True)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

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

    @classmethod
    async def delete(cls, session: AsyncSession, *filter, **filter_by) -> None:
        stmt = delete(cls.model).filter(*filter).filter_by(**filter_by)
        await session.execute(stmt)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
        )
        result = await session.execute(stmt)
        return result.scalars().one()