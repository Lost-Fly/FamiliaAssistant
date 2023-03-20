import openai
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from openai.error import APIConnectionError

from controllers.authorization.authorization import is_authorized
from controllers.gpt.chat_gpt_fsm import ChatGptState
from core.core import dispatcher, user_repository
from gpt_api.gpt_api import send_message
from gpt_api.gpt_exception import TooLongMessageException
from model.user import User
from utils import log


@dispatcher.message_handler(commands=['start_dialog'])
async def gpt_request(message: types.Message):
    if not await is_authorized(message.chat.id):
        return

    user: User = await user_repository.get_by_id(message.chat.id)
    if not user.get_name():
        return await message.answer("Вы не задали своё имя. Вызовите /name для этого\n"
                                    "Если вы уже вводили своё имя ранее, значит, я успел обновиться, "
                                    "и какая-то информация могла быть не сохранена(")

    await message.answer("Напишите свой вопрос или проблему")
    await message.answer("Если хотите завершить общение со мной, напишите `СТОП`", parse_mode=ParseMode.MARKDOWN)

    await ChatGptState.awaiting_user_message.set()

    log(message.chat.username, "successfully answered for /start_dialog")


@dispatcher.message_handler(state=ChatGptState.awaiting_user_message)
async def awaiting_user_message(message: types.Message, state: FSMContext):
    if message.text.upper() == "СТОП":
        await message.answer("Диалог завершен")
        await message.answer("Если захотите еще пообщаться, просто введите /start_dialog")

        log(message.chat.username, "successfully answered for 'СТОП'")
        await clear_messages_history(message.chat.id)

        return await state.finish()

    try:
        await message.answer(await send_message(message.chat.id, message.text))
        log(message.chat.username, "ChatGPT successfully answered")
    except openai.error.RateLimitError:
        await message.answer("К сожалению, у меня ограничение на количество вопросов в минуту(. "
                             "Постарайтесь, пожалуйста, спрашивать не так часто")
        log(message.chat.username, "ChatGPT limit reached")
    except TooLongMessageException:
        await message.answer("Ваше сообщение слишком длинное(. Постарайтесь сформулировать мысль более кратко")
        log(message.chat.username, "ChatGPT message is too long")
    except APIConnectionError:
        log(message.chat.username, "Error... Retrying")
        await awaiting_user_message(message, state)


async def clear_messages_history(user_id: int):
    user: User = await user_repository.get_by_id(user_id)
    user.messages_history.clear()
    await user_repository.save(user)
