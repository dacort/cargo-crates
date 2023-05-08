import datetime as dt
import time
import json
import os
import sys

import requests

ENV_VARS = ["SLACK_TOKEN", "SLACK_COOKIE_TOKEN", "SLACK_DS_COOKIE"]
API_BASE = "slack.com/api"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    cookies = {}
    if os.getenv("SLACK_TOKEN").startswith("xoxc"):
        cookies["d"] = os.getenv("SLACK_COOKIE_TOKEN")

    if os.getenv("SLACK_DS_COOKIE"):
        cookies["d-s"] = os.getenv("SLACK_DS_COOKIE")

    return requests.get(
        url,
        params=params,
        headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"},
        cookies=cookies,
    )


def team_info():
    """
    Returns the result of the team.info lookup.
    """
    r = get(endpoint("team.info"))
    return r.json().get("team")


def search(query):
    """
    Searches the Slack channel associated with the provided token.
    Documentation: https://api.slack.com/methods/search.messages
    """
    params = {"query": query, "sort": "timestamp"}

    r = get(endpoint("search.messages"), params)
    return r.json().get("messages").get("matches", [])


def channels():
    """
    Returns the channel listing for the org associated with the provided token.
    Documentation: https://api.slack.com/methods/conversations.list
    """
    params = {"exclude_archived": "true"}

    while True:
        r = get(endpoint("conversations.list"), params)
        data = r.json()
        for chan in data.get("channels", []):
            yield chan
        # Next cursor is by default an empty string, but in case it's not use that as the default.
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if cursor > "":
            params["cursor"] = cursor
        else:
            break


def history(channel_name, days=7, include_threads=True):
    """
    Returns a list of messages for a specific channel in the given timeframe (now-timeframe).
    Optionally includes thread messages by default.
    """
    chan_id = None
    for chan in channels():
        if chan["name"].lower() == channel_name.lower():
            chan_id = chan["id"]
            break

    if not chan_id:
        raise RuntimeError(f"Could not find channel '{channel_name}'")

    oldest = dt.datetime.utcnow() - dt.timedelta(days=days)
    params = {"channel": chan_id, "oldest": time.mktime(oldest.timetuple())}
    while True:
        r = get(endpoint("conversations.history"), params)
        data = r.json()
        for message in data.get("messages", []):
            yield message
        # Next cursor is by default an empty string, but in case it's not use that as the default.
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if cursor > "":
            params["cursor"] = cursor
        else:
            break


SUPPORTED_CMDS = ["search", "channels", "history"]

if __name__ == "__main__":
    cmd = "search"
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    team_info = team_info()
    team_name = team_info.get("name")
    team_id = team_info.get("id")
    team_domain = team_info.get("domain")

    if cmd == "search":
        query = sys.argv[2:]
        result = search(query)

    if cmd == "channels":
        result = channels()

    if cmd == "history":
        channel_name = sys.argv[2]
        timeframe = 1
        if len(sys.argv) > 3:
            timeframe = int(sys.argv[3])
        result = history(channel_name, timeframe)

    for r in result:
        r["team_name"] = team_name
        r["team_id"] = team_id
        r["team_domain"] = team_domain
        try:
            print(json.dumps(r))
        except BrokenPipeError:
            # We both catch the error *and* close stderr (stdout is already closed)
            # Reference: https://stackoverflow.com/a/26738736
            sys.stderr.close()
            exit(0)
