from aiogram.types import ReplyKeyboardMarkup

from .maker import make_keyboard, make_button


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Returns cancel keyboard."""
    return make_keyboard([[make_button("/cancel")]])
