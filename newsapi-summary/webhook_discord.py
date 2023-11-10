import os
import sys
import pandas as pd
import requests
from dotenv import load_dotenv
from news import news_articles

args = sys.argv


load_dotenv()
if args[1]=='dev':
    WEBHOOK_URL = os.environ['WEBHOOK_DEV']
elif args[1] == 'prod':
    WEBHOOK_URL = os.environ['WEBHOOK_PROD']
N = int(args[2])
USER_NAME= 'Chloe'
AVATAR_URL = os.environ['AVATAR_URL']

def generate_embed(df) -> list:
    embeds = []
    for index, row in df.iterrows():
        embed = {'title': row['title'],
                'description': row['description'],
                'url': row['url'],
                'author':{
                    'name': row['source']['name'],
                    },
                'image':{
                    'url': row['urlToImage'],
                },
                'footer': {
                    'text': 'Posted date: {}'.format(row['publishedAt']),
                    'icon_url': ''
                    },
                'color': 0xFF55AA,
            }
        embeds.append(embed)

    return embeds

if __name__ == "__main__":
    news = news_articles()
    news_df = news.get_articles()
    
    embeds = generate_embed(news_df.head(N))
        
    data = {
        'username': USER_NAME,
        'avatar_url': AVATAR_URL,
        'content': '本日のニュースです！',
        'embeds': embeds,
    }

    # POST
    try:
        print(WEBHOOK_URL)
        requests.post(WEBHOOK_URL, json=data)
    except requests.exceptions.RequestException as e:
        print(e)
        
