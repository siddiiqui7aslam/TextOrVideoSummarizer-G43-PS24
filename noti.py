from datetime import datetime, timedelta
import requests
import googleapiclient.discovery

# Replace with your FCM server key
FCM_SERVER_KEY = "AIzaSyAtZw82wLJBShSjjsh2fEDJ"
FCM_TOPIC = "new_videos"

def send_push_notification(title, body):
    FCM_URL = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={FCM_SERVER_KEY}",
    }
    payload = {
        "to": f"/topics/{FCM_TOPIC}",
        "notification": {
            "title": title,
            "body": body,
        },
    }
    response = requests.post(FCM_URL, headers=headers, json=payload)
    return response.json()

def get_new_videos(api_key, channel_id, last_checked):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    last_checked_rfc3339 = last_checked.isoformat("T") + "Z"
    
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=last_checked_rfc3339,
        type="video",
        order="date"
    )
    
    response = request.execute()
    return response

def notify_server(video_title):
    send_push_notification('New Video Alert', video_title)

def main():
    api_key = "AIzaSyDQvZJn_guoayk3rjkWleve9FXG71eI4I8"
    channel_id = "UCyqOskZj-THQ5mAl3zEfJAA"
    last_checked = datetime.utcnow() - timedelta(days=7)
    response = get_new_videos(api_key, channel_id, last_checked)
    
    new_videos = response.get('items', [])
    if not new_videos:
        print("No new videos found.")
    for video in new_videos:
        video_title = video['snippet']['title']
        print(f"New video detected: {video_title}")
        notify_server(video_title)

if __name__ == "__main__":
    main()
