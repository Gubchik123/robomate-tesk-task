from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_default_commands_for_(bot: Bot) -> None:
    """Sets default bot commands for uk and en languages."""
    bot_commands = {
        "uk": [],
        "en": [],
    }
    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=language_code,
        )
