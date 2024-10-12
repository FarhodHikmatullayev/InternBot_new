import asyncio
from datetime import datetime, timedelta, timezone

from loader import db, bot


async def notify_interns_with_ending_internship_period():
    while True:
        now = datetime.now(timezone.utc)
        interns = await db.select_all_intern_profiles()
        for intern in interns:
            internship_period = intern['internship_period']
            intern_user_id = intern['user_id']
            intern_user = await db.select_user(user_id=intern_user_id)

            end_time = (intern['created_at'] + timedelta(days=internship_period)).replace(tzinfo=timezone.utc)

            if now > end_time:
                await db.update_intern_profile(profile_id=intern['id'], is_active=False)
                # for interns
                await bot.send_message(
                    chat_id=intern_user['telegram_id'],
                    text="⏳ Sizning stajirovka muddatingiz tugadi"
                )
                hr_profiles = await db.select_all_hr_profiles()
                for hr in hr_profiles:
                    hr_user_id = hr['user_id']
                    hr_user = await db.select_user(user_id=hr_user_id)

                    # for hrs
                    await bot.send_message(
                        chat_id=hr_user['telegram_id'],
                        text=(f"🔔 {intern_user['full_name']}ning stajirovka muddati tugadi,\n"
                              f"Iltimos, stajirning baholarini ko'rib chiqib yakuniy xulosaga keling!")
                    )
                department_id = intern['department_id']
                chief_profiles = await db.select_chief_profiles(department_id=department_id)
                if chief_profiles:
                    chief = chief_profiles[0]
                    chief_user_id = chief['user_id']
                    chief_user = await db.select_user(user_id=chief_user_id)

                    # for chiefs
                    await bot.send_message(
                        chat_id=chief_user['telegram_id'],
                        text=(f"🔔 {intern_user['full_name']}ning stajirovka muddati tugadi,\n"
                              f"Iltimos, stajirning baholarini ko'rib chiqib yakuniy xulosaga keling!")
                    )
                teacher_profile = await db.select_teacher_profile(profile_id=intern['teacher_id'])
                teacher_user_id = teacher_profile['user_id']
                teacher_user = await db.select_user(user_id=teacher_user_id)

                # for teacher
                await bot.send_message(
                    chat_id=teacher_user['telegram_id'],
                    text=(f"🔔 {intern_user['full_name']}ning stajirovka muddati tugadi,\n"
                          f"Iltimos, stajirning baholarini ko'rib chiqib yakuniy xulosaga keling!")
                )
                admin_users = await db.select_users(role='admin')
                for admin in admin_users:
                    # for admins
                    await bot.send_message(
                        chat_id=admin['telegram_id'],
                        text=(f"🔔 {intern_user['full_name']}ning stajirovka muddati tugadi,\n"
                              f"Iltimos, stajirning baholarini ko'rib chiqib yakuniy xulosaga keling!")
                    )

        await asyncio.sleep(86400)  # Har 24 soatda qayta tekshirish
