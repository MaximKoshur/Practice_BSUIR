import uuid
from .services import UserService
from ..session import get_db
from .schemas import CreateUser
from .schemas import UpdateUser
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
user_router = APIRouter(prefix="/users")


@user_router.get("")
async def get_users_list(
    session: AsyncSession = Depends(get_db)
):
    return await UserService.get_users_list(session=session)


@user_router.post("")
async def create_users(
        user: CreateUser,
        session: AsyncSession = Depends(get_db)
):
    return await UserService.create_new_user(user=user, session=session)


@user_router.get("/{user_id}")
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    return await UserService.get_user(user_id, session)


@user_router.put("/{user_id}")
async def update_user(
    user: UpdateUser,
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    return await UserService.update_user(user_id, user, session)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    await UserService.delete_user(user_id, session)
    return {"message": "User was deleted"}
