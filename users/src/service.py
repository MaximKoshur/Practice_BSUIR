import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import status


class BaseService:
    CreateSchema = None
    UpdateSchema = None
    ModelDAO = None
    Model = None
    Massage = None

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            object_exist = await cls.ModelDAO.find_one_or_none(session=session, email=object.email)
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
    async def update_object(
            cls,
            object_id: uuid.UUID,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.find_one_or_none(session, id=object_id)
            if db_object is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
                )
            object_update = await cls.ModelDAO.update(
                session, cls.Model.id == object_id, obj_in=object
            )
            return object_update

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
            await cls.ModelDAO.update(session, cls.Model.id == object_id, obj_in={"is_active": False})
            await session.commit()

    @classmethod
    async def get_objects_list(
        cls,
        *filter,
        session: AsyncSession,
        **filter_by
    ):
        async with session.begin():
            objects = await cls.ModelDAO.find_all(
                session, *filter, **filter_by
            )
        if objects is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.Massage} not found"
            )
        return objects

