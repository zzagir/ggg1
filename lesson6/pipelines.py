# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy3105

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary_list = []
            for _ in item['salary']:
                s = _.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            item['salary'] = salary_list
            if item['salary'][0] == 'от':
                item['salary_min'] = int(item['salary'][1])
                if item['salary'][2] == 'до':
                    item['salary_max'] = int(item['salary'][3])
                else:
                    item['salary_max'] = 'NA'
            elif item['salary'][0] == 'до':
                item['salary_min'] = 'NA'
                item['salary_max'] = int(item['salary'][1])
                item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'з/п не указана':
                item['salary_min'] = 'NA'
                item['salary_max'] = 'NA'
            else:
                item['salary_min'] = 'wrong'
                item['salary_max'] = 'wrong'
            del item['salary']


        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item
