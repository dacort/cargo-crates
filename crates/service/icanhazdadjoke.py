import json
import sys
import requests

ENV_VARS = []
API_BASE = "icanhazdadjoke.com"


def endpoint(path: str=""):
    return f"https://{API_BASE}/{path}"


def get(url, params={}) -> requests.Response:
    return requests.get(url, params=params, headers={"Accept": "application/json"})


def dad_joke():
    r = get(endpoint())
    # We manually parse the utf-8 decoded content because it's includes unicode control characters
    return [json.loads(r.content.decode('utf-8'))]

def search(query: str=None):
    params = {}
    if query:
        params = {"term": query}
    r = get(endpoint("search"), params)

    return json.loads(r.content.decode('utf-8'))['results']

SUPPORTED_CMDS = ['search']

if __name__ == "__main__":
    # By default, we print a single dad joke
    if len(sys.argv) == 1:
        result = dad_joke()
    else:
        cmd = sys.argv[1]
        if cmd not in SUPPORTED_CMDS:
            print(f"ERR: '{cmd}' is not a supported commmand.")
            exit(1)
        options = None
        if len(sys.argv) > 2:
            options = sys.argv[2:]
        # search is only supported command today
        result = search(options)

    for r in result:
        try:
            print(json.dumps(r))
        except BrokenPipeError:
            # We both catch the error *and* close stderr (stdout is already closed)
            # Reference: https://stackoverflow.com/a/26738736
            sys.stderr.close()
            exit(0)