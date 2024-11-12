import logging
import traceback
from typing import Union

from aiogram.types import Message, CallbackQuery

from .admins import send_to_admins


async def send_message_about_error(
    event: Union[Message, CallbackQuery],
    error: str,
    error_place: str = "",
    message_to_user: bool = True,
) -> None:
    """Sends the given error message to the admins (and user) and logs it."""
    logging.error(f"{error.capitalize()}{error_place}")
    await send_to_admins(
        get_admin_error_message(event, error, error_place),
        get_traceback_file_path(),
    )
    if message_to_user:
        await event.answer(get_user_error_message())


def get_admin_error_message(
    event: Union[Message, CallbackQuery], error: str, error_place: str
) -> str:
    """Returns the default admin error message."""
    user = event.from_user
    reason = (
        f"message: '{event.text}'"
        if isinstance(event, Message)
        else f"clicking '{event.data}' on message\n---\n{event.message.text}"
    )
    return (
        f"❗️ <b>Exception{error_place}</b> "
        f"with user <code>{user.id}</code> (@{user.username})\n\n"
        f"{error.capitalize()}\n\nafter {reason}"
    )


def get_traceback_file_path() -> str:
    """Returns the path to the file with traceback."""
    file_path = "traceback.txt"
    with open(file_path, "w") as file:
        traceback.print_exc(file=file)
    return file_path


def get_user_error_message() -> str:
    """Returns the default user error message."""
    return (
        "Виникла помилка! 😥\n\n"
        "Адміністратори вже були сповіщені про це "
        "і виправлять проблему якнайшвидше.\n\n"
        "Будь ласка, спробуйте ще раз або перезапустіть бота командою /start."
    )
