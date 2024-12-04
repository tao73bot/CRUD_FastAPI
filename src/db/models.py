from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
import uuid
from typing import Optional, List


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

    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"User: {self.username}"



class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publish_date: str
    pages: int
    language: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    updated_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"Book: {self.title}"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    rating: int = Field(default=0, lt=5)
    review_text: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    book_id: Optional[uuid.UUID] = Field(default=None, foreign_key="books.id")
    created_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    updated_at: str = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow()))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"Review for book: {self.book_id} by user: {self.user_id}"
