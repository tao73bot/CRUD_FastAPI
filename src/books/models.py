from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
import uuid
from typing import Optional
from auth import models

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publish_date: str
    pages: int
    language: str
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.id"
    )
    created_at: str = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow()
        )
    )
    updated_at: str = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.utcnow()
        )
    )
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"Book: {self.title}"