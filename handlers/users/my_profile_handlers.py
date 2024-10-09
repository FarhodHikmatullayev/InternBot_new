from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.change_profile import change_profile_default_keyboard
from keyboards.default.go_to_registration import go_registration_default_keyboard
from loader import dp, db, bot


@dp.message_handler(text="👤 Mening Profilim", state="*")
async def open_my_profile_function(message: types.Message, state: FSMContext):
    print(1)
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
        phone_number = user['phone']
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        user_id = user['id']
        if user_role == "admin":
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: ADMIN\n")
            await message.answer(text=text, reply_markup=change_profile_default_keyboard)
        elif user_role == 'teacher':
            teacher_profiles = await db.select_teacher_profiles(user_id=user_id)
            if not teacher_profiles:
                text = "❌ Sizda hali profil mavjud emas"
                await message.reply(text=text)
                return
            teacher = teacher_profiles[0]
            department_id = teacher['department_id']
            text = f"Siz"
            department = await db.select_department(department_id=department_id)
            department_name = department['name']
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: {department_name} bo'limida stajorlarga mas'ul xodim\n")
            await message.answer(text=text, reply_markup=change_profile_default_keyboard)
        elif user_role == 'intern':
            intern_profiles = await db.select_intern_profiles(user_id=user_id)
            if not intern_profiles:
                text = "❌ Sizda hali profil mavjud emas"
                await message.reply(text=text)
                return
            intern = intern_profiles[0]
            internship_period = intern['internship_period']
            if internship_period:
                internship_period = f"{internship_period} kun"
            else:
                internship_period = "Hali kiritilmagan"
            teacher_id = intern['teacher_id']
            teacher_profile = await db.select_teacher_profile(profile_id=teacher_id)
            teacher_user_id = teacher_profile['user_id']
            teacher_user = await db.select_user(user_id=teacher_user_id)
            teacher_full_name = teacher_user['full_name']
            department_id = intern['department_id']
            department = await db.select_department(department_id=department_id)
            department_name = department['name']
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: {department_name} bo'limida stajor\n"
                    f"👨‍🏫 Sizga ish o'rgatuvchi xodim: {teacher_full_name}\n"
                    f"📅 Stajirovkangiz muddati: {internship_period}\n"
                    f"📅 Bugun: {(datetime.now().date() - intern['created_at'].date()).days + 1} - kun")
            await message.answer(text=text, reply_markup=change_profile_default_keyboard)
        elif user_role == 'chief':
            chief_profiles = await db.select_chief_profiles(user_id=user_id)
            if not chief_profiles:
                text = "❌ Sizda hali profil mavjud emas"
                await message.reply(text=text)
                return
            chief = chief_profiles[0]
            department_id = chief['department_id']
            department = await db.select_department(department_id=department_id)
            department_name = department['name']
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: {department_name} bo'limi boshlig'i \n")
            await message.answer(text=text, reply_markup=change_profile_default_keyboard)
        elif user_role == 'hr':
            hr_profiles = await db.select_hr_profiles(user_id=user_id)
            if not hr_profiles:
                text = "❌ Sizda hali profil mavjud emas"
                await message.reply(text=text)
                return
            hr = hr_profiles[0]
            text = (f"📋 Sizning ma'lumotlaringiz 👇\n"
                    f"🧑‍💼 Ismingiz: {first_name}\n"
                    f"👤 Familiyangiz: {last_name}\n"
                    f"📞 Telefon raqamingiz: {phone_number}\n"
                    f"🔑 Rol: HR xodim\n")
            await message.answer(text=text, reply_markup=change_profile_default_keyboard)
        else:
            text = "❌ Sizda hali profil mavjud emas"
            await message.reply(text=text)
            return
