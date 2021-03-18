import logging
import json

from crates.common.output import OutputRecord

from smart_open import open


logger = logging.getLogger(__name__)


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
