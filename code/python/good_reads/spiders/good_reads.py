# -*- coding: utf-8 -*-
import scrapy
from good_reads.items import BookItem


class BookSpider(scrapy.Spider):
	name = "good_reads"
	allowed_domains = ["goodreads.com"]
	start_urls = ["https://www.goodreads.com"]
	