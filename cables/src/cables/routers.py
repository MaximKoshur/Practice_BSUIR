import uuid
from .service import CablesService
from .service import TypeService
from .service import MarkService
from .service import NewsService
from .schemas import CreateCables
from .schemas import UpdateCables
from .schemas import CreateType
from .schemas import UpdateType
from .schemas import CreateMark
from .schemas import UpdateMark
from .schemas import CreateNews
from .schemas import UpdateNews
from .schemas import ShowMark
from .models import Mark
from ..session import get_db
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

Cables_router = APIRouter()
News_router = APIRouter()
Type_router = APIRouter()
Mark_router = APIRouter()


"""
Routers
for
Cables
"""


@Cables_router.get("")
async def get_Cables_list(
        session: AsyncSession = Depends(get_db)
):
    return await CablesService.get_objects_list(session=session)


@Cables_router.post("")
async def create_cables(
        cables: CreateCables,
        session: AsyncSession = Depends(get_db)
):
    return await CablesService.create_new_object(object=cables, session=session)


@Cables_router.get("/{Cables_id}")
async def get_Cables(
        Cables_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await CablesService.get_object(object_id=Cables_id, session=session)


@Cables_router.put("/{Cables_id}")
async def update_Cables(
        Cables: UpdateCables,
        Cables_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await CablesService.update_object(object_id=Cables_id, object=Cables, session=session)


@Cables_router.delete("/{Cables_id}")
async def delete_Cables(
        Cables_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    await CablesService.delete_object(object_id=Cables_id, session=session)
    return {"message": "Cables was deleted"}



"""
Routers 
for 
Type
"""


@Type_router.get("")
async def get_Type_list(
        session: AsyncSession = Depends(get_db)
):
    return await TypeService.get_objects_list(session=session)


@Type_router.post("")
async def create_Type(
        Type: CreateType,
        session: AsyncSession = Depends(get_db)
):
    return await TypeService.create_new_object(object=Type, session=session)


@Type_router.get("/{Type_id}")
async def get_Type(
        Type_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await TypeService.get_object(object_id=Type_id, session=session)


@Type_router.put("/{Type_id}")
async def update_Type(
        Type: UpdateType,
        Type_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await TypeService.update_object(object_id=Type_id, object=Type, session=session)


@Type_router.delete("/{Type_id}")
async def delete_Type(
        Type_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    await TypeService.delete_object(object_id=Type_id, session=session)
    return {"message": "Type was deleted"}


"""
Routers 
for 
Marks
"""


@Mark_router.get("")
async def get_Mark_list(
        session: AsyncSession = Depends(get_db)
):
    return await MarkService.get_objects_list(session=session)


@Mark_router.post("")
async def create_Mark(
        Mark: CreateMark,
        session: AsyncSession = Depends(get_db)
):
    return await MarkService.create_new_object(object=Mark, session=session)


@Mark_router.get("/{Mark_id}")
async def get_Mark(
        Mark_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await MarkService.get_object(object_id=Mark_id, session=session)


@Mark_router.put("/{mark_id}")
async def update_mark(
        mark: UpdateMark,
        mark_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await MarkService.update_object(object_id=mark_id, object=mark, session=session)


@Mark_router.delete("/{Mark_id}")
async def delete_Mark(
        Mark_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    await MarkService.delete_object(object_id=Mark_id, session=session)
    return {"message": "Mark was deleted"}


"""
Routers
for
News
"""


@News_router.get("")
async def get_News_list(
        session: AsyncSession = Depends(get_db)
):
    return await NewsService.get_objects_list(session=session)


@News_router.post("")
async def create_News(
        News: CreateNews,
        session: AsyncSession = Depends(get_db)
):
    return await NewsService.create_new_object(object=News, session=session)


@News_router.get("/{News_id}")
async def get_News(
        News_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await NewsService.get_object(object_id=News_id, session=session)


@News_router.put("/{News_id}")
async def update_News(
        News: UpdateNews,
        News_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await NewsService.update_object(object_id=News_id, object=News, session=session)


@News_router.delete("/{News_id}")
async def delete_News(
        News_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    await NewsService.delete_object(object_id=News_id, session=session)
    return {"message": "News was deleted"}
