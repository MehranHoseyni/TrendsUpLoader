# search_trending.py
"""
استخراج کلیدواژه‌های ترند مرتبط با ایران از منابع مختلف با مدیریت خطا.
"""
import json
import os
from googleapiclient.discovery import build
from pytrends.request import TrendReq

# Constants
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GOOGLE_TRENDS_GEO = 'IR'
MAX_KEYWORDS = 10
CACHE_FILE = 'trends.json'

# Initialize PyTrends
pytrends = TrendReq(hl='fa', tz=180)

def get_google_trends(top_n=MAX_KEYWORDS):
    """
    دریافت ترندهای مرتبط با ایران از Google Trends
    """
    try:
        pytrends.build_payload(['ایران'], cat=0, timeframe='now 1-d', geo=GOOGLE_TRENDS_GEO)
        related = pytrends.related_topics().get('ایران', {}).get('top', None)
        if related is not None:
            return related['topic_title'].tolist()[:top_n]
    except Exception:
        pass
    return []


def get_youtube_trending(top_n=MAX_KEYWORDS):
    """
    دریافت ویدیوهای ترند YouTube برای ایران
    """
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        req = youtube.videos().list(part='snippet', chart='mostPopular', regionCode='IR', maxResults=top_n)
        res = req.execute()
        return [item['snippet']['title'] for item in res.get('items', [])]
    except Exception:
        return []


def get_trending_keywords():
    """
    ترکیب نتایج Google Trends و YouTube Trending و کش کردن در فایل
    """
    # 1. Try loading cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    # 2. Fetch from sources
    google = get_google_trends()
    youtube = get_youtube_trending()

    # 3. Combine and prioritize common keywords
    common = [kw for kw in google if kw in youtube]
    if len(common) < MAX_KEYWORDS:
        combined = list(dict.fromkeys(common + google + youtube))
    else:
        combined = common

    # 4. Limit and cache
    keywords = combined[:MAX_KEYWORDS]
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(keywords, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return keywords
