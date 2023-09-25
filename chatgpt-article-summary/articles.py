import requests
from bs4 import BeautifulSoup

class zenn_article:
    def __init__(self) -> None:
        self.articles_api_url = 'https://zenn.dev/api/articles'
        self.base_url = 'https://zenn.dev'

    def get_info(self, N) -> dict:
        """zennの記事情報をjson形式で返す

        Args:
            N: N件目の記事
        Returns:
            dict: N件目の記事の情報
        """
        zenn_response = requests.get(self.articles_api_url)
        zenn_json = zenn_response.json()
        return zenn_json['articles'][N]
    
    def get_content(self, path) -> str:
        """記事の内容を文字列で返す

        Args:
            path: 記事のpath
        Returns:
            str: 記事の内容
        """
        # get content
        article_url = '{}{}'.format(self.base_url, path)
        print(article_url)
        article_response = requests.get(article_url)

        # get text
        soup = BeautifulSoup(article_response.text,'html.parser')
        for script in soup(['script', 'style']):
            script.decompose()
        text = soup.get_text()

        return text