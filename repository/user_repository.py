import pickle

import redis.asyncio as redis

from constants import REDIS_SOCKET, REDIS_DB
from model.user import User


class UserRepository:
    def __init__(self):
        self.__redis_client: redis.Redis = redis.Redis(unix_socket_path=REDIS_SOCKET,
                                                       db=REDIS_DB,
                                                       decode_responses=False)

    async def get_by_id(self, user_id: int) -> User:
        user: User | None = await self.__redis_client.get(user_id)

        return pickle.loads(user) if user else User(user_id)

    async def save(self, user: User):
        await self.__redis_client.set(user.get_id(), pickle.dumps(user))

    async def close(self):
        await self.__redis_client.close()
