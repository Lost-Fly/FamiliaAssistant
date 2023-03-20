import tiktoken
from tiktoken import Encoding

from constants import GPT_MODEL
from gpt_api.gpt_exception import TooLongMessageException


class MessagesHistory:
    def __init__(self):
        self.__messages_history: list[dict] = []

    def get(self) -> list[dict]:
        return self.__messages_history

    def update_user_name(self, user_name):
        self.__messages_history = [{"role": "system", "content": f"Имя пользователя: {user_name}"}]

    def __tokens_number(self, text: str) -> int:
        encoding: Encoding = tiktoken.encoding_for_model(GPT_MODEL)
        return len(encoding.encode(text))

    def __reduce_history(self):
        def tokens_amount() -> int:
            return sum(self.__tokens_number(message_set["content"]) for message_set in self.__messages_history)

        while tokens_amount() >= 1400:
            self.__messages_history.pop(1)

    def append_message(self, role: str, message: str):
        if (role == "user") and (self.__tokens_number(message) >= 1000):
            raise TooLongMessageException()

        self.__messages_history.append({"role": role, "content": message})
        self.__reduce_history()

    def clear(self):
        # keep only username
        self.__messages_history = self.__messages_history[:1]
