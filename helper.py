from logging import exception
import os
import googleapiclient.discovery
from sql_app.schemas import Video
from decouple import config


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
# DEVELOPER_KEY = "AIzaSyDEfvOCF_LQRA7wV7870OuPCREzvqzB9BE"

DEVELOPER_KEY = config("DEVELOPER_KEY")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def get_videos():
    request = youtube.search().list(
        part="snippet",
        q="coding",
        type="video",
        publishedAfter="2019-01-01T00:00:00Z",
    )
    response = request.execute()
    return request, response


def next_response(request, response):
    next_response = youtube.search().list_next(request, response)
    return next_response.execute()


def process_response(obj):

    video_obj = Video
    video_obj.title = obj["snippet"]["title"]
    video_obj.description = obj["snippet"]["description"]
    video_obj.published_at = obj["snippet"]["publishedAt"]
    video_obj.default_thumbnail = obj["snippet"]["thumbnails"]["default"]["url"]
    video_obj.medium_thumbnail = obj["snippet"]["thumbnails"]["medium"]["url"]
    video_obj.high_thumbnail = obj["snippet"]["thumbnails"]["high"]["url"]
    return video_obj
