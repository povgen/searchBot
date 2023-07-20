from aiogram import types
from aiogram.utils import executor

from keyboards import default_keyboard
from post_controller import show_posts, usersData, show_post, post_count_on_page
from settings import dp, bot
from translator import translate_to_sr


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id,
                           f'Привет {message["from"].first_name}, я могу найти для тебя что-нибудь',
                           reply_markup=default_keyboard)


@dp.message_handler(text='Назад')
async def prev_posts(message):
    user_id = message['from'].id

    if usersData[user_id]['offset'] <= 0:
        usersData[user_id]['offset'] = 30
        if usersData[user_id]['url_parts']['page'] > 1:
            usersData[user_id]['url_parts']['page'] -= 1
    else:
        usersData[user_id]['offset'] -= post_count_on_page

    await show_posts(message)


@dp.message_handler(text='Дальше')
async def next_posts(message):
    user_id = message['from'].id
    if usersData[user_id]['offset'] >= 25:
        usersData[user_id]['offset'] = 0
        usersData[user_id]['url_parts']['page'] += 1
        await bot.send_message(message.chat.id, 'Погружаем следующую страницу...')
    else:
        usersData[user_id]['offset'] += post_count_on_page

    await show_posts(message)


@dp.message_handler(text='Вернуться к объявлениям')
async def back_to_posts(message):
    await show_posts(message)
    await bot.send_message(message.chat.id, 'Возвращаемся к просмотру...', reply_markup=default_keyboard)


@dp.message_handler()
async def search(message):
    keywords = translate_to_sr(message.text.lower())
    await bot.send_message(message.chat.id, f'Начинаем поиск по запросу: "{keywords}"')
    usersData[message['from'].id] = {
        'url_parts': {
            'keywords': keywords,
            'page': 1,
        },
        'offset': 0
    }
    await show_posts(message)


@dp.callback_query_handler()
async def handler(callback_query: types.CallbackQuery):
    await show_post(callback_query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
