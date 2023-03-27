from aiogram import types

from constants import GOD_ALLOWED_COMMANDS
from controllers.authorization.authorization import is_authorized, is_god
from core.core import dispatcher, user_repository
from utils import log


async def exec_command(command: str, argument: str = "") -> str:
    from constants import ALLOWED_PHONES

    if command == "commands":
        return "Hint: commands, user_by_id, user_by_nickname, save_phone, all_phones, delete_phone\n\n" + \
               " ".join(GOD_ALLOWED_COMMANDS)
    elif command == "ap":
        return " ".join(ALLOWED_PHONES) + f"\n\nTotally: {len(ALLOWED_PHONES)}"

    if not argument:
        return "Argument must be non null!"

    match command:
        case "ubi":
            return str(await user_repository.get_by_id(int(argument)))
        case "ubn":
            return str(await user_repository.get_by_nickname(argument))
        case "sp":
            from constants import update_env

            ALLOWED_PHONES += [argument]
            update_env("ALLOWED_PHONES", " ".join(ALLOWED_PHONES))
            return "successfully"
        case "dp":
            from constants import update_env

            if argument not in ALLOWED_PHONES:
                return "There's no such phone number!"

            ALLOWED_PHONES.remove(argument)
            update_env("ALLOWED_PHONES", " ".join(ALLOWED_PHONES))
            return "successfully"


async def process_god(message: types.Message) -> bool:
    if not await is_god(message):
        return False

    # dont unpack because argument may not exists.
    # it raise error: ValueError: not enough values to unpack (expected 2, got 1)
    command_argument: list[str] = message.text.split(" ")
    if command_argument[0] not in GOD_ALLOWED_COMMANDS:
        return False

    await message.answer(await exec_command(*command_argument), parse_mode="HTML")
    return True


@dispatcher.message_handler()
async def random_text_message(message: types.Message):
    if message.text.lower() in ["абоба", "aboba"]:
        await message.answer("❤️")
        return log(message.chat.username, "successfully answered for " + message.text)

    if not await is_authorized(message):
        return

    # should be after is_authorized
    if await process_god(message):
        return

    await message.answer("Вы хотите начать со мной диалог? Вызовите /start_dialog для этого.\n"
                         "Если что-то непонятно, можете просмотреть пояснительное сообщение: /start")
    log(message.chat.username, "successfully answered for random text")
