from crates.common.s3 import S3Uploader
from crates.common.stdout import StdOutputter


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