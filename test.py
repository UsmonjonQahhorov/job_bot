import schedule
import asyncio

from aiogram.types import ParseMode

from db.utils import AbstractClass
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.auth import delete_user
from bot.buttons.inline_buttons import come_go
from bot.dispatcher import bot
from db.utils import AbstractClass

cred = credentials.Certificate("bot/sdkkey2.json")
initialize_app(cred)
db = firestore.client()


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
    query = messages_ref.where("status", "==", "true")
    try:
        query_result = query.get()
        for document in query_result:
            data = document.to_dict()
            chat_id = data.get("chat_id")
            message_text = data.get("text")
            # Send the message to the Telegram user
            await send_message_to_user(chat_id, message_text)
            # Update the status in Firebase to mark the message as processed
            document.reference.update({"status": "processed"})

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
        new_text = (f"ℹAdmin habaringizni o'qidi👀\n\n"
                    f"Admin javobi💬: <strong>{text}</strong>")
        await bot.send_message(chat_id, new_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Error sending message to user: {e}")


# This function used to for send remind message to user every working day.
async def send_reminder(chat_id, come_time):
    message_text1 = ("<i>Assalomu Alaykum, Xayirli Tong!😊\n Iltimos ertalab soat 9:00 da ishka kelganingizda"
                     " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")

    new_text = ("<i>Assalomu Alaykum, Xayirli Tong!😊\n Iltimos ertalab soat 13:00 da ishka kelganingizda"
                " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")

    now = datetime.now()
    time_come = come_time.strftime("%H")
    if now.weekday() != 6:
        if now.hour == 23 and time_come == "15":
            await bot.send_message(chat_id, message_text1, reply_markup=await come_go(chat_id=chat_id),
                                   parse_mode="HTML")
            await asyncio.sleep(120)
        elif now.hour == 17 and now.minute == "00" and time_come == "13":
            await bot.send_message(chat_id, new_text, reply_markup=await come_go(chat_id=chat_id))


async def send_message_everyday():
    try:
        user = await AbstractClass.get_all_users("workers")
        for i in user:
            if i[14]:
                await send_reminder(i[14], come_time=i[8])
                chat_id = i[14]
    except Exception as e:
        print(f"Error sending message to user: {e}")


# async def save_to_daily(user_id:str, come_time:str):
#     today = datetime.now().strftime("20%y-%m-%d")
#     data = await AbstractClass.get_by_userID(user_id = "706d21b3-e0fd-411f-984f-f61d8bd7a050", database="daily")
#     print(data)


async def on_startup(dp):
    # Schedule the periodic task
    asyncio.create_task(periodic_check())


async def periodic_check():
    while True:
        await get_all_messages()
        await send_message_everyday()
        await asyncio.sleep(10)

# if __name__ == '__main__':
