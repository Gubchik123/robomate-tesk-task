from aiogram import Router
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message()
async def handle_all_other_messages(message: Message):
    """Handles all other messages."""
    try:
        await message.answer(
            "I don't understand you :(\n"
            "I advise you to use buttons or commands for the result."
        )
    except TelegramBadRequest:
        pass
