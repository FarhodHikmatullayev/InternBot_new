from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def interns_default_keyboard(user_id):
    teacher_profiles = await db.select_teacher_profiles(user_id=user_id)
    hr_profiles = await db.select_hr_profiles(user_id=user_id)
    chief_profiles = await db.select_chief_profiles(user_id=user_id)
    if hr_profiles:
        interns = await db.select_all_intern_profiles()
    elif chief_profiles:
        chief_profile = chief_profiles[0]
        department_id = chief_profile['department_id']
        interns = await db.select_intern_profiles(department_id=department_id)
    else:
        teacher = teacher_profiles[0]
        interns = await db.select_intern_profiles(teacher_id=teacher['id'])

    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for intern in interns:
        user_id = intern['user_id']
        user = await db.select_user(user_id=user_id)
        text_button = user['full_name']
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Bosh Menyu"))

    return markup
