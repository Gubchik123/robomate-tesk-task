from typing import Dict, Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_dict_inline_keyboard(
    items: Dict[str, Union[str, int]], callback_data: str
) -> InlineKeyboardMarkup:
    """Returns a dict inline keyboard with the given items."""
    return (
        InlineKeyboardBuilder()
        .row(
            *[
                InlineKeyboardButton(
                    text=key, callback_data=f"{callback_data}:{value}"
                )
                for key, value in items.items()
            ],
            width=1,
        )
        .as_markup()
    )
