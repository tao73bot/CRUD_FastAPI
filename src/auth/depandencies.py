from fastapi.security import HTTPBearer
from fastapi import Request,status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_access_token
from fastapi.exceptions import HTTPException
from redis_utils import is_jti_blocklisted

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