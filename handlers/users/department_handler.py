from aiogram import types
from aiogram.dispatcher import FSMContext
from pyexpat.errors import messages

from keyboards.default.all_departments import all_departments_default_keyboard
from keyboards.default.department_actions import department_actions_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from loader import dp, db, bot
from states.chief_states import CreateChiefProfileState
from states.department_states import DepartmentState, CreateDepartmentState, UpdateDepartmentState, \
    DeleteDepartmentState


@dp.message_handler(text="🔙 Orqaga", state=[CreateDepartmentState.name, DepartmentState.department_id])
@dp.message_handler(text="👥 Bo'limlar", state="*")
async def go_to_departments(message: types.Message, state: FSMContext):
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


@dp.message_handler(state=DepartmentState.department_id, text="➕ Yangi bo'lim qo'shish")
async def start_creating_new_department(message: types.Message, state: FSMContext):
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
        text = "📂 Yangi bo'lim uchun nom kiriting: "
        await message.answer(text=text, reply_markup=go_back_default_keyboard)
        await CreateDepartmentState.name.set()


@dp.message_handler(state=DepartmentState.department_id, text="🔄 Bo'limni o'zgartirish")
async def start_updating_department(message: types.Message, state: FSMContext):
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
        text = f"📂 {department['name']} bo'limi uchun yangi nom kiriting: "
        await message.answer(text=text, reply_markup=go_back_default_keyboard)
        await UpdateDepartmentState.name.set()
        await state.update_data(department_id=department_id)


@dp.message_handler(state=DepartmentState.department_id, text="🗑️ Bo'limni o'chirish")
async def start_updating_department(message: types.Message, state: FSMContext):
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
        department_name = department['name']
        text = f"Haqiqatdan ham {department_name} bo'limini o'chirmoqchimisiz❓"
        await message.answer(text=text, reply_markup=confirm_keyboard)
        await DeleteDepartmentState.department_id.set()
        await state.update_data(department_id=department_id)

@dp.message_handler(state=[UpdateDepartmentState.name, CreateChiefProfileState.user_id], text="🔙 Orqaga")
@dp.message_handler(state=DepartmentState.department_id)
async def get_department_name(message: types.Message, state: FSMContext):
    department_name = message.text
    if department_name != "🔙 Orqaga":
        departments = await db.select_departments(name=department_name)
        if not departments:
            text = "⚠️ Bunday bo'lim topilmadi"
            await message.answer(text=text, reply_markup=go_back_default_keyboard)
            return
        department = departments[0]
        department_id = department['id']
        await state.update_data(department_id=department_id)
        chief_profiles = await db.select_chief_profiles(department_id=department_id)
        if chief_profiles:
            chief_profile = chief_profiles[0]
            user_id = chief_profile['user_id']
            user = await db.select_user(user_id=user_id)
            department_chief_full_name = user['full_name']
        else:
            department_chief_full_name = "Hali tayinlanmagan"

        teacher_profiles = await db.select_teacher_profiles(department_id=department_id)
        if not teacher_profiles:
            teachers = "Hali mavjud emas"
        else:
            teachers = ""
            tr = 0
            for teacher in teacher_profiles:
                tr += 1
                user_id = teacher['user_id']
                user = await db.select_user(user_id=user_id)
                teacher_full_name = user['full_name']
                teachers += f"\n{tr}. {teacher_full_name}"
        interns = await db.select_intern_profiles(department_id=department_id)
        count_interns = len(interns)

        text = (f"🏢 Bo'lim nomi: {department['name']}\n"
                f"👔 Bo'lim boshlig'i: {department_chief_full_name}\n"
                f"👩‍🎓 Bo'limdagi stajorlar soni: {count_interns} ta\n"
                f"👨‍🏫 Bo'limdagi ustoz xodimlar: {teachers}\n")
        await message.answer(text=text)
    await message.answer(text="Amallardan birini tanlang 👇", reply_markup=department_actions_default_keyboard)
    await DepartmentState.department_id.set()


# for create department
@dp.callback_query_handler(state=CreateDepartmentState.name, text="yes")
async def confirm_creating_new_department(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    department_name = data.get('name')
    department = await db.create_department(name=department_name)
    await call.message.answer(text="✅ Bo'lim yaratildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=CreateDepartmentState.name, text='no')
async def cancel_creating_new_department(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ Saqlash bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=CreateDepartmentState.name)
async def get_name_for_new_department(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    text = (f"📂 Yangi bo'lim nomi: {name}\n\n"
            f"Saqlashni xohlaysizmi❓")
    await message.answer(text=text, reply_markup=confirm_keyboard)


# for update department
@dp.callback_query_handler(state=UpdateDepartmentState.name, text="yes")
async def confirm_updating_new_department(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    department_name = data.get('name')
    department_id = data.get('department_id')
    department = await db.update_department(
        department_id=department_id,
        name=department_name
    )
    await call.message.answer(text="✅ Bo'lim o'zgartirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=UpdateDepartmentState.name, text='no')
async def cancel_creating_new_department(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'zgartirish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=UpdateDepartmentState.name)
async def get_name_for_update_department(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    text = (f"📂 Bo'limning yangi nomi: {name}\n\n"
            f"Saqlashni xohlaysizmi❓")
    await message.answer(text=text, reply_markup=confirm_keyboard)


# for delete department
@dp.callback_query_handler(state=DeleteDepartmentState.department_id, text="yes")
async def confirm_deleting_department(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    department_id = data.get('department_id')
    teachers = await db.select_teacher_profiles(department_id=department_id)
    chiefs = await db.select_chief_profiles(department_id=department_id)
    interns = await db.select_intern_profiles(department_id=department_id)
    # for interns
    for intern in interns:
        user_id = intern['user_id']
        marks = await db.select_marks(intern_id=intern['id'])
        for mark in marks:
            await db.delete_mark(mark_id=mark['id'])
        await db.delete_intern_profile(profile_id=intern['id'])
        await db.update_user(user_id=user_id, role='user')
    # for teachers
    for teacher in teachers:
        user_id = teacher['user_id']
        await db.delete_teacher_profile(profile_id=teacher['id'])
        await db.update_user(user_id=user_id, role='user')
    # for chiefs
    for chief in chiefs:
        user_id = chief['user_id']
        await db.delete_chief_profile(profile_id=chief['id'])
        await db.update_user(user_id, role='user')

    await db.delete_department(department_id=department_id)
    await call.message.answer(text="✅ Bo'lim o'chirildi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(state=DeleteDepartmentState.department_id, text='no')
async def cancel_deleting_department(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="❌ O'chirish bekor qilindi", reply_markup=back_to_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
