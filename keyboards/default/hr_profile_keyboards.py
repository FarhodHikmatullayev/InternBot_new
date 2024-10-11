from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

hr_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ HR xodim qo'shish"),
            KeyboardButton(text="➖ HR xodimni o'chirish")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu")
        ]
    ]
)
