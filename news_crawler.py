import requests
from bs4 import BeautifulSoup

from data_storage import DataStorage


class NewsCrawler:
    def __init__(self, is_total=False):
        self.data_storage = DataStorage('data/data.csv')
        self.domain = 'news.buaa.edu.cn'
        self.url_prefix = 'http://news.buaa.edu.cn/bhrw/'
        self.urls = ['http://news.buaa.edu.cn/bhrw.htm']
        if is_total:
            for idx in range(1, 17):
                self.urls.append(self.url_prefix + str(idx) + '.htm')

    def _crawl_article(self, url):
        article_html = requests.get(url)
        if article_html.status_code == 200:
            soup = BeautifulSoup(article_html.content.decode('utf-8', 'ignore'), 'html.parser')
            title_div = soup.find('div', class_='newslefttit auto')
            content_div = soup.find('div', class_='v_news_content')
            title, content = None, []

            if not title_div or not content_div:
                return None

            h1_tag = title_div.find('h1')
            # print(f'标题: {h1_tag.get_text()}')
            title = h1_tag.get_text()
            p_tags = content_div.find_all('p')
            # print("内容:")
            # 输出每个 p 标签的内容
            for p_tag in p_tags:
                content.append(p_tag.get_text())
            self.data_storage.add_entry(title, content)
            print('===========================')
        else:
            print(f'获取文章内容失败！{article_html.status_code}')

    def crawl(self):
        for url in self.urls:
            resp = requests.get(url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')

                target_divs = soup.find_all('div', class_='listleftop1 auto')
                article_urls = []
                # 提取每个 div 中的 href 属性
                for div in target_divs:
                    href_tag = div.find('a', href=True)
                    if href_tag:
                        href_value = href_tag['href']
                        article_urls.append('http://' + self.domain + '/' + href_value)

                print(f"文章链接列表：{article_urls}")
                for article_url in article_urls:
                    self._crawl_article(article_url)
            else:
                print(f'获取失败!，code:{resp.status_code}')


if __name__ == '__main__':
    news_crawler = NewsCrawler(is_total=True)
    news_crawler.crawl()
