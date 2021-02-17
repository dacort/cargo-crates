import os
import json

import requests

OURA_PAT = os.getenv("OURA_PAT")
API_BASE = "api.ouraring.com/v1"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url, params=params, headers={"Authorization": f"Bearer {OURA_PAT}"}
    )


def sleep(start_date=None, end_date=None):
    """
    Retrieves sleep data from the Oura API between start_date and end_date
    See https://cloud.ouraring.com/docs/sleep for data response definition
    # https://api.ouraring.com/v1/sleep?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    params = {}
    if start_date is not None:
        params["start"] = start_date
    if end_date is not None:
        params["end"] = end_date

    r = get(endpoint("sleep"), params)
    return r.json()


if __name__ == "__main__":
    start_date, end_date = [None, None]
    if os.getenv("start"):
        start_date = os.getenv("start")
    result = sleep(start_date)
    print(json.dumps(result))