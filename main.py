import datetime
import os
from search_trending import get_trending_keywords
from download_video import download_video
from youtube_upload import upload_video_file
from utils import save_json

LOG_FILE = 'output.txt'
MAX_TRENDS = 5


def generate_title(trend):
    return f'ویدیوی داغ دربارهٔ «{trend}»'


def generate_description(trend, url):
    return f'این ویدیو دربارهٔ موضوع ترند «{trend}» است. منبع: {url}\nبرای ویدیوهای بیشتر سابسکرایب کنید.'


def process_trend(trend, log):
    entry = {'trend': trend, 'status': None}
    path = None  # مقدار اولیه برای جلوگیری از خطا

    # دانلود ویدیو
    try:
        query = f'ytsearch:{trend}'
        path = download_video(query)
        entry['video_path'] = path
    except Exception as e:
        print(f"Error downloading video for trend '{trend}': {e}")
        entry.update({'status': 'failed', 'error': f"Download error: {str(e)}"})

    # فقط اگر دانلود موفق بود، آپلود انجام میشه
    if path:
        try:
            title = generate_title(trend)
            desc = generate_description(trend, path)
            vid_id = upload_video_file(path, title, desc, [trend])
            entry.update({'youtube_id': vid_id, 'status': 'uploaded'})
        except Exception as e:
            print(f"Error uploading video for trend '{trend}': {e}")
            entry.update({'status': 'failed', 'error': f"Upload error: {str(e)}"})

    log.setdefault('runs', []).append(entry)


def main():
    start = datetime.datetime.now().isoformat()
    overall = {'started_at': start, 'runs': []}

    trends = get_trending_keywords()
    print("Trends fetched:", trends)
    save_json('trends.json', trends)

    if trends:
        for t in trends[:MAX_TRENDS]:
            process_trend(t, overall)
    else:
        overall['error'] = 'No trends found'

    save_json(LOG_FILE, overall)
    print('Finished. Log saved.')


if __name__ == '__main__':
    main()
