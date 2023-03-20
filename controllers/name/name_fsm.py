from aiogram.dispatcher.filters.state import State, StatesGroup


class NameState(StatesGroup):
    awaiting_user_name: State = State()
