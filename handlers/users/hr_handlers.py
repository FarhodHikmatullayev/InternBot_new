from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all_hrs import all_hr_profiles_default_keyboard
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.hr_profile_keyboards import hr_actions_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.hr_states import CreateHrProfileState, DeleteHrProfileState
from states.teacher_states import DeleteTeacherProfileState


@dp.message_handler(state=[CreateHrProfileState.user_id, DeleteHrProfileState.user_id], text="🔙 Orqaga")
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
            text = "👥 Barcha HR xodimlar:\n"
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


@dp.message_handler(text="➕ HR xodim qo'shish", state='*')
async def add_hr_profile(message: types.Message, state: FSMContext):
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
            markup = await all_users_default_keyboard()
            await message.answer(text="HR xodim qo'shish uchun foydalanuvchilardan birini tanlang 👇",
                                 reply_markup=markup)
            await CreateHrProfileState.user_id.set()


@dp.message_handler(text="➖ HR xodimni o'chirish", state='*')
async def delete_hr_profile(message: types.Message, state: FSMContext):
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
            if not hr_profiles:
                await message.answer(text="⚠️ Hali HR xodimlar mavjud emas", reply_markup=go_back_default_keyboard)
                return
            markup = await all_hr_profiles_default_keyboard()
            await message.answer(text="O'chirish uchun HR xodimlardan birini tanlang 👇", reply_markup=markup)
            await DeleteHrProfileState.user_id.set()


# for delete hr profile
@dp.callback_query_handler(state=DeleteHrProfileState.user_id, text='yes')
async def delete_hr_profile_final_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    profile_id = data.get('profile_id')
    await db.update_user(user_id=user_id, role='user')
    await db.delete_hr_profile(profile_id=profile_id)
    await call.message.answer(text="✅ HR xodim o'chirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

@dp.callback_query_handler(state=DeleteHrProfileState.user_id, text='no')
async def cancel_deleting_hr_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'chirish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=DeleteHrProfileState.user_id)
async def get_full_name_for_delete_hr_profile(message: types.Message, state: FSMContext):
    full_name = message.text
    users = await db.select_users(full_name=full_name)
    if not users:
        await message.answer(text="⚠️ Bunday HR xodim topilmadi", reply_markup=go_back_default_keyboard)
        return
    user = users[0]
    user_id = user['id']
    hr_profiles = await db.select_hr_profiles(user_id=user_id)
    hr_profile = hr_profiles[0]
    await state.update_data(user_id=user_id, profile_id=hr_profile['id'])
    await message.answer(text=f"Haqiqatdan ham {full_name}ni HR likdan chiqarib tashlamoqchimisiz❓",
                         reply_markup=confirm_keyboard)


# for create hr profile
@dp.callback_query_handler(state=CreateHrProfileState.user_id, text='yes')
async def confirm_creating_new_hr_profile_final_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    user = await db.update_user(
        user_id=user_id,
        role='hr'
    )
    await db.create_hr_profile(user_id=user_id)
    await call.message.answer(text="✅ Hr muvaffaqiyatli qo'shildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateHrProfileState.user_id, text='no')
async def cancel_creating_hr_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlash rad etildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateHrProfileState.user_id)
async def get_hr_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    users = await db.select_users(full_name=full_name)
    if not users:
        await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi", reply_markup=go_back_default_keyboard)
        return
    user = users[0]
    user_id = user['id']
    await state.update_data(user_id=user_id)
    await message.answer(text=f"Haqiqatdan ham {full_name}ni HR xodim qilmoqchimisiz❓", reply_markup=confirm_keyboard)
