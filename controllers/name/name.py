from aiogram import types
from aiogram.dispatcher import FSMContext

from controllers.authorization.authorization import is_authorized
from controllers.name.name_fsm import NameState
from core.core import dispatcher, user_repository
from model.user import User
from utils import log


@dispatcher.message_handler(commands=['name'])
async def set_name(message: types.Message):
    if not await is_authorized(message.chat.id):
        return

    await message.answer("Напишите своё имя")
    await NameState.awaiting_user_name.set()

    log(message.chat.username, "successfully answered for /name")


@dispatcher.message_handler(state=NameState.awaiting_user_name)
async def awaiting_user_name(message: types.Message, state: FSMContext):
    user: User = await user_repository.get_by_id(message.chat.id)
    user.set_name(message.text)
    await user_repository.save(user)

    await message.answer("Запомнил)")

    log(message.chat.username, "successfully remembered user name")

    await state.finish()
