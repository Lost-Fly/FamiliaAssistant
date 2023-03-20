from typing import Any


def log(tag: Any, message: Any):
    if not tag:
        tag = "(undefined)"
    if not message:
        message = "..."

    print(tag, ":", message)
