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


@dp.message_handler(Text(late), state="*")
async def case_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Nima uchun kech qolasiz sababini kiriting👇", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("case")


@dp.message_handler(state="case")
async def get_case_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        data["late_hours"] = msg.text
    await msg.answer("Qancha vaqt davomida kech qolishingizni kiriting yoki tanlang",
                     reply_markup=await late_hours())

    await state.set_state("time")


@dp.message_handler(state="time")
async def time_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        data["vaqt"] = msg.text
        hour = data["late_hours"]
        print(hour)
    a = await msg.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await bot.delete_message(msg.from_user.id, a.message_id)
    reply_markup = await send_button()
    await msg.answer(f"Vaqt⏱:{msg.text}\n"
                     f"Sabab: {data['late_hours']}\n\n"
                     f"Ushbu malumot adminga jonatilsinmi?",
                     reply_markup=reply_markup)
    await state.set_state("send_admin")


@dp.callback_query_handler(lambda call: call.data.startswith(roziman), state="send_admin")
async def send_handler(call: CallbackQuery, state: FSMContext):
    print(call.data)
    try:
        user = await AbstractClass.get_chat_id("workers", chat_id=str(call.from_user.id))
        async with state.proxy() as data:
            text = (f"Ishchi {data['vaqt']} kech qolishini bildiryapdi\n"
                    f"Sabab: {data['late_hours']}")
        await send_message_admin(text=text, chat_id=str(call.from_user.id), user_id=str(user[0][0]))
        await call.answer("Habaringiz adminga yetkazildi✅")
        await state.finish()
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


"""Ishlatilmaydigan qismi. Keraksiz"""
#
#
# @dp.callback_query_handler(lambda call: call.data.startswith("bek"))
# async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
#     await call.message.delete()
#     chat_id = call.data.split(":")[1]
#     async with state.proxy() as data:
#         data["cancel_id"] = chat_id
#     await state.set_state("boldimi")
#     await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")
#
#
#
# @dp.message_handler(state='boldimi')
# async def not_save_handler(msg: types.Message, state: FSMContext):
#     await bot.delete_message(msg.from_user.id, msg.message_id - 1)
#     async with state.proxy() as data:
#         chat_id = data.get('cancel_id')
#     await bot.send_message(chat_id=chat_id,
#                            text=f"<b>Sizning sorovingiz bekor qilindi❗️\nAdmin javobi: {msg.text}\n\nMurojat uchun: @U_Qahhorov</b>",
#                            parse_mode="HTMl")
#
#
# @dp.callback_query_handler(lambda call: call.data.startswith("Ruxsat"))
# async def basicsave_handler(call: types.CallbackQuery, state: FSMContext):
#     chat_id = call.data.split(":")[1]
#     await bot.send_message(chat_id=chat_id, text="<b>Admin ruxsat berdi</b>", parse_mode="HTML")
