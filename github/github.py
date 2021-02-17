import os
import sys
import json
import logging

import requests

from s3 import get_output_stream

GITHUB_PAT = os.getenv("GITHUB_PAT")
API_BASE = "api.github.com"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url, params=params, headers={"Authorization": f"Bearer {GITHUB_PAT}"}
    )


def traffic(repo, traffic_path=None):
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
    for path in traffic_path:
        url = f"repos/{repo}/traffic/{path}"
        response = get(endpoint(url))
        # results[path] = response.json()
        results.append({"repo": repo, "path": path, "stats": response.json()})

    return results


SUPPORTED_CMDS = ["traffic"]

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)

    # Ensure a valid command is provided
    cmd = sys.argv[1]
    options = sys.argv[2:]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    # Then determine where to output our data
    outstream = get_output_stream(
        os.getenv("OUTPUT_TYPE"), json.loads(os.getenv("OUTPUT_PARAMS"))
    )

    if cmd == "traffic":
        repo = options[0]
        path = None
        if len(options) > 1:
            path = options[1].split(",")
        result = traffic(repo, path)

    for r in result:
        outstream.add_record(r)
    outstream.close()
