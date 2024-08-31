from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

bt1 = KeyboardButton(text="/help")
bt2 = KeyboardButton(text="/desc")
bt3 = KeyboardButton(text="/turnover")
bt4 = KeyboardButton(text="/product")
bt5 = KeyboardButton(text="/stock")
bt6 = KeyboardButton(text="/restock")

turnover_bt1 = InlineKeyboardButton(text="Today", callback_data="today")
turnover_bt2 = InlineKeyboardButton(text="7 days", callback_data="7days")
turnover_bt3 = InlineKeyboardButton(text="15 days", callback_data="15days")
turnover_bt4 = InlineKeyboardButton(text="All time", callback_data="alltime")

main_cmds_kb = ReplyKeyboardMarkup(
    keyboard=[[bt1, bt2, bt3], [bt4, bt5, bt6]],
    resize_keyboard=True,
)

turnover_kb = InlineKeyboardMarkup(
    inline_keyboard=[[turnover_bt1, turnover_bt2, turnover_bt3, turnover_bt4]]
)
