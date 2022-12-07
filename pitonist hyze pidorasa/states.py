from aiogram.dispatcher.filters.state import StatesGroup, State

class Find(StatesGroup):
    step1 = State()
    step2 = State()