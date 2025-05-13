import json
import os
import sys
from datetime import datetime

import requests

ENV_VARS = ["GITHUB_PAT"]
API_BASE = "api.github.com"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}, headers={}):
    headers.update({"Authorization": f"Bearer {os.getenv('GITHUB_PAT')}"})
    return requests.get(url, params=params, headers=headers)


def search(type, query):
    """
    Searches GitHub for the specific query.
    Defaults to descending sort by date with no way to change it.
    """
    url = f"search/{type}"
    params = {
        "q": query,
        "sort": "created",
        "order": "desc",
        "per_page": 100,
    }
    response = get(
        endpoint(url), params, {"Accept": "application/vnd.github.v3.text-match+json"}
    )

    return response.json().get("items")


def releases(repos):
    """
    Retrieves release data for a specific {owner}/{repo}
    """

    results = []
    for repo in repos:
        url = f"repos/{repo}/releases"
        response = get(endpoint(url))
        for release in response.json():
            results.append(
                {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "utcisonow": datetime.utcnow().isoformat(),
                    "repo": repo,
                    "release_info": release,
                }
            )

    # print(results)
    return results


def traffic(repos, traffic_path=None):
    """
    Retrieves different traffic data from the specificed {owner}/{repo}
    Supports the following traffic paths:
        - clones
        - popular/paths
        - popular/referrers
        - views
    If no path is provided, we will fetch _ALL_ traffic and merge into a dictionary.
    If a single path is provided, we fetch that path and return it as a dictionary.
    """
    if traffic_path is None:
        traffic_path = ["clones", "popular/paths", "popular/referrers", "views"]
    elif type(traffic_path) is not list:
        traffic_path = [traffic_path]

    results = []
    for repo in repos:
        for path in traffic_path:
            url = f"repos/{repo}/traffic/{path}"
            response = get(endpoint(url))
            # results[path] = response.json()
            results.append(
                {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "utcisonow": datetime.utcnow().isoformat(),
                    "repo": repo,
                    "path": path,
                    "stats": response.json(),
                }
            )

    return results


SUPPORTED_CMDS = ["traffic", "releases", "search"]

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)

    # Ensure a valid command is provided
    cmd = sys.argv[1]
    options = sys.argv[2:]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "traffic":
        repo = options[0].split(",")
        path = None
        if len(options) > 1:
            path = options[1].split(",")
        result = traffic(repo, path)

    if cmd == "releases":
        repos = options[0].split(",")
        result = releases(repos)

    if cmd == "search":
        search_type = options[0]
        search_query = options[1]
        result = search(search_type, search_query)

    for r in result:
        try:
            print(json.dumps(r))
        except BrokenPipeError:
            # We both catch the error *and* close stderr (stdout is already closed)
            # Reference: https://stackoverflow.com/a/26738736
            sys.stderr.close()
            exit(0)
