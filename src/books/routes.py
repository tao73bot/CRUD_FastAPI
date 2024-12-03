from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel.ext.asyncio.session import AsyncSession
from config import get_session
from .service import BookService
from .schemas import BookCreate,BookUpdate,Book
from typing import List
from auth.depandencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))

@book_router.get("/",response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    print(user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/{book_id}",response_model=Book, dependencies=[role_checker])
async def get_book_by_id(book_id:str,session: AsyncSession = Depends(get_session),user_details= Depends(access_token_bearer)):
    book = await book_service.get_book_by_id(book_id,session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    return book

@book_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Book, dependencies=[role_checker])
async def create_book(book_data:BookCreate,session: AsyncSession = Depends(get_session),user_details= Depends(access_token_bearer)):
    book = await book_service.create_book(book_data,session)
    return book

@book_router.patch("/{book_id}",response_model=Book, dependencies=[role_checker])
async def update_book(book_id:str,book_data:BookUpdate,session: AsyncSession = Depends(get_session),user_details= Depends(access_token_bearer)):
    book = await book_service.update_book(book_id,book_data,session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    return book

@book_router.delete("/{book_id}",response_model=Book, dependencies=[role_checker])
async def delete_book(book_id:str,session: AsyncSession = Depends(get_session),user_details= Depends(access_token_bearer)):
    book = await book_service.delete_book(book_id,session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    return book