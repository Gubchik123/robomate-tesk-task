from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.resume import Resume
from data.config import JOB_SITES
from utils.resumes import get_resume_scraper_by_
from keyboards.default.cancel import get_cancel_keyboard
from keyboards.inline.maker import make_dict_inline_keyboard

from .menu import handle_menu


router = Router()


@router.message(F.text.lower().in_(JOB_SITES))
async def handle_resume(message: Message, state: FSMContext):
    """Handles the start of the given job site resume searching."""
    await message.answer("Введіть позицію", reply_markup=get_cancel_keyboard())
    await state.set_state(Resume.position)
    await state.update_data(site_name=message.text.lower())


@router.message(Resume.position)
async def handle_position_input(message: Message, state: FSMContext):
    """Handles the position input."""
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    await message.answer(
        "Оберіть або введіть локацію",
        reply_markup=make_dict_inline_keyboard(
            resume_scraper.get_locations(), "location"
        ),
    )
    await state.update_data(position=message.text)
    await state.set_state(Resume.location)


@router.message(Resume.location)
@router.callback_query(Resume.location, F.data.startswith("location"))
async def handle_location(
    event: Union[Message, CallbackQuery], state: FSMContext
):
    """Handles the location input or choice."""
    location = (
        event.text if isinstance(event, Message) else event.data.split(":")[1]
    )
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    url = resume_scraper.get_url_by_(data["position"], location)
    answer_method = (
        event.answer if isinstance(event, Message) else event.message.edit_text
    )
    await answer_method(
        "Оберіть досвід роботи",
        reply_markup=make_dict_inline_keyboard(
            resume_scraper.get_experience_by_(url), "experience"
        ),
    )
    await state.update_data(location=location)
    await state.set_state(Resume.experience)


@router.callback_query(Resume.experience, F.data.startswith("experience"))
async def handle_experience(query: CallbackQuery, state: FSMContext):
    """Handles the experience choice."""
    experience = query.data.split(":")[1]
    await state.update_data(experience=experience)
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    url = resume_scraper.get_url_by_(
        data["position"], data["location"], {"experience": experience}
    )
    salary_from = resume_scraper.get_salary(url, "from")
    if salary_from is None:
        return await _handle_salary_to(query, state)
    await query.message.edit_text(
        "Оберіть зарплату від",
        reply_markup=make_dict_inline_keyboard(salary_from, "salary_from"),
    )
    await state.set_state(Resume.salary_from)


async def _handle_salary_to(query: CallbackQuery, state: FSMContext):
    """Handles the salary to choice."""
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    url = resume_scraper.get_url_by_(
        data["position"], data["location"], {"experience": data["experience"]}
    )
    salary_to = resume_scraper.get_salary(url, "to")
    if salary_to is None:
        return await _handle_search(query, state)
    await query.message.edit_text(
        "Оберіть зарплату до",
        reply_markup=make_dict_inline_keyboard(salary_to, "salary_to"),
    )
    await state.set_state(Resume.salary_to)


@router.callback_query(Resume.salary_from, F.data.startswith("salary_from"))
async def handle_salary_from(query: CallbackQuery, state: FSMContext):
    """Handles the salary from choice."""
    salary_from = query.data.split(":")[1]
    await state.update_data(salary_from=salary_from)
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    url = resume_scraper.get_url_by_(
        data["position"],
        data["location"],
        {
            "experience": data["experience"],
            "salary_from": data["salary_from"],
        },
    )
    salary_to = resume_scraper.get_salary(url, "to")
    if salary_to is None:
        return await _handle_search(query, state)
    await query.message.edit_text(
        "Оберіть зарплату до",
        reply_markup=make_dict_inline_keyboard(salary_to, "salary_to"),
    )
    await state.set_state(Resume.salary_to)


@router.callback_query(Resume.salary_to, F.data.startswith("salary_to"))
async def handle_salary_to(query: CallbackQuery, state: FSMContext):
    """Handles the salary to choice."""
    salary_to = query.data.split(":")[1]
    await state.update_data(salary_to=salary_to)
    await _handle_search(query, state)


async def _handle_search(query: CallbackQuery, state: FSMContext):
    """Handles the resume search."""
    data = await state.get_data()
    resume_scraper = get_resume_scraper_by_(data["site_name"])

    url = resume_scraper.get_url_by_(
        data["position"],
        data["location"],
        {
            "experience": data["experience"],
            "salary_from": data.get("salary_from"),
            "salary_to": data.get("salary_to"),
        },
    )
    await query.message.edit_text(
        resume_scraper.parse_resumes(url),
        reply_markup=None,
        disable_web_page_preview=True,
    )
    await state.clear()
    await handle_menu(query.message)
