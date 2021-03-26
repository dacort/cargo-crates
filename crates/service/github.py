import os
import sys
import json
from datetime import datetime

import requests

ENV_VARS = ["GITHUB_PAT"]
API_BASE = "api.github.com"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url, params=params, headers={"Authorization": f"Bearer {os.getenv('GITHUB_PAT')}"}
    )

def releases(repo):
    """
    Retrieves release data for a specific {owner}/{repo}
    """
    url = f"repos/{repo}/releases"
    response = get(endpoint(url))

    return response.json()


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
            results.append({
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "utcisonow": datetime.utcnow().isoformat(),
                "repo": repo,
                "path": path,
                "stats": response.json()
            })

    return results


SUPPORTED_CMDS = ["traffic", "releases"]

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
        repo = options[0]
        result = releases(repo)

    for r in result:
        print(json.dumps(r))
