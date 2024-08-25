from aiogram.fsm.state import State, StatesGroup


class StockInfo(StatesGroup):
    item = State()
