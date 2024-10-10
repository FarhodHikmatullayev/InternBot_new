from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

department_actions_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔄 Bo'limni o'zgartirish"),
            KeyboardButton(text="🗑️ Bo'limni o'chirish"),
        ],
        [
            KeyboardButton(text="➕ Stajor qo'shish"),
            KeyboardButton(text="🗑️ Stajorni o'chirish")
        ],
        [
            KeyboardButton(text="➕ Bo'lim boshlig'i qo'shish"),
            KeyboardButton(text="🗑️ Bo'lim boshlig'ini o'chirish")
        ],
        [
            KeyboardButton(text="➕ Mas'ul xodim qo'shish"),
            KeyboardButton(text="🗑️ Mas'ul xodimni o'chirish")
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ]
)
