from model.messages_history import MessagesHistory


class User:
    def __init__(self, user_id: int, nickname: str, phone_number: str, real_name: str,
                 is_authorized: bool, is_god: bool):
        self.__id: int = user_id
        self.__nickname: str = nickname
        self.__phone_number: str = phone_number
        self.__real_name: str = real_name
        self.__name: str = ""

        self.__is_authorized: bool = is_authorized
        self.__is_god: bool = is_god
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

    def get_nickname(self) -> str:
        return self.__nickname

    def authorized(self, is_authorized: bool):
        self.__is_authorized: bool = is_authorized

    def is_authorized(self) -> bool:
        return self.__is_authorized

    def is_god(self) -> bool:
        return self.__is_god

    @staticmethod
    def empty():
        return User(0, "", "", "", False, False)

    def __str__(self):
        return (
            f"id: <u><b>{self.__id}</b></u>\n"
            f"nickname: @{self.__nickname}\n"
            f"phone number: +{self.__phone_number}\n"
            f"real name: <u><b>{self.__real_name}</b></u>\n"
            f"name for ChatGPT: <u><b>{self.__name}</b></u>\n\n"

            f"is GOD: <u><b>{self.__is_god}</b></u>\n"
            f"Saved messages history:\n\n"

            f"{self.messages_history}\n"
        )
