from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_to_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)

use_bot_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🤖 Botdan foydalanish 🤖")
        ]
    ]
)


async def main_menu_default_keyboard(user_role):
    if user_role == "admin":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🧑‍💼 Hr xodimlar"),  # Hr xodimlar tugmasi
                ],
                [
                    KeyboardButton(text="👥 Bo'limlar")  # Guruhlar tugmasi
                ],
                [
                    KeyboardButton(text="📥 Baholarni yuklab olish")
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "hr":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🌟 Stajorlarni baholash")
                ],
                [
                    KeyboardButton(text="👥 Bo'limlar")  # Guruhlar tugmasi
                ],
                [
                    KeyboardButton(text="📥 Baholarni yuklab olish")
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "intern":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="📊 Mening baholarim")  # Baholar reytingi tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "teacher":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🌟 Stajorlarni baholash")  # Guruhlarim tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    elif user_role == "chief":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🌟 Stajorlarni baholash")  # Guruhlarim tugmasi
                ],
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening profilim tugmasi
                ]
            ]
        )
    else:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="👤 Mening Profilim")  # Mening Profilim tugmasi
                ]
            ]
        )

    return markup


go_back_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ]
)
