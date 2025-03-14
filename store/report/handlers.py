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
from states import StockInfo, ProductInfo, RestockInfo
from stock import get_stock, get_restock
from products import get_product_info
from permissions import check_permission
from validators import validate_nomenclature_restock, validate_nomenclature_stock

# The router is used instead of dp as a decorator to avoid circular imports.
router = Router()


# Restock dates
@router.message(Command("restock"))
@check_permission
async def cmd_restock_dates_first(message: Message, state: FSMContext):
    await state.set_state(RestockInfo.item)
    await message.answer(
        text="👕 Enter a nomenclature (7 signs)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(RestockInfo.item)
async def cmd_restock_dates_second(message: Message, state: FSMContext):
    item = message.text.strip()

    validated, msg = await validate_nomenclature_restock(item)

    if not validated:
        await state.clear()
        return await message.answer(text=msg, reply_markup=main_cmds_kb)

    await state.update_data(item=message.text)
    data = await state.get_data()
    item_code = data.get("item")
    await state.clear()

    result = await get_restock(db="stock", item=item_code)

    if result:
        return await message.answer(text=result, reply_markup=main_cmds_kb)
    return await message.answer(
        text=item_not_found_msg,
        reply_markup=main_cmds_kb,
    )


# Stock
@router.message(Command("stock"))
@check_permission
async def cmd_stock_first(message: Message, state: FSMContext) -> None:
    await state.set_state(StockInfo.item)
    await message.answer(
        text="👕 Enter a nomenclature (5 or 7 signs)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StockInfo.item)
async def cmd_stock_second(message: Message, state: FSMContext):
    item = message.text.strip()

    validated, msg = await validate_nomenclature_stock(item)

    if not validated:
        await state.clear()
        return await message.answer(text=msg, reply_markup=main_cmds_kb)

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


# Product info
@router.message(Command("product"))
@check_permission
async def cmd_product_first(message: Message, state: FSMContext) -> None:
    await state.set_state(ProductInfo.product)
    await message.answer(
        text="👕 Enter a product code (3 signs)", reply_markup=ReplyKeyboardRemove()
    )


@router.message(ProductInfo.product)
async def cmd_product_second(message: Message, state: FSMContext):
    product = message.text.strip()

    if len(product) != 3:
        await state.clear()
        return await message.answer(
            text="Incorrect product code. It must be 3 signs long.",
            reply_markup=main_cmds_kb,
        )
    else:
        await state.update_data(product=message.text)
        data = await state.get_data()
        product_code = data.get("product")
        await state.clear()

        result = await get_product_info(product_code)

        if result:
            return await message.answer(text=result, reply_markup=main_cmds_kb)
        return await message.answer(
            text=item_not_found_msg,
            reply_markup=main_cmds_kb,
        )


# Turnover stats
@router.message(Command("turnover"))
@check_permission
async def cmd_turnover(message: Message) -> None:
    await message.answer(text="⌚️ Select a time period", reply_markup=turnover_kb)


@router.callback_query(F.data == "alltime")
async def get_all_time_sales(callback: CallbackQuery) -> None:
    await callback.answer(callback_answer)
    data = await turnover_all_time()
    await callback.message.answer(text=data)


@router.callback_query(F.data == "today")
async def get_seven_days_sales(callback: CallbackQuery) -> None:
    await callback.answer(callback_answer)
    data = await turnover_all_time(1)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "7days")
async def get_seven_days_sales(callback: CallbackQuery) -> None:
    await callback.answer(callback_answer)
    data = await turnover_all_time(7)
    await callback.message.answer(text=data)


@router.callback_query(F.data == "15days")
async def get_fifteen_days_sales(callback: CallbackQuery) -> None:
    await callback.answer(callback_answer)
    data = await turnover_all_time(15)
    await callback.message.answer(text=data)


# Basic commands
@router.message(Command("desc"))
@check_permission
async def cmd_help(message: Message) -> None:
    await message.answer(text=description_msg)


@router.message(Command("help"))
@check_permission
async def cmd_help(message: Message) -> None:
    await message.answer(text=help_msg)


@router.message(CommandStart())
@check_permission
async def cmd_start(message: Message) -> None:
    await message.answer(text=start_msg, reply_markup=main_cmds_kb)
