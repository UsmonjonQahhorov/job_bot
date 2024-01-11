from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from bot.dispatcher import dp
from bot.buttons.text import early



@dp.message_handler(Text(early), state="*")
async def early_leave_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Nima uchun ishdan vaqtidan oldin ketmoqchisiz? Sababini yozing 👇", reply_markup=ReplyKeyboardRemove())
    await state.set_state("sabab_early")


@dp.message_handler(state="sabab_early")
async def early_sabab_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["sabab"] = msg.text
    await msg.answer("<b>Bugun ishga qaytasizmi?</b>",
                 parse_mode="HTML")
    await state.set_state("enter_coming")


@dp.message_handler(state="enter_coming")
async def qaytish_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["today_come"] = msg.text
    



