from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_hr_profiles_default_keyboard():
    hrs = await db.select_all_hr_profiles()
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for hr in hrs:
        user_id = hr['user_id']
        user = await db.select_user(user_id=user_id)
        text_button = user['full_name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup