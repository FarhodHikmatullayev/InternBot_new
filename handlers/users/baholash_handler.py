from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.intern_keyboards import interns_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.mark_keyboards import marks_keyboard
from loader import dp, db, bot
from states.mark_states import CreateMarkState


@dp.message_handler(text="🔙 Orqaga", state=CreateMarkState.intern_id)
@dp.message_handler(text="🌟 Stajorlarni baholash", state='*')
async def mark_function(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="🚫 Sizda botdan foydalanish uchun ruxsat mavjud emas,\n"
                                  "📝 Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak 👇",
                             reply_markup=go_registration_default_keyboard)
    else:
        user = users[0]
        user_role = user['role']
        if user_role in ['intern', 'admin', 'user']:
            await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                                reply_markup=back_to_menu)
        else:
            markup = await interns_default_keyboard(user_id=user['id'])
            await message.answer(text="Baholash uchun stajorlardan birini tanlang 👇", reply_markup=markup)
            await CreateMarkState.intern_id.set()


@dp.message_handler(state=CreateMarkState.intern_id)
async def get_intern_id(message: types.Message, state: FSMContext):
    intern_full_name = message.text
    users = await db.select_users(full_name=intern_full_name)

    if not users:
        await message.answer(text="⚠️ Bu stajor allaqachon o'chirib yuborilgan",
                             reply_markup=go_back_default_keyboard)
        return
    user = users[0]
    user_id = user['id']
    interns = await db.select_intern_profiles(user_id=user_id)
    intern = interns[0]
    intern_id = intern['id']
    rated_by_telegram_id = message.from_user.id
    rated_by_users = await db.select_users(telegram_id=rated_by_telegram_id)
    rated_user = rated_by_users[0]
    rated_user_id = rated_user['id']
    intern_marks = await db.select_today_marks(intern_id=intern_id, rated_by_id=rated_user_id)
    if intern_marks:
        await message.answer(
            text="⚠️ Bu stajorga allaqachon baho qo'ydingiz, bir kun uchun bir marta baho qo'yish mumkin",
            reply_markup=go_back_default_keyboard)
        return
    await state.update_data(intern_id=intern_id)
    await message.answer(text="Bosh menyuga qaytish uchun 'Bosh Menyu' tugmasini bosing 👇", reply_markup=back_to_menu)
    await message.answer(text="Stajorning muomalasiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.muomala.set()


@dp.callback_query_handler(state=CreateMarkState.muomala)
async def get_muomala_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(muomala=mark)
    await call.message.edit_text(text="Stajorning kirishimliligiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.kirishimlilik.set()


@dp.callback_query_handler(state=CreateMarkState.kirishimlilik)
async def get_kirishimlilik_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(kirishimlilik=mark)
    await call.message.edit_text(text="Stajorning chaqqonligi va malakasiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.chaqqonlik_va_malaka.set()


@dp.callback_query_handler(state=CreateMarkState.chaqqonlik_va_malaka)
async def get_chaqqonlik_va_malaka_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(chaqqonlik_va_malaka=mark)
    await call.message.edit_text(text="Stajorning masuliyatiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.masuliyat.set()


@dp.callback_query_handler(state=CreateMarkState.masuliyat)
async def get_masuliyat_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(masuliyat=mark)
    await call.message.edit_text(text="Stajorning o'zlashtirish qobiliyatiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.ozlashtirish_qobiliyati.set()


@dp.callback_query_handler(state=CreateMarkState.ozlashtirish_qobiliyati)
async def get_ozlashtirish_qobiliyati_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(ozlashtirish_qobiliyati=mark)
    await call.message.edit_text(text="Stajorning ichki tartibga rioya qilishiga baho bering:",
                                 reply_markup=marks_keyboard)
    await CreateMarkState.ichki_tartibga_rioyasi.set()


@dp.callback_query_handler(state=CreateMarkState.ichki_tartibga_rioyasi)
async def get_ichki_tartibga_rioyasi_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(ichki_tartibga_rioyasi=mark)
    await call.message.edit_text(text="Stajorning shaxsiy intizomiga baho bering:", reply_markup=marks_keyboard)
    await CreateMarkState.shaxsiy_intizomi.set()


@dp.callback_query_handler(state=CreateMarkState.shaxsiy_intizomi, text="yes")
async def confirm_getting_description(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="✍️ Izoh yozing", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await CreateMarkState.description.set()


@dp.callback_query_handler(state=CreateMarkState.shaxsiy_intizomi, text='no')
async def cancel_getting_description(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    intern_id = data.get("intern_id")
    muomala = data.get("muomala")
    kirishimlilik = data.get("kirishimlilik")
    chaqqonlik_va_malaka = data.get("chaqqonlik_va_malaka")
    masuliyat = data.get("masuliyat")
    ozlashtirish_qobiliyati = data.get("ozlashtirish_qobiliyati")
    ichki_tartibga_rioyasi = data.get("ichki_tartibga_rioyasi")
    shaxsiy_intizomi = data.get("shaxsiy_intizomi")

    intern_profile = await db.select_intern_profile(profile_id=intern_id)
    user_id = intern_profile['user_id']
    user = await db.select_user(user_id=user_id)
    full_name = user['full_name']

    text = (f"Siz quyidagicha baholadingiz: ⭐\n"
            f"👤 Stajor: {full_name}\n"
            f"🤝 Muomalasi: {muomala}\n"
            f"🚀 Kirishimliligi: {kirishimlilik}\n"
            f"⚡  Chaqqonligi va malakasi: {chaqqonlik_va_malaka}\n"
            f"🔒 Mas'uliyati: {masuliyat}\n"
            f"🧠 O'zlashtirish qobiliyati: {ozlashtirish_qobiliyati}\n"
            f"📋 Ichki tartibga rioyasi: {ichki_tartibga_rioyasi}\n"
            f"🕵️‍♂️ Shaxsiy intizomi: {shaxsiy_intizomi}\n")
    await call.message.edit_text(text=text)
    await call.message.answer(text="Bu bahoni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)
    await CreateMarkState.description.set()


@dp.callback_query_handler(state=CreateMarkState.shaxsiy_intizomi)
async def get_shaxsiy_intizomi_mark(call: types.CallbackQuery, state: FSMContext):
    mark = call.data
    mark = int(mark)
    await state.update_data(shaxsiy_intizomi=mark)
    await call.message.edit_text(text="Nega bunday baholaganingizga izoh yozasizmi?", reply_markup=confirm_keyboard)


@dp.callback_query_handler(state=CreateMarkState.description, text="yes")
async def save_mark_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    intern_id = data.get("intern_id")
    muomala = data.get("muomala")
    kirishimlilik = data.get("kirishimlilik")
    chaqqonlik_va_malaka = data.get("chaqqonlik_va_malaka")
    masuliyat = data.get("masuliyat")
    ozlashtirish_qobiliyati = data.get("ozlashtirish_qobiliyati")
    ichki_tartibga_rioyasi = data.get("ichki_tartibga_rioyasi")
    shaxsiy_intizomi = data.get("shaxsiy_intizomi")
    description = data.get('description')

    rated_by = call.from_user.id
    rated_users = await db.select_users(telegram_id=rated_by)
    rated_user = rated_users[0]
    rated_by_id = rated_user['id']
    rated_user_full_name = rated_user['full_name']
    rated_user_role = rated_user['role']

    mark = await db.create_mark(
        intern_id=intern_id,
        muomala=muomala,
        kirishimlilik=kirishimlilik,
        chaqqonlik_va_malaka=chaqqonlik_va_malaka,
        masuliyat=masuliyat,
        ozlashtirish_qobiliyati=ozlashtirish_qobiliyati,
        ichki_tartibga_rioyasi=ichki_tartibga_rioyasi,
        shaxsiy_intizomi=shaxsiy_intizomi,
        description=description,
        rated_by_id=rated_by_id
    )
    intern_profile = await db.select_intern_profile(profile_id=intern_id)
    user_id = intern_profile['user_id']
    user = await db.select_user(user_id=user_id)
    full_name = user['full_name']

    if rated_user_role == 'teacher':
        role = "Ustoz xodim"
    elif rated_user_role == 'chief':
        role = "Bo'lim boshlig'i"
    else:
        role = 'HR xodim'

    text = (f"Sizning bugungi bahoyingiz: 🌟\n"
            f"🏅 Baholagan shaxs: {role} {rated_user_full_name}\n"
            f"🤝 Muomalasi: {muomala}\n"
            f"🚀 Kirishimliligi: {kirishimlilik}\n"
            f"⚡  Chaqqonligi va malakasi: {chaqqonlik_va_malaka}\n"
            f"🔒 Mas'uliyati: {masuliyat}\n"
            f"🧠 O'zlashtirish qobiliyati: {ozlashtirish_qobiliyati}\n"
            f"📋 Ichki tartibga rioyasi: {ichki_tartibga_rioyasi}\n"
            f"🕵️‍♂️ Shaxsiy intizomi: {shaxsiy_intizomi}")

    if description:
        text += f"\n💬 Izoh: {description}"

    user_telegram_id = user['telegram_id']
    await bot.send_message(chat_id=user_telegram_id, text=text)

    await call.message.answer(text="✅ Baho saqlandi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateMarkState.description, text="no")
async def cancel_saving_mark(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Bahoni saqlash bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateMarkState.description)
async def get_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    data = await state.get_data()
    intern_id = data.get("intern_id")
    muomala = data.get("muomala")
    kirishimlilik = data.get("kirishimlilik")
    chaqqonlik_va_malaka = data.get("chaqqonlik_va_malaka")
    masuliyat = data.get("masuliyat")
    ozlashtirish_qobiliyati = data.get("ozlashtirish_qobiliyati")
    ichki_tartibga_rioyasi = data.get("ichki_tartibga_rioyasi")
    shaxsiy_intizomi = data.get("shaxsiy_intizomi")
    description = data.get('description')

    intern_profile = await db.select_intern_profile(profile_id=intern_id)
    user_id = intern_profile['user_id']
    user = await db.select_user(user_id=user_id)
    full_name = user['full_name']

    text = (f"Siz quyidagicha baholadingiz: ⭐\n"
            f"👤 Stajor: {full_name}\n"
            f"🤝 Muomalasi: {muomala}\n"
            f"🚀 Kirishimliligi: {kirishimlilik}\n"
            f"⚡  Chaqqonligi va malakasi: {chaqqonlik_va_malaka}\n"
            f"🔒 Mas'uliyati: {masuliyat}\n"
            f"🧠 O'zlashtirish qobiliyati: {ozlashtirish_qobiliyati}\n"
            f"📋 Ichki tartibga rioyasi: {ichki_tartibga_rioyasi}\n"
            f"🕵️‍♂️ Shaxsiy intizomi: {shaxsiy_intizomi}\n"
            f"💬 Izohingiz: {description}")  # Izoh uchun ikonka
    await message.answer(text=text)
    await message.answer(text="Bu bahoni saqlashni xohlaysizmi?", reply_markup=confirm_keyboard)
