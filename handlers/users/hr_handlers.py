from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.hr_profile_keyboards import hr_actions_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from loader import dp, db, bot


@dp.message_handler(text="🧑‍💼 Hr xodimlar", state='*')
async def get_hr_profiles(message: types.Message, state: FSMContext):
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
        if user_role != 'admin':
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            hr_profiles = await db.select_all_hr_profiles()
            text = "Barcha HR xodimlar:\n"
            tr = 0
            for hr in hr_profiles:
                tr += 1
                user_id = hr['user_id']
                user = await db.select_user(user_id=user_id)
                full_name = user['full_name']
                text += f" {tr}. {full_name}\n"
            if tr > 0:
                await message.answer(text=text, reply_markup=hr_actions_default_keyboard)
            else:
                await message.answer(text="Hali HR xodim mavjud emas", reply_markup=hr_actions_default_keyboard)
