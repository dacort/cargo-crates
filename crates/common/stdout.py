import json


class StdOutputter:
    """
    StdOutputter is an output mechanism for Cargo Crates thate outputs data to stdout.
    """

    def add_record(self, record) -> None:
        print(json.dumps(record))

    def close(self):
        pass