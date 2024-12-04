from fastapi import APIRouter, Depends, HTTPException, status
from db.models import User
from config import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreate
from .service import ReviewService
from auth.depandencies import get_current_user

review_service = ReviewService()

reviews_router = APIRouter()


@reviews_router.post("/book/{book_id}")
async def add_review_to_book(
    book_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_id=book_id,
        review_data=review_data,
        session=session,
    )
    return new_review