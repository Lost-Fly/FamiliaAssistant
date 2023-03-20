from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatGptState(StatesGroup):
    awaiting_user_message: State = State()
