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

    response = requests.get(
        url,
        params=params,
        headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"},
        cookies=cookies,
    )

    if response.status_code != 200 or response.json().get("ok") is False:
        raise RuntimeError(f"Error from API({response.status_code}): {response.json()}")

    return response


def __lookup_channel_id(channel_name_or_id: str) -> str:
    """Looks up the channel ID based on the name.

    If the passed channel_name_or_id starts with CID, the user already provided the exact channel ID.

    Args:
        channel_name_or_id (str): The channel name or an ID that starts with CID

    Returns:
        str: The channel ID
    """
    # If the passed channel name is CID-XXX, the user provided us with a channel ID.
    # Use that instead of trying to find the channel using channels.list
    chan_id: str | None = None
    if channel_name_or_id.startswith("CID-"):
        chan_id = channel_name_or_id.split("-")[1]
    else:
        for chan in channels(include_private=True):
            if chan["name"].lower() == channel_name_or_id.lower():
                chan_id = chan["id"]
                break

    if not chan_id:
        raise RuntimeError(f"Could not find channel '{channel_name_or_id}'")

    return chan_id


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


def channel_members(channel_name: str):
    """Looks up the members that belong to the given channel.

    Args:
        channel_name (str): The name of the channel
    """
    chan_id = __lookup_channel_id(channel_name)

    params = {"channel": chan_id}
    while True:
        r = get(endpoint("conversations.members"), params)
        data = r.json()
        for userid in data.get("members", []):
            yield __user_lookup(userid)
        # Next cursor is by default an empty string, but in case it's not use that as the default.
        cursor = data.get("response_metadata", {}).get("next_cursor")
        if cursor:
            params["cursor"] = cursor
        else:
            break


def __user_lookup(user_id: str):
    """Look up user info

    Args:
        user_id (str): The user's slack ID
    """
    params = {"user": user_id}
    r = get(endpoint("users.info"), params)
    if r.status_code != 200:
        raise RuntimeError(f"Error from API({r.status_code}): {r.json()}")
    return r.json().get('user')


def channels(include_private=False):
    """
    Returns the channel listing for the org associated with the provided token.
    Documentation: https://api.slack.com/methods/conversations.list
    """
    params = {"exclude_archived": "true"}
    if include_private:
        # This /kind of/ works if I set params['team_id'] - could be hitting rate limits?
        params["types"] = "public_channel,private_channel"

    params["team_id"] = team_id

    while True:
        r = get(endpoint("conversations.list"), params)
        if r.status_code != 200:
            raise RuntimeError(f"Error from API({r.status_code}): {r.json()}")
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
    chan_id = __lookup_channel_id(channel_name)

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


SUPPORTED_CMDS = ["search", "channels", "history", "channel_members"]

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
        show_private = False
        if len(sys.argv) > 2:
            show_private = True
        result = channels(show_private)

    if cmd == "history":
        channel_name = sys.argv[2]
        timeframe = 1
        if len(sys.argv) > 3:
            timeframe = int(sys.argv[3])
        result = history(channel_name, timeframe)
    
    if cmd == "channel_members":
        channel_name = sys.argv[2]
        result = channel_members(channel_name)

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
