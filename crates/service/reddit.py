import json
import os
import sys

import requests
import requests.auth

ENV_VARS = ["CLIENT_ID", "CLIENT_SECRET", "USERNAME", "PASSWORD"]
API_BASE = "oauth.reddit.com"
WWW_BASE = "www.reddit.com"
USER_AGENT = "Cargo-Crates v0.0.1"


def get(url, access_token, params={}):
    return requests.get(
        url,
        params=params,
        headers={"User-Agent": USER_AGENT, "Authorization": f"bearer {access_token}"},
    )


def get_access_token() -> str:
    client_auth = requests.auth.HTTPBasicAuth(
        os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")
    )
    post_data = {
        "grant_type": "password",
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
    )
    return response.json().get("access_token")


def saved(username: str, start_date: str = None):
    """
    Returns the most recent saved posts of the provided user.
    """

    access_token = get_access_token()
    params = {"limit": 100}
    url = f"https://{API_BASE}/user/{username}/saved"
    r = get(url, access_token, params)
    return r.json().get("data", {}).get("children", [])


SUPPORTED_CMDS = ["saved"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERR: Expected 2 arguments")
        exit(1)

    cmd = sys.argv[1]
    username = sys.argv[2]

    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    start_date = None
    if os.getenv("start"):
        start_date = os.getenv("start")
    result = saved(username)

    for r in result:
        print(json.dumps(r))