import json
import os
import sys

import requests

ENV_VARS = ["YOUTUBE_API_KEY"]
API_BASE = "youtube.googleapis.com/youtube/v3"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(url, params=params)


def videos(video_ids):
    """
    Retrieves basic info about the provided videos as well as statistics.
    Intended to retrieve data about _public_ videos.
    Google Docs: https://developers.google.com/youtube/v3/docs/videos/list
    """
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_ids,
        "key": os.getenv("YOUTUBE_API_KEY"),
    }

    r = get(endpoint("videos"), params)
    return r.json().get("items", [])


SUPPORTED_CMDS = ["videos"]

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

    for r in result:
        print(json.dumps(r))
