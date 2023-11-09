"""
Define your item pipelines here

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""

# -*- coding: utf-8 -*-
import json


class GoodReadsPipeline:
    def open_spider(self, spider):
        self.listItem = []

    def close_spider(self, spider):
        with open("./data/" + spider.name + ".json", "w", encoding="utf-8") as outfile:
            json.dump(self.listItem, outfile, default=str)

    def process_item(self, item, spider):
        self.listItem.append(dict(item))
        return item
