# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BankItem(scrapy.Item):
    _id = scrapy.Field()
    _collection = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phone01 = scrapy.Field()
    phone02 = scrapy.Field()
    email = scrapy.Field()
    site = scrapy.Field()
    branches_url = scrapy.Field()
    atms_url = scrapy.Field()
    requisites_url = scrapy.Field()
    requisites_id = scrapy.Field()
    description = scrapy.Field()
    manager = scrapy.Field()
    actives = scrapy.Field()
    actives_rating = scrapy.Field()
    profit = scrapy.Field()
    profit_rating = scrapy.Field()


class RequisitesItem(scrapy.Item):
    _id = scrapy.Field()
    _collection = scrapy.Field()
    id = scrapy.Field()
    full_name = scrapy.Field()
    licence = scrapy.Field()


class BranchOrAtmItem(scrapy.Item):
    _id = scrapy.Field()
    _collection = scrapy.Field()
    id = scrapy.Field()
    address = scrapy.Field()
    coordinates = scrapy.Field()
    in_city_url = scrapy.Field()
    city_id = scrapy.Field()
    bank_id = scrapy.Field()