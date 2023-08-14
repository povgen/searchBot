import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from translator import translate_to_ru


async def _get_soap_from_page(url) -> BeautifulSoup():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    #todo переделать на
    # element = driver.find_element_by_class_name('pagination-r')
    # driver.execute_script("arguments[0].click();", element)
    # https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y

    browser.get(url)
    buttons = browser.find_elements(By.CLASS_NAME, 'ButtonExpand_expandHolder__ZnxCZ')
    if len(buttons) > 0:
        browser.execute_script("arguments[0].click();",  buttons[1 if len(buttons) >= 2 else 0])

        #browser.find_element(By.CLASS_NAME, 'Modal_closeIcon__29nCg').click()
        #browser.find_element(By.CLASS_NAME, 'CookieConsent_button__z3J_H').click()

        # if len(buttons) >= 2:
        #     buttons[1].click()
        # else:
        #     buttons[0].click()

    soup = BeautifulSoup(browser.page_source, features='html.parser')
    browser.quit()
    return soup


async def search_posts(source_url):
    soup = await _get_soap_from_page(source_url)
    logging.info('url запроса: ' + source_url)
    posts = []
    crumbs = soup.findAll('div', 'BreadcrumbHolder_breadcrumb__utk3j')[0]
    crumbs = crumbs.find_next('div')
    total = int(crumbs.text.split('>')[-1].split('rezultata')[0].replace('.', ''))
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

    price = soup.findAll('div', 'AdViewInfo_adInfoPrice__pVuSx')[0].find_next('h2').text
    title_block = soup.findAll('div', 'AdViewInfo_nameHolder__md4J1')[0]
    title = title_block.find_next('h1').text
    condition = title_block.find_next('div').text
    [account_age, location] = soup.findAll('div', 'UserSummary_userDetails__tNXN7')[0].find_next('div').contents

    buttons = soup.findAll('div', 'ButtonExpand_holder___pAqB')

    if len(buttons) == 1:
        phone = buttons[0].find_next('span').text
    elif len(buttons) > 1:
        phone = buttons[1].find_next('span').text
    else:
        phone = '-'

    info = soup.findAll('section', 'AdViewDescription_descriptionHolder__9hET7')[0].find_next('div')
    images_src = []
    images = soup.findAll('div', 'GalleryThumbnail_imageGalleryThumbnailInner___ou1n')
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
        'location': location.text
    }
