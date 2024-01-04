from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import main_menu, early_leave
from bot.buttons.text import ochirish
from bot.dispatcher import dp


@dp.callback_query_handler(lambda call: call.data.startswith(ochirish), state="confirm_order")
async def cancel_order(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Bosh menuga qaydingiz")
    await call.message.delete()
    keyboard = await main_menu()
    await call.message.answer("Menulardan birini tanlang👇", reply_markup=keyboard)
    await state.set_state('menu')


@dp.callback_query_handler(lambda call: call.data.startswith("Orqaga"))
async def back_handler(call: types.CallbackQuery, state: FSMContext):
    print(1)
    await call.message.delete()
    await call.message.answer(text=f"<b>{call.from_user.full_name}Ortga qaytingiz⬇️</b>",
                              reply_markup=await early_leave(), parse_mode='HTML')
