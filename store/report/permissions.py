from functools import wraps

from aiogram.types import Message

from messages import denied_msg
from conf import USER_ID


async def permission(message: Message) -> bool:
    if str(message.from_user.id) != USER_ID:
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
