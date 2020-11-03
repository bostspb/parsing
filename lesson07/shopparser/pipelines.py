from pprint import pprint
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from urllib.parse import urlparse


class ShopparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.shop

    def process_item(self, item, spider):
        params = item['params']
        item['params'] = dict(zip(params[:len(params) // 2], params[len(params) // 2:]))
        pprint(item)
        collection = self.db[spider.name]
        collection.save(item)
        return item


class ShopparserPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return str(item['_id']) + '/' + os.path.basename(urlparse(request.url).path)
