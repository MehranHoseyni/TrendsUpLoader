# download_video.py
import os
import yt_dlp

def download_video(query: str) -> str:
    """
    دانلود اولین نتیجه جستجوی YouTube با استفاده از yt-dlp و فایل کوکی.
    query: فرمت "ytsearch:KEYWORD"
    بازگشت مسیر فایل دانلودشده.
    """
    DOWNLOAD_DIR = 'downloads'
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # مسیر فایل cookies که در workflow می‌سازیم
    cookie_path = os.getenv('COOKIE_FILE', 'cookies.txt')

    ydl_opts = {
        'format': 'best[height<=480]',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title).70s.%(ext)s',
        'default_search': 'ytsearch',
        'cookiefile': cookie_path,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        return ydl.prepare_filename(info)
