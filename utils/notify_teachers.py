import asyncio
from datetime import datetime, timedelta

from loader import db, bot


async def notify_teachers_for_mark_function():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=15, minute=28, second=20, microsecond=0)

        if now >= target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        teacher_profiles = await db.select_all_teacher_profiles()
        for teacher_profile in teacher_profiles:
            intern_ids = []
            intern_profiles = await db.select_intern_profiles(teacher_id=teacher_profile['id'])
            for intern_profile in intern_profiles:
                marks = await db.select_today_marks(intern_id=intern_profile['id'], rated_by_id=teacher_profile['user_id'])
                if not marks:
                    intern_ids.append(intern_profile['id'])
            if not intern_ids:
                text = ("🎉 Bugun siz barcha stajorlarni baholadingiz,\n"
                        "🙏 Katta rahmat!")
            else:
                text = "❌ Siz ushbu stajorlarga bugun hisobidan baho qo'ymadingiz:\n"
                tr = 0
                for intern_id in intern_ids:
                    tr += 1
                    intern = await db.select_intern_profile(profile_id=intern_id)
                    user_id = intern['user_id']
                    user = await db.select_user(user_id=user_id)
                    full_name = user['full_name']
                    text += f" {tr}. {full_name}\n"
                text += "\n⚠️ Iltimos, hoziroq stajorlarni baholab qo'ying."
            teacher_user_id = teacher_profile['user_id']
            teacher_user = await db.select_user(user_id=teacher_user_id)
            teacher_telegram_id = teacher_user['telegram_id']
            await bot.send_message(chat_id=teacher_telegram_id, text=text)