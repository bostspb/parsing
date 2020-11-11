import scrapy
from scrapy.http import HtmlResponse
from lesson08.instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class ProfileSpider(scrapy.Spider):
    name = 'profile'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    username = 'kuritsenko.sergei'
    enc_password = '**************'
    login_endpoint = 'https://www.instagram.com/accounts/login/ajax/'
    target_profiles = ['marta_8220', 'mukhtarenlik']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_query_hash = 'c76146de99bb02f6415203be841dd25a'
    following_query_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        """Авторизуемся."""
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_endpoint,
            method='POST',
            callback=self.authorization_result_parse,
            formdata={'username': self.username, 'enc_password': self.enc_password},
            headers={'X-CSRFToken': csrf_token}
        )

    def authorization_result_parse(self, response: HtmlResponse):
        """Начинаем парсить после авторизации."""
        authorization_result = json.loads(response.text)
        if authorization_result['authenticated']:
            for username in self.target_profiles:
                yield response.follow(
                    f'/{username}/',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': username}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        """Собираем ссылки на подписчиков и подписки"""
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            'include_reel': True,
            'fetch_mutual': True,
            'first': 24
        }
        # Переходим к сбору подписчиков
        yield response.follow(
            f'{self.graphql_url}query_hash={self.followers_query_hash}&{urlencode(variables)}',
            callback=self.followers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )
        # Переходим к сбору подписок
        yield response.follow(
            f'{self.graphql_url}query_hash={self.following_query_hash}&{urlencode(variables)}',
            callback=self.followings_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        """Собираем подписчиков"""
        followers_json = json.loads(response.text)
        page_info = followers_json.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):                  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']    # Курсор для запроса следующей порции подписчиков
            followers_url = f'{self.graphql_url}query_hash={self.followers_query_hash}&{urlencode(variables)}'
            # Запрашиваем слудующую порцию подписчиков
            yield response.follow(
                followers_url,
                callback=self.followers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )
        # Извлекаем список подписчиков из текущей порции
        followers = followers_json.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            profile = {
                '_id': user_id + '_' + follower['node']['id'],
                '_collection': 'followers',
                'id': follower['node']['id'],
                'username': follower['node']['username'],
                'full_name': follower['node']['full_name'],
                'profile_pic_url': follower['node']['profile_pic_url'],
                'is_private': follower['node']['is_private'],
                'is_verified': follower['node']['is_verified'],
                'linked_user_id': user_id,
                'linked_username': username
            }
            yield InstaparserItem(**profile)

    def followings_parse(self, response: HtmlResponse, username, user_id, variables):
        """Собираем подписки"""
        followings_json = json.loads(response.text)
        page_info = followings_json.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):                  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']    # Курсор для запроса следующей порции подписок
            followings_url = f'{self.graphql_url}query_hash={self.followers_query_hash}&{urlencode(variables)}'
            # Запрашиваем слудующую порцию подписок
            yield response.follow(
                followings_url,
                callback=self.followings_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )
        # Извлекаем список подписок из текущей порции
        followings = followings_json.get('data').get('user').get('edge_follow').get('edges')
        for following in followings:
            profile = {
                '_id': user_id + '_' + following['node']['id'],
                '_collection': 'followings',
                'id': following['node']['id'],
                'username': following['node']['username'],
                'full_name': following['node']['full_name'],
                'profile_pic_url': following['node']['profile_pic_url'],
                'is_private': following['node']['is_private'],
                'is_verified': following['node']['is_verified'],
                'linked_user_id': user_id,
                'linked_username': username
            }
            yield InstaparserItem(**profile)

    def fetch_csrf_token(self, text):
        """Извлекаем CSRF-токен"""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """Извлекаем ID пользователя"""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
