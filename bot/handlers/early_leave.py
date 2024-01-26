from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from bot.dispatcher import dp
from bot.buttons.text import early
from db.utils import AbstractClass
from test import send_message_admin, post_to_api


@dp.message_handler(Text(early), state="*")
async def early_leave_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Nima uchun ishdan vaqtidan oldin ketmoqchisiz? Sababini yozing 👇",
                     reply_markup=ReplyKeyboardRemove())
    await state.set_state("sabab_early")


@dp.message_handler(state="sabab_early")
async def early_sabab_handler(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Xabaringiz adminga yetkazildi✅</b>", parse_mode="HTML")
    await msg.answer("Raxmat! Yaxshi yetib oling😊\nYaxshi dam oling!")
    user = await AbstractClass.get_chat_id("workers", chat_id=str(msg.from_user.id))
    user_id1 = user[0][0]
    text = (f"Ishchi vaqtidan oldin ishdan ketmoqchi"
            f" Sabab:{msg.text}")
    api_url = "https://tizimswag.astrolab.uz/v1/daily"
    data_to_send = {
        "id": str(user[0][0])
    }
    result = await post_to_api(api_url, data_to_send)
    await send_message_admin(text=text, chat_id=str(msg.from_user.id), user_id=str(user_id1))
