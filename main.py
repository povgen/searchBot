import datetime
import json
import logging
import os

from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.utils import executor

from helper import var_dump
from keyboards import default_keyboard, order_keyboard
from post_controller import show_posts, usersData, show_post, post_count_on_page
from settings import dp, bot, BotStates, orders, r
from translator import translate_to_sr
from user import User

os.makedirs('logs', exist_ok=True)
logging.basicConfig(level=logging.INFO, filename="logs/log.log", format="%(asctime)s;%(levelname)s;%(message)s")


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    user = User(message['from'].id)
    user.user_info = message["from"].__dict__['_values']

    await bot.send_message(message.chat.id,
                           f'Привет, {message["from"].first_name}, я могу найти для тебя что-нибудь\n'
                           f'Для этого просто напиши, что ты ищешь',
                           reply_markup=default_keyboard)

    user.save()


@dp.message_handler(commands=['users'])
async def get_users(message):
    if message['from'].id != 1843600386:
        return

    user_id_list = json.JSONDecoder().decode(r.get('registered_users'))

    for user_id in user_id_list:
        user_info = r.get(user_id)
        if user_info is not None:
            msg = var_dump(json.JSONDecoder().decode(user_info))
            await bot.send_message(message.chat.id, msg)
        else:
            await bot.send_message(message.chat.id, f'пользователь с id: {user_id}, не найден :(')


@dp.message_handler(commands=['feedback'])
async def get_feedback(message):
    await bot.send_message(message.chat.id, 'Пожалуйста, введите ваш отзыв')
    await BotStates.feedback.set()


@dp.message_handler(state=BotStates.feedback)
async def save_feedback(message, state: FSMContext):
    username = message['from'].username
    name = message['from'].first_name
    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M")

    feedback = f'{now} {name} (@{username}): \n\t {message.text} \n\n'

    with open('logs/feedback.txt', 'a', encoding="utf-8") as f:
        f.write(feedback)

    await bot.send_message(message.chat.id, 'Спасибо за ваш отзыв')
    await state.finish()


@dp.message_handler(commands=['donate'])
async def get_donate_info(message):
    await bot.send_message(message.chat.id, """
    Вы можете отблагодарить разработчика одним из следующих способов:
    - Написать отзыв
    - Посоветовать бота друзьям
    - Отправить чаевые по реквизитам из описания бота
    """)


@dp.message_handler(text='⬅️ Назад')
async def prev_posts(message):
    user = User(message['from'].id)

    if user.offset <= 0:
        user.offset = 30
        if user.request_params['page'] > 1:
            user.request_params['page'] -= 1
    else:
        user.offset -= post_count_on_page

    user.save()
    await show_posts(message, user)


@dp.message_handler(text='➡️ ️Дальше')
async def next_posts(message):
    user = User(message['from'].id)

    if user.offset >= 25:
        user.offset = 0
        user.request_params['page'] += 1
        await bot.send_message(message.chat.id, 'Погружаем следующую страницу...')
    else:
        user.offset += post_count_on_page

    user.save()
    await show_posts(message, user)


@dp.message_handler(filters.Text(startswith='📶'))
async def next_posts(message):
    user = User(message['from'].id)
    if message.text == '📶 Сортировка':
        keys = [key for key, value in orders.items() if value == user.request_params['order']]
        await bot.send_message(message.chat.id, f'Выберите сортировку, текущая: {keys[0]}',
                               reply_markup=order_keyboard)
    elif message.text in orders:
        user.request_params['order'] = orders[message.text]
        user.save()
        await bot.send_message(message.chat.id, 'Сортировка изменена, возвращаемся к просмотру...',
                               reply_markup=default_keyboard)
        await show_posts(message, user)
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
