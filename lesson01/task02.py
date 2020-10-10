"""
    2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
    Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
    Ответ сервера записать в файл.
    Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
    Сделайте запрос, чтб получить список всех сообществ на которые вы подписаны.
"""

import requests
import json

app_id = 7624066
vk_version = '5.124'
auth_url = f'https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v={vk_version}';

print(f'Перейдите по ссылке:\n{auth_url}\nи получите токен доступа.')
access_token = input('\nВведите токен доступа: ')

response = requests.get(f'https://api.vk.com/method/groups.get?extended=1&access_token={access_token}&v={vk_version}')
response_json = response.json()
with open('task02_response.json', 'w') as file:
    json.dump(response_json, file)

print('\nСписок сообществ, на которые вы подписаны')
for group in response_json['response']['items']:
    print(f"{group['name']}")