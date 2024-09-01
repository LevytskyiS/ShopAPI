from functools import wraps

from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from messages import denied_msg
from conf import USER_ID, URI_MONGO


async def fetch_mongo_users(user_id):
    client = AsyncIOMotorClient(URI_MONGO, server_api=ServerApi("1"))
    db = client["auth"]
    collection = db["user"]
    user = await collection.find_one({"tg_id": user_id})
    return user


async def permission(message: Message) -> bool:
    user = await fetch_mongo_users(message.from_user.id)
    if not user:
        return
    return True


def check_permission(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        allowed = await permission(message)

        if not allowed:
            return message.answer(text=denied_msg)
        return await handler(message, *args, **kwargs)

    return wrapper
