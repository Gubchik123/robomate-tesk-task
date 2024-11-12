from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import clear_state_before


router = Router()


@router.message(Command("help"))
@clear_state_before
async def handle_help_command(message: Message, *args):
    """Handles the /help command."""
    await message.answer()
