# youtube_upload.py
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os

def upload_video_file(file_path: str, title: str, description: str, tags: list):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # دریافت یوزر تاژن از سکرت
    api_key = os.environ.get('YOUTUBE_API_KEY')

    if not api_key:
        raise ValueError("YouTube API key is not set in the environment variables.")

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
        },
        'status': {
            'privacyStatus': 'public',  # می‌توانید وضعیت حریم خصوصی را تغییر دهید
        }
    }

    # آپلود ویدیو
    media_file = MediaFileUpload(file_path, mimetype='video/mp4', resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)
    
    response = request.execute()

    return response['id']
