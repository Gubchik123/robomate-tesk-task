from typing import Union

from aiogram import Dispatcher, F
from aiogram.types import ErrorEvent, Message, CallbackQuery

from utils.admins import notify_admins_on_startup_of_
from utils.error import send_message_about_error
from utils.bot_commands import set_default_commands_for_
from middlewares import CallbackQueryTimeoutMiddleware

from bot import bot
from handlers import handlers_router


dispatcher = Dispatcher()


@dispatcher.error(
    F.update.message.as_("event") | F.update.callback_query.as_("event")
)
async def handle_all_errors(
    error_event: ErrorEvent, event: Union[Message, CallbackQuery]
):
    """Handles all errors."""
    error = error_event.exception
    await send_message_about_error(
        event, str(error), error_place=f" {str(error.__class__)[8:-2]}"
    )


@dispatcher.startup()
async def on_startup() -> None:
    """Runs useful functions on bot startup."""
    dispatcher.include_router(handlers_router)
    _register_middlewares()
    await set_default_commands_for_(bot)
    await notify_admins_on_startup_of_(bot)


def _register_middlewares() -> None:
    """Registers middlewares."""
    # CallbackQuery middlewares
    dispatcher.callback_query.middleware(CallbackQueryTimeoutMiddleware())


if __name__ == "__main__":
    dispatcher.run_polling(bot)
