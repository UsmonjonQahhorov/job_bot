from datetime import datetime, timedelta
import asyncio

async def check_and_notify(user_id, late_time_limit):
    # Bazadan foydalanuvchi ma'lumotlarini olish
    user = await get_user_data(user_id)

    # Foydalanuvchi ishga kelayotgan vaqtini va kechikgan vaqtni aniqlash
    come_time = user.get('come_time')  # Ma'lumotlar bazasidan olingan misol
    current_time = datetime.now()
    late_time = current_time - come_time

    # Agar kechikma muddati limitdan oshmasa, habar yuborish
    if late_time > timedelta(minutes=late_time_limit):
        await send_late_notification(user_id, late_time)
    else:
        print(f"No late notification for user {user_id}")

async def get_user_data(user_id):
    # Bazadan foydalanuvchi ma'lumotlarini olish
    # Bu joyda SQL so'rov yozishingiz kerak, jadval nomi va ma'lumotlar bazasiga qarang
    # Masalan: SELECT * FROM users WHERE user_id = :user_id
    # Natijani dict shaklida qaytarish mumkin
    user_data = {'come_time': datetime(2024, 1, 1, 9, 0)}  # Ma'lumotlar bazasidan olingan misol
    return user_data

async def send_late_notification(user_id, late_time):
    # Foydalanuvchiga xabar yuborish
    message = f"You're {late_time} late for work!"
    # Bu joyda foydalanuvchiga xabar yuborish uchun aiogram yoki boshqa kerakli kutubxonalarni ishlatishingiz kerak
    # Masalan: await bot.send_message(user_id, message)

async def main():
    user_id = 123456789  # Foydalanuvchi chat ID
    late_time_limit = 30  # Muddati minutda belgilangan kechikma limiti

    await check_and_notify(user_id, late_time_limit)

if __name__ == "__main__":
    asyncio.run(main())
