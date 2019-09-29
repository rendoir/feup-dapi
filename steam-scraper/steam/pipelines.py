# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import ProductItem


class SteamPipeline(object):
    def process_item(self, item, spider):
        return item

class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        if type(item) is ProductItem:
            item.setdefault('sentiment', 'null')
            item.setdefault('percent_positive', 'null')
            item.setdefault('n_reviews', '0')
        return item
