from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_departments_default_keyboard():
    departments = await db.select_all_departments()
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    markup.insert(KeyboardButton(text="➕ Yangi bo'lim qo'shish"))
    for department in departments:
        text_button = department['name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup
