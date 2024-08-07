import uuid
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from .models import UserModel
from .DAO import UserDAO
from users.src.users.schemas import CreateUser, UpdateUser


class UserService:
    @classmethod
    async def create_new_user(
            cls,
            user: CreateUser,
            session: AsyncSession
    ):
        async with session.begin():
            user_exist = await UserDAO.find_one_or_none(session, email=user.email)
            if user_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
                )
            db_user = await UserDAO.add(session, **user.dict())
        return db_user

    @classmethod
    async def get_user(
            cls,
            user_id: uuid.UUID,
            session: AsyncSession
    ):
        async with session.begin():
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    @classmethod
    async def update_user(
            cls,
            user_id: uuid.UUID,
            user: UpdateUser,
            session: AsyncSession
    ) -> UserModel:
        async with session.begin():
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
            if db_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            user_update = await UserDAO.update(
                session, UserModel.id == user_id, obj_in=user
            )
            return user_update

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID, session: AsyncSession):
        async with session.begin():
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
            if db_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            await UserDAO.update(session, UserModel.id == user_id, obj_in={"is_active": False})
            await session.commit()

    @classmethod
    async def get_users_list(
        cls,
        *filter,
        session: AsyncSession,
        **filter_by
    ):
        async with session.begin():
            users = await UserDAO.find_all(
                session, *filter, **filter_by
            )
        if users is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
            )
        return users
