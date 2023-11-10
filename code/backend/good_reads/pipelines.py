"""
Define your item pipelines here

Don't forget to add your pipeline to the ITEM_PIPELINES setting
See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""

# -*- coding: utf-8 -*-
import json

from elasticsearch import Elasticsearch
from scrapy.exporters import JsonLinesItemExporter


class GoodReadsPipeline:
    def __init__(self):
        self.es = Elasticsearch(hosts=["https://localhost:9200"])
        self.index_name = "good_reads"

    def open_spider(self, spider):
        self.listItem = []

    def close_spider(self, spider):
        with open("./data/" + spider.name + ".json", "w", encoding="utf-8") as outfile:
            json.dump(self.listItem, outfile, default=str)

    def process_item(self, item, spider):
        self.listItem.append(dict(item))
        self.es.index(index=self.index_name, body=dict(item))
        return item
