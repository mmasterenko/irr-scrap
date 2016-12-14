import time
import requests
from bs4 import BeautifulSoup

from .models import Ads, Categories
from project.celery import app

URL = 'http://m.irr.ru/food/'


def get_base_url(url):
    parsed = requests.utils.urlparse(url)
    return '%s://%s' % (parsed.scheme, parsed.netloc)


@app.task
def test_task(n):
    time.sleep(n)
    return 'have sleep %s seconds' % n


@app.task
def get_ads(url, cat_id=None):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    items = bs.find_all('div', {'class': 'listingItem__info'})
    count = 0
    for i, item in enumerate(items):
        header = item.a.text
        price = item.span.b.text
        try:
            city = item.find_all('p')[2].text.strip()
        except IndexError:
            city = ''
        position = i + 1
        Ads.objects.create(header=header, price=price, city=city, position=position, category_id=cat_id)
        count += 1
    show_more = bs.find('a', {'class': 'js-showMoreButton'})
    if show_more:
        href = show_more.attrs.get('href')
        show_more_url = get_base_url(URL) + href
        get_ads.delay(show_more_url, cat_id=cat_id)
    return '%s ads processed in "%s"' % (count, url)


@app.task
def get_categories():
    response = requests.get(URL)
    bs = BeautifulSoup(response.text, 'html.parser')
    items = bs.find('div', {'class': 'catList__body'}).find_all('a')
    count = 0
    results = []
    for item in items:
        name = item.find('span', {'class': 'catList__itemName'}).text
        url = get_base_url(URL) + item.attrs.get('href')
        obj, is_created = Categories.objects.get_or_create(name=name, url=url)
        res = get_ads.delay(obj.url, cat_id=obj.id)
        results.append(res)
        count += 1
    while not all([r.ready() for r in results]):
        time.sleep(1)
    return '%s categories processed' % count
