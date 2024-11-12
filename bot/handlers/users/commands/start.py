from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

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
        _(
            "Привіт, {name}!\n"
            "Я той, хто допоможе Вам знайти резюме з популярних сайтів роботи."
        ).format(name=message.from_user.full_name)
    )
    await handle_menu(message)
