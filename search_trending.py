# search_trending.py
"""
استخراج کلیدواژه‌های ترند از Google Trends و YouTube به صورت جهانی.
"""

import json
import os
from googleapiclient.discovery import build
from pytrends.request import TrendReq

# Constants
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
MAX_KEYWORDS = 10
CACHE_FILE = 'trends.json'

# Initialize PyTrends (زبان و منطقه به صورت عمومی/انگلیسی)
pytrends = TrendReq(hl='en-US', tz=360)

def get_google_trends(top_n=MAX_KEYWORDS):
    """
    دریافت ترندهای جهانی از Google Trends
    """
    try:
        pytrends.build_payload(kw_list=["world"], cat=0, timeframe='now 1-d')
        trending_searches = pytrends.trending_searches()
        return trending_searches[0:top_n].tolist()
    except Exception as e:
        print(f"[Google Trends Error] {e}")
        return []

def get_youtube_trending(top_n=MAX_KEYWORDS):
    """
    دریافت ویدیوهای ترند یوتیوب به صورت جهانی
    """
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        req = youtube.videos().list(
            part='snippet',
            chart='mostPopular',
            maxResults=top_n
        )
        res = req.execute()
        return [item['snippet']['title'] for item in res.get('items', [])]
    except Exception as e:
        print(f"[YouTube API Error] {e}")
        return []

def get_trending_keywords():
    """
    ترکیب نتایج Google Trends و YouTube Trending و ذخیره در کش
    """
    # Load from cache if available
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    # Fetch new trends
    google = get_google_trends()
    youtube = get_youtube_trending()

    # Combine and prioritize common keywords
    common = [kw for kw in google if kw in youtube]
    if len(common) < MAX_KEYWORDS:
        combined = list(dict.fromkeys(common + google + youtube))
    else:
        combined = common

    keywords = combined[:MAX_KEYWORDS]

    # Save to cache
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(keywords, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Cache Write Error] {e}")

    return keywords

# For direct execution
if __name__ == "__main__":
    result = get_trending_keywords()
    print("Top Keywords:", result)
