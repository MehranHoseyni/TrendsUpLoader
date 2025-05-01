# main.py

import os
import json
import datetime
from search_trending import get_trending_keywords
from download_video import download_video
from youtube_upload import upload_video_file

# Config
MAX_TRENDS = 5
MAX_VIDEOS_PER_TREND = 3
LOG_FILE = "output.txt"

def generate_title(trend: str) -> str:
    """Generate a catchy Persian title based on the trend keyword."""
    return f"ویدیوی داغ دربارهٔ «{trend}»"

def generate_description(trend: str, source_url: str) -> str:
    """Generate a short Persian description for the video."""
    return (
        f"این ویدیو دربارهٔ موضوع ترند «{trend}» است. "
        f"منبع اصلی: {source_url}\n\n"
        "برای ویدیوهای بیشتر کانال را سابسکرایب کنید!"
    )

def process_trend(trend: str, log: dict) -> None:
    """
    For a single trend:
      - search and download a video
      - upload it to YouTube
      - record results in log
    """
    log_entry = {"trend": trend, "status": None}
    try:
        # 1. Download best video (or get direct URL)
        video_path = download_video(trend)  # returns local file path or URL
        if not video_path:
            raise RuntimeError("No video found for this trend")
        log_entry["video"] = video_path

        # 2. Build metadata
        title = generate_title(trend)
        description = generate_description(trend, video_path)
        log_entry["title"] = title

        # 3. Upload
        video_id = upload_video_file(
            file_path=video_path,
            title=title,
            description=description,
            tags=[trend]
        )
        log_entry["youtube_id"] = video_id
        log_entry["status"] = "uploaded"

    except Exception as e:
        log_entry["status"] = "failed"
        log_entry["error"] = str(e)

    finally:
        log.setdefault("runs", []).append(log_entry)

def main():
    now = datetime.datetime.now().isoformat()
    overall_log = {"started_at": now, "runs": []}

    # 1. Get trending keywords
    trends = get_trending_keywords()[:MAX_TRENDS]
    if not trends:
        overall_log["error"] = "No trends found"
    else:
        for trend in trends:
            process_trend(trend, overall_log)

    # 2. Save log to file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(overall_log, f, ensure_ascii=False, indent=2)
    print(f"Done. Log saved to {LOG_FILE}")

if __name__ == "__main__":
    main()
