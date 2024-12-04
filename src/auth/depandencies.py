from fastapi.security import HTTPBearer
from fastapi import Request,status,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_access_token
from fastapi.exceptions import HTTPException
from redis_utils import is_jti_blocklisted
from sqlmodel.ext.asyncio.session import AsyncSession
from config import get_session
from .service import UserService
from typing import List
from db.models import User

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self,request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)
        print(token_data)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid token")

        if await is_jti_blocklisted(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={
                "error":"Token has been revoked",
                "message":"Please login again"
                }
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self,token:str)-> bool:
        payload = decode_access_token(token)
        return True if payload else False

    def verify_token_data(self,token_data:dict)->None:
        raise NotImplementedError("Please Override this method")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please provide access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please provide refresh token")


async def get_current_user(token_details:dict = Depends(AccessTokenBearer()),
                    session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']

    user = await user_service.get_user_by_email(user_email,session)
    return user


class RoleChecker:
    def __init__(self,allowed_roles:List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self,user:User = Depends(get_current_user)):
        if user.role_name not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to perform this action")
        return True