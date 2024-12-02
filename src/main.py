from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import init_db
from books.routes import book_router
from auth.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Server is starting up")
    yield
    print("Server is shutting down")


version = "v1"
app = FastAPI(
    title="CRUD with FastAPI",
    description="This is a simple CRUD with FastAPI",
    version=version,
    lifespan=lifespan
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])