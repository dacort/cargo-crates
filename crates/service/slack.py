import json
import os
import sys

import requests

ENV_VARS = ["SLACK_TOKEN"]
API_BASE = "slack.com/api"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url,
        params=params,
        headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"},
    )


def team_name():
    """
    Returns the team name of the authenticated user.
    """
    r = get(endpoint("team.info"))
    return r.json().get("team").get("name")


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

    channel_list = []

    while True:
        r = get(endpoint("conversations.list"), params)
        data = r.json()
        channel_list.extend(data.get("channels", []))
        # Next cursor is by default an empty string, but in case it's not use that as the default.
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if cursor > "":
            params["cursor"] = cursor
        else:
            break

    return channel_list


SUPPORTED_CMDS = ["search", "channels"]

if __name__ == "__main__":
    cmd = "search"
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    team_name = team_name()

    if cmd == "search":
        query = sys.argv[2:]
        result = search(query)

    if cmd == "channels":
        result = channels()

    for r in result:
        r["team_name"] = team_name
        print(json.dumps(r))