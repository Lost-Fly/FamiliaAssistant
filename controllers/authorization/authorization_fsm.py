from aiogram.dispatcher.filters.state import StatesGroup, State


class Authorization(StatesGroup):
    awaiting_user_phone: State = State()
