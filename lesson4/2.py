from lxml import html
import requests
from pprint import pprint
import re
from pymongo import MongoClient


url = 'https://yandex.ru/news/'
headers = {'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@class, 'mg-card mg-card_')]")


list_items = []
for item in items[1:]:
    item_info = {}
    source_name = item.xpath(".//a[contains(@class, 'mg-card__source-link')]/text()")
    name = item.xpath(".//a[contains(@class, 'mg-card__link')]/text()")
    link = item.xpath(".//a[contains(@class, 'mg-card__link')]/@href")
    date = item.xpath(".//span[@class = 'mg-card-source__time']/text()")


    name = str(name)
    name = name.replace("\\xa0", " ")


    item_info['source_name'] = source_name
    item_info['name'] = name
    item_info['link'] = link
    item_info['date'] = date
    list_items.append(item_info)


client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news

for item in list_items:
    news.update_one(item, {'$setOnInsert': item}, upsert=True)
    print(item)