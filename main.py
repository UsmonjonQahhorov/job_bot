import asyncio
import logging
from aiogram import executor
from bot.dispatcher import dp
import bot.handlers
from db import db
from test import send_message_everyday
from bot.middlewares.discrimin_filter import DiscriminationMiddleware
from test import on_startup, on_shutdown

if __name__ == '__main__':
    db.init()
    dp.middleware.setup(DiscriminationMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
