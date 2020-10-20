"""
    2. Написать функцию, которая производит поиск и выводит на экран вакансии
    с заработной платой больше введённой суммы.
    UPD: будем искать банки, по которым недособирали расширенную информацию
"""
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['bankchart_ru']
for result in db.banks.find({'address': {'$exists': True}}):
    pprint(result)

