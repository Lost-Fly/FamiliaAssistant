from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants import ALLOWED_PHONES
from core.core import user_repository, telegram_bot, dispatcher
from model.user import User
from utils import log


async def is_authorized(user_id: int):
    def create_phone_keyboard() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить номер', request_contact=True))

    user: User = await user_repository.get_by_id(user_id)
    if user.is_authorized():
        return True

    await telegram_bot.send_message(user_id,
                                    "Вас приветствует бот клиники Fамилия!\n"
                                    "Давайте пройдем мини-авторизацию - напишите, пожалуйста, свой номер телефона.\n\n"
                                    "P.S. Чтобы это сделать, нужно стереть весь текст в сообщении и "
                                    "нажать на значок 🎛 в правом нижнем углу (рядом со значком скрепки 📎)",
                                    reply_markup=create_phone_keyboard())
    log(user_id, "User authorization...")


@dispatcher.message_handler(content_types=types.ContentType.CONTACT)
async def handle_user_phone(message: types.Message):
    log(message.chat.username, message.contact.phone_number)

    if message.contact.phone_number not in ALLOWED_PHONES:
        log(message.chat.username, "User not authorized!")

        return await message.answer("К сожалению, вы не находитесь в списке разрешенных пользователей(\n"
                                    "Если произошла ошибка, обратитесь, пожалуйста, к администратору: @mihalisM")

    await message.answer("Вы успешно авторизованы. Можете продолжать пользоваться ботом)")
    await user_repository.save(User(user_id=message.chat.id, is_authorized=True))
    log(message.chat.username, "User authorized!")
