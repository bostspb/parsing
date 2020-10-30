# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from pymongo import MongoClient
import re
from lesson06.bankparser.items import BankItem
from lesson06.bankparser.items import RequisitesItem
from lesson06.bankparser.items import BranchOrAtmItem


class BankparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.banks20201030

    def _save(self, item):
        collection = self.db[item['_collection']]
        collection.save(item)

    def process_item(self, item, spider):
        if item['_collection'] == 'banks':
            self.process_bank(item)
        elif item['_collection'] == 'requisites':
            self.process_requisites(item)
        elif item['_collection'] == 'branches':
            self.process_branch_or_atm(item)
        elif item['_collection'] == 'atms':
            self.process_branch_or_atm(item)
        return item

    def process_bank(self, item: BankItem):
        item['id'] = int(re.search('(\d+$)', item['_id']).group(0))
        item['requisites_id'] = int(re.search('(\d+$)', item['requisites_url']).group(0))
        self._save(item)

    def process_requisites(self, item: RequisitesItem):
        item['id'] = int(re.search('(\d+$)', item['_id']).group(0))
        self._save(item)

    def process_branch_or_atm(self, item: BranchOrAtmItem):
        ids_regexp = re.search('(\d+)\/any\/(\d+$)', item['in_city_url'])
        coordinates_regexp = re.search('mapFeatureItemGeometry\[\"coordinates\"\] = \[ (\d+.\d+), (\d+.\d+) \];', item['coordinates'])
        item['id'] = int(re.search('(\d+$)', item['_id']).group(0))
        item['coordinates'] = [coordinates_regexp.group(1), coordinates_regexp.group(2)]
        item['city_id'] = int(ids_regexp.group(1))
        item['bank_id'] = int(ids_regexp.group(2))
        self._save(item)

