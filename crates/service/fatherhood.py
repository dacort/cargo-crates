import json
import requests

ENV_VARS = []
API_BASE = "fatherhood.gov/jsonapi/node"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(url, params=params)


def dad_joke():
    r = get(endpoint("dad_jokes"))

    # We only return a small portion of the data
    data = r.json()
    return [
        {
            "setup": j["attributes"]["field_joke_opener"],
            "punchline": j["attributes"]["field_joke_response"],
            "created_at": j["attributes"]["created"],
        }
        for j in data["data"]
    ]


if __name__ == "__main__":
    for joke in dad_joke():
        print(json.dumps(joke))