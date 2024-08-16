import asyncio
import logging

from aiogram.methods import DeleteWebhook
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from handlers import router

env_vars = dotenv_values(".env")
TOKEN = env_vars.get("TG_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router=router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
