from logging import exception
import os
import googleapiclient.discovery
from sql_app.schemas import Video
from decouple import config


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

DEVELOPER_KEYS = config("DEVELOPER_KEYS")
AVAILABLE_KEYS = DEVELOPER_KEYS.split(",")
USED_KEYS = []


def get_yt(developer_key):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key
    )
    return youtube


def get_keys():

    global AVAILABLE_KEYS
    global USED_KEYS

    if len(AVAILABLE_KEYS) == 0:
        AVAILABLE_KEYS = USED_KEYS
        USED_KEYS = []

    key = AVAILABLE_KEYS[0]
    return key


def get_videos():

    global AVAILABLE_KEYS
    global USED_KEYS

    key = get_keys()

    try:
        youtube = get_yt(key)
        request = youtube.search().list(
            part="snippet",
            q="coding",
            type="video",
            publishedAfter="2019-01-01T00:00:00Z",
        )
        response = request.execute()
        return request, response

    except Exception as e:
        del AVAILABLE_KEYS[0]
        USED_KEYS.append(key)



def next_response(request, response):
    key = get_keys()
    youtube = get_yt(key)
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
