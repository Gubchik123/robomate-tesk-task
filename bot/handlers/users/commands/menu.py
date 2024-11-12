from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import clear_state_before

from ..menu import handle_menu


router = Router()


@router.message(Command("menu"))
@router.message(Command("cancel"))
@clear_state_before
async def handle_menu_command(message: Message, *args) -> None:
    """Handles the /menu and /cancel commands."""
    await handle_menu(message)
