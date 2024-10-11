from aiogram import types
from aiogram.dispatcher import FSMContext

import states.department_states
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.chief_states import CreateChiefProfileState, DeleteChiefProfileState
from states.department_states import DepartmentState, DeleteDepartmentState


@dp.message_handler(state=DepartmentState.department_id, text="➕ Bo'lim boshlig'i qo'shish")
async def start_creating_chief(message: types.Message, state: FSMContext):
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
        data = await state.get_data()
        department_id = data.get('department_id')
        department = await db.select_department(department_id=department_id)
        markup = await all_users_default_keyboard()
        await message.answer(
            text=f"{department['name']} bo'limi boshlig'ini qo'shish uchun foydalanuvchilardan birini tanlang 👇",
            reply_markup=markup)
        await CreateChiefProfileState.user_id.set()
        await state.update_data(department_id=department_id)


@dp.message_handler(state=DepartmentState.department_id, text="🗑️ Bo'lim boshlig'ini o'chirish")
async def start_deleting_chief(message: types.Message, state: FSMContext):
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
        data = await state.get_data()
        department_id = data.get('department_id')
        department = await db.select_department(department_id=department_id)
        chiefs = await db.select_chief_profiles(department_id=department_id)
        if not chiefs:
            await message.answer(text=f"🚫 {department['name']} bo'limi uchun hali bo'lim boshlig'i mavjude emas",
                                 reply_markup=go_back_default_keyboard)
            return
        chief = chiefs[0]
        chief_user_id = chief['user_id']
        chief_user = await db.select_user(user_id=chief_user_id)
        chief_full_name = chief_user['full_name']
        await message.answer(
            text=f"Haqiqatdan ham {chief_full_name}ni {department['name']} bo'limi boshliqligidan chiqarib tashlamoqchimisiz❓",
            reply_markup=confirm_keyboard)
        await DeleteChiefProfileState.department_id.set()
        await state.update_data(department_id=department_id, user_id=chief_user_id, profile_id=chief['id'])

@dp.callback_query_handler(state=DeleteChiefProfileState.department_id, text='yes')
async def delete_chief(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    department_id = data.get('department_id')
    user_id = data.get('user_id')
    profile_id = data.get('profile_id')
    await db.delete_chief_profile(profile_id=profile_id)
    await db.update_user(user_id=user_id, role='user')
    await call.message.answer(text="✅ Bo'lim boshlig'i o'chirib yuborildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

@dp.callback_query_handler(state=DeleteChiefProfileState.department_id, text="no")
async def cancel_delete_chief(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'chirish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()