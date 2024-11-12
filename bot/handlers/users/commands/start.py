from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from utils.decorators import clear_state_before

from ..menu import handle_menu


router = Router()


@router.message(CommandStart())
@clear_state_before
async def handle_start_command(message: Message):
    """Handles the /start command."""
    await message.answer_sticker(
        "CAACAgIAAxkBAAENG_pnMx2l0j2ceR1pPO86hRDoAAH9Fj4AAisHAAJjK-IJn8R5tQ5lfPI2BA"
    )
    await message.answer(
        f"Hello, {message.from_user.full_name}!\n"
        "I am the bot who will help you find a resume from popular work sites."
    )
    await handle_menu(message)
