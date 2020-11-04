# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class LabirintparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.labirint

    def process_item(self, item, spider):
        if spider.name == "labirint":
            item['price'], item['discount'] = self.get_real_price(item['price'], item['discount'])
            item['price'] = float(item['price'])
        if item['discount'] is not None:
            item['discount'] = float(item['discount'])
            item['rate'] = float(item['rate'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
    def get_real_price(self, price, discount):
        if discount is not None:
            discount = ''.join([i for i in discount if i.isdigit()])
            price, discount = discount, price
        return price, discount