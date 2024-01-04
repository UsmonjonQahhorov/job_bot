from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from bot.buttons.text import early


@dp.message_handler(Text(early), state="*")
async def absence_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Nima uchun ishka kelmaysiz? Sababini yozing 👇", reply_markup=ReplyKeyboardRemove())
    await state.set_state("sabab_early")


@dp.message_handler(state="sabab_early")
async def absence_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sabab"] = msg.text
    await msg.answer("<b>Qaysi kunlarda kela olmaysiz iltimos tanlang</b>",
                 parse_mode="HTML")
    await state.set_state("choose_day")
