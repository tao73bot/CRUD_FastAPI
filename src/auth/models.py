from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
import uuid
from books import models
from typing import List


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    username: str
    email: str
    password: str = Field(exclude=True)
    role_name: str = Field(sa_column=Column(pg.VARCHAR, server_default="user"))
    is_varified: bool = False
    created_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    updated_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    books: List["models.Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"User: {self.username}"
