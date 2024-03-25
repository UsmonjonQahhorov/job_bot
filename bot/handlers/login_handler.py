from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.buttons.reply_buttons import main_menu
from bot.buttons.text import register, login
from aiogram.dispatcher.filters import Text
from bot.dispatcher import dp, bot
from db.utils import AbstractClass, format_phone_number


@dp.message_handler(Text([login]), state="menu")
async def login_handler(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Telefon raqamingizni kiriting👇\n</b>"
                     "<strong>Misol: +998(71) 200-03-21 </strong>", parse_mode="HTML")
    await state.set_state("phone_number")


@dp.message_handler(state="phone_number")
async def number_handler(msg: types.Message, state: FSMContext):
    phone_number = msg.text
    number = await format_phone_number(phone_number)
    async with state.proxy() as data:
        data["phone_number"] = number
        db_data = await AbstractClass.get_phone("workers", number)
        if db_data:
            for user in db_data:
                if user[11] == None:
                    if number == user[6]:
                        await msg.answer("<i>Raxmat! Endi sizga berilgan <strong>ID</strong> kiriting👇</i>",
                                         parse_mode="HTML")
                        await state.set_state("token")
                    else:
                        await msg.answer(
                            "<b>Raqam notog'ri kiritdingiz yoki fomat notog'ri!\nMisol uchun: +998991234567\n"
                            "Qayta urinib ko'ring👇</b>", parse_mode="HTML")
        else:
            await msg.answer("Siz tizimda mavjud emassiz!")


@dp.message_handler(state="token")
async def token_handler(msg: types.Message, state: FSMContext):
    token = msg.text
    chat_id = msg.from_user.id
    async with state.proxy() as data:
        number = data["phone_number"]
        try:
            info = await AbstractClass.get_phone("workers", number)
        except:
            pass
        print(info[0][12])
        if token == info[0][12]:
            await msg.answer("<i>Siz tizimdasiz!\nMenulardan birini tanlang👇</i>", parse_mode="HTML",
                             reply_markup=await main_menu())
            try:
                await AbstractClass.set_status_true("workers", number)
                await AbstractClass.update("workers", "chat_id", str(chat_id), "contact", number)
            except:
                pass

            await state.set_state("menu2")
        else:
            await msg.answer("<i>Ushbu <strong>ID</strong> aniqlanmadi!</i>", parse_mode="HTML")
