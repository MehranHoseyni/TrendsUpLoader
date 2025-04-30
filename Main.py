import os
import json
import yt_dlp
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# ====== Config ======
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PEXELS_API_KEY  = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
TREND_KEYWORD   = "ایران"
MAX_TRENDS      = 5
MAX_VIDEOS_PER_TREND = 3
DOWNLOAD_SIZE_LIMIT = 30_000_000  # 30MB

# ====== Helper Functions ======

def get_google_trends_keywords(limit=MAX_TRENDS):
    # نمونه ثابت تا بعداً با API‌ واقعی جایگزین شود
    return ["ایران"]  

def search_pexels_videos(query, per_page=MAX_VIDEOS_PER_TREND):
    headers = {"Authorization": PEXELS_API_KEY}
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={"query": query, "per_page": per_page}
    )
    data = resp.json().get("videos", [])
    return [v["video_files"][0]["link"] for v in data]

def search_pixabay_videos(query, per_page=MAX_VIDEOS_PER_TREND):
    resp = requests.get(
        "https://pixabay.com/api/videos/",
        params={"key": PIXABAY_API_KEY, "q": query, "per_page": per_page}
    )
    data = resp.json().get("hits", [])
    return [v["videos"]["medium"]["url"] for v in data]

def choose_video(videos):
    # Adaptive quality: اولین ویدیو زیر حد حجم را انتخاب کن
    for url in videos:
        info = yt_dlp.YoutubeDL({'quiet': True}).extract_info(url, download=False)
        size = info.get("filesize") or info.get("filesize_approx", 0)
        if size <= DOWNLOAD_SIZE_LIMIT:
            return url
    # اگر هیچ‌کدام زیر حد نبود، اولین گزینه را برگردان
    return videos[0]

def upload_stream(video_url):
    # استریم دانلود و آپلود مستقیم به یوتیوب
    ydl_opts = {'format': 'best', 'quiet': True, 'outtmpl': '-'}
    buffer = io.BytesIO()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        buffer.seek(0)
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    body = {
        "snippet": {
            "title": f"Trending: {TREND_KEYWORD}",
            "description": video_url
        },
        "status": {"privacyStatus": "public"}
    }
    media = MediaIoBaseUpload(buffer, mimetype="video/mp4", resumable=True)
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
    return resp.get("id")

def main():
    # ۱. دریافت ترندها
    trends = get_google_trends_keywords()
    selected_videos = []

    # ۲. جستجو و انتخاب ویدیو برای هر ترند
    for term in trends:
        vids = []
        vids.extend(search_pexels_videos(term))
        vids.extend(search_pixabay_videos(term))
        pick = choose_video(vids)
        selected_videos.append(pick)

    # ۳. لاگ ویدیوهای انتخاب‌شده
    with open("output.txt", "w", encoding="utf-8") as f:
        json.dump(selected_videos, f, ensure_ascii=False, indent=2)
    print("Videos selected:", selected_videos)

    # ۴. آپلود هر ویدیو
    for url in selected_videos:
        vid_id = upload_stream(url)
        print("Uploaded video ID:", vid_id)

if __name__ == "__main__":
    main()
