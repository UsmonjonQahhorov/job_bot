from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from datetime import datetime
from bot.buttons.reply_buttons import location, early_leave, main_menu
from bot.dispatcher import dp
from geopy import Nominatim
from db.utils import AbstractClass
import asyncio
import aiohttp
from test import save_to_daily, post_to_api
from bot.buttons.text import keldim

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
        if address.split(",")[0] == "ТГЭУ Ректорат" or address.split(",")[
            0] == "Toshkent Davlat Iqtisodiyot Universiteti":
            await msg.answer(text=f"<b>Raxmat!\nSiz ayni damda ishdasiz🙂\n Kuningiz xayirli o'tsin!</b>",
                             parse_mode="HTML",
                             reply_markup=await early_leave())
            user = await AbstractClass.get_chat_id("workers", msg.from_user.id)
            api_url = "https://tizimswag.astrolab.uz/v1/daily"
            data_to_send = {
                "id": str(user[0][0])
            }
            result = await post_to_api(api_url, data_to_send)
            print(result)
            if result:
                print(f"Natija: {result}")
            else:
                print("So'rovda xatolik yuz berdi.")
            # save = await save_to_daily(user[0][0], datetime.now().strftime("%H:%M:%S"))
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
    user = await AbstractClass.get_chat_id("workers", msg.from_user.id)

    await msg.answer("Raxmat!. Siz ishdan ketkanligingizni tasdiqladingiz👍\n"
                     "Yaxshi dam oling😊")
    api_url = "https://tizimswag.astrolab.uz/v1/daily"
    data_to_send = {
        "id": str(user[0][0])
    }
    result = await post_to_api(api_url, data_to_send)
    print(result)
    if result:
        print(f"Natija: {result}")
    else:
        print("So'rovda xatolik yuz berdi.")
