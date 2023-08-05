from sys import stderr, stdout


def reconfigure_output_and_error(encoding: str = "utf-8") -> None:
    """
    Sets the encoding for both stdout and stderr.

    It is especially useful when logging UTF-8 text to stdout/stderr.
    """
    getattr(stdout, "reconfigure")(encoding=encoding)
    getattr(stderr, "reconfigure")(encoding=encoding)
