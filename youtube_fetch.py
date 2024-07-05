import requests
import json
import time
import firebase_admin
from firebase_admin import credentials, messaging

API_KEY = 'AIzaSyDQvZJn_guoayk3rjkWleve9FXG71eI4I8'
CHANNEL_ID = 'UCyqOskZj-THQ5mAl3zEfJAA'
FCM_CREDENTIALS = r"C:\Users\siddi\OneDrive\Desktop\flutter\firebase\firebase-adminsdk.json.json"

# Initialize the Firebase app
cred = credentials.Certificate(FCM_CREDENTIALS)
firebase_admin.initialize_app(cred)

def get_latest_video(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            latest_video = data['items'][0]
            video_id = latest_video['id']['videoId']
            title = latest_video['snippet']['title']
            description = latest_video['snippet']['description']
            return {
                'video_id': video_id,
                'title': title,
                'description': description
            }
    return None

def send_notification(video_id, title):
    message = messaging.Message(
        notification=messaging.Notification(
            title='New YouTube Video Uploaded!',
            body=title,
        ),
        topic='youtube_updates',
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)

def main():
    last_video_id = None
    while True:
        latest_video = get_latest_video(API_KEY, CHANNEL_ID)
        if latest_video:
            video_id = latest_video['video_id']
            if video_id != last_video_id:
                send_notification(video_id, latest_video['title'])
                last_video_id = video_id
        time.sleep(600)  # Check every 10 minutes

if __name__ == "__main__":
    main()
