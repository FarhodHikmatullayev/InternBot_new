from aiogram import types
from aiogram.dispatcher import FSMContext
from jinja2 import pass_environment

from keyboards.default.go_to_registration import go_registration_default_keyboard
from loader import dp, db, bot


@dp.message_handler(text="✏️ Profilni o'zgartirish", state="*")
async def start_change_profile(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.reply(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                 "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                            reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role == 'admin':
            pass
        elif user_role == 'teacher':
            pass
        elif user_role == 'intern':
            pass
        elif user_role == 'chief':
            pass
        elif user_role == 'hr':
            pass
        else:
            text = "❌ Sizda hali profil mavjud emas"
            await message.reply(text=text)
            return

