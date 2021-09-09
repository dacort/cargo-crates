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


def show_bearer_token():
    """
    Simply generates and returns a bearer token with the provided credentials.
    """
    access_token = get_access_token()
    return f"{access_token}"


def saved(username: str, start_date: str = None):
    """
    Returns the most recent saved posts of the provided user.
    """

    access_token = get_access_token()
    params = {"limit": 100}
    url = f"https://{API_BASE}/user/{username}/saved"
    r = get(url, access_token, params)
    return r.json().get("data", {}).get("children", [])


def search(keyword: str, subreddit_path: str = None):
    access_token = get_access_token()
    params = {"type": "link", "sort": "new", "limit": 100, "q": keyword}
    url = f"https://{API_BASE}/search.json"
    if subreddit_path is not None:
        params["restrict_sr"] = "true"
        url = f"https://{API_BASE}/{subreddit_path}/search.json"

    r = get(url, access_token, params)
    print(url, params)
    return r.json().get("data", {}).get("children", [])


SUPPORTED_CMDS = ["saved", "search", "show_bearer_token"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERR: Expected 2 arguments")
        exit(1)

    cmd = sys.argv[1]

    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "saved":
        username = sys.argv[2]
        start_date = None
        if os.getenv("start"):
            start_date = os.getenv("start")
        result = saved(username)

    if cmd == "search":
        # We (optionally) take the subreddit as the first argument because the search term can be arbitrarily long
        search_term = " ".join(sys.argv[2:])
        subreddit = None
        if sys.argv[2].startswith("r/"):
            subreddit = sys.argv[2]
            search_term = " ".join(sys.argv[3:])
        result = search(search_term, subreddit)

    if cmd == "show_bearer_token":
        result = [show_bearer_token()]

    for r in result:
        try:
            print(json.dumps(r))
        except BrokenPipeError:
            # We both catch the error *and* close stderr (stdout is already closed)
            # Reference: https://stackoverflow.com/a/26738736
            sys.stderr.close()
            exit(0)