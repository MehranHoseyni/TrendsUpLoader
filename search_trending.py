# search_trending.py
"""
استخراج کلیدواژه‌های ترند مرتبط با ایران از منابع مختلف.
"""
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup

# تابع PyTrends برای Google Trends
pytrends = TrendReq(hl='fa', tz=180)

def get_google_trends(top_n=10):
    pytrends.build_payload(['ایران'], cat=0, timeframe='now 1-d', geo='IR')
    data = pytrends.related_topics()['ایران']['top']
    return data['topic_title'].tolist()[:top_n]

# YouTube Trending
from googleapiclient.discovery import build
YOUTUBE_API_KEY = None

def get_youtube_trending(top_n=10):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    req = youtube.videos().list(part='snippet', chart='mostPopular', regionCode='IR', maxResults=top_n)
    res = req.execute()
    return [item['snippet']['title'] for item in res.get('items', [])]

# توابع ترکیبی
def get_trending_keywords():
    # بارگذاری کش
    try:
        import json
        with open('trends.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        g = get_google_trends(10)
        y = get_youtube_trending(10)
        # ترکیب و اولویت مشترک‌ها
        common = list(set(g) & set(y))
        if not common:
            common = g + y
        # ذخیره کش
        with open('trends.json', 'w', encoding='utf-8') as f:
            json.dump(common, f, ensure_ascii=False, indent=2)
        return common
