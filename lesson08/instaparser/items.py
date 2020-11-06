# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    _collection = scrapy.Field()
    id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    profile_pic_url = scrapy.Field()
    is_private = scrapy.Field()
    is_verified = scrapy.Field()
    linked_user_id = scrapy.Field()
    linked_username = scrapy.Field()
