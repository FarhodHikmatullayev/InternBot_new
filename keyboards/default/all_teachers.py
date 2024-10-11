from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.db.models.lookups import Regex

from loader import db


async def all_teachers_in_the_department_default_keyboard(department_id):
    teachers = await db.select_teacher_profiles(department_id=department_id)
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for teacher in teachers:
        user_id = teacher['user_id']
        user = await db.select_user(user_id=user_id)
        text_button = user['full_name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup
