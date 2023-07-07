from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from browser import search_product
from translator import translate_to_sr

# You can set parse_mode by default. HTML or MARKDOWN
# bot = telebot.TeleBot('6036963706:AAFQ-CgoSuJInd2EI4wMPDpKVu-nR7oBjpE', parse_mode=None)

API_TOKEN = '6036963706:AAFQ-CgoSuJInd2EI4wMPDpKVu-nR7oBjpE'

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.reply("Я могу переводить найти для тебя что-нибудь")


@dp.message_handler()
async def echo_all(message):
    await search_product(translate_to_sr(message.text), send_post, message.chat.id)


cb = CallbackData('my', 'url')


async def send_post(post, chat_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Просмотреть", callback_data=cb.new('gg')))

    await bot.send_photo(chat_id, post['img'],
                         f"[{post['title']}]({post['url']})\n"
                         f"Цена: {post['price']}\n"
                         f"Локация: {post['location']}\n"
                         f"Описание:\n{post['description']}",
                         parse_mode='MARKDOWN',
                         reply_markup=keyboard
                         )


@dp.callback_query_handler()
async def show_post(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(callback_data['action'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
