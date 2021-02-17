from datetime import datetime, timezone
import logging
import json

from smart_open import open


logger = logging.getLogger(__name__)


def get_output_stream(output_type=None, output_params={}):
    """
    Based on environment variables passed in from Docker, return an output stream.
    By default, we return a basic stdout object that the caller can write to.

    For more advanced usage (like S3), the caller can provide a set of parameters that
    specify where to write the resulting data.
    """
    if output_type is None or output_type == "stdout":
        return StdOutputter()

    if output_type == "s3":
        return S3Uploader(
            output_params.get("bucket"), output_params.get("path_template")
        )


class OutputRecord:
    def __init__(self, record, path_template) -> None:
        self._record = record
        self._template = path_template

    def path(self):
        # I realize this is *dangerous* but
        # a) It's what I want to do and
        # b) I control the input :)

        # There *MUST* be a better way to do this
        json = lambda k: self.json(k)
        today = lambda: self.today()

        return eval(f"f'{self._template}'")

    def json(self, path):
        """
        Currently only supports top-level attributes
        """
        return self._record.get(path)

    def today(self):
        return f"{datetime.now(tz=timezone.utc).date()}"


class StdOutputter:
    """
    StdOutputter is an output mechanism for Cargo Crates thate outputs data to stdout.
    """

    def add_record(self, record) -> None:
        print(json.dumps(record))

    def close(self):
        pass


class S3Uploader:
    """
    S3Uploader is an output mechanism for Cargo Crates that can upload streams of data
    to a templated S3 location. It can append or overwrite data.
    """

    def __init__(self, bucket, path_template) -> None:
        self._bucket = bucket
        self._path_template = path_template
        self._output_writers = {}

    def _get_writer(self, path):
        if path not in self._output_writers:
            self._output_writers[path] = open(path, "w")

        return self._output_writers.get(path)

    def add_record(self, record) -> None:
        s3_uri = f"s3://{self._bucket}/{self._path_template}"
        output_record = OutputRecord(record, s3_uri)
        path = output_record.path()
        logging.debug(f"Output path is {path}")
        writer = self._get_writer(path)
        writer.write(json.dumps(record) + "\n")

    def close(self):
        for writer in self._output_writers.values():
            writer.close()
