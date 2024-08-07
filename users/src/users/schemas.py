from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
import re
import uuid

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class CreateUser(BaseModel):
    """Model for creating User"""
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


class Token(BaseModel):
    access_token: str
    token_type: str


