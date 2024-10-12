from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_interns_default_keyboard():
    interns = await db.select_all_intern_profiles()
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for intern in interns:
        user_id = intern['user_id']
        user = await db.select_user(user_id=user_id)
        text_button = user['full_name']
        markup.insert(KeyboardButton(text=text_button))

    markup.insert(KeyboardButton(text="🔙 Bosh Menyu"))
    return markup


async def all_interns_in_department_default_keyboard(department_id):
    interns = await db.select_intern_profiles(department_id=department_id)
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for intern in interns:
        user_id = intern['user_id']
        user = await db.select_user(user_id=user_id)
        text_button = user['full_name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup
