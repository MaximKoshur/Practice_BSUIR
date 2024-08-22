from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, ForeignKey, Table, Boolean, DateTime, UniqueConstraint
import uuid

Base = declarative_base()

cables_marks_association = Table(
    'cables_marks_association',
    Base.metadata,
    Column('cable_id', UUID(as_uuid=True), ForeignKey('cables.id')),
    Column('mark_id', UUID(as_uuid=True), ForeignKey('mark.id')),
    UniqueConstraint('cable_id', 'mark_id', name='uq_cable_mark')
)


class Cables(Base):
    __tablename__ = "cables"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    documents = Column(String, nullable=False)
    appointments = Column(String, nullable=False)
    specifications = Column(String, nullable=False)
    term_of_use = Column(String, nullable=False)
    type = Column(UUID(as_uuid=True), ForeignKey("type.id"), nullable=True)
    marks = relationship("Mark", secondary=cables_marks_association, back_populates="cables", passive_deletes=True)


class Type(Base):
    __tablename__ = "type"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    parent = Column(UUID(as_uuid=True), ForeignKey("type.id"), nullable=True)


class Mark(Base):
    __tablename__ = "mark"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    descriptions = Column(String, nullable=False)
    cables = relationship("Cables", secondary=cables_marks_association, back_populates="marks", passive_deletes=True)


class News(Base):
    __tablename__ = "news"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

