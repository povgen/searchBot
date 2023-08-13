from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='⬅️ Назад'), KeyboardButton(text='➡️ ️Дальше')],
    [KeyboardButton(text='📶 Сортировка')],
])

post_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='Вернуться к объявлениям')]
])

order_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='📶 Подешевле'), KeyboardButton(text='📶 Подороже')],
    [KeyboardButton(text='📶 Новые'), KeyboardButton(text='📶 Популярные'), KeyboardButton(text='📶 Релевантные')]
])
#⬅️➡️📶 ️️