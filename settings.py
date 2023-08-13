import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
