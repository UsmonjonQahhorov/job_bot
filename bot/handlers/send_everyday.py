from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from datetime import datetime
from bot.buttons.reply_buttons import location, early_leave, main_menu
from bot.dispatcher import dp
from geopy import Nominatim
from db.utils import AbstractClass
from test import save_to_daily


geolocator = Nominatim(user_agent="my_geocoding_app")


@dp.callback_query_handler(lambda call: call.data.startswith("✅Keldim"))
async def confirm_order(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Unday bolsa iltimos locationni jonating🗺", reply_markup=await location())
    await state.set_state("location")


@dp.message_handler(state='location', content_types=ContentType.LOCATION)
async def location_handler(msg: types.Message, state: FSMContext):
    lat = msg.location.latitude
    lon = msg.location.longitude
    location = geolocator.reverse((lat, lon), exactly_one=True)

    print("location: {location}")

    if location:
        address = location.raw.get('display_name', 'Unknown Address')
        print(address)
        print(address.split(",")[2])
        if address.split(",")[0] == "ТГЭУ Ректорат" or address.split(",")[0] == "Toshkent Davlat Iqtisodiyot Universiteti":

            await msg.answer(text=f"<b>Raxmat!\nSiz ayni damda ishdasiz🙂\n Kuningiz xayirli o'tsin!</b>",
                             parse_mode="HTML",
                             reply_markup=await early_leave())
            user = await AbstractClass.get_chat_id("workers", msg.from_user.id)
            save = await save_to_daily(user[0][0], datetime.now().strftime("%H:%M:%S"))
        else:
            await msg.answer(
                "Yuborilgan manzil notogri❌, siz ishga hali kelmagansiz! Ishga kelgandan song qayta urinib ko'ring,\n"
                "Yoki menulardan birini tanlang⤵️", reply_markup=await main_menu())
    else:
        await msg.answer(text="<b>Manzil topilmadi</b>", parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("yoqKelmadim"))
async def late_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Unday bolsa menulardan birini tanlang", reply_markup=await main_menu())
    await state.set_state("menu2")


@dp.callback_query_handler(lambda call: call.data.startswith("🚶🏻ketdim"))
async def ketdim_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Unday bolsa iltimos locationni jonating🗺", reply_markup=await location())
    await state.set_state("leave_location")


@dp.message_handler(state='leave_location', content_types=ContentType.LOCATION)
async def location_handler(msg: types.Message, state: FSMContext):
    lat = msg.location.latitude
    lon = msg.location.longitude
    location = geolocator.reverse((lat, lon), exactly_one=True)

    today = datetime.now().strftime("20%y-%m-%d")
    leave_time = datetime.now().strftime("%H:%M:%S")
    user = await AbstractClass.get_chat_id("workers", msg.from_user.id)
    user_data = await AbstractClass.update_leave_time(user[0][0], today, leave_time)
    print("done")
    print(user_data)

