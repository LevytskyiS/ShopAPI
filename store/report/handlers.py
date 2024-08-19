from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from query import turnover_all_time
from messages import start_msg, description_msg, help_msg
from keyboards import main_cmds_kb, turnover_kb

# router ставится вместо dp в качестве декоратора, чтобы не было
# циклического импорта
router = Router()


@router.message(Command("turnover"))
async def cmd_turnover(message: Message):
    await message.answer(text="Select a time period", reply_markup=turnover_kb)


@router.callback_query(F.data == "alltime")
async def get_all_time_sales(callback: CallbackQuery):
    await callback.answer("Sent request")
    data = await turnover_all_time()
    await callback.message.answer(text=data)


@router.callback_query(F.data == "today")
async def get_seven_days_sales(callback: CallbackQuery):
    await callback.answer("Sent request")
    data = await turnover_all_time(1)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "7days")
async def get_seven_days_sales(callback: CallbackQuery):
    await callback.answer("Sent request")
    data = await turnover_all_time(7)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "15days")
async def get_fifteen_days_sales(callback: CallbackQuery):
    await callback.answer("Sent request")
    data = await turnover_all_time(15)
    await callback.message.answer(text=data)


# класс F - фильтр сообщений
# @router.message(F.text == "kek")
# async def cmd_kek(message: Message):
#     await message.answer(text="kek")


@router.message(Command("desc"))
async def cmd_help(message: Message):
    await message.answer(text=description_msg)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(text=help_msg)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=start_msg, reply_markup=main_cmds_kb)
