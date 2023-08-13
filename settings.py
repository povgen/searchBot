import os

import redis
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

host: str = os.getenv('REDIS_HOST')
port: int = int(os.getenv('REDIS_PORT'))
r = redis.Redis(host=host, port=port, decode_responses=True)


class BotStates(StatesGroup):
    feedback = State()


orders = {
    '📶 Подешевле': 'price',
    '📶 Подороже': 'price desc',
    '📶 Новые': 'posted desc',
    '📶 Популярные': 'view_count desc',
    '📶 Релевантные': 'relevance'
}
