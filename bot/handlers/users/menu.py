from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from keyboards.default.menu import get_menu_keyboard


router = Router()


@router.callback_query(F.data == "btn_menu")
async def handle_menu(message: Message) -> None:
    """Handles main menu."""
    await message.answer(
        _(
            "Ви у головному меню.\n"
            "Виберіть подальші дії за допомогою кнопок нижче."
        ),
        reply_markup=get_menu_keyboard(),
    )
