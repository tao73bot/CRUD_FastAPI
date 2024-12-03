from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, email:str,session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)
        user = result.first()
        return user if user else None

    async def user_exists(self,email:str,session: AsyncSession):
        user = await self.get_user_by_email(email,session)
        return True if user else False

    async def create_user(self,user_data:UserCreate,session: AsyncSession):
        user = user_data.model_dump()
        new_user = User(**user)
        new_user.password = generate_password_hash(user["password"])
        new_user.role_name = "user"
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user