from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from constants import ALLOWED_PHONES, GODS
from core.core import user_repository, dispatcher
from model.user import User
from utils import log

send_me_phone_number: str = """
Вас приветствует бот клиники Fамилия!
Давайте пройдем мини-авторизацию - пришлите, пожалуйста, свой номер телефона.

P.S. Чтобы это сделать, нужно стереть весь текст в сообщении и нажать на значок 🎛 в правом нижнем углу (рядом со значком скрепки 📎)
P.P.S. Если вы на телефоне, то можно также нажать на кнопку "Отправить номер", если убрать клавиатуру
"""


async def is_authorized(message: types.Message):
    def create_phone_keyboard() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить номер', request_contact=True))

    user: User = await user_repository.get_by_id(message.chat.id)
    if user.is_authorized():
        return True

    await message.answer(send_me_phone_number, reply_markup=create_phone_keyboard())
    log(message.chat.username, "User authorization...")


async def is_god(message: types.Message):
    user: User = await user_repository.get_by_id(message.chat.id)
    return user.is_god()


@dispatcher.message_handler(content_types=types.ContentType.CONTACT)
async def handle_user_phone(message: types.Message):
    log(message.chat.username, message.contact.phone_number)

    if message.contact.phone_number not in (ALLOWED_PHONES + GODS):
        log(message.chat.username, "User not authorized!")

        return await message.answer("К сожалению, вы не находитесь в списке разрешенных пользователей(\n"
                                    "Если произошла ошибка, обратитесь, пожалуйста, к администратору: @mihalisM")

    if message.contact.phone_number in GODS:
        await message.answer("Ну привет админ)\ncommands тебе в помощь))", reply_markup=ReplyKeyboardRemove())

        await user_repository.save(User(message.chat.id, message.chat.username, message.contact.phone_number,
                                        message.chat.full_name, is_authorized=True, is_god=True))
        return log(message.chat.username, "User is GOD!")

    await message.answer("Вы успешно авторизованы. Можете продолжать пользоваться ботом)",
                         reply_markup=ReplyKeyboardRemove())
    await user_repository.save(User(message.chat.id, message.chat.username, message.contact.phone_number,
                                    message.chat.full_name, is_authorized=True, is_god=False))
    log(message.chat.username, "User authorized!")
