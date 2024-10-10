from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all_departments import all_departments_default_keyboard
from keyboards.default.department_actions import department_actions_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from keyboards.default.menu_keyboards import back_to_menu, go_back_default_keyboard
from loader import dp, db, bot
from states.department_states import DepartmentState, CreateDepartmentState


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
    text = "Yangi bo'lim uchun nom kiriting: "
    await message.answer(text=text, reply_markup=go_back_default_keyboard)
    await CreateDepartmentState.name.set()


@dp.message_handler(state=DepartmentState.department_id)
async def get_department_name(message: types.Message, state: FSMContext):
    department_name = message.text
    departments = await db.select_departments(name=department_name)
    if not departments:
        text = "⚠️ Bu bo'lim allaqachon o'chirib yuborilgan"
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

    text = (f"Bo'lim nomi: {department['name']}\n"
            f"Bo'lim boshlig'i: {department_chief_full_name}\n"
            f"Bo'limdagi stajorlar soni: {count_interns} ta\n"
            f"Bo'limdagi ustoz xodimlar: {teachers}\n")
    await message.answer(text=text)
    await message.answer(text="Amallardan birini tanlang 👇", reply_markup=department_actions_default_keyboard)
