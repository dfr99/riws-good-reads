"""
Spider code to crawl and scrape Good Reads books data
"""


# -*- coding: utf-8 -*-

from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import scraper.scraper as scraper
from good_reads.items import BookItem


class BookSpider(CrawlSpider):
    name = "good_reads"
    allowed_domains = ["goodreads.com"]
    start_urls = [
        "https://www.goodreads.com/list/show/3116.Best_historical_fiction_novels"
    ]
    for i in range(2, 12):
        page = "?page=" + str(i)
        start_urls.append(start_urls[0] + page)
    rules = (Rule(LinkExtractor(allow="/book/show/.*"), callback="parse_book_details"),)

    @staticmethod
    def _extract_item(url) -> BookItem:
        item = BookItem()
        data = scraper.extract_data(url)
        item["title"] = data[0]
        item["author"] = data[1]
        item["rating"] = data[2]
        item["summary"] = data[3]
        item["cover_page"] = data[4]
        item["genres"] = data[5]
        item["number_of_pages"] = data[6]
        item["release_date"] = data[7]
        item["isbn"] = data[8]
        item["language"] = data[9]

        return item

    def parse_book_details(self, response: Response):
        self.logger.info("Scraping %s...", response.url)
        self.logger.info("User-Agent for this request: %s", response.request.headers['User-Agent'])
        item = self._extract_item(response.url)
        yield item
