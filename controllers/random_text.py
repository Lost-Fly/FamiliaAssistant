from aiogram import types

from controllers.authorization.authorization import is_authorized
from core.core import dispatcher
from utils import log


@dispatcher.message_handler()
async def random_text_message(message: types.Message):
    if message.text.lower() in ["абоба", "aboba"]:
        await message.answer("❤️")
        return log(message.chat.username, "successfully answered for " + message.text)

    if not await is_authorized(message.chat.id):
        return

    await message.answer("Вы хотите начать со мной диалог? Вызовите /start_dialog для этого.\n"
                         "Если что-то непонятно, можете просмотреть пояснительное сообщение: /start")
    log(message.chat.username, "successfully answered for random text")
