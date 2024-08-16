from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

bt1 = KeyboardButton(text="/help")
bt2 = KeyboardButton(text="/desc")
bt3 = KeyboardButton(text="/turnover")

main_cmds_kb = ReplyKeyboardMarkup(
    keyboard=[
        [bt1, bt2, bt3],
    ],
    resize_keyboard=True,
    input_field_placeholder="Use one of the commands in the menu below.",
)
