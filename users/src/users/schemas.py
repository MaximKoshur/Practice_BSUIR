from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
import re
import uuid

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

"""Schemas for Users"""


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @validator("first_name", "last_name")
    def check_name(cls, v):
        if not LETTER_MATCH_PATTERN.match(v):
            raise HTTPException(status_code=400, detail="Name must contain only letters")
        return v


class UpdateUser(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None

    @validator("first_name", "last_name")
    def check_name(cls, v):
        if not LETTER_MATCH_PATTERN.match(v):
            raise HTTPException(status_code=400, detail="Name must contain only letters")
        return v


"""Schemas for Vacancy"""


class CreateVacancy(BaseModel):
    title: str
    requirements: str
    conditions: str
    salary: float


class UpdateVacancy(BaseModel):
    title: str = None
    requirements: str = None
    conditions: str = None
    salary: float = None


"""Schemas for Applications"""


class CreateApplication(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    text: str
    vacancy_id: uuid.UUID

    @validator("full_name")
    def check_name(cls, v):
        if not LETTER_MATCH_PATTERN.match(v):
            raise HTTPException(status_code=400, detail="Name must contain only letters")
        return v


"""Schemas for Tokens"""


class RefreshSessionCreate(BaseModel):
    refresh_token: uuid.UUID
    expires_in: int
    user_id: uuid.UUID


class RefreshSessionUpdate(RefreshSessionCreate):
    user_id: uuid.UUID


class Token(BaseModel):
    access_token: str
    refresh_token: uuid.UUID
    token_type: str
