from urllib import parse
from typing import Optional, List, Any
from furl import furl


def is_valid(url: str) -> bool:
    """
    >>> is_valid("https://www.baidu.com/")
    True

    :param url:
    :return:
    """
    try:
        result = parse.urlparse(url)
        scheme, netloc = result.scheme, result.netloc
        if not scheme:
            return False
        if not netloc:
            return False
        if scheme not in ("http", "https"):
            return False
        return True
    except ValueError:
        return False
