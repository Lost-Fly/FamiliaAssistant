import openai
from openai.openai_object import OpenAIObject

from constants import REQUEST_OPTIONS
from core.core import user_repository
from model.user import User
from utils import log


async def send_message(user_id: int, message: str) -> str:
    user: User = await user_repository.get_by_id(user_id)
    user.messages_history.append_message("user", message)

    response: OpenAIObject = await openai.ChatCompletion.acreate(
        **REQUEST_OPTIONS,
        messages=user.messages_history.get()
    )

    gpt_answer: str = response.choices[0].message.content
    user.messages_history.append_message("assistant", gpt_answer)

    await user_repository.save(user)
    log(user_id, user.messages_history.get())

    return gpt_answer
