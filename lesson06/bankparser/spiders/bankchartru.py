import scrapy
from scrapy.http import HtmlResponse
from lesson06.bankparser.items import BankItem
from lesson06.bankparser.items import RequisitesItem
from lesson06.bankparser.items import BranchOrAtmItem


class BankchartruSpider(scrapy.Spider):
    name = 'BankchartRu'
    allowed_domains = ['bankchart.ru']
    start_urls = ['https://bankchart.ru/spravochniki/banki']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='alphabet__list']//a[contains(@href,'/spravochniki/banki/id/')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.bank_parse)

    def bank_parse(self, response: HtmlResponse):
        bank = {
            '_id': response.url,
            '_collection': 'banks',
            'name': response.xpath("//h1/text()").extract_first(),
            'address': response.xpath("//h5[text() = 'Головной офис:']/parent::div/p/text()").extract_first(),
            'phone01': response.xpath("//h5[text() = 'Телефон головного офиса:']/parent::div/p/text()").extract_first(),
            'phone02': response.xpath("//h5[text() = 'Горячая линия:']/parent::div/p/a/text()").extract_first(),
            'email': response.xpath("//h5[text() = 'Email:']/parent::div/p/text()").extract_first(),
            'site': response.xpath("//h5[text() = 'Официальный сайт:']/parent::div/p/text()").extract_first().strip(),
            'branches_url':  response.xpath("//div[@class='bank__info-item']//a[text() = 'отделения']/@href").extract_first(),
            'atms_url':  response.xpath("//div[@class='bank__info-item']//a[text() = 'банкоматы']/@href").extract_first(),
            'requisites_url':  response.xpath("//h5[text() = 'Реквизиты:']/parent::div/p/a/@href").extract_first(),
            'description':  response.xpath("//div[@class='bank__text']/p/text()").extract(),
            'manager':  response.xpath("//p[@class='name']/a/text()").extract_first(),
            'actives':  response.xpath("//div[text() = 'Активы']/parent::div/div[@class='col col-fin-amount']/a/text()").extract_first(),
            'actives_rating':  response.xpath("//div[text() = 'Активы']/parent::div//span/text()").extract_first(),
            'profit':  response.xpath("//div[text() = 'Чистая прибыль']/parent::div/div[@class='col col-fin-amount']/a/text()").extract_first(),
            'profit_rating':  response.xpath("//div[text() = 'Чистая прибыль']/parent::div//span/text()").extract_first(),
        }
        yield BankItem(**bank)

        if bank['requisites_url']:
            yield response.follow(bank['requisites_url'], callback=self.requisites_parse)

        if bank['branches_url']:
            yield response.follow(bank['branches_url'], callback=self.branches_parse)

        if bank['atms_url']:
            yield response.follow(bank['atms_url'], callback=self.atms_parse)

    def requisites_parse(self, response: HtmlResponse):
        requisites = {
            '_id': response.url,
            '_collection': 'requisites',
            'full_name': response.xpath("//h5[text() = 'Полное название банка:']/parent::div/p/text()").extract_first(),
            'licence': int(response.xpath("//h5[text() = 'Генеральная лицензия:']/parent::div/p/text()").extract_first()),
        }
        yield RequisitesItem(**requisites)

    def branches_parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='alphabet__list']//a[contains(@href,'/spravochniki/otdeleniya/')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.branch_parse)

    def branch_parse(self, response: HtmlResponse):
        addresses = response.xpath(
            "//div[@class='row-last']/div[@class='col col-org_address']//span/text()").extract()
        coordinates = response.xpath(
            "//script[contains(text(), 'mapFeatureItemGeometry[\"coordinates\"]')]/text()").extract()
        links = response.xpath(
            "//div[@class='row-last']/div[@class='col col-org_address']//a/@href").extract()
        if len(addresses) == len(coordinates) == len(links):
            for i in range(len(addresses)):
                branch = {
                    '_id': links[i],
                    '_collection': 'branches',
                    'coordinates': coordinates[i],
                    'address': addresses[i],
                    'in_city_url': response.url
                }
                yield BranchOrAtmItem(**branch)

    def atms_parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='alphabet__list']//a[contains(@href,'/spravochniki/bankomaty/')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.atm_parse)

    def atm_parse(self, response: HtmlResponse):
        addresses = response.xpath(
            "//div[@class='row-last']/div[@class='col col-org_address']//span/text()").extract()
        coordinates = response.xpath(
            "//script[contains(text(), 'mapFeatureItemGeometry[\"coordinates\"]')]/text()").extract()
        links = response.xpath(
            "//div[@class='row-last']/div[@class='col col-org_address']//a/@href").extract()
        if len(addresses) == len(coordinates) == len(links):
            for i in range(len(addresses)):
                atm = {
                    '_id': links[i],
                    '_collection': 'atms',
                    'coordinates': coordinates[i],
                    'address': addresses[i],
                    'in_city_url': response.url
                }
                yield BranchOrAtmItem(**atm)
