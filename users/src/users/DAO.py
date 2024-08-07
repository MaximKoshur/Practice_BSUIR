from .models import UserModel
from .schemas import CreateUser
from .schemas import UpdateUser
from users.src.DAO import BaseDAO


class UserDAO(BaseDAO[UserModel, CreateUser, UpdateUser]):
    model = UserModel


