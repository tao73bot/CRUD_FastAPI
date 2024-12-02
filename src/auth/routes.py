from fastapi import APIRouter, Depends, HTTPException,status
from .schemas import UserCreate,User,UserLogin
from .service import UserService
from config import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,decode_access_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = timedelta(days=2)

@auth_router.post("/signup",response_model=User,status_code=status.HTTP_201_CREATED)
async def create_user(user_data:UserCreate, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    user = await user_service.create_user(user_data,session)
    return user

@auth_router.post("/signin",response_model=User,status_code=status.HTTP_200_OK)
async def login_user(login_data:UserLogin, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email,session)
    if user is not None:
        password_verified = verify_password(password,user.password)
        if password_verified:
            access_token = create_access_token(user_data={
                "id":str(user.id),
                "email":user.email
            })
            refresh_token = create_access_token(user_data={
                "id":str(user.id),
                "email":user.email
            },refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY.days))
            
            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user": {
                        "id":str(user.id),
                        "username":user.username,
                        "email":user.email
                    }
                }
            )

    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")