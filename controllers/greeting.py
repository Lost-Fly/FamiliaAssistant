from aiogram import types

from controllers.authorization.authorization import is_authorized
from main import dispatcher
from utils import log

greeting: str = """
Здравствуйте, я ваш личный цифровой помощник.
Вы можете задать мне любой вопрос или попросить выполнить какую-либо задачу, и я постараюсь вам помочь

Команды для управления мной:
    /start - Показать это приветствие
    /name - Задать своё имя
    /start_dialog - Начать диалог со мной
"""


@dispatcher.message_handler(commands=['start'])
async def greeting_message(message: types.Message):
    if not await is_authorized(message.chat.id):
        return

    await message.answer(greeting)
    log(message.chat.username, "successfully answered for /start")
