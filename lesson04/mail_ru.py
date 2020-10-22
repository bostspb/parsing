from pprint import pprint
from lxml import html
import requests


class MailRuParser:
    host = 'https://news.mail.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def parse(self) -> list:
        news_list = []
        response = requests.get(self.host, headers=self.headers)
        dom = html.fromstring(response.text)
        news_elements = dom.xpath("//ul[@data-module='TrackBlocks']/li[@class='list__item']")
        for element in news_elements:
            news = {
                'title': str(element.xpath(".//text()")[0]),
                'url': str(element.xpath("./a/@href")[0])
            }
            news = self._extend(news)
            news_list.append(news)
        return news_list

    def _extend(self, news: dict) -> dict:
        response = requests.get(news['url'], headers=self.headers)
        dom = html.fromstring(response.text)
        news['source'] = str(dom.xpath("//a[contains(@class,'breadcrumbs__link')]//text()")[0])
        news['publication_date'] = str(dom.xpath("//span[@datetime]/@datetime")[0])
        return news


if __name__ == '__main__':
    parser = MailRuParser()
    news_result = parser.parse()
    pprint(news_result)
