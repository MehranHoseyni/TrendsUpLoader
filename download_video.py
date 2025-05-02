# download_video.py
import os
import yt_dlp

def download_video(query: str) -> str:
    """
    دانلود اولین نتیجه جستجوی YouTube با استفاده از yt-dlp.
    query: فرمت "ytsearch:KEYWORD"
    بازگشت مسیر فایل دانلودشده یا URL مستقیم.
    """
    DOWNLOAD_DIR = 'downloads'
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # دریافت کوکی‌ها از سکرت
    cookies = os.environ.get('COOKIES_TXT')
    
    if not cookies:
        raise ValueError("Cookies are not set in the environment variables.")

    ydl_opts = {
        'format': 'best[height<=480]',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'default_search': 'ytsearch',
        'quiet': True,
        'cookies': cookies,  # استفاده از کوکی‌های ذخیره شده
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        return ydl.prepare_filename(info)
