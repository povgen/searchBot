
from aiogram import Bot, Dispatcher, types

API_TOKEN = '6036963706:AAFQ-CgoSuJInd2EI4wMPDpKVu-nR7oBjpE'

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
