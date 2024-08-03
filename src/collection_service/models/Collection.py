from datetime import date, datetime
from uuid import UUID, uuid4
import uuid
from sqlalchemy import Date, DateTime, Integer, String, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = declarative_base()


class CollectionType(str, PyEnum):
    BLACK_LIST = "black_list"
    FAVORITE = "favorite"


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )


class Collection(BaseModel):
    __tablename__ = "collections"

    user_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
    )
    game_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
    )
    type: Mapped[CollectionType] = mapped_column(Enum(CollectionType))
