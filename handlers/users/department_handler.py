from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all_departments import all_departments_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from loader import dp, db, bot
from states.department_states import DepartmentState


@dp.message_handler(text="👥 Bo'limlar", state="*")
async def go_to_departments(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
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
        if user_role not in ['hr', 'admin']:
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
            return
        markup = await all_departments_default_keyboard()
        await message.answer(text="Bo'limlardan birini tanlang 👇", reply_markup=markup)
        await DepartmentState.department_id.set()


@dp.message_handler(state="")
