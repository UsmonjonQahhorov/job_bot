import json
import asyncio
from aiogram.types import ParseMode
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from bot.buttons.inline_buttons import come_go, leave
from bot.dispatcher import bot
from db.utils import AbstractClass
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

cred = credentials.Certificate("bot/sdkkey2.json")
initialize_app(cred)
db = firestore.client()

scheduler = AsyncIOScheduler()


async def send_message_admin(text: str, chat_id: str, user_id: str):
    requests_ref = db.collection("messages")
    new_request = {
        "text": text,
        "chat_id": chat_id,
        "status": False,
        "sender_key": "user",
        "user_id": user_id,
        "createdAt": datetime.now().strftime("%A %m-%d-20%y %H:%M:%S")
    }
    result = requests_ref.add(new_request)
    document_id = result[1].get().id
    return document_id


async def get_messages_by_chat_id(chat_id):
    messages_ref = db.collection("messages")
    query = messages_ref.where("chat_id", "==", chat_id)
    query_result = query.stream()
    messages = []
    for document in query_result:
        data = document.to_dict()
        messages.append(data)

    return messages


async def get_all_messages():
    messages_ref = db.collection("messages")
    query = messages_ref.where("admin_status", "==", "true")
    try:
        query_result = query.get()
        for document in query_result:
            data = document.to_dict()
            chat_id = data.get("chat_id")
            message_text = data.get("text")
            # Send the message to the Telegram user
            await send_message_to_user(chat_id, message_text)
            # Update the status in Firebase to mark the message as processed
            document.reference.update({"admin_status": "processed"})

    except Exception as e:
        print(f"Error querying Firestore: {e}")


# Bu function fb dagi messageni statusini update qiladi
async def update_message_status_by_chat_id(chat_id, new_status):
    messages_ref = db.collection("messages")
    try:
        query = messages_ref.where("chat_id", "==", chat_id)
        query_result = query.stream()

        for document in query_result:
            document_ref = messages_ref.document(document.id)
            document_ref.update({"status": new_status})
    except Exception as e:
        print(f"Error updating message status: {e}")


# Bu funcsiya firebasedagi yangi messageni kerakli userga jonatish uchun ishlatiladi
async def send_message_to_user(chat_id, text):
    try:
        new_text = (f"Admin xabaringizni o'qidi👀\n\n"
                    f"Admin javobi💬: <strong>{text}</strong>")
        await bot.send_message(chat_id, new_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Error sending message to user: {e}")


"""Send message everyday at 9:00 to workers"""


async def send_message_everyday():
    today_date = datetime.now().strftime("20%y-%m-%d")
    try:
        user = await AbstractClass.get_all_users("workers")
        for i in user:
            query = await post_to_api_today(user_id=i[0], today_date=today_date)
            print(query)
            if query == None:
                if i[14]:
                    a = str(i[8])
                    if a == "09:00:00":
                        chat_id = i[14]
                        await send_message_9_am(chat_id)
                        print(f"Send message at 9:00 {chat_id}")
        # await asyncio.sleep(50)
    except Exception as e:
        print(f"Error sending message to user: {e}")


"""Send message everyday at 18:00 to workers"""


async def send_message_after():
    try:
        user = await AbstractClass.get_all_users("workers")
        for i in user:
            if i[14]:
                chat_id = i[14]
                await send_message_9_am(chat_id)
                print(chat_id)
    except Exception as e:
        print(f"Error sending message to user: {e}")


async def post_to_api(api_url, data_to_send):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(api_url, data=json.dumps(data_to_send), headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as err:
        print(f"Request exception: {err}")
        return None


async def post_exit_api(today_date):
    api_url = "https://tizimswag.astrolab.uz/v1/get-workers-by-day"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(f"{api_url}/{today_date}", headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as err:
        print(f"Request exception: {err}")


async def post_to_api_today(user_id, today_date):
    api_url = "https://tizimswag.astrolab.uz/v1/get-worker-day"
    url_params = f"{user_id}/{today_date}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(f"{api_url}/{url_params}", headers=headers)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as err:
        print(f"Request exception: {err}")


async def send_message_9_am(chat_id):
    now = datetime.now()
    if now.weekday() != 6:
        if now.hour == 9:
            print(f"sending message to {chat_id}")
            message_text = (
                f"<i>Assalomu Alaykum, Xayirli Tong!😊\nSoat {now.hour}:{now.minute} bo'ldi, ishga kelganingizda"
                " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")
            await bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=await come_go(chat_id))

        elif now.hour == 18:
            message_text = (
                f"<i>Assalomu Alaykum, Xayirli kech!😊\nSoat {now.hour}:{now.minute} bo'ldi, ishdan ketganingizda"
                " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Yaxshi dam oling.😊</i>")
            await bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=await leave(chat_id))


async def exit_all_workers(user_id):
    try:
        api_url = "https://tizimswag.astrolab.uz/v1/daily"
        today_date = datetime.now().strftime("20%y-%m-%d")
        data = await post_exit_api(today_date)
        for user in data["came"]:
            data_to_send = {
                "id": str(user["id"])
            }
            await post_to_api(api_url, data_to_send)
    except Exception as e:
        print(e)


scheduler.add_job(send_message_everyday, 'cron', hour="9", minute='0')  # Once a day
scheduler.add_job(send_message_after, 'cron', hour='18', minute='10')  # Everyday at 15:00
scheduler.add_job(exit_all_workers, 'cron', hour='20', minute='00')  # Everyday at 15:00


async def on_startup(dp):
    scheduler.start()
    asyncio.create_task(periodic_check())


async def on_shutdown(dp):
    scheduler.shutdown()


async def periodic_check():
    while True:
        await get_all_messages()
        await asyncio.sleep(5)
