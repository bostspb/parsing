from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson06.bankparser import settings
from lesson06.bankparser.spiders.bankchartru import BankchartruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(BankchartruSpider)

    process.start()
