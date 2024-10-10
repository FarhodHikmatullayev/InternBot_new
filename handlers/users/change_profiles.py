from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.change_profile_keyboard import next_change_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.change_profile_states import ChangeProfileState


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
        full_name = user['full_name']
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        phone_number = user['phone']
        if user_role != 'user':
            await ChangeProfileState.user_id.set()
            await state.update_data(
                user_id=user['id'],
                first_name=first_name,
                phone_number=phone_number,
                last_name=last_name
            )
            await message.answer(text="🆕 Yangi ism kiriting:\n"
                                      "Agar ismni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                                 reply_markup=next_change_default_keyboard)
            await ChangeProfileState.first_name.set()

        else:
            text = "❌ Sizda hali profil mavjud emas"
            await message.reply(text=text)
            return


@dp.message_handler(state=ChangeProfileState.first_name, text="Keyingi 🔜")
@dp.message_handler(state=ChangeProfileState.first_name)
async def get_first_name_function(message: types.Message, state: FSMContext):
    first_name = message.text
    if first_name != "Keyingi 🔜":
        await state.update_data(first_name=first_name)
    await message.answer(text="🆕 Yangi familiya kiriting:\n"
                              "Agar familiyani o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await ChangeProfileState.last_name.set()


@dp.message_handler(state=ChangeProfileState.last_name, text="Keyingi 🔜")
@dp.message_handler(state=ChangeProfileState.last_name)
async def get_last_name_function(message: types.Message, state: FSMContext):
    last_name = message.text
    if last_name != "Keyingi 🔜":
        await state.update_data(last_name=last_name)
    await message.answer(text="🆕 Yangi telefon raqam kiriting:\n"
                              "Agar telefon raqamni o'zgartirmoqchi bo'lmasangiz, 'Keyingi' tugmani bosing 👇",
                         reply_markup=next_change_default_keyboard)
    await ChangeProfileState.phone_number.set()


@dp.callback_query_handler(text='yes', state=ChangeProfileState.phone_number)
async def save_changes_profile_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    user_id = data.get('user_id')
    full_name = f"{first_name} {last_name}"
    user = await db.update_user(
        user_id=user_id,
        full_name=full_name,
        phone=phone_number,
    )
    await call.message.answer(text="✅ Profil muvaffaqiyatli o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=ChangeProfileState.phone_number)
async def cancel_changes_profile_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Profil o'zgarishini rad etdingiz", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=ChangeProfileState.phone_number, text="Keyingi 🔜")
@dp.message_handler(state=ChangeProfileState.phone_number)
async def get_phone_number_function(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number != "Keyingi 🔜":
        await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")

    text = (f"🔄 Profilingiz o'zgarishlardan so'ng quyidagicha bo'ladi 👇\n"
            f"🧑‍💼 Ismingiz: {first_name}\n"
            f"👤 Familiyangiz: {last_name}\n"
            f"📞 Telefon raqamingiz: {phone_number}\n")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)
