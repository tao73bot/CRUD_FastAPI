from pydantic import BaseModel
import uuid
from datetime import datetime

class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    publish_date: str
    pages: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    pages: int
    language: str

class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    pages: int
    language: str

