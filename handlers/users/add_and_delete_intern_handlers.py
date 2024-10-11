from aiogram import types
from aiogram.dispatcher import FSMContext
from pyexpat.errors import messages

from keyboards.default.all_interns import all_interns_in_department_default_keyboard
from keyboards.default.all_teachers import all_teachers_in_the_department_default_keyboard
from keyboards.default.all_users import all_users_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.department_states import DepartmentState
from states.intern_states import CreateInternState, DeleteInternState


@dp.message_handler(state=CreateInternState.teacher_id, text="🔙 Orqaga")
@dp.message_handler(state=DepartmentState.department_id, text="➕ Stajor qo'shish")
async def start_creating_new_intern_to_the_department(message: types.Message, state: FSMContext):
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
        markup = await all_users_default_keyboard()
        await message.answer(text="Yangi stajor qo'shish uchun foydalanuvchilardan bini tanlang 👇", reply_markup=markup)
        await CreateInternState.user_id.set()
        await state.update_data(department_id=department_id)


@dp.message_handler(state=DepartmentState.department_id, text="🗑️ Stajorni o'chirish")
async def start_deleting_intern_from_department(message: types.Message, state: FSMContext):
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
        markup = await all_interns_in_department_default_keyboard(department_id=department_id)
        await message.answer(text="O'chirish uchun stajorlardan birini tanlang", reply_markup=markup)
        await DeleteInternState.intern_id.set()
        await state.update_data(department_id=department_id)


# for create new intern to the department
@dp.message_handler(state=CreateInternState.internship_period, text="🔙 Orqaga")
@dp.message_handler(state=CreateInternState.user_id)
async def get_intern_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    if full_name != "🔙 Orqaga":
        users = await db.select_users(full_name=full_name)
        if not users:
            await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi", reply_markup=go_back_default_keyboard)
            return
        user = users[0]
        await state.update_data(user_id=user['id'])
    data = await state.get_data()
    department_id = data.get('department_id')
    markup = await all_teachers_in_the_department_default_keyboard(department_id=department_id)
    await message.answer(text="Bu stajor uchun mas'ul xodimlardan birini tanlang 👇", reply_markup=markup)
    await CreateInternState.teacher_id.set()


@dp.message_handler(state=CreateInternState.teacher_id)
async def get_teacher_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    users = await db.select_users(full_name=full_name)
    if not users:
        await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi", reply_markup=go_back_default_keyboard)
        return
    user = users[0]
    teachers = await db.select_teacher_profiles(user_id=user['id'])
    teacher = teachers[0]
    await state.update_data(teacher_id=teacher['id'])
    await message.answer(text="Stajirovka muddatini kiriting: (Misol 3)", reply_markup=go_back_default_keyboard)
    await CreateInternState.internship_period.set()


@dp.callback_query_handler(state=CreateInternState.internship_period, text='yes')
async def create_intern_final_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print('data', data)
    user_id = data.get('user_id')
    teacher_id = data.get('teacher_id')
    internship_period = data.get('internship_period')
    department_id = data.get('department_id')
    await db.create_intern_profile(
        user_id=user_id,
        teacher_id=teacher_id,
        department_id=department_id,
        internship_period=internship_period
    )
    await db.update_user(
        user_id=user_id,
        role='intern'
    )
    await call.message.answer(text="✅ Stajor qo'shildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateInternState.internship_period, text="no")
async def cancel_creating_intern(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Stajor qo'shish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateInternState.internship_period)
async def get_internship_period(message: types.Message, state: FSMContext):
    period = message.text
    try:
        period = int(period)
    except:
        await message.answer(text="⚠️ Stajirovka muddati son orqali kiritiladi, iltimos qayta kiriting:",
                             reply_markup=go_back_default_keyboard)
        return

    data = await state.get_data()
    user_id = data.get('user_id')
    teacher_id = data.get('teacher_id')
    department_id = data.get('department_id')
    department = await db.select_department(department_id=department_id)
    user = await db.select_user(user_id=user_id)
    teacher = await db.select_teacher_profile(profile_id=teacher_id)
    teacher_user_id = teacher['user_id']
    teacher_user = await db.select_user(user_id=teacher_user_id)

    await state.update_data(internship_period=period)
    text = (f"📋 Stajor ma'lumotlari:\n"
            f"👤 F.I.Sh: {user['full_name']}\n"
            f"🏢 Bo'lim: {department['name']}\n"
            f"👨‍🏫 Biriktirilgan xodim: {teacher_user['full_name']}\n"
            f"🗓️ Stajirovka muddati: {period} kun")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi❓", reply_markup=confirm_keyboard)


# for delete intern from department
@dp.callback_query_handler(state=DeleteInternState.intern_id, text='yes')
async def delete_intern_final_function(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print('data', data)
    user_id = data.get('user_id')
    intern_id = data.get('intern_id')
    department_id = data.get('department_id')
    user = await db.update_user(
        user_id=user_id,
        role='user'
    )
    marks = await db.select_marks(intern_id=intern_id)
    for mark in marks:
        await db.delete_mark(mark_id=mark['id'])
    await db.delete_intern_profile(profile_id=intern_id)
    await call.message.answer(text="✅ Stajor o'chirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

@dp.callback_query_handler(state=DeleteInternState.intern_id, text='no')
async def cancel_delete_intern_from_department(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'chirish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=DeleteInternState.intern_id)
async def get_intern_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    users = await db.select_users(full_name=full_name)
    if not users:
        await message.answer(text="⚠️ Bunday foydalanuvchi topilmadi", reply_markup=back_to_menu)
        return
    user = users[0]
    user_id = user['id']
    interns = await db.select_intern_profiles(user_id=user_id)
    intern = interns[0]
    intern_id = intern['id']
    data = await state.get_data()
    department_id = data.get('department_id')
    await state.update_data(user_id=user_id, intern_id=intern_id)
    department = await db.select_department(department_id=department_id)
    await message.answer(text=f"Haqiqatdan ham {user['full_name']}ni stajorlikdan chiqarmoqchimisiz❓",
                         reply_markup=confirm_keyboard)
