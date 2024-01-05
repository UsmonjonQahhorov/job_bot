import asyncio

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler

class DiscriminationMiddleware(BaseException):
    pass