import json
import sys

import requests

ENV_VARS = []
API_BASE = "api.stackexchange.com/2.3"
SUPPORTED_CMDS = ["search", "channels"]

def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url,
        params=params,
    )


def search(tags):
    """
    Searches Stack Overflow questions for a set of tags
    https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&tagged=amazon-emr%3Bemr-serverless&site=stackoverflow
    """
    params = {"order": "desc", "sort": "creation", "tagged": tags, "site": "stackoverflow"}

    r = get(endpoint("questions"), params)
    return r.json().get("items", [])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "search":
        query = sys.argv[2:]
        result = search(query)

    for r in result:
        try:
            print(json.dumps(r))
        except BrokenPipeError:
            # We both catch the error *and* close stderr (stdout is already closed)
            # Reference: https://stackoverflow.com/a/26738736
            sys.stderr.close()
            exit(0)
