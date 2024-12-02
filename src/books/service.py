from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreate,BookUpdate
from sqlmodel import select,desc
from .models import Book

class BookService:
    async def get_all_books(self,session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        return result.all()

    async def get_book_by_id(self, book_id:str,session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()
        return book if book else None

    async def create_book(self,book_data:BookCreate,session: AsyncSession):
        book = book_data.model_dump()
        new_book = Book(**book)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self,book_id:str,book_data:BookUpdate,session: AsyncSession):
        book_to_update = await self.get_book_by_id(book_id,session)
        if not book_to_update:
            return None
        book = book_data.model_dump()

        for key,value in book.items():
            setattr(book_to_update,key,value)

        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self,book_id:str,session: AsyncSession):
        book_to_delete = await self.get_book_by_id(book_id,session)
        if not book_to_delete:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete