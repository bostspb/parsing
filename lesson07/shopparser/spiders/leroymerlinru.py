import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lesson07.shopparser.items import ShopparserItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['spb.leroymerlin.ru']
    start_urls = ['https://spb.leroymerlin.ru/catalogue/klei/']

    def parse(self, response: HtmlResponse):
        last_page_number = int(response.xpath("//uc-pagination/@total").extract_first())
        for page_number in range(1, last_page_number + 1, 1):
            page_link = response.url + '?page=' + str(page_number)
            yield response.follow(page_link, callback=self.page_parse)

    def page_parse(self, response: HtmlResponse):
        product_links = response.xpath("//a[@slot='picture']")
        for link in product_links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopparserItem(), response=response)
        loader.add_value('_id', response.url, re='-(\d+)\/$')
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('params', "//div[@class='def-list__group']/dt/text()")
        loader.add_xpath('params', "//div[@class='def-list__group']/dd//text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        yield loader.load_item()
