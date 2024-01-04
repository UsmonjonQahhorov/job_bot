from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from bot.buttons.reply_buttons import get_days_keyboard, get_days_button, early_leave
from bot.buttons.inline_buttons import send_button
from bot.buttons.text import absence, roziman
from bot.dispatcher import dp, bot
from db.utils import AbstractClass
from test import send_message_admin


@dp.message_handler(Text(absence), state="*")
async def absence_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Nima uchun ishka kelmaysiz? Sababini yozing 👇", reply_markup=ReplyKeyboardRemove())
    await state.set_state("sabab_kiritish")


@dp.message_handler(state="sabab_kiritish")
async def absence_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sabab"] = msg.text
    await msg.answer("<b>Qaysi kunlarda kela olmaysiz iltimos tanlang</b>",
                     reply_markup=await get_days_keyboard(), parse_mode="HTML")
    await state.set_state("choose_day")


@dp.message_handler(state="choose_day")
async def callback_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["day_1"] = msg.text
    await msg.answer(f"Ishka qaytish kunini tanlang👇",
                     reply_markup=await get_days_button(
                         msg.text)
                     )
    await state.set_state("second_day")


@dp.message_handler(state="second_day")
async def second_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        day_1 = data["day_1"]
        data["day_2"] = msg.text
    try:
        await msg.answer(
            f"Siz {day_1} -- {msg.text} kunlari kela olmaysiz\n\n Sabab:{data['sabab']}",
            reply_markup=await send_button(),
        )
        await state.set_state("confirm_order")
        a = await msg.answer(".", reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(chat_id=msg.chat.id, message_id=a.message_id)
    except Exception as e:
        print(f"Error in callback_second_day: {e}")


@dp.callback_query_handler(lambda call: call.data.startswith(roziman), state="confirm_order")
async def confirm_order(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        day_1 = data["day_1"]
        day_2 = data["day_2"]
        sabab = data["sabab"]
    user = await AbstractClass.get_chat_id("workers", chat_id=str(call.from_user.id))
    user_id1 = user[0][0]
    text = (f"Ishchi {day_1} -- {day_2} kunlari kela olmaslikka ruxsat sorayapdi\n\n"
            f"Sabab:{sabab}")
    await send_message_admin(text=text, chat_id=str(call.from_user.id), user_id=str(user_id1))
    await call.answer("Sorovingiz adminga yetkazildi✅\n"
                      "Admin javobini kuting!"),
    await state.finish()

