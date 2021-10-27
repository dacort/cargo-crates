import os
import sys
import json
import requests

ENV_VARS = ["VANTAGE_TOKEN"]
API_BASE = "api.vantage.sh"


def endpoint(path: str):
    return f"https://{API_BASE}/{path}"


def get(url, params={}):
    return requests.get(
        url,
        params=params,
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer " + os.getenv("VANTAGE_TOKEN"),
        },
    )


def ec2_instance(instance_type: str):
    params = {"provider_id": "aws", "name": instance_type}
    r = get(endpoint("v1/products"), params=params)
    return r.json().get("products")[0]


SUPPORTED_CMDS = ["ec2-instance"]

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: vantage ec2-instance <instance-type>")
        print("Supported commands: " + ", ".join(SUPPORTED_CMDS))
        exit(1)

    cmd = sys.argv[1]

    if cmd not in SUPPORTED_CMDS:
        print(f"ERR: '{cmd}' is not a supported commmand.")
        exit(1)

    if cmd == "ec2-instance":
        instance_type = sys.argv[2]
        result = ec2_instance(instance_type)
        print(json.dumps(result))
