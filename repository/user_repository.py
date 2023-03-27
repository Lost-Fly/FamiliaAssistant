import pickle

import redis.asyncio as redis

from constants import REDIS_SOCKET, REDIS_DB
from model.user import User


class UserRepository:
    def __init__(self):
        self.__redis_client: redis.Redis = redis.Redis(unix_socket_path=REDIS_SOCKET,
                                                       db=REDIS_DB,
                                                       decode_responses=False)

    async def get_by_id(self, user_id: int | bytes) -> User:
        user: User = await self.__redis_client.get(user_id)
        return pickle.loads(user) if user else User.empty()

    async def get_by_nickname(self, nickname: str) -> User:
        users_id: list[bytes] = await self.__redis_client.keys()

        for uid in users_id:
            user: User = await self.get_by_id(uid)
            if user.get_nickname() == nickname:
                return user

    async def save(self, user: User):
        await self.__redis_client.set(user.get_id(), pickle.dumps(user))

    async def close(self):
        await self.__redis_client.close()
