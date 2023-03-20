from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession

from constants import REDIS_SOCKET, TELEGRAM_API_KEY, REDIS_DB_FSM
from repository.user_repository import UserRepository

user_repository: UserRepository = UserRepository()

telegram_bot: Bot = Bot(token=TELEGRAM_API_KEY)
dispatcher: Dispatcher = Dispatcher(telegram_bot, storage=RedisStorage2(unix_socket_path=REDIS_SOCKET, db=REDIS_DB_FSM))
client_session: ClientSession = ClientSession()
