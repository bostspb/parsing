from bs4 import BeautifulSoup
import requests
import re
import json


def extract_next_sibling_contents(soap, tag, pattern, with_text=False):
    wrapper = soap.find(tag, text=re.compile(pattern))
    if wrapper is not None:
        if with_text:
            return str(wrapper.next_sibling.contents[0].text.strip())
        else:
            return str(wrapper.next_sibling.contents[0].strip())
    else:
        return None


def extract_next_sibling(soap, tag, pattern, with_next=False):
    wrapper = soap.find(tag, text=re.compile(pattern))
    if wrapper is not None:
        if with_next:
            return str(wrapper.next_sibling.next_sibling.text.strip())
        else:
            return str(wrapper.next_sibling.text.strip())
    else:
        return None


def extract_href(soap, tag, pattern, link_number, host):
    result = None
    wrapper = soap.find(tag, text=re.compile(pattern))
    if wrapper is not None:
        try:
            result = str(host + wrapper.next_sibling.find_all('a')[link_number]['href'])
        except IndexError:
            pass
    return result


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
host = 'https://bankchart.ru'
banks_html = requests.get(host+'/spravochniki/banki', headers=headers)
soup = BeautifulSoup(banks_html.text, "lxml")
banks = []

for bank_div in soup.find_all('div', class_='abc-list_with-icon'):
    bank_name = bank_div.find('span').text
    bank_info_url = 'https://bankchart.ru' + bank_div.find('a')['href']
    bank_id = re.search('(\d+$)', bank_info_url).group(0)
    banks.append({'name': bank_name, 'info_url': bank_info_url, 'id': bank_id})

for bank in banks:
    bank_info_html = requests.get(bank['info_url'])
    bank_info_soup = BeautifulSoup(bank_info_html.text, "lxml")

    bank['address'] = extract_next_sibling_contents(bank_info_soup, 'h5', 'Головной офис:')
    bank['phone01'] = extract_next_sibling_contents(bank_info_soup, 'h5', 'Телефон головного офиса:')
    bank['phone02'] = extract_next_sibling_contents(bank_info_soup, 'h5', 'Горячая линия:', True)
    bank['email'] = extract_next_sibling_contents(bank_info_soup, 'h5', 'Email:')
    bank['site'] = extract_next_sibling_contents(bank_info_soup, 'h5', 'Официальный сайт:')

    bank['branches_url'] = extract_href(bank_info_soup, 'h5', 'Сеть банка:', 0, host)
    bank['atms_url'] = extract_href(bank_info_soup, 'h5', 'Сеть банка:', 1, host)
    bank['bank_requisites_url'] = extract_href(bank_info_soup, 'h5', 'Реквизиты:', 0, host)

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

    bank['actives'] = extract_next_sibling(bank_info_soup, 'div', 'Активы')
    bank['actives_rating'] = extract_next_sibling(bank_info_soup, 'div', 'Активы', True)

    bank['profit'] = extract_next_sibling(bank_info_soup, 'div', 'Чистая прибыль')
    bank['profit_rating'] = extract_next_sibling(bank_info_soup, 'div', 'Чистая прибыль', True)

    if bank['bank_requisites_url'] is not None:
        bank_requisites_html = requests.get(bank['bank_requisites_url'])
        bank_requisites_soap = BeautifulSoup(bank_requisites_html.text, "lxml")
        bank['full_name'] = extract_next_sibling_contents(bank_requisites_soap, 'h5', 'Сокращенное название банка:')
        bank['licence'] = extract_next_sibling_contents(bank_requisites_soap, 'h5', 'Генеральная лицензия:')

with open('task01_data.json', 'w') as file:
    file.write(json.dumps(banks))




