import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def strip_param(value: str):
    value = value.strip()
    return value


def parse_int(value: str):
    value = value.replace(' ', '')
    return int(value)


class ShopparserItem(scrapy.Item):
    _id = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    params = scrapy.Field(input_processor=MapCompose(strip_param))
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(parse_int), output_processor=TakeFirst())
