import uuid

from ..service import BaseService
from .schemas import CreateCables, UpdateCables, CreateType, UpdateType, CreateMark, UpdateMark, CreateNews, UpdateNews
from .DAO import CablesDAO
from .DAO import TypeDAO
from .DAO import MarkDAO
from .DAO import NewsDAO
from .models import Cables
from .models import Type
from .models import Mark
from .models import News
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession


class CablesService(BaseService):
    CreateSchema = CreateCables
    UpdateSchema = UpdateCables
    ModelDAO = CablesDAO
    Model = Cables
    Massage = "Cables"

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            object_exist = await cls.ModelDAO.find_one_or_none(session=session, title=object.title)
            if object_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=f"{cls.Massage} already exists"
                )
            db_object = await cls.ModelDAO.add(session, **object.dict())
        return db_object

    @classmethod
    async def get_object(
            cls,
            object_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
        if db_object is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
            )
        return db_object

    @classmethod
    async def delete_object(
            cls,
            object_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
            if db_object is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
                )
            await cls.ModelDAO.delete(session, object_id)
            await session.commit()


class TypeService(BaseService):
    CreateSchema = CreateType
    UpdateSchema = UpdateType
    ModelDAO = TypeDAO
    Model = Type
    Massage = "Type"

    @classmethod
    async def delete_object(
            cls,
            object_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
            if db_object is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
                )
            await cls.ModelDAO.delete(session, object_id)
            await session.commit()

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            object_exist = await cls.ModelDAO.find_one_or_none(session=session, title=object.title)
            if object_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=f"{cls.Massage} already exists"
                )
            db_object = await cls.ModelDAO.add(session, **object.dict())
        return db_object


class MarkService(BaseService):
    CreateSchema = CreateMark
    UpdateSchema = UpdateMark
    ModelDAO = MarkDAO
    Model = Mark
    Massage = "Mark"

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            object_exist = await cls.ModelDAO.find_one_or_none(session=session, title=object.title)
            if object_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=f"{cls.Massage} already exists"
                )
            db_object = await cls.ModelDAO.add(session, **object.dict())
        return db_object

    @classmethod
    async def get_object(
            cls,
            object_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
        if db_object is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
            )
        return db_object

    @classmethod
    async def delete_object(
            cls,
            object_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
            if db_object is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
                )
            await cls.ModelDAO.delete(session, object_id)
            await session.commit()


class NewsService(BaseService):
    CreateSchema = CreateNews
    UpdateSchema = UpdateNews
    ModelDAO = NewsDAO
    Model = News
    Massage = "News"

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            object_exist = await cls.ModelDAO.find_one_or_none(session=session, title=object.title)
            if object_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=f"{cls.Massage} already exists"
                )
            db_object = await cls.ModelDAO.add(session, **object.dict())
        return db_object

