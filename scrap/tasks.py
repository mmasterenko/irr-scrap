import os

from selenium import webdriver
from django.conf import settings

from .models import Ads, Categories
from project.celery import app

DRIVER_PATH = os.path.join(settings.BASE_DIR, 'bin/geckodriver')
URL = 'http://m.irr.ru/food/'


@app.task
def get_ads(url, cat_id=None):
    browser = webdriver.Firefox(executable_path=DRIVER_PATH)
    browser.get(url)
    items = browser.find_elements_by_class_name('listingItem__info')
    for i, item in enumerate(items):
        header = item.find_element_by_tag_name('a').text
        price = item.find_element_by_tag_name('span').text
        city = item.find_element_by_css_selector('p + p + p').text
        position = i + 1
        Ads.objects.create(header=header, price=price, city=city, position=position, category_id=cat_id)
        return '%s ads processed in "%s"' % (i, url)


@app.task
def get_categories():
    browser = webdriver.Firefox(executable_path=DRIVER_PATH)
    browser.get(URL)
    items = browser.find_elements_by_class_name('catList__item')
    count = 0
    for item in items:
        obj = Categories.objects.create(name=item.text, url=item.get_attribute('href'))
        get_ads.delay(obj.url, cat_id=obj.id)
        count += 1
    return '%s categories processed' % count
