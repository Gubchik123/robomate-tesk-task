from aiogram.types import ReplyKeyboardMarkup

from data.config import JOB_SITES
from .maker import make_keyboard, make_button


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns main menu keyboard."""
    return make_keyboard(
        [[make_button(job_site)] for job_site in JOB_SITES], one_time=True
    )
