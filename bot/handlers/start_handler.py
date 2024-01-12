from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from bot.buttons.reply_buttons import main_menu_buttons, main_menu, location
from bot.buttons.text import keldim
from bot.dispatcher import dp, bot
from db import db
from db.model import User
from db.utils import AbstractClass


@dp.message_handler(commands=['start', 'help'], state='*')
async def start_handler(msg: types.Message, state: FSMContext):
    user = await AbstractClass.get_chat_id("workers", chat_id=str(msg.from_user.id))
    if user:
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

    else:
        user_id = msg.from_user.id
        await bot.send_photo(chat_id=user_id,
                             photo=open("images/logo.png", "rb"),
                             caption=f"Assalomu alaykum {msg.from_user.full_name} botimizga Xush kelibsiz",
                             reply_markup=await main_menu_buttons())
        await state.set_state("menu")


@dp.message_handler(Text(keldim), state="menu2")
async def keldim_handler(msg: types.Message, state: FSMContext):
    print("Handler triggered!")
    print(f"Text: {msg.text}")
    try:
        markup = await location()
        print("Location markup:", markup)
        await msg.answer("Unday bolsa iltimos locationni jonating🗺", reply_markup=markup)
        await state.set_state("location")
    except Exception as e:
        print("Exception in keldim_handler:", e)
        raise
