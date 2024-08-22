from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator
from datetime import datetime
import uuid

"""Schemas for Cables"""


class CreateCables(BaseModel):
    title: str
    documents: str
    appointments: str
    specifications: str
    term_of_use: str
    type: uuid.UUID = None
    marks: List[uuid.UUID] = []


class UpdateCables(BaseModel):
    title: str = None
    documents: str = None
    appointments: str = None
    specifications: str = None
    term_of_use: str = None
    type: uuid.UUID = None
    marks: List[uuid.UUID] = []


"""Schemas for Type"""


class CreateType(BaseModel):
    title: str
    parent: uuid.UUID = None


class UpdateType(BaseModel):
    title: str = None


"""Schemas for Mark"""


class ShowMark(BaseModel):
    title: str
    descriptions: str
    cables: List[uuid.UUID] = []


class CreateMark(BaseModel):
    title: str
    descriptions: str
    cables: List[uuid.UUID] = []


class UpdateMark(BaseModel):
    title: str = None
    descriptions: str = None
    cables: List[uuid.UUID] = []


"""Schemas for News"""


class CreateNews(BaseModel):
    title: str
    content: str


class UpdateNews(BaseModel):
    title: str = None
    content: str = None


