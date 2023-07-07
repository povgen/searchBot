from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from translator import translate_to_ru


async def search_product(request, callback, chat_id):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # service=Service(FirefoxDriverManager().install())
    browser = webdriver.Firefox(options=options)

    browser.get("https://novi.kupujemprodajem.com/pretraga?keywords=" + request)
    soup = BeautifulSoup(browser.page_source, features='html.parser')
    browser.quit()

    cards = soup.findAll('section', 'AdItem_adOuterHolder__i2qTf')
    print(f'searched: {len(cards)}')
    for card in cards[:3]:
        article = card.find_next('article')
        main_block = article.find_next('a').find_next_sibling('div')
        [title_box, price_block, some_info, location_block] = main_block.contents

        img = article.find_next('a').find_next('img').get_attribute_list('src')[0]
        print(f'searched: {img}')

        a = title_box.find_next('a')
        title = a.find_next('div').text

        url = a.get_attribute_list('href')[0]
        description = title_box.find_next('p').text

        price = price_block.find_next('div').find_next('div').text
        location = location_block.find_next('p').text

        await callback({
            'img': img.replace('tmb-300x300', 'big'),
            'url': 'https://novi.kupujemprodajem.com' + url,
            'title': translate_to_ru(title),
            'description': translate_to_ru(description),
            'price': translate_to_ru(price),
            'location': location
        }, chat_id)
