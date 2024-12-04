from db.models import Review
from auth.service import UserService
from books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreate
from fastapi import HTTPException,status

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(self, user_email: str, book_id: str, review_data: ReviewCreate, session: AsyncSession):
        try:
            book = await book_service.get_book_by_id(book_id, session)
            user = await user_service.get_user_by_email(user_email, session)
            review = review_data.model_dump()
            new_review = Review(**review)
            if not book or not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book or User not found")
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))