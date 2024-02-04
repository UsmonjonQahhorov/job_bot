"""
Ushbu python fileda biror sabab orqali
 kech keladigan hodimlar uchun yozilgan functions bor
"""

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types

from bot.buttons.inline_buttons import soat_button, send_button, agree_or_dis
from bot.buttons.reply_buttons import main_menu, late_hours
from bot.buttons.text import late, ochirish, roziman
from bot.dispatcher import dp, bot

from aiogram.types import CallbackQuery, ParseMode

from db.utils import AbstractClass
from test import send_message_admin


@dp.message_handler(Text(late), state="menu2")
async def case_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        "<i>Iltimos, Nima uchun ishga kech qolasiz sababini ko'rsating👇.</i>",
        reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
    await state.set_state("case")


@dp.message_handler(state="case")
async def get_case_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["late_case"] = msg.text
    await msg.answer("Yaxshi👌. Qanchaga kechikishingizni kiriting🤔, Biror vaqtni tanlang🕐",
                     reply_markup=await late_hours())
    await state.set_state("time")


# Ishchi kech qolishini bildirmoqchi bolganda hamma malumotni olib adminga jonatish joyi shu yerda
@dp.message_handler(state="time")
async def time_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        data['vaqt'] = msg.text
        a = await msg.answer(".", reply_markup=types.ReplyKeyboardRemove())
        await bot.delete_message(msg.from_user.id, a.message_id)
        reply_markup = await send_button()
        await msg.answer(f"Vaqt⏱:{msg.text}\n"
                         f"Sabab: {data['late_case']}\n\n"
                         f"Ushbu ma'lumot adminga jonatilsinmi?",
                         reply_markup=reply_markup)
    await state.set_state("send_admin")


# Adminga jonatish user tomonidan tasdiqlangandan song adminga habar jonatiladi
@dp.callback_query_handler(lambda call: call.data.startswith(roziman), state="send_admin")
async def send_handler(call: CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        user = await AbstractClass.get_chat_id("workers", chat_id=str(call.from_user.id))
        async with state.proxy() as data:
            text = (f"Ishchi {data['vaqt']} kech qolishini bildiryapdi\n"
                    f" Sabab: {data['late_case']}")
        await send_message_admin(text=text, chat_id=str(call.from_user.id), user_id=str(user[0][0]))
        await call.message.answer("Xabaringiz adminga yetkazildi✅\n\n Iltimos, 👨‍💻admin javobini kuting",
                                  reply_markup=await main_menu())
        await state.set_state("menu2")
    except:
        pass


@dp.callback_query_handler(lambda call: call.data.startswith(ochirish), state="send_admin")
async def cancel_order(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    await call.answer("Bosh menuga qaydingiz")
    await call.message.delete()
    keyboard = await main_menu()
    await call.message.answer("Menulardan birini tanlang👇", reply_markup=keyboard)
    await state.set_state('menu')
