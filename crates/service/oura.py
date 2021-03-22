import json
import os
import sys

import requests

ENV_VARS = ["OURA_PAT"]
API_BASE = "api.ouraring.com/v1"


def endpoint(path):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url, params=params, headers={"Authorization": f"Bearer {os.getenv('OURA_PAT')}"}
    )

def daily_summary(summary_type, start_date=None, end_date=None):
    """
    Retrieves Daily Summary data from the Oura API between start_date and end_date
    See https://cloud.ouraring.com/docs/daily-summaries for data response definition
    # https://api.ouraring.com/v1/sleep?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    params = {}
    if start_date is not None:
        params["start"] = start_date
    if end_date is not None:
        params["end"] = end_date

    r = get(endpoint(summary_type), params)
    return r.json()

SUPPORTED_CMDS = ['sleep', 'activity', 'readiness']

if __name__ == "__main__":
    cmd = 'sleep'
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    start_date, end_date = [None, None]
    if os.getenv("start"):
        start_date = os.getenv("start")
    if os.getenv("end"):
        end_date = os.getenv("end")
    result = daily_summary(cmd, start_date, end_date)
    for r in result.get(cmd, []):
        r['activity_type'] = cmd
        print(json.dumps(r))
