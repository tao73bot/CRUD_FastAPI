from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from config import settings
import uuid
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_data:dict, expiry:timedelta = timedelta(minutes=15),refresh:bool = False):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.utcnow() + expiry
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_access_token(token:str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None