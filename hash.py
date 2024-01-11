from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
import asyncio

# Telegram bot tokenni o'zgartiring
BOT_TOKEN = '6320281570:AAFj4HaOQIPQIBNmCAGFhXQQbN9AyRCXmJw'

# Botni ishga tushirish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# O'zgartiriladigan ma'lumotlar
chat_ids = ['6108693014', '1105995218']  # Userning usernameni o'zgartiring
scheduler_times = ["09:00", "15:49", "15:43"]
message_text = "Assalomu alaykum! Bot ishladi va message jonatildi!"

# Scheduler obyekti
scheduler = AsyncIOScheduler()

async def send_daily_message():
    for user in chat_ids:
        print(user)
        await bot.send_message(user, message_text, parse_mode=ParseMode.MARKDOWN)

# Har kuni 09:00, 13:00 va 18:00 da ishga tushirish
for time in scheduler_times:
    scheduler.add_job(send_daily_message, 'cron', hour=int(time.split(":")[0]), minute=int(time.split(":")[1]))

# Asosiy loop
async def on_startup(dp):
    scheduler.start()

if __name__ == '__main__':
    from aiogram import executor
    from aiogram import types

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    asyncio.get_event_loop().run_forever()
