import logging

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from settings import get_webdriver
from translator import translate_to_ru


async def _get_soap_from_page(url) -> BeautifulSoup:
    browser = get_webdriver()

    browser.get(url)
    buttons = browser.find_elements(By.CLASS_NAME, 'ButtonExpand_expandHolder__JnA8X')
    if len(buttons) > 0:
        browser.execute_script("arguments[0].click();", buttons[1 if len(buttons) >= 2 else 0])

    soup = BeautifulSoup(browser.page_source, features='html.parser')
    browser.quit()
    return soup


async def search_posts(source_url):
    soup = await _get_soap_from_page(source_url)
    logging.info('url запроса: ' + source_url)
    posts = []
    crumbs = soup.findAll('div', 'BreadcrumbHolder_breadcrumbHolder__riFtq')[0]
    crumbs = crumbs.find_next('div')
    total = int(crumbs.text.split('>')[-1].split('rezultata')[0].replace('.', ''))
    cards = soup.findAll('section', 'AdItem_adOuterHolder__lACeh')
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
        logging.info('url объявления: ' + url)

        posts.append({
            'img': img.replace('tmb-300x300', 'big'),
            'small_img': img,
            'url': 'https://novi.kupujemprodajem.com' + url,
            'title': translate_to_ru(title),
            'description': translate_to_ru(description),
            'price': translate_to_ru(price),
            'location': location
        })

    return {
        'posts': posts,
        'total': total
    }


async def get_post(url):
    soup = await _get_soap_from_page(url)

    price = soup.select_one('h2.AdViewInfo_price__J_NcC').text
    title = soup.select_one('h1.AdViewInfo_name__VIhrl').text
    condition = soup.select_one('.AdViewInfoData_conditionAndAvailableNowHolder__mk0TA > div:nth-child(1)').text
    location = soup.select_one('.AdViewInfoData_adViewDataHolder__4kPlh > div:nth-child(1)').text

    buttons = soup.findAll('div', 'ButtonExpand_holder__cJJnC')

    if len(buttons) == 1:
        phone = buttons[0].find_next('span').text
    elif len(buttons) > 1:
        phone = buttons[1].find_next('span').text
    else:
        phone = '-'

    info = soup.select_one('.AdViewDescription_descriptionHolder__kOWyx > div:nth-child(1)')
    images_src = []
    images = soup.findAll('div', 'GalleryThumbnail_imageGalleryThumbnailInner__Kr_Oz')
    for image in images:
        images_src.append(image.find_next('img').get_attribute_list('src')[0].replace('tmb-300x300-', ''))

    return {
        'url': url,
        'title': translate_to_ru(title),
        'price': translate_to_ru(price),
        'condition': translate_to_ru(condition),
        'description': translate_to_ru(info.text),
        'images': images_src,
        'phone': phone,
        'location': location
    }
