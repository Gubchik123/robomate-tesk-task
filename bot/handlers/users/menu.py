from aiogram import Router, F
from aiogram.types import Message

from keyboards.default.menu import get_menu_keyboard


router = Router()


@router.callback_query(F.data == "btn_menu")
async def handle_menu(message: Message) -> None:
    """Handles main menu."""
    await message.answer(
        "You are on the main menu.\n"
        "Choose further steps using the buttons below.",
        reply_markup=get_menu_keyboard(),
    )
