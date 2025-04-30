# download_video.py

import os
import yt_dlp

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(video_url):
    """
    Download the given YouTube video URL into the downloads/ folder
    using adaptive quality (<=480p if size > 30MB).
    Returns the local file path.
    """
    # مرحله‌ی انتخاب کیفیت تطبیقی
    ydl = yt_dlp.YoutubeDL({'quiet': True, 'format': 'best[height<=480]'})
    info = ydl.extract_info(video_url, download=False)
    filesize = info.get("filesize") or info.get("filesize_approx", 0)

    if filesize <= 30_000_000:
        fmt = "best"
    else:
        fmt = "best[height<=480]"

    ydl_opts = {
        'format': fmt,
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
        result = ydl2.download([video_url])
        # yt_dlp دانلود را برمی‌گرداند، مسیر فایل در outtmpl ذخیره شده
        return ydl2.prepare_filename(info)

if __name__ == "__main__":
    # تست سریع
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    path = download_video(test_url)
    print("Downloaded to:", path)
