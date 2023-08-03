import urllib

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile
import requests
from browser import search_posts, get_post
from helper import get_cached_data, Store
from keyboards import post_keyboard
from settings import bot
import urllib.parse

post_count_on_page = 5  # кол-во выводимых постов

usersData = {}
store = Store()
orders = ('price', 'price desc', 'posted desc', 'view_count desc', 'relevance')


def get_post_item_keyboard(url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотреть', callback_data=store.get_hash(url))]
    ])


def get_search_url(user_id):
    return 'https://novi.kupujemprodajem.com/pretraga?' + urllib.parse.urlencode(usersData[user_id]['url_parts'])


async def show_posts(message):
    url = get_search_url(message['from'].id)
    searched_data = await get_cached_data(url, search_posts)
    posts = searched_data['posts']
    total = searched_data['total']
    offset = usersData[message['from'].id]['offset']

    if len(posts) == 0:
        await bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено :(')
        return

    for key, post in enumerate(posts[offset:offset + post_count_on_page]):
        keyboard = get_post_item_keyboard(post['url'])
        num = (usersData[message['from'].id]['url_parts']['page'] - 1) * 30 + key + 1 + offset
        caption = f"""
[{post['title']}]({post['url']})
Цена: {post['price']}
Локация: {post['location']}
Описание:\n{post['description']}
Объявление {num} из {total} """ # todo переделать на отображение в клавиатуре?

        caption = caption.replace('*', '\*')

        image = post['img']
        print(post)
        img_file = requests.get(image)

        if img_file.content.__sizeof__() > 10000000:
            img_file = requests.get(post['small_img'])
            image = post['small_img']

        img_ext: str = image.split('.')[-1]

        if img_ext == 'HEIC':
            file_name = f'./images/{hash(image)}.jpg'
            out = open(file_name, 'wb')
            out.write(img_file.content)
            out.close()
            image = InputFile(file_name)

        #  todo
        #   добавить сортировки
        #   добавить фильтры
        #   добавить настройку отображения кол-ва постов на странице

        await bot.send_photo(message.chat.id, image, caption, parse_mode='MARKDOWN',
                             reply_markup=keyboard)


async def show_post(callback_query):
    post_url = store.get_data(callback_query.data)

    if not post_url:
        await bot.send_message(callback_query.from_user.id, 'Ссылка устарела, произведите новый поиск')
        return

    post = await get_cached_data(post_url, get_post)

    images = []
    for index, img in enumerate(post['images']):
        images.append(InputMediaPhoto(img))

        if len(images) == 10 or index == len(post['images']) - 1:
            await bot.send_media_group(callback_query.from_user.id, images)
            images = []

    # todo добавить отображение цены, контактов, ссылку, заголовок, локацию
    #  добавить провреку на длину описания и разбивать его на несколько сообщений тогда
    await bot.send_message(callback_query.from_user.id, post['description'], reply_markup=post_keyboard)
