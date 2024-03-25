from datetime import datetime
from uuid import UUID

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from bot.buttons.reply_buttons import main_menu_buttons, main_menu, location, early_leave
from bot.buttons.text import keldim
from bot.dispatcher import dp, bot
from db.utils import AbstractClass
from test import post_to_api_today


@dp.message_handler(commands=['start', 'help'], state='*')
async def start_handler(msg: types.Message, state: FSMContext):
    user = await AbstractClass.get_chat_id("workers", chat_id=str(msg.from_user.id))
    today_date = datetime.now().strftime("20%y-%m-%d")
    try:
        if user and user[0]:
            result = await post_to_api_today(user_id=user[0][0], today_date=today_date)
            if result:
                await msg.answer("Siz allaqachon ishga kelgansiz!", reply_markup=await early_leave())
        #     else:
        #         raise Exception("User data is empty.")
        # except Exception as e:
        #     print(f"Error in start_handler: {e}")

        if user and user[0] and result is None:
            full_name = f"{user[0][2]} {user[0][3]}"
            position = user[0][4]
            departament = user[0][5]
            contact_number = user[0][6]

            text = (f"<b>Assalomu alaykum👋.\n\n"
                    f"F.I.O👤: {full_name}\n"
                    f"Lavozim💼: {position}\n"
                    f"Bo'lim👷‍♂️: {departament}\n"
                    f"Telefon№: {contact_number}\n\n</b>")

            await msg.answer(text=text, reply_markup=await main_menu(), parse_mode=ParseMode.HTML)
            await state.set_state("menu2")

        elif not user or not user[0]:
            user_id = msg.from_user.id
            await bot.send_photo(chat_id=user_id,
                                 photo=open("images/img.png", "rb"),
                                 caption=f"Assalomu aleykum {msg.from_user.full_name} botimizga Xush kelibsiz!",
                                 reply_markup=await main_menu_buttons())
        await state.set_state("menu")
    except Exception as e:
        print(f"Error in start_handler: {e}")


@dp.message_handler(Text(keldim), state="*")
async def keldim_handler(msg: types.Message, state: FSMContext):
    print("Handler triggered!")
    print(f"Text: {msg.text}")
    try:
        markup = await location()
        print("Location markup:", markup)
        await msg.answer("Iltimos joylashuvni yuboring🗺", reply_markup=markup)
        await state.set_state("location")
    except Exception as e:
        print("Exception in keldim_handler:", e)
        raise
