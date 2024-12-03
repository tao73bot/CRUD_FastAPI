from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from books.schemas import BookCreate

class UserCreate(BaseModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)


class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    is_varified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    books: List[BookCreate]

class UserLogin(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=6)