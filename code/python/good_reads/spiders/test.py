# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor

from good_reads.items import BookItem


class TestBookSpider(CrawlSpider):
    name = "test"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/list/show/3116.Best_historical_fiction_novels"]
    rules = (Rule(LinkExtractor(allow="/book/show/.*"), callback="parse_book_details"), )

    @staticmethod
    def _extract_item(response: Response) -> BookItem:
        item = BookItem()
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('span', itemprop='name').get_text(strip=True)
        # Título
        item['title'] = response.css('span[itemprop="name"]::text').get().strip()
        # Autor
        item['author'] = response.css('a.authorName span[itemprop="name"]::text').get().strip()
        # Rating
        rating_data = response.css('span.minirating::text').get()
        if rating_data:
            rating = rating_data.split()[0]
            item['rating'] = float(rating.strip())
        # Imagen de Portada
        item['cover_page'] = response.css('img.bookCover::attr(src)').get().strip()
        # Resumen (suponiendo un selector ficticio, tendrás que ajustarlo)
        item['summary'] = response.css('div.bookDescription span:last-child::text').get().strip()
        # Géneros (también un selector ficticio)
        item['genres'] = response.css('div.bookGenres a::text').getall()
        # Fecha de Publicación (selector ficticio)
        item['release_date'] = response.css('div.publishDate::text').get().strip()
        # Número de páginas (selector ficticio)
        item['number_of_pages'] = response.css('span#pages::text').get().strip()
        # ISBN (selector ficticio)
        item['isbn'] = response.css('span#isbn::text').get().strip()
        # Idioma (selector ficticio)
        item['language'] = response.css('span#language::text').get().strip()

        return item

    def parse_book_details(self, response: Response):
        # Extraer los libros de la lista
        book_rows = response.css('tr[itemtype="http://schema.org/Book"]')

        for row in book_rows:
            book_link = row.css('a.bookTitle::attr(href)').get()
            if book_link:
                item = self._extract_item(response)
                yield item
