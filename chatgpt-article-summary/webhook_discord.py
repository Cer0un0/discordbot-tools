import requests
from dotenv import load_dotenv
import os
from articles import zenn_article
from gpt import gpt_summary
import sys

args = sys.argv

load_dotenv()
if args[1]=='dev':
  WEBHOOK_URL = os.environ['WEBHOOK_DEV']
elif args[1] == 'prod':
  WEBHOOK_URL = os.environ['WEBHOOK_PROD']
USER_NAME= 'Chloe'
AVATAR_URL = os.environ['AVATAR_URL']
# どの記事から対象にするか
START_N = int(args[2])
# どの記事まで対象にするか
# args[2]: 記事数
END_N = int(args[3]) + START_N
CONTENT_SIZE = 8000

def generate_embed(article, summary) -> dict:
  base_url = 'https://zenn.dev'
  article_url = '{}{}'.format(base_url, article['path'])
  embed = {'title': article['title'],
            'description': summary,
            'url': article_url,
            'author':{
              'name': article['user']['username'],
              'icon_url': article['user']['avatar_small_url'],
              },
            'footer': {
              'text': article['published_at'],
              'icon_url': ''
              },
            'color': 0x00bfff,
            'fields': [
              {
                'name': ":heart:",
                'value': article['liked_count'],
                'inline': True
                },
            ]
  }
  return embed

if __name__ == "__main__":
  

  zenn_articles = zenn_article()

  embeds = []
  for i in range(START_N-1, END_N-1):
    article = zenn_articles.get_info(i)
    print(article)
    content = zenn_articles.get_content(article['path'])

    gpt_sum = gpt_summary(model_name='gpt-3.5-turbo-16k')
    summary = gpt_sum.summary(content[:CONTENT_SIZE])
    embeds.append(generate_embed(article, summary))


  data = {
      'username': USER_NAME,
      'avatar_url': AVATAR_URL,
      'content': 'Zennの本日のトレンドです！',
      'embeds': embeds,
      }


  # POST
  try:
      requests.post(WEBHOOK_URL, json=data)
  except requests.exceptions.RequestException as e:
      print(e)
      
  print(START_N)
  print(END_N)