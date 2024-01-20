import datetime
import re

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.buttons.text import on, yigirma, ottiz, qirq, ellik, bir_soat, roziman, ochirish
from bot.dispatcher import bot


async def soat_button():
    design = [
        [InlineKeyboardButton(text=on, callback_data=on)],
        [InlineKeyboardButton(text=yigirma, callback_data=yigirma)],
        [InlineKeyboardButton(text=ottiz, callback_data=ottiz)],
        [InlineKeyboardButton(text=qirq, callback_data=qirq)],
        [InlineKeyboardButton(text=ellik, callback_data=ellik)],
        [InlineKeyboardButton(text=bir_soat, callback_data=bir_soat)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=design, row_width=4)


async def send_button():
    design = [
        [InlineKeyboardButton(text=roziman, callback_data=roziman)],
        [InlineKeyboardButton(text=ochirish, callback_data=ochirish)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=design, row_width=2)


async def agree_or_dis(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ruxsat✅", callback_data=f"Ruxsat:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"bekor qilish:{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


"""Ishlayapdi"""


async def get_confirmation_keyboard():
    design = [
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="✅ Tasdiqlash")],
        [InlineKeyboardButton(text="❌ Tozalash", callback_data="❌ Tozalash")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=design)


async def come_go(chat_id: str):
    design = [
        [InlineKeyboardButton(text="✅Keldim", callback_data=f"✅Keldim{chat_id}")],
        [InlineKeyboardButton(text="❌Kelmadim", callback_data=f"yoqKelmadim{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def leave(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ketdim🚶🏻", callback_data=f"uchibkettim")],
        [InlineKeyboardButton(text="Ketmadim🙅‍♂️", callback_data=f"yoqvalbat")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
