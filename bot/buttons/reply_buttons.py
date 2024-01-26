import datetime
from aiogram import types
import re
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.buttons.text import login, register, late, absence, early, ketdim
from bot.buttons.text import on, yigirma, ottiz, qirq, ellik, bir_soat, keldim


async def main_menu_buttons():
    design = [
        [login],
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    design = [keldim, late, absence]
    return keyboard.add(*design)


async def late_hours():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [on, yigirma, ottiz, qirq, ellik, bir_soat]
    return keyboard.add(*buttons)


async def get_days_keyboard():
    current_date = datetime.datetime.now()
    days = []
    for i in range(0, 7):
        next_day = current_date + datetime.timedelta(days=i)
        if next_day.weekday() != 6:
            days.append(next_day)

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for day in days:
        callback_data = f"{day.strftime('%d/%m/%Y')}"
        button = types.KeyboardButton(text=day.strftime("%d/%m/%Y"))
        buttons.append(button)
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    for row in rows:
        keyboard.add(*row)

    return keyboard


def get_next_five_dates(selected_date):
    selected_date = datetime.datetime.strptime(selected_date, "%d/%m/%Y")
    dates = []

    for day_offset in range(1, 8):
        current_date = selected_date + datetime.timedelta(days=day_offset)
        if current_date.weekday() != 6:
            formatted_date = current_date.strftime("%d/%m/%Y")
            dates.append(formatted_date)
    return dates


async def get_days_button(input_string: str):
    match = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", input_string)

    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        formatted_date = f"{day}/{month}/{year}"
    else:
        print("Invalid input string")
        return

    selected_date = formatted_date

    try:
        next_five_dates = get_next_five_dates(selected_date)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        buttons = []

        for date in next_five_dates:
            callback_data = f"{date.replace('/', '/')}_{year}_{month}_{day}_{formatted_date}"
            print(callback_data)
            call_data = callback_data.split("_", 2)[0]
            print(call_data)
            button = types.KeyboardButton(text=call_data)
            buttons.append(button)

        # Organize buttons into rows
        rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

        for row in rows:
            keyboard.add(*row)

        return keyboard
    except Exception as e:
        print(f"Error: {e}")


async def location():
    design = [[KeyboardButton(text="Joylashuvni yuborish📍", request_location=True)]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def early_leave():
    design = [[early]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def ketdim_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = [ketdim]
    return keyboard.add(*button)
