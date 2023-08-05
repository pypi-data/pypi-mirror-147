from datetime import datetime
from os import stat
from os.path import getmtime
from typing import Optional, Union


def get_size_in_mb(file_path: Union[str, int]) -> Optional[float]:
    """
    Returns the file of the size in MB, or None on error.
    """
    try:
        file_stats = stat(file_path)
        return file_stats.st_size / (1024 * 1024)
    except OSError:
        return None


def get_modification_datetime(file: Union[str, int]) -> Optional[datetime]:
    """
    Returns the modification datetime of the given file, or None on error.
    """
    try:
        timestamp = getmtime(file)
        return datetime.fromtimestamp(timestamp)
    except OSError:
        return None
