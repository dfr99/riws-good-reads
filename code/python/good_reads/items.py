"""
Define here the models for your scraped items

See documentation in:
https://docs.scrapy.org/en/latest/topics/items.html
"""

# -*- coding: utf-8 -*-
import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    summary = scrapy.Field()
    genres = scrapy.Field()
    release_date = scrapy.Field()
    number_of_pages = scrapy.Field()
    isbn = scrapy.Field()
    language = scrapy.Field()
    cover_page = scrapy.Field()
