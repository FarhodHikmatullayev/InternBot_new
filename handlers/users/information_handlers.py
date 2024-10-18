import os
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu
from loader import dp, db, bot


@dp.message_handler(text="🏢 Kompaniya haqida ma'lumot", state="*")
async def get_pdf_information(message: types.Message, state: FSMContext):
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
        return
    user = users[0]
    user_role = user['role']
    if user_role != 'intern':
        await message.reply(text="⚠️ Bu buyruqdan foydalanish uchun sizda ruxsat mavjud emas!",
                            reply_markup=back_to_menu)
        return
    pdf_documents = await db.select_all_information_pdfs()  # Agar birinchi faylni olishni xohlasangiz
    if pdf_documents and pdf_documents[0]['pdf_file']:
        # file_path = 'media/pdfs/FARHODJON_HIKMATULLAYEVV.docx'
        file_path = 'media/' + pdf_documents[0]['pdf_file']
        if os.path.exists(file_path):  # Fayl mavjudligini tekshirish
            with open(file_path, 'rb') as doc_file:
                await bot.send_document(chat_id=message.chat.id, document=doc_file)
        else:
            await message.reply("Kechirasiz, fayl topilmadi.")
