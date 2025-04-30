# youtube_upload.py

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def upload_video_file(file_path, title, description="", tags=None, category_id="22"):
    """
    Upload a local video file to YouTube.
    Returns the uploaded video ID.
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {"privacyStatus": "public"}
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
    return response.get("id")

if __name__ == "__main__":
    # تست سریع
    vid_id = upload_video_file("downloads/example.mp4", "Test Upload", "Description here", ["ایران", "ترند"])
    print("Uploaded video ID:", vid_id)
