import logging

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.utils import executor

from keyboards import default_keyboard, order_keyboard
from post_controller import show_posts, usersData, show_post, post_count_on_page
from settings import dp, bot
from translator import translate_to_sr
from user import User

orders = {
    '📶 Подешевле': 'price',
    '📶 Подороже': 'price desc',
    '📶 Новые': 'posted desc',
    '📶 Популярные': 'view_count desc',
    '📶 Релевантные': 'relevance'
}

logging.basicConfig(level=logging.INFO, filename="log.log")


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    user = User(message['from'].id)

    user.user_info = message["from"]

    await bot.send_message(message.chat.id,
                           f'Привет {message["from"].first_name}, я могу найти для тебя что-нибудь',
                           reply_markup=default_keyboard)


@dp.message_handler(text='⬅️ Назад')
async def prev_posts(message):
    user = User(message['from'].id)

    if user.offset <= 0:
        user.offset = 30
        if user.request_params['page'] > 1:
            user.request_params['page'] -= 1
    else:
        user.offset -= post_count_on_page

    await show_posts(message)


@dp.message_handler(text='➡️ ️Дальше')
async def next_posts(message):
    user = User(message['from'].id)

    if user.offset >= 25:
        user.offset = 0
        user.request_params['page'] += 1
        await bot.send_message(message.chat.id, 'Погружаем следующую страницу...')
    else:
        user.offset += post_count_on_page

    await show_posts(message)


@dp.message_handler(filters.Text(startswith='📶'))
async def next_posts(message):
    user = User(message['from'].id)
    if message.text == '📶 Сортировка':
        keys = [key for key, value in orders.items() if value == user.request_params['order']]
        await bot.send_message(message.chat.id, f'Выберите сортировку, текущая: {keys[0]}',
                               reply_markup=order_keyboard)
    elif message.text in orders:
        user.request_params['order'] = orders[message.text]
        await bot.send_message(message.chat.id, 'Сортировка изменена, возвращаемся к просмотру...',
                               reply_markup=default_keyboard)
        await show_posts(message)
    else:
        await bot.send_message(message.chat.id, f'Пожалуйста выберите из списка',
                               reply_markup=order_keyboard)


@dp.message_handler(text='Вернуться к объявлениям')
async def back_to_posts(message):
    await show_posts(message)
    await bot.send_message(message.chat.id, 'Возвращаемся к просмотру...', reply_markup=default_keyboard)


@dp.message_handler()
async def search(message):
    keywords = translate_to_sr(message.text.lower())
    await bot.send_message(message.chat.id, f'Начинаем поиск по запросу: "{keywords}"')
    user = User(message['from'].id)
    user.request_params['keywords'] = keywords
    user.save()

    await show_posts(message)


@dp.callback_query_handler()
async def handler(callback_query: types.CallbackQuery):
    await show_post(callback_query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
