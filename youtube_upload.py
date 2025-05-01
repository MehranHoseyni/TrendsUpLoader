# youtube_upload.py
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def upload_video_file(file_path, title, description='', tags=None, category_id='22'):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    body = {
        'snippet': {'title': title, 'description': description, 'tags': tags or [], 'categoryId': category_id},
        'status': {'privacyStatus': 'public'}
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
    return resp.get('id')
