import uuid
from datetime import datetime
from .models import Cables
from .models import Type
from .models import Mark
from .models import News
from .models import cables_marks_association
from .schemas import CreateCables, UpdateCables
from .schemas import CreateMark, UpdateMark
from .schemas import CreateType, UpdateType
from .schemas import CreateNews, UpdateNews
from sqlalchemy.orm import selectinload
from ..DAO import BaseDAO
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


class CablesDAO(BaseDAO[Cables, CreateCables, UpdateCables]):
    model = Cables

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ):
        try:
            marks = kwargs.pop("marks")
        except:
            marks = []
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        cable = result.scalars().one_or_none()
        values_to_insert = []
        if marks:
            for mark_id in marks:
                values_to_insert.append({'mark_id': mark_id, 'cable_id': cable.id})
            stmt = insert(cables_marks_association).values(values_to_insert)
            await session.execute(stmt)
        return cable

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filter,
            **filter_by
    ):
        stmt = (
            select(cls.model)
            .filter(*filter)
            .options(selectinload(Cables.marks))
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        cable = result.scalars().one_or_none()
        return cable

    @classmethod
    async def find_all(
            cls,
            session: AsyncSession,
            *filter,
            **filter_by,
    ):
        stmt = (
            select(cls.model)
            .filter(*filter)
            .options(selectinload(Cables.marks))
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in,
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        try:
            marks = obj_in.pop("marks")
        except:
            marks = []
        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
        )
        result = await session.execute(stmt)
        cable = result.scalars().one_or_none()
        if marks:
            values_to_insert = []
            for mark_id in marks:
                values_to_insert.append({'mark_id': mark_id, 'cable_id': cable.id})
            stmt = insert(cables_marks_association).values(values_to_insert)
            await session.execute(stmt)
        return cable

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        id: uuid.UUID,
    ):
        stmt = (
            delete(cables_marks_association)
            .where(cables_marks_association.c.cable_id == id)
        )
        await session.execute(stmt)

        stmt = (
            delete(cls.model)
            .where(cls.model.id == id)
            )
        await session.execute(stmt)


class TypeDAO(BaseDAO[Type, CreateType, UpdateType]):
    model = Type

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        id: uuid.UUID,
    ):
        stmt = (
            delete(cls.model)
            .where(cls.model.id == id)
        )
        try:
            await TypeDAO.update(session, cls.model.parent == id, obj_in={"parent": None})
        except:
            pass
        try:
            await CablesDAO.update(session, Cables.type == id, obj_in={"type": None})
        except:
            pass
        await session.execute(stmt)


class MarkDAO(BaseDAO[Mark, CreateMark, UpdateMark]):
    model = Mark

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ):
        try:
            cables = kwargs.pop("cables")
        except:
            cables = []
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        mark = result.scalars().one_or_none()
        values_to_insert = []
        if cables:
            for cable_id in cables:
                values_to_insert.append({'mark_id': mark.id, 'cable_id': cable_id})
            stmt = insert(cables_marks_association).values(values_to_insert)
            await session.execute(stmt)
        return mark

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filter,
            **filter_by
    ):
        stmt = (
            select(cls.model)
            .filter(*filter)
            .options(selectinload(Mark.cables))
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
    ):
        stmt = (
            select(cls.model)
            .filter(*filter)
            .options(selectinload(Mark.cables))
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in,
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        try:
            cables = update_data.pop("cables")
        except:
            cables = []
        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
        )
        result = await session.execute(stmt)
        mark = result.scalars().one_or_none()
        if cables:
            values_to_insert = []
            for cable_id in cables:
                values_to_insert.append({'mark_id': mark.id, 'cable_id': cable_id})
            stmt = insert(cables_marks_association).values(values_to_insert)
            await session.execute(stmt)

        return mark

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        id: uuid.UUID,
    ):
        stmt = (
            delete(cables_marks_association)
            .where(cables_marks_association.c.mark_id == id)
        )
        await session.execute(stmt)

        stmt = (
            delete(cls.model)
            .where(cls.model.id == id)
            )
        await session.execute(stmt)


class NewsDAO(BaseDAO[News, CreateNews, UpdateNews]):
    model = News

    @classmethod
    async def add(
            cls,
            session,
            **kwargs
    ):
        kwargs["date"] = datetime.now()
        stmt = insert(cls.model).values(kwargs).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

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
    ):
        stmt = (
            select(cls.model)
            .where(cls.model.is_active == True)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
