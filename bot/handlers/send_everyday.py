from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from bot.buttons.reply_buttons import location, early_leave, main_menu
from bot.dispatcher import dp
from geopy import Nominatim

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

    if location:
        address = location.raw.get('display_name', 'Unknown Address')
        print(address.split(",")[0])
        if address.split(",")[0] == "Toshkent Davlat Iqtisodiyot Universiteti":
            await msg.answer(text=f"<b>Raxmat!\nSiz ayni damda ishdasiz🙂</b>", parse_mode="HTML",
                             reply_markup=await early_leave())
        else:
            await msg.answer("Yuborilgan manzil notogri, siz ishka hali kelmagansiz!")
    else:
        await msg.answer(text="<b>Manzil topilmadi</b>", parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("yoqKelmadim"))
async def late_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Unday bolsa menulardan birini tanlang", reply_markup=await main_menu())
    await state.set_state("menu2")
