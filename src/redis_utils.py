from redis.asyncio import Redis as aioredis
from config import settings

JTI_EXPIRY = 3600

token_blocklist = aioredis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

async def add_jti_to_blocklist(jti:str)->None:
    await token_blocklist.set(name=jti,value="",ex=JTI_EXPIRY)

async def is_jti_blocklisted(jti:str)->bool:
    return await token_blocklist.get(jti) is not None