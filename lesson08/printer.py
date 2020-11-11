from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.insta

print('Подписчики пользователя marta_8220')
marta_8220_followers = db.followers.find({'linked_username': 'marta_8220'})
for follower in marta_8220_followers:
    pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


print('\n\nПодписки пользователя marta_8220')
marta_8220_followings = db.followings.find({'linked_username': 'marta_8220'})
for following in marta_8220_followings:
    pprint(f"{following.get('username')} |:| {following.get('full_name')}")


print('\n\nПодписчики пользователя mukhtarenlik')
mukhtarenlik_followers = db.followers.find({'linked_username': 'mukhtarenlik'})
for follower in mukhtarenlik_followers:
    pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


print('\n\nПодписки пользователя mukhtarenlik')
mukhtarenlik_followings = db.followings.find({'linked_username': 'mukhtarenlik'})
for following in mukhtarenlik_followings:
    pprint(f"{following.get('username')} |:| {following.get('full_name')}")

