import scrapy
from scrapy.http import HtmlResponse
from labirintparser.items import LabirintparserItem


class LabirintSpiders(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2537/']

    def parse_1(self, response: HtmlResponse):
        links = response.xpath("//div[data-title='все в жанре Зарубежная фантастика]"
                               "//div[data-dir='book']//a[class='cover']/@href").extract()
        next_page = response.xpath("//div[@class='pagination-next']"
                                   "/a[class='pagination-next__text'/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.parse_book)
        if next_page:
            yield response.follow(next_page, callback=self.parse_1)

    def parse_book(self, response: HtmlResponse):
        link = response.url
        title = response.xpath("//div[@id='product-info']/@data-name").extract_first()
        authors = response.xpath("//div[@class='authors']//a[@data-event-label='author]/text").extract()
        price = response.xpath("//div[@id='product-info']/@data-price").extract_first()
        discount = response.xpath("div[id='product-info']/@data-discount-price").extract_first()
        rate = response.xpath("div[id='rate']/text()").extract_first()
        _id = response.xpath("//div[id='product-info']/@data-product-id").extract_first()
        yield LabirintparserItem(link=link, title=title, authors=authors,
                                 price=price, discount=discount, rate=rate, _id=_id)
