import os

import redis
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

host: str = os.getenv('REDIS_HOST')
port: int = int(os.getenv('REDIS_PORT'))
r = redis.Redis(host=host, port=port, decode_responses=True)


def get_webdriver() -> webdriver:
    is_firefox = os.getenv('SELENIUM_BROWSER') and os.getenv('SELENIUM_BROWSER').lower() == 'firefox'
    options = FirefoxOptions() if is_firefox else ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if is_firefox:
        return webdriver.Chrome(options=options, service=FirefoxService(GeckoDriverManager().install()))
    else:
        return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


class BotStates(StatesGroup):
    feedback = State()


orders = {
    '📶 Подешевле': 'price',
    '📶 Подороже': 'price desc',
    '📶 Новые': 'posted desc',
    '📶 Популярные': 'view_count desc',
    '📶 Релевантные': 'relevance'
}
