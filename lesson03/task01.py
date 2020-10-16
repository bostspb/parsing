"""
    1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
    записывающую собранные вакансии в созданную БД.
    UPD: вместо вакансий будет информация о банках из прошлого урока
"""

from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient


class BankchartRuParser:
    host = 'https://bankchart.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    banks = []

    def __init__(self):
        banks_html = requests.get(self.host+'/spravochniki/banki', headers=self.headers)
        soup = BeautifulSoup(banks_html.text, "lxml")
        for bank_div in soup.find_all('div', class_='abc-list_with-icon'):
            bank_name = bank_div.find('span').text
            bank_info_url = 'https://bankchart.ru' + bank_div.find('a')['href']
            bank_id = re.search('(\d+$)', bank_info_url).group(0)
            self.banks.append({'name': bank_name, 'info_url': bank_info_url, 'id': bank_id})

    def parse_bank_info(self, bank):
        bank_info_html = requests.get(bank['info_url'], headers=self.headers)
        bank_info_soup = BeautifulSoup(bank_info_html.text, "lxml")

        bank['address'] = self.__extract_next_sibling_contents(self, bank_info_soup, 'h5', 'Головной офис:')
        bank['phone01'] = self.__extract_next_sibling_contents(self, bank_info_soup, 'h5', 'Телефон головного офиса:')
        bank['phone02'] = self.__extract_next_sibling_contents(self, bank_info_soup, 'h5', 'Горячая линия:', True)
        bank['email'] = self.__extract_next_sibling_contents(self, bank_info_soup, 'h5', 'Email:')
        bank['site'] = self.__extract_next_sibling_contents(self, bank_info_soup, 'h5', 'Официальный сайт:')

        bank['branches_url'] = self.__extract_href(bank_info_soup, 'h5', 'Сеть банка:', 0)
        bank['atms_url'] = self.__extract_href(bank_info_soup, 'h5', 'Сеть банка:', 1)
        bank['bank_requisites_url'] = self.__extract_href(bank_info_soup, 'h5', 'Реквизиты:', 0)

        description = bank_info_soup.find('div', class_='bank__text').find_all('p')
        bank['description'] = ''
        for p in description:
            if p.text != '':
                bank['description'] += str(p)

        manager_wrapper = bank_info_soup.find('p', class_='name')
        if manager_wrapper is not None:
            bank['manager'] = str(manager_wrapper.text)
        else:
            bank['manager'] = None

        bank['actives'] = self.__extract_next_sibling(self, bank_info_soup, 'div', 'Активы')
        bank['actives_rating'] = self.__extract_next_sibling(self, bank_info_soup, 'div', 'Активы', True)

        bank['profit'] = self.__extract_next_sibling(self, bank_info_soup, 'div', 'Чистая прибыль')
        bank['profit_rating'] = self.__extract_next_sibling(self, bank_info_soup, 'div', 'Чистая прибыль', True)

        if bank['bank_requisites_url'] is not None:
            bank_requisites_html = requests.get(bank['bank_requisites_url'], headers=self.headers)
            bank_requisites_soap = BeautifulSoup(bank_requisites_html.text, "lxml")
            bank['full_name'] = self.__extract_next_sibling_contents(self, bank_requisites_soap, 'h5', 'Сокращенное название банка:')
            bank['licence'] = self.__extract_next_sibling_contents(self, bank_requisites_soap, 'h5', 'Генеральная лицензия:')

        return bank

    @staticmethod
    def __extract_next_sibling_contents(self, soap, tag, pattern, with_text=False):
        wrapper = soap.find(tag, text=re.compile(pattern))
        if wrapper is not None:
            if with_text:
                return str(wrapper.next_sibling.contents[0].text.strip())
            else:
                return str(wrapper.next_sibling.contents[0].strip())
        else:
            return None

    @staticmethod
    def __extract_next_sibling(self, soap, tag, pattern, with_next=False):
        wrapper = soap.find(tag, text=re.compile(pattern))
        if wrapper is not None:
            if with_next:
                return str(wrapper.next_sibling.next_sibling.text.strip())
            else:
                return str(wrapper.next_sibling.text.strip())
        else:
            return None

    def __extract_href(self, soap, tag, pattern, link_number):
        result = None
        wrapper = soap.find(tag, text=re.compile(pattern))
        if wrapper is not None:
            try:
                result = str(self.host + wrapper.next_sibling.find_all('a')[link_number]['href'])
            except IndexError:
                pass
        return result


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['bankchart_ru']
    parser = BankchartRuParser()
    for bank in parser.banks:
        bank = parser.parse_bank_info(bank)
        db.banks.insert_one(bank)




