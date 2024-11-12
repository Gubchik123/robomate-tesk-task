from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_default_commands_for_(bot: Bot) -> None:
    """Sets default bot commands for uk and en languages."""
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="start", description="Start working with the bot"
            ),
            BotCommand(command="help", description="Get basic usage rules"),
            BotCommand(command="menu", description="Get main menu"),
            BotCommand(
                command="cancel", description="Cancel the current operation"
            ),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
