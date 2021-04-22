import json
import os
import sys

import requests

ENV_VARS = ["YOUTUBE_API_KEY"]
API_BASE = "youtube.googleapis.com/youtube/v3"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    params.update({"key": os.getenv("YOUTUBE_API_KEY")})
    return requests.get(url, params=params)


def _get_upload_playlist_id(channel_id):
    params = {
        "part": "contentDetails",
        "id": channel_id,
    }
    r = get(endpoint("channels"), params)
    return (
        r.json()
        .get("items")[0]
        .get("contentDetails")
        .get("relatedPlaylists")
        .get("uploads")
    )


def _get_playlist_video_ids(playlist_id):
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50
    }
    # TODO: Pagination
    r = get(endpoint("playlistItems"), params)
    video_ids = []

    for item in r.json().get("items", []):
        video_ids.append(item.get("snippet").get("resourceId").get("videoId"))

    return video_ids


def channel_videos(channel_id):
    """
    Retrieves all videos from a specific channel.
    This requires us to:
        - get the "upload" playlist
        - get a list of the videos in that playlist
        - fetch the stats for each video
    """
    upload_id = _get_upload_playlist_id(channel_id)
    video_ids = _get_playlist_video_ids(upload_id)
    return videos(video_ids)


def videos(video_ids):
    """
    Retrieves basic info about the provided videos as well as statistics.
    Intended to retrieve data about _public_ videos.
    Google Docs: https://developers.google.com/youtube/v3/docs/videos/list

    Up to 50 video ids can be provided at once
    """
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_ids,
    }

    r = get(endpoint("videos"), params)
    return r.json().get("items", [])


SUPPORTED_CMDS = ["videos", "channel_videos"]

if __name__ == "__main__":
    # Ensure a valid command is provided
    cmd = sys.argv[1]
    options = sys.argv[2:]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "videos":
        video_ids = options[0].split(",")
        result = videos(video_ids)

    if cmd == "channel_videos":
        channel_id = options[0]
        result = channel_videos(channel_id)

    for r in result:
        print(json.dumps(r))
