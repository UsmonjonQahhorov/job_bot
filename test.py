import schedule
import asyncio

from aiogram.types import ParseMode

from db.utils import AbstractClass
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.auth import delete_user
from bot.buttons.inline_buttons import come_go, leave
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


# This function used to for send remind message to user every working day.
# async def send_reminder(chat_id, come_time):
#     message_text1 = ("<i>Assalomu Alaykum, Xayirli Tong!😊\n Iltimos ertalab soat 9:00 da ishga kelganingizda"
#                      " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")
#
#     new_text = ("<i>Assalomu Alaykum, Xayirli Tong!😊\n Iltimos ertalab soat 13:00 da ishga kelganingizda"
#                 " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")
#
#     now = datetime.now()
#     time_come = come_time.strftime("%H")
#     if now.weekday() != 6:
#         if now.hour == 14 and now.minute == 58 and time_come == "09":
#             await bot.send_message(chat_id, message_text1, reply_markup=await come_go(chat_id=chat_id),
#                                    parse_mode="HTML")
#
#         elif now.hour == 14 and now.minute == 22 and time_come == "09":
#             await bot.send_message(chat_id, new_text, reply_markup=await come_go(chat_id=chat_id),
#                                    parse_mode=ParseMode.HTML)
#             await asyncio.sleep(60)


async def send_message_everyday():
    try:
        user = await AbstractClass.get_all_users("workers")
        for i in user:
            if i[14]:
                a = str(i[8])
                if a == "09:00:00":
                    chat_id = i[14]
                    await send_message_9_am(chat_id)
                    print(chat_id)
        await asyncio.sleep(60)

    except Exception as e:
        print(f"Error sending message to user: {e}")


# async def send_message_when_leave():
#     try:
#         user = await AbstractClass.get_all_users("workers")
#         for i in user:
#             if i[14]:
#                 chat_id = i[14]
#                 await send_message_9_am(chat_id)
#         await asyncio.sleep(60)
#
#     except Exception as e:
#         print(f"Error sending message to user: {e}")


async def send_message_9_am(chat_id):
    now = datetime.now()
    soat = "51"
    if now.weekday() != 6:
        if now.hour == 16 and now.minute == int(soat):
            print("sending")
            message_text = ("<i>Assalomu Alaykum, Xayirli Tong!😊\n Iltimos soat 9:00 da ishga kelganingizda"
                            " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Kuningiz samarali o'tsin!🚀</i>")
            await bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=await come_go(chat_id))


        elif now.hour == 16 and now.minute == 53:
            message_text = ("<i>Assalomu Alaykum, Xayirli kech!😊\n Iltimos soat 18:00 da ishdan ketganingizda"
                            " bizga xabar berishni unutmang. Sizning punktualligingiz juda qadirlanadi. Yaxshi dam oling😊</i>")
            await bot.send_message(chat_id, message_text, parse_mode="HTML", reply_markup=await leave(chat_id))


async def save_to_daily(user_id, come_time):
    today = datetime.now().strftime("20%y-%m-%d")
    come_time = datetime.now().strftime("%H:%M:%S")
    data = await AbstractClass.get_by_userID(user_id=user_id, database="daily")
    for user in data:
        if user[0] != datetime.now().strftime("20%y-%m-%d"):
            await AbstractClass.insert_into_to_daily(database="daily",
                                                     w_date=today,
                                                     worker_id=user_id,
                                                     come_time=come_time,
                                                     status=True,
                                                     late_min=160
                                                     )
        else:
            return False


async def on_startup(dp):
    # Schedule the periodic task
    asyncio.create_task(periodic_check())
    asyncio.create_task(deriodic_cjeck1())


async def deriodic_cjeck1():
    while True:
        await send_message_everyday()
        # await send_message_when_leave()


async def periodic_check():
    while True:
        await get_all_messages()
        await asyncio.sleep(5)
