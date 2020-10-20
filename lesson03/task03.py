"""
    3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
    UPD: будем добавлять информацию только по новым банкам
"""

from lesson03.task01 import BankchartRuParser
from pymongo import MongoClient

parser = BankchartRuParser()
client = MongoClient('127.0.0.1', 27017)
db = client['bankchart_ru']
for bank in parser.banks:
    bank_in_db = db.banks.find_one({'id': bank['id']})
    if bank_in_db is None:
        bank_with_info = parser.parse_bank_info(bank)
        db.banks.insert_one(bank_with_info)