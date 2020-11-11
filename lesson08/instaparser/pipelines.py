from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.insta

    def process_item(self, item, spider):
        collection = self.db[item['_collection']]
        collection.save(item)
        return item
