from model.messages_history import MessagesHistory


class User:
    def __init__(self, user_id: int, name="", is_authorized=False):
        self.__id: int = user_id
        self.__name: str = name
        self.__is_authorized: bool = is_authorized
        self.messages_history: MessagesHistory = MessagesHistory()

    def set_id(self, user_id: int):
        self.__id: int = user_id

    def get_id(self) -> int:
        return self.__id

    def set_name(self, name: str):
        self.__name: str = name
        self.messages_history.update_user_name(name)

    def get_name(self) -> str:
        return self.__name

    def authorized(self, is_authorized: bool):
        self.__is_authorized: bool = is_authorized

    def is_authorized(self) -> bool:
        return self.__is_authorized
