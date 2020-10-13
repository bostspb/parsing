"""
    1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
    сохранить JSON-вывод в файле *.json.
"""

import requests
import json

user = input('Введите имя пользователя: ')
pwd = input('Введите пароль: ')
response = requests.get('https://api.github.com/user/repos', auth=(user, pwd))
response_json = response.json()
with open('task01_response.json', 'w') as file:
    json.dump(response_json, file)

print('\nСписок репозиториев')
for repo in response_json:
    print(f"{repo['name']} - {repo['description']}")