from aiogram import Router

from .commands import commands_router
from .menu import router as menu_router
from .resume import router as resume_router
from .other import router as other_router


users_router = Router()

users_router.include_routers(  # ! Order is important
    commands_router,
    menu_router,
    resume_router,
    other_router,
)
