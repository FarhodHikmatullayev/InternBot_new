import asyncio

from aiogram import executor

from data.config import DEVELOPMENT_MODE, BOT_TOKEN
from keep_alive import keep_alive
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admin_for_interns import notify_interns_with_ending_internship_period
from utils.notify_chiefs import notify_chief_for_mark_function
from utils.notify_hrs import notify_hr_for_mark_function
from utils.notify_teachers import notify_teachers_for_mark_function
from utils.set_bot_commands import set_default_commands

if not DEVELOPMENT_MODE:
    keep_alive()


async def on_startup(dispatcher):
    await db.create()

    await set_default_commands(dispatcher)
    asyncio.create_task(notify_hr_for_mark_function())
    asyncio.create_task(notify_chief_for_mark_function())
    asyncio.create_task(notify_teachers_for_mark_function())
    asyncio.create_task(notify_interns_with_ending_internship_period())



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
