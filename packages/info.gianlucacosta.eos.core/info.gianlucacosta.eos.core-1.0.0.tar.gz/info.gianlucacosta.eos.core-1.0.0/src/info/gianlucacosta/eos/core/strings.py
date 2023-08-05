from typing import Optional


def strip_to_none(source: Optional[str]) -> Optional[str]:
    """
    Returns the given string stripped, but returns None if the source was None or the result
    would be empty.
    """

    if source is None:
        return source

    actual_value = source.strip()

    return actual_value or None
