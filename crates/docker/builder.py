import sys
import os
import json
import importlib
from string import Template

import crates.service as s

def template_file():
    return os.path.join(os.path.dirname(__file__), 'template.dockerfile')

if __name__ == "__main__":
    modules = sys.argv[1:] or s.ALL

    for m in modules:
        mod_name = f"crates.service.{m}"
        i = importlib.import_module(mod_name)
        config = {
            'env': '\n'.join([f"ENV {var}=" for var in i.ENV_VARS]),
            'entry': json.dumps(["python", "-m", f"{mod_name}"])
        }

        with open(template_file(), 'r') as f:
            src = Template(f.read())
            result = src.substitute(config)
            print(result)


