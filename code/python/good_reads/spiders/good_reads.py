# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from good_reads.items import BookItem
from scrapy_splash import SplashRequest 


lua_script = """
function main(splash, args)
    assert(splash:go(args.link))

    local element_genres = splash:select('button[aria-label="Show all items in the list"]')
    element_genres:mouse_click()
    
    local element_details = splash:select('button[aria-label="Book details and editions"]')
    element_details:mouse_click()

    splash:wait(splash.args.wait)  
    return splash:html()
end
"""


class BookSpider(CrawlSpider):
    name = "good_reads"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/list/show/3116.Best_historical_fiction_novels"]
    
    for i in range(2, 12):
        page = "?page=" + str(i)
        start_urls.append(start_urls[0] + page)
        i += 1
    rules = (Rule(LinkExtractor(allow="/book/show/.*"), callback="parse_book_details"), )

    @staticmethod
    def _extract_item(response: Response) -> BookItem:
        item = BookItem()
        soup = BeautifulSoup(response.text, 'lxml')
        
        item['title'] = soup.find('h1', {'class': 'Text__title1'}).text
        item['author'] = soup.find('span', {'class': 'ContributorLink__name'}).text
        item['rating'] = soup.find('div', {'class': 'RatingStatistics__rating'}).text
        # Revisar formato de texto, caracteres raros, \n ". . ."
        item['summary'] = soup.find('div', {'class': 'DetailsLayoutRightParagraph__widthConstrained'}).text
        item['cover_page'] = soup.find('img', {'class': 'ResponsiveImage'}).get('src')
        
        # Estos items solo son visibles si se clickan los botones
        # seleccionado en lua_script
        genres = []
        for genre in soup.find_all('span', {'class': 'BookPageMetadataSection__genreButton'}):
            genres.append(genre.find('span',{'class': 'Button__labelItem'}).text)
        item['genres'] = genres

        for item in soup.find_all('div', {'class': 'DescListItem'})[-4:]:
            selector = item.find('dt').text
            if selector == 'Format':
                item['number_of_pages'] = item.find('div', {'class': 'TruncatedContent'})
                                              .find('div', {'data-testid': 'contentContainer'})
                                              .text.split(',')[0].split(' ')[0]
            elif selector == 'Published':
                item['release_date'] = ' '.join(item.find('div', {'class': 'TruncatedContent'})
                                          .find('div', {'data-testid': 'contentContainer'})
                                          .text.split(' ')[:3])
            elif selector == 'ISBN':
                # TODO: casuistica en la que no aparece el ISBN
                # añadir un valor por defecto a ese campo
                item['isbn'] = item.find('div', {'class': 'TruncatedContent'})
                                   .find('div', {'data-testid': 'contentContainer'})
                                   .text.split(' ')[0]
            elif selector == 'Language':
                item['language'] = item.find('div', {'class': 'TruncatedContent'})
                                       .find('div', {'data-testid': 'contentContainer'})
                                       .text
            else:
                continue

        print(item)
        return item


    def parse_book_details(self, response: Response):
        item = self._extract_item(response)
        yield item


    def parse_page(self, response: Response):
        for link in response.css('a::attr(href)').extract():
            if '/book/show/' in link:
                absolute_link = "https://goodreads.com" + link
                yield SplashRequest(absolute_link, self.parse_book_details, args={'wait': 2, 'lua_source': lua_script})


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_page, args={'wait': 0})
