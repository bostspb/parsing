"""
    Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
    Для парсинга использовать XPath.
    Структура данных должна содержать:
        название источника;
        наименование новости;
        ссылку на новость;
        дата публикации.
    Сложить собранные данные в БД
"""

from pymongo import MongoClient
from pprint import pprint
from lesson04.lenta_ru import LentaRuParser
from lesson04.yandex_ru import YandexRuParser
from lesson04.mail_ru import MailRuParser


client = MongoClient('127.0.0.1', 27017)
db = client['news']

news_result = LentaRuParser().parse()
news_result += YandexRuParser().parse()
news_result += MailRuParser().parse()

# TODO: добавлять+обновлять
# TODO: нормализовать поле даты
db.news.insert_many(news_result)

pprint(news_result)