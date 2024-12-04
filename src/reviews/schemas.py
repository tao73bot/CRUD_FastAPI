from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Review(BaseModel):
    id: uuid.UUID
    rating: int =  Field(lt=5)
    review_text: str
    user_id: Optional[uuid.UUID]
    book_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

class ReviewCreate(BaseModel):
    rating: int = Field(lt=5)
    review_text: str