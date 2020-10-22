from pprint import pprint
from lxml import html
import requests


class YandexRuParser:
    host = 'https://yandex.ru/news'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def parse(self) -> list:
        news_list = []
        response = requests.get(self.host, headers=self.headers)
        dom = html.fromstring(response.text)
        news_elements = dom.xpath("//div[contains(@class,'news-top-stories')]/div")
        for element in news_elements:
            news = {
                'title': str(element.xpath(".//h2/text()")[0]),
                'url':  str(element.xpath(".//a[@class='news-card__link']/@href")[0]),
                'source': str(element.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]),
                'publication_date': str(element.xpath(".//span[@class='mg-card-source__time']/text()")[0])
            }
            news_list.append(news)
        return news_list


if __name__ == '__main__':
    parser = YandexRuParser()
    news_result = parser.parse()
    pprint(news_result)
