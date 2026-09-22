from datetime import datetime, timezone
from typing import Optional

def datetime_to_utc_str(dt: Optional[datetime]) -> Optional[str]:
    """ Converts a datetime to ISO string in UTC.

    Args:
        dt (Optional[datetime]): Original datetime value.

    Returns:
        Optional[str]: ISO date/time string in UTC, or "None", if it was passed as argument.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.isoformat()

def normalize(string:str) -> str:
    """  Removes empty spaces at both ends 
    of a string, and makes it uppercase.

    Args:
        string (str): Original string.

    Returns:
        str: Normalized string.
    """
    return string.strip().upper()

def build_str_params(query) -> str:
    """ Builds a string to show

    Args:
        query: Schema class used for search queries.

    Returns:
        str: A string containing each query parameter, separated by a "|".
    """
    return " | ".join(f"'{k}': {v}" for k, v in query.model_dump().items())