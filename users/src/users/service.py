from ..service import BaseService
from .schemas import CreateUser, UpdateUser, CreateVacancy, UpdateVacancy, CreateApplication
from .DAO import UserDAO, VacancyDAO, ApplicationDAO
from .models import UserModel, Vacancy, Application
from sqlalchemy.ext.asyncio import AsyncSession


class UserService(BaseService):
    CreateSchema = CreateUser
    UpdateSchema = UpdateUser
    ModelDAO = UserDAO
    Model = UserModel
    Massage = "User"


class VacancyService(BaseService):
    CreateSchema = CreateVacancy
    UpdateSchema = UpdateVacancy
    ModelDAO = VacancyDAO
    Model = Vacancy
    Massage = "Vacancy"

    @classmethod
    async def create_new_object(
            cls,
            object,
            session: AsyncSession
    ):
        async with session.begin():
            db_object = await cls.ModelDAO.add(session, **object.dict())
        return db_object


class ApplicationService(BaseService):
    CreateSchema = CreateApplication
    ModelDAO = ApplicationDAO
    Model = Application
    Massage = "Application"
