from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from sales import turnover_all_time
from messages import (
    start_msg,
    description_msg,
    help_msg,
    callback_answer,
    item_not_found_msg,
)
from keyboards import main_cmds_kb, turnover_kb
from states import StockInfo
from stock import get_stock

# The router is used instead of dp as a decorator to avoid circular imports.
router = Router()


# Stock
@router.message(Command("stock"))
async def cmd_stock_first(message: Message, state: FSMContext):
    await state.set_state(StockInfo.item)
    await message.answer(
        text="👕 Enter a nomenclature", reply_markup=ReplyKeyboardRemove()
    )


@router.message(StockInfo.item)
async def cmd_stock_second(message: Message, state: FSMContext):
    item = message.text.strip()

    if not item.isdigit():
        await state.clear()
        return await message.answer(
            text="It must be a number", reply_markup=main_cmds_kb
        )

    if len(item) != 5 and len(item) != 7:
        await state.clear()
        return await message.answer(
            text="Incorrect nomenclature", reply_markup=main_cmds_kb
        )
    else:
        await state.update_data(item=message.text)
        data = await state.get_data()
        item_code = data.get("item")
        await state.clear()

        result = await get_stock(item_code)

        if result:
            return await message.answer(text=result, reply_markup=main_cmds_kb)
        return await message.answer(
            text=item_not_found_msg,
            reply_markup=main_cmds_kb,
        )


# Turnover stats
@router.message(Command("turnover"))
async def cmd_turnover(message: Message):
    await message.answer(text="⌚️ Select a time period", reply_markup=turnover_kb)


@router.callback_query(F.data == "alltime")
async def get_all_time_sales(callback: CallbackQuery):
    await callback.answer(callback_answer)
    data = await turnover_all_time()
    await callback.message.answer(text=data)


@router.callback_query(F.data == "today")
async def get_seven_days_sales(callback: CallbackQuery):
    await callback.answer(callback_answer)
    data = await turnover_all_time(1)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "7days")
async def get_seven_days_sales(callback: CallbackQuery):
    await callback.answer(callback_answer)
    data = await turnover_all_time(7)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "15days")
async def get_fifteen_days_sales(callback: CallbackQuery):
    await callback.answer(callback_answer)
    data = await turnover_all_time(15)
    await callback.message.answer(text=data)


# класс F - фильтр сообщений
# @router.message(F.text == "kek")
# async def cmd_kek(message: Message):
#     await message.answer(text="kek")


# Basic commands
@router.message(Command("desc"))
async def cmd_help(message: Message):
    await message.answer(text=description_msg)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(text=help_msg)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=start_msg, reply_markup=main_cmds_kb)
