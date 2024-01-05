import asyncio
import logging
from aiogram import executor
from bot.dispatcher import dp
import bot.handlers
from db import db
from db.model import User
from test import main, send_message_everyday
from bot.middlewares.discrimin_filter import DiscriminationMiddleware

if __name__ == '__main__':
    db.init()
    # asyncio.run(main())
    # asyncio.run(send_message_everyday())
    dp.middleware.setup(DiscriminationMiddleware())
    executor.start_polling(dp, skip_updates=True)
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()

