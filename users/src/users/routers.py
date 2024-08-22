import uuid
from .models import UserModel
from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from .service import UserService
from .service import ApplicationService
from .service import VacancyService
from .schemas import CreateUser
from .schemas import UpdateUser
from .schemas import CreateVacancy
from .schemas import UpdateVacancy
from .schemas import CreateApplication
from .schemas import Token
from ..session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from ..global_utils import TokenUtils
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()
vacancy_router = APIRouter()
application_roter = APIRouter()
tokens_roter = APIRouter()


"""
Routers
for
Tokens
"""


@tokens_roter.post("/login")
async def login(
        response: Response,
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_db)
) -> Token:
    user = await TokenUtils.authenticate_user(
        credentials.username, credentials.password
    )
    if not user:
        raise status.HTTP_404_NOT_FOUND
    token = await TokenUtils.create_token(user_id=user.id)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True,
    )
    return token


@tokens_roter.post("/logout")
async def logout(
    request,
    response: Response,
    current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    await TokenUtils.logout(request.cookies.get("refresh_token"))
    return {"message": "Logged out successfully"}


@tokens_roter.post("/refresh_token")
async def refresh_token(request, response: Response) -> Token:
    new_token = await TokenUtils.refresh_token(
        uuid.UUID(request.cookies.get("refresh_token"))
    )

    response.set_cookie(
        "access_token",
        new_token.access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        new_token.refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True,
    )
    return new_token

"""
Routers
for
Users
"""


@user_router.get("")
async def get_users_list(
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await UserService.get_objects_list(session=session)


@user_router.post("")
async def create_users(
        user: CreateUser,
        session: AsyncSession = Depends(get_db),
):
    return await UserService.create_new_object(object=user, session=session)


@user_router.get("/{user_id}")
async def get_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await UserService.get_object(object_id=user_id, session=session)


@user_router.put("/{user_id}")
async def update_user(
        user: UpdateUser,
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await UserService.update_object(object_id=user_id, object=user, session=session)


@user_router.delete("/{user_id}")
async def delete_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    await UserService.delete_object(object_id=user_id, session=session)
    return {"message": "User was deleted"}


"""
Routers 
for 
Vacancy
"""


@vacancy_router.get("")
async def get_vacancy_list(
        session: AsyncSession = Depends(get_db)
):
    return await VacancyService.get_objects_list(session=session)


@vacancy_router.post("")
async def create_vacancy(
        vacancy: CreateVacancy,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await VacancyService.create_new_object(object=vacancy, session=session)


@vacancy_router.get("/{vacancy_id}")
async def get_vacancy(
        vacancy_id: uuid.UUID,
        session: AsyncSession = Depends(get_db)
):
    return await VacancyService.get_object(object_id=vacancy_id, session=session)


@vacancy_router.put("/{vacancy_id}")
async def update_vacancy(
        vacancy: UpdateVacancy,
        vacancy_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await VacancyService.update_object(object_id=vacancy_id, object=vacancy, session=session)


@vacancy_router.delete("/{vacancy_id}")
async def delete_vacancy(
        vacancy_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    await VacancyService.delete_object(object_id=vacancy_id, session=session)
    return {"message": "Vacancy was deleted"}


"""
Routers 
for 
Applications
"""


@application_roter.get("")
async def get_application_list(
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await ApplicationService.get_objects_list(session=session)


@application_roter.post("")
async def create_application(
        application: CreateApplication,
        session: AsyncSession = Depends(get_db)
):
    return await ApplicationService.create_new_object(object=application, session=session)


@application_roter.get("/{application_id}")
async def get_application(
        application_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    return await ApplicationService.get_object(object_id=application_id, session=session)


@application_roter.delete("/{application_id}")
async def delete_application(
        application_id: uuid.UUID,
        session: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(TokenUtils.get_current_user)
):
    await ApplicationService.delete_object(object_id=application_id, session=session)
    return {"message": "Application was deleted"}
