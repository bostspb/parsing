from pprint import pprint
from lxml import html
import requests


class LentaRuParser:
    host = 'https://lenta.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def parse(self) -> list:
        news_list = []
        response = requests.get(self.host, headers=self.headers)
        dom = html.fromstring(response.text)
        news_elements = dom.xpath("//section[contains(@class,'js-top-seven')]//div[@class='item']")
        for element in news_elements:
            news = {
                'title': str(element.xpath("./a/text()")[0]),
                'url':  self.host + str(element.xpath("./a/@href")[0]),
                'source': 'LENTA_RU',
                'publication_date': str(element.xpath("./a/time/@datetime")[0])
            }
            news_list.append(news)
        return news_list


if __name__ == '__main__':
    parser = LentaRuParser()
    news_result = parser.parse()
    pprint(news_result)
