from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from translator import translate_to_ru


async def _get_soap_from_page(url) -> BeautifulSoup():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # service=Service(FirefoxDriverManager().install())
    browser = webdriver.Firefox(options=options)

    browser.get(url)
    soup = BeautifulSoup(browser.page_source, features='html.parser')
    browser.quit()
    return soup


async def search_posts(source_url):
    soup = await _get_soap_from_page(source_url)
    print(source_url)
    posts = []
    cards = soup.findAll('section', 'AdItem_adOuterHolder__i2qTf')
    for card in cards:
        article = card.find_next('article')
        main_block = article.find_next('a').find_next_sibling('div')
        [title_box, price_block, some_info, location_block] = main_block.contents

        img = article.find_next('a').find_next('img').get_attribute_list('src')[0]

        a = title_box.find_next('a')
        title = a.find_next('div').text

        url = a.get_attribute_list('href')[0]
        description = title_box.find_next('p').text

        price = price_block.find_next('div').find_next('div').text
        location = location_block.find_next('p').text
        print(url)

        posts.append({
            'img': img.replace('tmb-300x300', 'big'),
            'small_img': img,
            'url': 'https://novi.kupujemprodajem.com' + url,
            'title': translate_to_ru(title),
            'description': translate_to_ru(description),
            'price': translate_to_ru(price),
            'location': location
        })

    return posts


async def get_post(url):
    soup = await _get_soap_from_page(url)

    info = soup.findAll('section', 'AdViewDescription_descriptionHolder__9hET7')[0].find_next('div')
    images_src = []
    images = soup.findAll('div', 'GalleryThumbnail_imageGalleryThumbnailInner___ou1n')
    for image in images:
        images_src.append(image.find_next('img').get_attribute_list('src')[0].replace('tmb-300x300-', ''))

    print(images_src)

    return {
        'description': translate_to_ru(info.text),
        'images': images_src
    }
