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


SUPPORTED_CMDS = ["search", "channels"]

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
