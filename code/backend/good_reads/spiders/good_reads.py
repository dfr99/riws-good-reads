"""
Spider code to crawl and scrape Good Reads books data
"""


# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from good_reads.items import BookItem
from scraper import scraper

load_dotenv()


class BookSpider(CrawlSpider):
    name = "good_reads"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/list/show/" + os.getenv("GOOD_READS_LIST")]
    rules = (
        Rule(LinkExtractor(allow="/book/show/.*"), callback="parse_book_details"),
        Rule(
            LinkExtractor(restrict_css="a.next_page"),
            callback="parse_page",
            follow=True,
        ),
    )

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
        self.logger.info("Scraping book %s...", response.url)
        self.logger.info(
            "User-Agent for this request: %s", response.request.headers["User-Agent"]
        )
        item = self._extract_item(response.url)
        yield item

    def parse_page(self, response: Response):
        self.logger.info("Scraping page %s...", response.url)
        self.logger.info(
            "User-Agent for this request: %s", response.request.headers["User-Agent"]
        )
        self.parse_book_details(response)
