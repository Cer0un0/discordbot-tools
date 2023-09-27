import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd



class news_articles:
    def __init__(self) -> None:
        load_dotenv()
        self.base_url = 'https://newsapi.org/v2'
        self.headline_api_url = 'https://newsapi.org/v2/top-headlines'
        self.headers = {'X-Api-Key': os.environ['NEWS_API_KEY']}

    def get_articles(self, country='jp') -> pd.DataFrame:
        params= {
            'country': country,
        }
        response = requests.get(self.headline_api_url, headers=self.headers, params=params)

        if response.ok:
            data = response.json()
            df = pd.DataFrame(data['articles'])
            print('totalResults:', data['totalResults'])
        print(df[[ 'publishedAt', 'title', 'url']])


        return df
    
    
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