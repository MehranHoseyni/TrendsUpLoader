# main.py
import datetime
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
    try:
        # دانلود
        query = f'ytsearch:{trend}'
        path = download_video(query)
        entry['video_path'] = path

        # آپلود
        title = generate_title(trend)
        desc = generate_description(trend, path)
        vid_id = upload_video_file(path, title, desc, [trend])
        entry.update({'youtube_id': vid_id, 'status': 'uploaded'})

    except Exception as e:
        entry.update({'status': 'failed', 'error': str(e)})

    log.setdefault('runs', []).append(entry)


def main():
    start = datetime.datetime.now().isoformat()
    overall = {'started_at': start, 'runs': []}

    trends = get_trending_keywords()[:MAX_TRENDS]
    save_json('trends.json', trends)

    if trends:
        for t in trends:
            process_trend(t, overall)
    else:
        overall['error'] = 'No trends found'

    save_json(LOG_FILE, overall)
    print('Finished. Log saved.')


if __name__ == '__main__':
    main()
