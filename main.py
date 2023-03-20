import openai
from aiogram import Dispatcher, types
from aiogram.utils import executor

from constants import GPT_API_KEY
from core.core import dispatcher, client_session, user_repository

# ОБЯЗАТЕЛЬНО
from controllers import *


def init_openai():
    openai.api_key = GPT_API_KEY

    openai.aiosession.set(client_session)


async def startup(dp: Dispatcher):
    print("Bot started")

    init_openai()

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Показать приветствие"),
        types.BotCommand("name", "Задать своё имя"),
        types.BotCommand("start_dialog", "Начать диалог со мной"),
    ])


async def shutdown(dp: Dispatcher):
    await client_session.close()

    await dp.storage.close()
    await user_repository.close()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False, on_startup=startup, on_shutdown=shutdown)
