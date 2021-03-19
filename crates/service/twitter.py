import os
import sys
import json

from TwitterAPI import TwitterAPI


ENV_VARS = [
    "CONSUMER_KEY",
    "CONSUMER_SECRET",
    "ACCESS_TOKEN_KEY",
    "ACCESS_TOKEN_SECRET",
]


def client_v2():
    return TwitterAPI(
        os.getenv("CONSUMER_KEY"),
        os.getenv("CONSUMER_SECRET"),
        os.getenv("ACCESS_TOKEN_KEY"),
        os.getenv("ACCESS_TOKEN_SECRET"),
        api_version="2",
    )


def user_info_by_username(username):
    r = client_v2().request(f"users/by/username/:{username}")
    return r.json().get("data")


# Should probably make this a generator function, I like that pattern better for what we're doing
def followers_by_userid(userid):
    followers = []
    params = {
        "user.fields": "created_at,description,public_metrics",
        "max_results": "1000",
    }
    while True:
        response = client_v2().request(f"users/:{userid}/followers", params)
        data = response.json()
        followers.extend(data.get("data", []))
        if "meta" in data and "next_token" in data.get("meta", {}):
            params["pagination_token"] = data.get("meta").get("next_token")
        else:
            break

    return followers


SUPPORTED_CMDS = ["followers", "users/show"]

if __name__ == "__main__":
    cmd = sys.argv[1]
    options = sys.argv[2:]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "users/show":
        username = options[0]
        result = user_info_by_username(username)
        print(json.dumps(result))

    if cmd == "followers":
        username = options[0]
        user_info = user_info_by_username(username)
        followers = followers_by_userid(user_info.get("id"))
        for follower in followers:
            print(json.dumps(follower))