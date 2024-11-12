from aiogram.fsm.state import State, StatesGroup


class Resume(StatesGroup):
    """States to search for a resume."""

    position = State()
    location = State()
    experience = State()
    salary_from = State()
    salary_to = State()
