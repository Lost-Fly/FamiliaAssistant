import os

import dotenv

env_file: str = dotenv.find_dotenv()
dotenv.load_dotenv()

GPT_API_KEY: str = os.getenv("GPT_API_KEY")

TELEGRAM_API_KEY: str = os.getenv("TELEGRAM_API_KEY")

REDIS_SOCKET: str = os.getenv('REDIS_SOCKET')
REDIS_DB: int = int(os.getenv('REDIS_DB'))
REDIS_DB_FSM: int = int(os.getenv('REDIS_DB_FSM'))

GPT_MODEL: str = "gpt-3.5-turbo"

REQUEST_OPTIONS: dict = {
    "model": GPT_MODEL,
    "max_tokens": 2500,
    "temperature": 0,
    "presence_penalty": 0,
    "frequency_penalty": 0,
}

ALLOWED_PHONES: list[str] = os.getenv('ALLOWED_PHONES').split(" ")
GODS: list[str] = os.getenv('GODS').split(" ")

# commands, user_by_id, user_by_nickname, save_phone, all_phones, delete_phone
GOD_ALLOWED_COMMANDS: list[str] = ["commands", "ubi", "ubn", "sp", "ap", "dp"]


def update_env(key: str, value: str):
    dotenv.set_key(env_file, key_to_set=key, value_to_set=value)
