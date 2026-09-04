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