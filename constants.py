import os

from dotenv import load_dotenv

load_dotenv()

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
