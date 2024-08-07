from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, String, Column, Float, ForeignKey
import uuid

Base = declarative_base()


class Vacancy(Base):
    """Main model Vacancy class"""
    __tablename__ = "vacancy"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    requirements = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    conditions = Column(String, default=False)
    salary = Column(Float, nullable=False)


class Application(Base):
    __tablename__ = "application"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    text = Column(String, nullable=True)
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey("vacancy.id"), nullable=False)


class UserModel(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
