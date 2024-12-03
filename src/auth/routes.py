from fastapi import APIRouter, Depends, HTTPException,status
from .schemas import UserCreate,User,UserLogin
from .service import UserService
from config import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,decode_access_token,verify_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from .depandencies import RefreshTokenBearer,AccessTokenBearer,get_current_user,RoleChecker
from redis_utils import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_cheacker = RoleChecker(["admin",'user'])

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
                "email":user.email,
                "role_name":user.role_name
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


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.utcnow():
        new_access_token = create_access_token(user_data=token_details['user'])
    return JSONResponse(content={
        "access_token":new_access_token
    })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired token")

@auth_router.get('/me', response_model=User)
async def get_current_user(user = Depends(get_current_user), _ :bool = Depends(role_cheacker)):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details:dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(content={
        "message":"Logout successful",
    },status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")